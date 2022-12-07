"""Order book data model objects."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List


@dataclass(frozen=True)
class Order:
    """Order entry object."""

    symbol: str
    timestamp: datetime
    is_buy: bool
    qty: float
    price: float


@dataclass(frozen=True)
class Fill:
    """Order fill."""

    timestamp: datetime
    qty: float
    price: float


class OrderFillStatus(Enum):
    """Status of an order fill."""

    NONE = None
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"


@dataclass
class OrderFill:
    """An order and its fills information."""

    order: Order
    fills: List[Fill] = field(default_factory=list)

    @property
    def fill_qty(self) -> float:
        """Return the current fill quantity."""
        return sum(f.qty for f in self.fills) if self.fills else 0

    @property
    def open_qty(self) -> float:
        """Return the quantity still available to be filled."""
        return self.order.qty - self.fill_qty

    @property
    def avg_fill_price(self) -> float:
        """Return the average fill price."""
        return sum(f.qty * f.price for f in self.fills) / self.fill_qty

    @property
    def status(self) -> OrderFillStatus:
        """Return the fill status of this order."""
        f = self.fill_qty
        if f == self.order.qty:
            return OrderFillStatus.FILLED
        elif f:
            return OrderFillStatus.PARTIALLY_FILLED
        else:
            return OrderFillStatus.NONE

    def register_fill(
        self, timestamp: datetime, fill_qty: float, fill_price: float
    ) -> None:
        """Register a fill."""
        # check that the order quantity is compatible with available quantity
        # for this order
        if not fill_qty:
            raise ValueError(f"Invalid fill quantity: {fill_qty}!")
        if not fill_price:
            raise ValueError(f"Invalid fill price: {fill_price}!")
        open_qty = self.open_qty
        if fill_qty > open_qty:
            raise ValueError(
                f"Invalid fill quantity {fill_qty} "
                f"for order with open quantity {self.open_qty}!"
            )
        # check that the fill price is compatible with the order's limit price
        if self.order.is_buy:
            fill_price_ok = fill_price <= self.order.price
        else:
            fill_price_ok = fill_price >= self.order.price
        if not fill_price_ok:
            raise ValueError(
                f"Invalid fill price {fill_price} for {self.order}!"
            )
        self.fills.append(Fill(timestamp, fill_qty, fill_price))
