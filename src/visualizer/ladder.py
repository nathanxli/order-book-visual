"""
Renders the order book as a ladder
"""

from rich.table import Table
from textual.widgets import Static

from orderbook import OrderBook


class LadderView(Static):
    """Trader-style ladder with asks above bids on a shared price axis."""

    def __init__(self, levels_per_side: int = 12) -> None:
        super().__init__()
        self.levels_per_side = levels_per_side
        self.orderbook: OrderBook | None = None

    def set_orderbook(self, orderbook: OrderBook) -> None:
        self.orderbook = orderbook
        self.refresh()

    def render(self) -> Table:
        table = Table(title="Level 2 Trader Ladder", expand=True)

        table.add_column("Buy Size", justify="right")
        table.add_column("Price", justify="center")
        table.add_column("Sell Size", justify="right")

        if self.orderbook is None:
            table.add_row("", "Waiting for data...", "")
            return table

        bids = self.orderbook.bids[: self.levels_per_side]
        asks = self.orderbook.asks[: self.levels_per_side]

        # Ask rows first (top of ladder = higher prices)
        for ask in reversed(asks):
            table.add_row(
                "",
                f"{ask.price:.2f}",
                f"{ask.size:.6f}",
            )

        # Spread / inside market separator
        best_bid = self.orderbook.best_bid()
        best_ask = self.orderbook.best_ask()

        if best_bid is not None and best_ask is not None:
            table.add_section()
            table.add_row(
                f"{best_bid.size:.6f}",
                f"{best_bid.price:.2f} / {best_ask.price:.2f}",
                f"{best_ask.size:.6f}",
            )
            table.add_section()

        # Bid rows next
        for bid in bids:
            table.add_row(
                f"{bid.size:.6f}",
                f"{bid.price:.2f}",
                "",
            )

        return table