import requests
from datetime import datetime, timezone

PUMPFUN_API = "https://pump.fun/api/token/{}"
LATEST_API = "https://pump.fun/api/latest-tokens"

def fetch_latest_tokens():
    try:
        res = requests.get(LATEST_API, timeout=5)
        res.raise_for_status()
        return res.json().get("tokens", [])
    except Exception as e:
        print(f"[!] Ошибка получения токенов: {e}")
        return []

def fetch_token_info(mint: str):
    try:
        res = requests.get(PUMPFUN_API.format(mint), timeout=5)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"[!] Ошибка получения info: {e}")
        return None

def minutes_since(timestamp):
    now = datetime.now(timezone.utc).timestamp()
    return (now - timestamp) / 60
