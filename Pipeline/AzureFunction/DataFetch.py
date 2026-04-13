import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_rates():
    """Fetches live rates from open.er-api.com"""
    data = requests.get(
        "https://open.er-api.com/v6/latest/USD",
        verify=False).json()
    data["conversion_rates"] = data["rates"]
    print(f"Fetched {len(data['conversion_rates'])} currencies")
    return data

if __name__ == "__main__":
    raw_data = fetch_rates()