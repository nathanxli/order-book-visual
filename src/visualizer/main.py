"""
1. Creates an OrderBook object
2. Fetches snapshots every second
3. Updates OrderBook object
4. Prints summary (best bid/ask & spread)
"""

import time

from api import fetch_orderbook_snapshot
from orderbook import OrderBook

def main() -> None:
    product_id = "BTC-USD"
    orderbook = OrderBook(product_id = product_id)

    print(f"Starting order book visualizer for {product_id}...")

    while True:
        try:
            snapshot = fetch_orderbook_snapshot(product_id=product_id, level=2)
            orderbook.update_from_snapshot(snapshot)

            # Placeholder for future visualization updates
            print(orderbook.summary())

        except KeyboardInterrupt:
            print("\nStopping application.")
            break
        except Exception as exc:
            print(f"Error: {exc}")

        time.sleep(1)


if __name__ == "__main__":
    main()