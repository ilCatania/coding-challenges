"""Order book data model objects."""
import operator
from bisect import bisect_left
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Union


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
    def price(self) -> float:
        """Return the order price."""
        return self.order.price

    @property
    def is_buy(self) -> bool:
        """Return the order buy flag."""
        return self.order.is_buy

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


@dataclass
class OrderBookEntry:
    """An entry into the order book.

    An entry is comprised of orders with the same price level and direction
    (buy/sell), and their fills information for partially filled orders.
    """

    price: float
    is_buy: bool
    open_orders: List[OrderFill] = field(default_factory=list)

    @staticmethod
    def from_order(o: Union[Order, OrderFill]) -> "OrderBookEntry":
        """Create an order book entry from a single order."""
        if isinstance(o, OrderFill):
            of = o
        elif isinstance(o, Order):
            of = OrderFill(order=o)
        else:
            raise ValueError(f"Invalid input: {o}!")
        return OrderBookEntry(price=o.price, is_buy=o.is_buy, open_orders=[of])

    def __bool__(self):
        """Return true if this entry has any open orders."""
        return bool(self.open_orders)

    def __iter__(self):
        """Iterate over open orders."""
        return iter(self.open_orders)

    def __cmp__(self, other) -> int:
        """Provide ordering.

        Order book entries are considered to be ordered descending with respect
        to price on the sell side, and ascending on the buy side, so they can be
        more efficiently matched against incoming orders from the opposite side.
        """
        type_ok = (
            isinstance(other, OrderBookEntry)
            or isinstance(other, OrderFill)
            or isinstance(other, Order)
        )
        if type_ok and self.is_buy == other.is_buy:
            if self.price == other.price:
                return 0
            if self.is_buy:
                return 1 if self.price < other.price else -1
            else:  # sell
                return -1 if self.price < other.price else 1
        else:
            return NotImplemented

    def __gt__(self, other) -> bool:
        """Provide ordering."""
        return self.__cmp__(other) > 0

    def __ge__(self, other) -> bool:
        """Provide ordering."""
        return self.__cmp__(other) >= 0

    def __lt__(self, other) -> bool:
        """Provide ordering."""
        return self.__cmp__(other) < 0

    def __le__(self, other) -> bool:
        """Provide ordering."""
        return self.__cmp__(other) <= 0

    def append(self, o: OrderFill):
        """Add an order to this entry."""
        if o.order.price == self.price and o.order.is_buy == self.is_buy:
            self.open_orders.append(o)
        else:
            raise ValueError(
                f"Can't add {o} to entry with "
                "price: {self.price}, buy: {self.is_buy}!"
            )

    def match_against(self, incoming_order: OrderFill) -> List[OrderFill]:
        """Receive an order and match it with open orders.

        Modify the input order to match it with any fills, and return any orders
        that were fully filled by this order.
        """
        if self.is_buy == incoming_order.order.is_buy:
            raise ValueError(
                "Can't match order in the same direction:"
                f"\n{incoming_order}\n{self}"
            )
        incoming_price = incoming_order.order.price
        if incoming_order.order.is_buy and incoming_price < self.price:
            raise ValueError(
                f"Can't match buy order with price {incoming_price}, "
                f"entry limit price is {self.price}!"
            )
        elif not incoming_order.order.is_buy and incoming_price > self.price:
            raise ValueError(
                f"Can't match sell order with price {incoming_price}, "
                f"entry limit price is {self.price}!"
            )
        incoming_ts = incoming_order.order.timestamp
        filled_orders = []
        qty_to_fill = incoming_order.open_qty
        for oo in self.open_orders:
            fill_qty = min(qty_to_fill, oo.open_qty)
            oo.register_fill(incoming_ts, fill_qty, self.price)
            if oo.status == OrderFillStatus.FILLED:
                filled_orders.append(oo)
            qty_to_fill -= fill_qty
            if not qty_to_fill:
                break
        self.open_orders[:] = [
            o for o in self.open_orders if o.status != OrderFillStatus.FILLED
        ]
        incoming_filled_qty = incoming_order.open_qty - qty_to_fill
        # register a single fill on the upcoming order even if it was matched
        # against multiple orders
        incoming_order.register_fill(
            incoming_ts,
            incoming_filled_qty,
            self.price,
        )
        return filled_orders


class OrderBook:
    """An order book."""

    def __init__(self) -> None:
        self.buy_orders: List[OrderBookEntry] = []
        """The buy orders, kept in descending order of price."""
        self.sell_orders: List[OrderBookEntry] = []
        """The sell orders, kept in ascending order of price."""

    def __repr__(self):
        """Return the string representation."""
        return (
            f"{type(self).__name__}(buy_orders={self.buy_orders},"
            "sell_orders={self.sell_orders})"
        )

    def append(self, order: OrderFill):
        """Append an order to this order book.

        This just adds the order to the order book, without trying to match any
        existing orders. It creates an order book entry if needed.
        """
        to_append = self.buy_orders if order.is_buy else self.sell_orders
        idx = bisect_left(to_append, order)
        if idx < len(to_append):
            entry = to_append[idx]
            if entry.price == order.price:
                # append order to existing entry
                entry.append(order)
                return
        # insert new order book entry
        to_append.insert(idx, OrderBookEntry.from_order(order))

    def receive(self, order: Order) -> List[OrderFill]:
        """Receive an order and try to match it with existing orders.

        Record the order in the order book unless it's fully filled, and return
        all the orders that have been filled and removed from the order book,
        including the input order if it was fully filled.
        """
        of = OrderFill(order=order)
        if order.is_buy:
            orders_to_match = self.sell_orders
            cannot_match = operator.lt
        else:
            orders_to_match = self.buy_orders
            cannot_match = operator.gt

        filled_orders = []
        for obe in orders_to_match:
            if (
                cannot_match(order.price, obe.price)
                or of.status == OrderFillStatus.FILLED
            ):
                break
            filled = obe.match_against(of)
            filled_orders.extend(filled)
        if of.status == OrderFillStatus.FILLED:
            filled_orders.append(of)
        else:
            self.append(of)

        # remove entries with no orders from the book
        orders_to_match[:] = [o for o in orders_to_match if o]
        return filled_orders
