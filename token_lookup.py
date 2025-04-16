
import requests

def get_token_name_from_cronoscan(contract_address: str, api_key: str) -> str:
    url = "https://api.cronoscan.com/api"
    params = {
        "module": "token",
        "action": "tokeninfo",
        "contractaddress": contract_address,
        "apikey": api_key
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data["status"] == "1" and data["result"]:
            return data["result"][0].get("symbol", "Non rilevato")
    except Exception as e:
        print(f"Errore recuperando info da CronoScan: {e}")
    return "Non rilevato"
