import requests
import json
from pathlib import Path

ENDPOINT = Path("endpoint.txt")
OUTPUT_FILE = Path("data/orderbook_snapshot.json")

URL = ENDPOINT.read_text().strip()

def fetch_orderbook():
    response = requests.get(URL)
    response.raise_for_status()
    return response.json()

def save_json(data):
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

def main():
    data = fetch_orderbook()
    save_json(data)

if __name__ == "__main__":
    main()