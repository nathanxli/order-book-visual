"""
1. Creates an OrderBook object
2. Fetches snapshots every second
3. Updates OrderBook object
"""

import time
import asyncio

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from api import fetch_orderbook_snapshot
from orderbook import OrderBook
from ladder import LadderView


class OrderBookApp(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def __init__(self, product_id: str = "BTC-USD") -> None:
        super().__init__()
        self.product_id = product_id
        self.orderbook = OrderBook(product_id=product_id)
        self.ladder = LadderView(levels_per_side=15)
        self._fetch_in_progress = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield self.ladder
        yield Footer()

    async def on_mount(self) -> None:
        self.title = "Order Book Visualizer"
        self.sub_title = self.product_id

        await self.refresh_orderbook()
        self.set_interval(1.0, self.refresh_orderbook)

    async def refresh_orderbook(self) -> None:
        if self._fetch_in_progress:
            return

        self._fetch_in_progress = True

        try:
            snapshot = await asyncio.to_thread(
                fetch_orderbook_snapshot,
                self.product_id,
                2,
            )

            self.orderbook.update_from_snapshot(snapshot)
            self.ladder.set_orderbook(self.orderbook)
            self.sub_title = self.orderbook.summary()

        except Exception as exc:
            self.sub_title = f"Error: {exc}"

        finally:
            self._fetch_in_progress = False



def main() -> None:
    app = OrderBookApp(product_id="BTC-USD")
    app.run()


if __name__ == "__main__":
    main()