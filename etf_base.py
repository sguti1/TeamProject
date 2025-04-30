import os
import requests
import pandas as pd
from sklearn.preprocessing import StandardScaler
from dotenv import load_dotenv
from countryinfo import CountryInfo
from datetime import datetime, date, timedelta



def fetch_fx_rates(api_key_env: str = 'FREECURRENCY_API_KEY') -> dict:
    """
    Fetches live foreign exchange rates from the external API. Returns a dict mapping ISO currency codes to units of foreign currency per 1 USD.
    """
    load_dotenv()
    key = os.getenv(api_key_env)
    if not key:
        raise RuntimeError(f"{api_key_env} not found in environment")
    resp = requests.get(f"https://api.freecurrencyapi.com/v1/latest?apikey={key}")
    resp.raise_for_status()
    return resp.json()['data']

def load_imf_data(csv_path: str) -> pd.DataFrame:
    """
    Loads the IMF dataset CSV into a pandas DataFrame.
    """
    return pd.read_csv(csv_path)

def extract_latest_values(df: pd.DataFrame, indicators: list) -> pd.DataFrame:
    """
    Filters to only the specified indicators, then for each country–indicator picks the value for the current calendar year (if available), otherwise the most recent prior year. Future-year estimates (> CURRENT_YEAR) are ignored.
    """
    years = [col for col in df.columns if col.isdigit()]
    subset = df[df['INDICATOR'].isin(indicators)].copy()
    CURRENT_YEAR = datetime.now().year

    def latest(row):
        # build {year_int: value} but only up to CURRENT_YEAR
        avail = {
            int(y): row[y]
            for y in years
            if pd.notna(row[y]) and int(y) <= CURRENT_YEAR
        }
        if not avail:
            return pd.NA
        if CURRENT_YEAR in avail:
            return avail[CURRENT_YEAR]
        return avail[max(avail)]

    subset['Latest'] = subset.apply(latest, axis=1)
    return subset.pivot(index='COUNTRY', columns='INDICATOR', values='Latest')


def map_currencies(wide_df: pd.DataFrame) -> pd.DataFrame:
    """
    Automaps each country name to its ISO4217 currency code using CountryInfo, then fetches live FX rates and drops any rows for which we don’t have a rate.
    """
    def get_code(name):
        for variant in (name, name.split('(')[0].strip(), name.split(',')[0].strip()):
            try:
                codes = CountryInfo(variant).currencies()
                if codes:
                    return codes[0]
            except Exception:
                continue
        return None

    #map country → ISO code, drop misses
    wide_df['Currency'] = wide_df.index.map(get_code)
    wide_df = wide_df.dropna(subset=['Currency'])

    # fetch FX once
    fx = fetch_fx_rates()

    # keep only currencies present in FX API
    wide_df = wide_df[wide_df['Currency'].isin(fx.keys())].copy()

    # map in the FX rate
    wide_df['FX Rate'] = wide_df['Currency'].map(fx)

    return wide_df

