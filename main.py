import requests

try:
    url = "https://iss.moex.com/iss/statistics/engines/currency/markets/selt/rates.json?iss.meta=off"
    data = requests.get(url, timeout=1)
except requests.exceptions.Timeout as e:
    print("Timeout while connection to moex.")

