"""
Defines internal order book representation.
"""

from dataclasses import dataclass, field
from decimal import Decimal

@dataclass
class PriceLevel:
    price: Decimal
    size: Decimal
    num_orders: int

@dataclass
class OrderBook:
    product_id:str
    bids: list[PriceLevel] = field(default_factory=list)
    asks: list[PriceLevel] = field(default_factory=list)
    sequence: int | None = None

    def update_from_snapshot(self, snapshot: dict) -> None:
        self.sequence = snapshot.get("sequence")

        self.bids = [
            PriceLevel(
                price = Decimal(level[0]),
                size = Decimal(level[1]),
                num_orders=int(level[2])
            )
            for level in snapshot.get("bids", [])
        ]

        self.asks = [
            PriceLevel(
                price = Decimal(level[0]),
                size = Decimal(level[1]),
                num_orders=int(level[2])
            )
            for level in snapshot.get("asks", [])
        ]

        ## sort snapshots
        self.bids.sort(key=lambda level: level.price, reverse=True)
        self.asks.sort(key=lambda level: level.price)

    def best_bid(self) -> PriceLevel | None:
        return self.bids[0] if self.bids else None
    
    def best_ask(self) -> PriceLevel | None:
        return self.asks[0] if self.asks else None
    
    def spread(self) -> float | None:
        bid = self.best_bid()
        ask = self.best_ask()
        if bid is None or ask is None:
            return None
        return ask.price - bid.price
    
    def summary(self) -> str:
        bid = self.best_bid()
        ask = self.best_ask()
        spread = self.spread()

        if spread is None:
            return f"{self.product_id}: order book is empty"
        
        return (
            f"{self.product_id} | "
            f"best bid = {bid.price: .4f} ({bid.size: .9f}) | "
            f"best ask = {ask.price: .4f} ({ask.size: .9f}) | "
            f"spread = {spread: .4f}"
        )