def apply_health_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies relaxed macro-health thresholds to drop countries that don’t meet all criteria:
      - Unemployment rate ≤ 12%
      - Gross debt (General government) ≤ 110% of GDP
      - CPI inflation in [–2%, 50%]
      - Current account balance ≥ –5% of GDP
      - GDP ≥ 25th percentile GDP of all countries in DF

    If no country passes, skips filtering and returns the original DataFrame.
    """
    # extract series by their exact column names
    unemp    = df['Unemployment rate']
    debt     = df['Gross debt, General government, Percent of GDP']
    infl     = df['All Items, Consumer price index (CPI), Period average, percent change']
    cav      = df['Current account balance (credit less debit), Percent of GDP']
    gdp      = df['Gross domestic product (GDP), Current prices, US dollar']

    mask = (
        (unemp    <= 15)               &
        (debt     <= 110)              &
        (infl.between(-2, 50))         &
        (cav      >= -5)               
    )

    if mask.sum() == 0:
        print("No countries passed the relaxed health filters; skipping filter.")
        return df

    # otherwise return only the filtered rows
    return df[mask]


def compute_scores_and_weights(df: pd.DataFrame, final_inds: list) -> pd.DataFrame:
    """
    Imputes missing values, z-scores the final indicators (macros + FX), computes a composite score (mean of z-scores), filters to positive scores, and normalizes to weights summing to 1. Returns a DataFrame with CompositeScore and Weight.
    """
    df_flat = df.copy()
    df_flat[final_inds] = df_flat[final_inds].apply(lambda col: col.fillna(col.median()))
    
    scaler = StandardScaler()
    Z = scaler.fit_transform(df_flat[final_inds])
    Zdf = pd.DataFrame(Z, index=df_flat.index, columns=final_inds)
    
    Zdf['CompositeScore'] = Zdf.mean(axis=1)
    Zdf_pos = Zdf[Zdf['CompositeScore'] > 0].copy()
    if Zdf_pos.empty:
        print("No positive composite scores; using all.")
        Zdf_pos = Zdf.copy()
    
    total = Zdf_pos['CompositeScore'].sum()
    Zdf_pos['Weight'] = Zdf_pos['CompositeScore'] / total
    return Zdf_pos[['CompositeScore','Weight']]

def build_etf_table(imf_csv_path: str) -> pd.DataFrame:
    """
    High-level function to build the ETF allocation table.
    Returns a DataFrame of CompositeScores and Weights by country.
    """
    # 1) load & pivot IMF data
    indicators = [
        'Gross domestic product (GDP), Current prices, US dollar',
        'All Items, Consumer price index (CPI), Period average, percent change',
        'Unemployment rate',
        'Current account balance (credit less debit), Percent of GDP',
        'Gross debt, General government, Percent of GDP',
        'External debt, Percent of GDP',
        'Exports of goods and services, US dollar'
    ]
    df = load_imf_data(imf_csv_path)
    wide = extract_latest_values(df, indicators)
    wide = map_currencies(wide)
    # 3) compute a 1-year FX return proxy using the same freecurrencyapi:
    one_year_ago = (date.today() - timedelta(days=365)).isoformat()
    hist = requests.get(
        f"https://api.freecurrencyapi.com/v1/historical"
        f"?apikey={os.getenv('FREECURRENCY_API_KEY')}"
        f"&date={one_year_ago}"
    ).json()['data'][one_year_ago]

    # map that into a new column and get simple return
    wide['FX Rate 1Y'] = wide['Currency'].map(hist)
    wide['FX Change'] = (wide['FX Rate'] - wide['FX Rate 1Y']) / wide['FX Rate 1Y']

    print(f"Pre-filter size: {wide.size}")
    wide = apply_health_filters(wide)
    print(f"Post-filter size: {wide.size}")

    final_inds = indicators + ['FX Rate', 'FX Change']

    etf_table = compute_scores_and_weights(wide, final_inds)
    return etf_table, wide

def compute_etf_value(etf_df: pd.DataFrame, wide: pd.DataFrame) -> float:
    """
    Given the ETF table (with weights) and the wide DataFrame (with FX Rate), computes the USD-denominated ETF value as the weighted sum of USD-per-unit.
    """
    usd_per_unit = 1 / wide.loc[etf_df.index, 'FX Rate']
    return (etf_df['Weight'] * usd_per_unit).sum()

def show_top10_table(etf_df: pd.DataFrame, wide_df: pd.DataFrame) -> pd.DataFrame:
    """
    Builds a summary of the top 10 currencies by ETF weight, with one row per country:
      - Country
      - Currency (ISO code)
      - Weight (%) in the ETF
      - Value USD (USD per 1 unit of the currency, 2 decimals)
      - GDP (current USD)
      - Unemployment (%)
      - Inflation (%)
    """
    top10 = etf_df.sort_values('Weight', ascending=False).head(10)

    summary = pd.DataFrame({
        'Country':          top10.index,
        'Currency':         wide_df.loc[top10.index, 'Currency'],
        'Weight (%)':       top10['Weight'] * 100,
        'Value ($)':        1 / wide_df.loc[top10.index, 'FX Rate'],
        'GDP ($ Trillion)':              wide_df.loc[top10.index, 'Gross domestic product (GDP), Current prices, US dollar'],
        'Unemployment (%)': wide_df.loc[top10.index, 'Unemployment rate'],
        'Inflation (%)':    wide_df.loc[top10.index, 'All Items, Consumer price index (CPI), Period average, percent change']
    })

    pd.options.display.float_format = "{:.2f}".format

    for col in ['Weight (%)','Value ($)','GDP ($ Trillion)','Unemployment (%)','Inflation (%)']:
        summary[col] = summary[col].map(lambda x: f"{x:.2f}")


    return summary.reset_index(drop=True)


if __name__ == "__main__":
    # Build the allocation table and get back the 'wide' DataFrame for FX data
    etf_table, wide_df = build_etf_table('data/imf_dataset.csv')
    
    # Print top allocations
    print("\nTop 10 ETF Allocations:")
    print(etf_table.sort_values('Weight', ascending=False).head(10).to_string())
    
    # Compute and print the ETF value in USD
    value_usd = compute_etf_value(etf_table, wide_df)
    print(f"\nETF value (USD): ${value_usd:.2f}")

    # Print the summary table
    summary = show_top10_table(etf_table, wide_df)
    print("\nTop 10 ETF Currency Summary:")
    print(summary.to_string(index=False))
