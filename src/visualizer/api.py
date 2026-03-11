import requests
from pathlib import Path

ENDPOINT = Path("endpoint.txt")
OUTPUT_FILE = Path("data/orderbook_snapshot.json")

URL = ENDPOINT.read_text().strip()

def fetch_orderbook_snapshot() -> dict:
    response = requests.get(URL)
    response.raise_for_status()
    return response.json()