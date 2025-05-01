import os, csv
from datetime import datetime
from etf_base import build_etf_table, compute_etf_value


def log_etf_value(value, path='data/etf_history.csv'):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if not os.path.isfile(path):
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'etf_value'])

    timestamp = datetime.now().isoformat()
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, value])

if __name__ == "__main__":
    etf_df, wide_df  = build_etf_table('data/imf_dataset.csv')
    etf_value        = compute_etf_value(etf_df, wide_df)

    log_etf_value(etf_value)
    print(f"Logged ETF value: {etf_value:.2f}")
