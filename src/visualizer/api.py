"""
Interfaces with api. 
Fetches raw data from API and returns it as Python data.
"""

import requests

BASE_URL = "https://api.exchange.coinbase.com"


def fetch_orderbook_snapshot(product_id: str = "BTC-USD", level: int = 2) -> dict:
    """
    Fetch a level-2 order book snapshot from Coinbase Exchange API.

    Returns:
        Parsed JSON response as a Python dictionary.
    """
    url = f"{BASE_URL}/products/{product_id}/book"
    params = {"level": level}

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    return response.json()