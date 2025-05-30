import requests
from config import COINCAP_API_KEY, PAGE_SIZE

class CoinCapClient:
    BASE_URL = "https://rest.coincap.io/v3"

    def __init__(self):
        self.headers = {"Authorization": f"Bearer {COINCAP_API_KEY}"}

    def fetch_assets(self, limit=PAGE_SIZE, offset=0):
        params = {"limit": limit, "offset": offset}
        r = requests.get(f"{self.BASE_URL}/assets", headers=self.headers, params=params)
        r.raise_for_status()
        return r.json().get("data", [])

    def fetch_asset_history(self, slug, interval="d1"):
        params = {"interval": interval}
        r = requests.get(f"{self.BASE_URL}/assets/{slug}/history", headers=self.headers, params=params)
        r.raise_for_status()
        return r.json().get("data", [])