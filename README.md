# Team Project

## Team Members
Khushi Chindaliya and Stephanie Gutierrez

# Currency Insight: Smart Conversion Meets Context

## Big Idea / Goal

Our goal was to create a smart, easy-to-use currency conversion and analysis tool that offers real-time exchange rates and macroeconomic context. Instead of just giving raw data, our tool enhances financial awareness by incorporating insights from the IMF, exchange rate data, and OpenAI. 

We chose **FreeCurrencyAPI** for its generous free tier (5,000 requests/month) and reliability. We enrich the analysis with IMF macroeconomic indicators and use OpenAI to generate plain-language insights from currency trends.

We also created a visually designed web interface using HTML and CSS to present ETF results and enable an interactive chat experience. This site displays the ETF value, top allocations, and lets users ask the AI assistant questions about the ETF's structure and logic.

--------------------------------------------------------

## User Instructions

### How to Set It Up

1. **Clone the repository:**

```bash
git clone https://github.com/sguti1/TeamProject
```

2. **Installing dependencies manually:**

Install each of the following Python packages individually:

These are the packages we downloaded to our command prompt
```bash
pip install requests pandas scikit-learn python-dotenv countryinfo flask openai
```

These are the main libraries used in this project:

```python
import os
import requests
import pandas as pd
from sklearn.preprocessing import StandardScaler
from dotenv import load_dotenv
from countryinfo import CountryInfo
from datetime import datetime, date, timedelta
from openai import OpenAI
```


3. **Set up your `.env` file:**

In the root directory, create a `.env` file and include the following:

```env
FREECURRENCY_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

DO NOT SHARE THE .ENV FILE

--------------------------------------------------------------------------
## Implementation Information

### Project Structure & Tools

- **APIs Used:**
  - FreeCurrencyAPI for real-time FX rates
  - OpenAI API for contextual currency insights
  - CountryInfo for country-to-currency mapping

- **Libraries:** `requests`, `pandas`, `scikit-learn`, `dotenv`, `flask`, `openai`
- **Frontend:** HTML + CSS (custom template)

### Application Flow

1. Loads macroeconomic data from an IMF CSV.
2. Uses CountryInfo to map countries to ISO currency codes.
3. Fetches current and one-year-old FX rates from FreeCurrencyAPI.
4. Filters countries based on health indicators (unemployment, inflation, etc.).
5. Standardizes and scores countries based on key metrics.
6. Builds a weighted ETF-style basket of currencies.
7. Flask renders the results on a custom HTML page with styling.
8. Users interact with an AI chatbot embedded on the webpage.

---------------------------------------------------------------------------------------

## Results

Example console output:

```
Top 10 ETF Allocations:
                             CompositeScore    Weight
COUNTRY
China, People's Republic of        0.902322  0.175407
Brazil                             0.859559  0.167094
Indonesia                          0.741196  0.144085
Spain                              0.639769  0.124368
Mexico                             0.461142  0.089644
India                              0.441163  0.085760
Hungary                            0.223938  0.043532
Belgium                            0.210307  0.040883
Austria                            0.142430  0.027688
Finland                            0.141455  0.027498

ETF value (USD): $0.38

Top 10 ETF Currency Summary:
                    Country Currency Weight (%) Value ($) GDP ($ Trillion) Unemployment (%) Inflation (%)
China, People's Republic of      CNY      17.54      0.14         19231.71             5.10         -0.03
                     Brazil      BRL      16.71      0.18          2125.96             7.15          5.31
                  Indonesia      IDR      14.41      0.00          1429.74             5.00          1.68
                      Spain      EUR      12.44      1.13          1799.51            11.13          2.22
                     Mexico      MXN       8.96      0.05          1692.64             3.85          3.54
                      India      INR       8.58      0.01          4187.02             4.94          4.24
                    Hungary      HUF       4.35      0.00           237.07             4.60          4.92
                    Belgium      EUR       4.09      1.13           684.86             5.90          3.20
                    Austria      EUR       2.77      1.13           534.30             5.59          3.18
                    Finland      EUR       2.75      1.13           303.94             8.12          1.97
```

Rendered webpage includes:
- ETF value in large font
- Styled table of top 10 allocations
- Interactive chat box for AI questions

Sample AI-generated response:

```
Question: Which countries in the ETF have the lowest unemployment?
Answer: The countries in the ETF with the lowest unemployment are: 1. Mexico with an unemployment rate of 3.85%. 2. India with an unemployment rate of 4.94%.
```

---

## Project Evolution

- Began with a simple exchange-rate tool.
- Integrated IMF macroeconomic indicators for deeper analysis.
- Automated country-currency mapping.
- Developed a scoring algorithm using z-scores.
- Built a Flask web app to display results.
- Added a fully styled HTML/CSS webpage for presentation.
- Embedded OpenAI assistant into the interface.

---

## Attribution

- FX Data: [FreeCurrencyAPI](https://freecurrencyapi.com/)
- Macroeconomic Data: IMF public dataset
- Country Info: [CountryInfo](https://pypi.org/project/CountryInfo/)
- AI Integration: [OpenAI API](https://openai.com/)
- Web Framework: [Flask](https://flask.palletsprojects.com/)
- Frontend Styling: Custom HTML and CSS
- Data Analysis: `pandas`, `scikit-learn`

---

This project demonstrates practical data engineering, API integration, full-stack web development, and applied AI for real-world financial analysis.
