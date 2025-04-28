import os
from dotenv import load_dotenv
import freecurrencyapi
import requests
from requests.structures import CaseInsensitiveDict


load_dotenv() 

FREECURRENCY_API_KEY = os.getenv('FREECURRENCY_API_KEY')  
client = freecurrencyapi.Client(FREECURRENCY_API_KEY)
url = f"https://api.freecurrencyapi.com/v1/latest?apikey={FREECURRENCY_API_KEY}"
resp = requests.get(url)


def get_usd_to_currency(currency):
    result = client.latest(base_currency='USD', currencies=[currency])
    return result['data'][currency]


def main():
    currency = 'CAD'
    rate = get_usd_to_currency(currency)
    print(f"1 USD = {rate} {currency}")


#Retrieve Currencies
# currency_result = client.currencies(currencies=['EUR', 'CAD'])
# print(currency_result)

# #Retrieve Latest Exchange Rates
# exrate_result = client.latest()
# print(exrate_result)

# # Retrieve Historical Exchange Rates
# historical_result = client.historical('2022-02-02')
# print(historical_result)


# print(resp.status_code)
# print(url)