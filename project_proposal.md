# Currency-Backed ETF for a Stablecoin-Pegged Cross-Border Transactions

## The Big Idea

We aim to build a diversified **Currency-Backed Exchange-Traded Fund (ETF)** composed of various fiat currencies. This ETF is constructed based on real-time **foreign exchange rates** (via Exchange Rates API or similar) and weighted according to approximately **10 macroeconomic indicators** sourced from open data made available by reputable institutions such as the **World Bank** and **IMF**. 

The ETF is not designed to outperform traditional indexes but to **maintain stability**, serving as a base peg for a **stablecoin**, thereby reducing currency risk for cross-border transactions. 

Our MVP includes:
- A web-based dashboard showing:
  - A **table of currencies** included in the ETF and the associated **key economic indicators** influencing each currency
  - A **performance graph** of the ETF value over time
- An **AI-powered chatbot** (OpenAI API) to answer user questions about data and methodology

Our stretch goal:
- Run **user simulations** showing how cross-border transaction values fluctuate with traditional stablecoins vs. our ETF-backed stablecoin

---

## Learning Objectives

### Shared Goals:
- Understand how to integrate economic data into a financial index
- Learn how to use APIs and automate data ingestion
- Gain hands-on experience with backend and frontend web development
- Apply basic AI/NLP via OpenAI API to answer user queries

### Individual Goals:
- Khushi: Master data wrangling from complex CSV/JSON sources (World Bank, IMF) and build a dynamic UI that updates with real-time data
- Stephanie: Train and implement OpenAI-powered chat assistant and lead backend development and integration of APIs

---

## Implementation Plan

- Use Python for backend API calls and data processing
- Libraries: `pandas`, `numpy`, `plotly`, `openai` (initial )
- API: Open Exchange Rates
- Download local files from World Bank Open Data API or IMF data portals for static indicators
- For chat integration: OpenAI’s GPT API
- Data ingestion and processing pipeline to refresh at fixed intervals (e.g., every 24 hours)

---

## Project Schedule

| Week | Milestone |
|------|-----------|
| Week 1 | Implement economic indicator weighting model + ETF formula |
| Week 2 | Build frontend dashboard (table + graphs), backend API integration |
| Week 3 | Integrate OpenAI chatbot, documentation, polish UI/UX |

---

## Collaboration Plan

- Use agile methodology and  do weekly sprints and check-ins 
- Maintain a running list of tasks
- Discussing each other's code to develop a shared understanding

---

## Risks and Limitations

- **Data availability and formatting** from World Bank/IMF may be inconsistent
- **Real-time data reliability** could limit accuracy of ETF updates
- **OpenAI API costs** and latency could affect chat module

---

## Relevant Course Content

- API
- Data types and data analysis
- Flask
- Functions

---

