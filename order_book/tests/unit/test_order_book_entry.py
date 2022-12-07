from datetime import datetime

import pytest

from order_book.model import (
    Fill,
    Order,
    OrderBookEntry,
    OrderFill,
    OrderFillStatus,
)


def test_order_book_entry_magic_methods():
    """Test behaviour of magic methods."""
    obe = OrderBookEntry(price=10, is_buy=True)
    assert not obe

    o1 = OrderFill(
        Order(
            symbol="AAPL.OQ",
            timestamp=datetime.utcnow(),
            is_buy=True,
            qty=8,
            price=10,
        )
    )
    o2 = OrderFill(
        Order(
            symbol="AAPL.OQ",
            timestamp=datetime.utcnow(),
            is_buy=True,
            qty=6,
            price=10,
        )
    )
    obe.append(o1)
    assert obe
    obe.append(o2)
    assert obe
    it = iter(obe)
    assert next(it) == o1
    assert next(it) == o2


def test_order_book_entry_simple():
    """Simple test matching two opposite orders."""
    sell_order = Order(
        symbol="AAPL.OQ",
        timestamp=datetime.utcnow(),
        is_buy=False,
        qty=20,
        price=12,
    )
    buy_order = Order(
        symbol="AAPL.OQ",
        timestamp=datetime.utcnow(),
        is_buy=True,
        qty=20,
        price=12,
    )
    existing_order = OrderFill(order=sell_order)
    incoming_order = OrderFill(order=buy_order)
    expected_fill = Fill(timestamp=buy_order.timestamp, qty=20, price=12)
    expected_match = OrderFill(order=sell_order, fills=[expected_fill])
    obe = OrderBookEntry(price=12, is_buy=False, open_orders=[existing_order])
    assert incoming_order.status == OrderFillStatus.NONE
    matched = obe.match_against(incoming_order)
    # check that the correct existing order is matched and returned, and removed
    # from the order book entry
    assert matched == [expected_match]
    assert not obe.open_orders
    # check that the input order has been modified and filled too
    assert incoming_order.status == OrderFillStatus.FILLED
    assert incoming_order.fill_qty == 20
    assert incoming_order.open_qty == 0
    assert incoming_order.avg_fill_price == 12
    assert incoming_order.fills == [expected_fill]


def test_order_book_entry_invalid_prices():
    """Test that trying to fill incompatible orders raises an error."""
    existing_order = OrderFill(
        order=Order(
            symbol="AAPL.OQ",
            timestamp=datetime.utcnow(),
            is_buy=False,
            qty=20,
            price=10,
        )
    )
    incoming_order = OrderFill(
        order=Order(
            symbol="AAPL.OQ",
            timestamp=datetime.utcnow(),
            is_buy=True,
            qty=20,
            price=8,
        )
    )
    obe = OrderBookEntry(price=10, is_buy=False, open_orders=[existing_order])
    assert incoming_order.status == OrderFillStatus.NONE

    # check that trying to match orders with incompatible limit prices raises
    # an exception
    with pytest.raises(ValueError, match="price"):
        obe.match_against(incoming_order)

    # check that everything is unchanged and no fills were generated
    assert incoming_order.status == OrderFillStatus.NONE
    assert not incoming_order.fills
    assert existing_order.status == OrderFillStatus.NONE
    assert not existing_order.fills


def test_order_book_entry_partially_fill_existing():
    """Test that an incoming order fills multiple existing orders sitting in
    the order book entry, including partial fills.
    """
    sell_order_1 = Order(
        symbol="AAPL.OQ",
        timestamp=datetime.utcnow(),
        is_buy=False,
        qty=8,
        price=10,
    )
    sell_order_2 = Order(
        symbol="AAPL.OQ",
        timestamp=datetime.utcnow(),
        is_buy=False,
        qty=6,
        price=10,
    )
    buy_order = Order(
        symbol="AAPL.OQ",
        timestamp=datetime.utcnow(),
        is_buy=True,
        qty=10,
        price=13,
    )
    incoming_order = OrderFill(order=buy_order)
    expected_full_match = OrderFill(
        order=sell_order_1,
        fills=[
            Fill(timestamp=buy_order.timestamp, qty=8, price=10),
        ],
    )
    expected_partial_match = OrderFill(
        order=sell_order_2,
        fills=[
            Fill(timestamp=buy_order.timestamp, qty=2, price=10),
        ],
    )
    obe = OrderBookEntry(
        price=10,
        is_buy=False,
        open_orders=[
            OrderFill(order=sell_order_1),
            OrderFill(order=sell_order_2),
        ],
    )
    matched = obe.match_against(incoming_order)
    # check that sell orders 1 and 2 are matched. sell order 1 is fully filled,
    # while sell order 2 is only partially filled
    assert matched == [expected_full_match]
    assert obe.open_orders == [expected_partial_match]
    # check that the input order has been modified and filled too
    assert incoming_order.status == OrderFillStatus.FILLED
    assert incoming_order.fill_qty == 10
    assert incoming_order.open_qty == 0
    assert incoming_order.avg_fill_price == 10
    assert incoming_order.fills == [
        Fill(
            timestamp=buy_order.timestamp,
            qty=10,
            price=10,
        )
    ]


def test_order_book_entry_partially_fill_incoming():
    """Test that an incoming order is partially filled by multiple existing
    orders sitting in the order book entry.
    """
    buy_order_1 = Order(
        symbol="AAPL.OQ",
        timestamp=datetime.utcnow(),
        is_buy=True,
        qty=8,
        price=10,
    )
    buy_order_2 = Order(
        symbol="AAPL.OQ",
        timestamp=datetime.utcnow(),
        is_buy=True,
        qty=6,
        price=10,
    )
    sell_order = Order(
        symbol="AAPL.OQ",
        timestamp=datetime.utcnow(),
        is_buy=False,
        qty=20,
        price=9,
    )
    incoming_order = OrderFill(order=sell_order)
    expected_full_match_1 = OrderFill(
        order=buy_order_1,
        fills=[Fill(timestamp=sell_order.timestamp, qty=8, price=10)],
    )
    expected_full_match_2 = OrderFill(
        order=buy_order_2,
        fills=[Fill(timestamp=sell_order.timestamp, qty=6, price=10)],
    )
    obe = OrderBookEntry(
        price=10,
        is_buy=True,
        open_orders=[
            OrderFill(order=buy_order_1),
            OrderFill(order=buy_order_2),
        ],
    )
    matched = obe.match_against(incoming_order)
    # check that sell orders 1 and 2 are matched and fully filled
    assert matched == [expected_full_match_1, expected_full_match_2]
    assert not obe.open_orders
    # check that the input order has been modified and partially filled too
    assert incoming_order.status == OrderFillStatus.PARTIALLY_FILLED
    assert incoming_order.fill_qty == 14
    assert incoming_order.open_qty == 6
    assert incoming_order.avg_fill_price == 10
    assert incoming_order.fills == [
        Fill(
            timestamp=sell_order.timestamp,
            qty=14,
            price=10,
        )
    ]
