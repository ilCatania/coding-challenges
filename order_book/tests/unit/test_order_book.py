from datetime import datetime

from order_book.model import (
    Fill,
    Order,
    OrderBook,
    OrderBookEntry,
    OrderFill,
    OrderFillStatus,
)


def test_order_book_simple():
    """Test adding one order to the order book."""
    ob = OrderBook()
    o = Order(
        "AAPL.OQ",
        datetime(2022, 12, 5, 11, 45, 33, 154),
        is_buy=True,
        qty=10,
        price=12,
    )

    filled_orders = ob.receive(o)
    assert not filled_orders
    assert len(ob.buy_orders) == 1
    assert not ob.sell_orders
    assert ob.buy_orders[0] == OrderBookEntry(
        price=12, is_buy=True, open_orders=[OrderFill(o)]
    )


def test_order_book_multiple_same_price():
    """Test adding multiple orders at the same level."""
    ob = OrderBook()
    o1 = Order(
        "AAPL.OQ",
        datetime(2022, 12, 5, 11, 45, 33, 154),
        is_buy=True,
        qty=10,
        price=12,
    )
    o2 = Order(
        "AAPL.OQ",
        datetime(2022, 12, 5, 11, 45, 33, 624),
        is_buy=True,
        qty=5,
        price=12,
    )

    filled_orders = ob.receive(o1)
    assert not filled_orders
    filled_orders = ob.receive(o2)
    assert len(ob.buy_orders) == 1
    assert not ob.sell_orders
    expected_obe = OrderBookEntry(
        price=12, is_buy=True, open_orders=[OrderFill(o1), OrderFill(o2)]
    )
    assert ob.buy_orders[0] == expected_obe


def test_order_book_multiple_opposite():
    """Test adding orders in opposite directions."""
    ob = OrderBook()
    buy_order = Order(
        "AAPL.OQ",
        datetime(2022, 12, 5, 11, 45, 33, 154),
        is_buy=True,
        qty=10,
        price=12,
    )
    sell_order = Order(
        "AAPL.OQ",
        datetime(2022, 12, 5, 11, 45, 33, 624),
        is_buy=False,
        qty=8,
        price=15,
    )

    filled_orders = ob.receive(buy_order)
    assert not filled_orders
    filled_orders = ob.receive(sell_order)
    assert not filled_orders
    # orders do not cross so they should remain in the book
    assert len(ob.buy_orders) == 1
    assert len(ob.sell_orders) == 1
    assert ob.buy_orders[0] == OrderBookEntry(
        price=12, is_buy=True, open_orders=[OrderFill(buy_order)]
    )
    assert ob.sell_orders[0] == OrderBookEntry(
        price=15, is_buy=False, open_orders=[OrderFill(sell_order)]
    )


def test_order_book_multiple_prices():
    """Test adding multiple orders in the same direction at different levels.

    Buy orders should be sorted descending, while sell orders should be sorted
    ascending.
    """
    buy1 = Order(
        "AAPL.OQ",
        datetime(2022, 12, 5, 11, 45, 33, 154),
        is_buy=True,
        qty=10,
        price=12,
    )
    buy2 = Order(
        "AAPL.OQ",
        datetime(2022, 12, 5, 11, 45, 33, 624),
        is_buy=True,
        qty=8,
        price=13,
    )
    buy3 = Order(
        "AAPL.OQ",
        datetime(2022, 12, 5, 11, 45, 33, 751),
        is_buy=True,
        qty=5,
        price=11,
    )
    sell1 = Order(
        "AAPL.OQ",
        datetime(2022, 12, 5, 11, 45, 55, 154),
        is_buy=False,
        qty=2,
        price=15,
    )
    sell2 = Order(
        "AAPL.OQ",
        datetime(2022, 12, 5, 11, 45, 55, 331),
        is_buy=False,
        qty=11,
        price=19,
    )
    sell3 = Order(
        "AAPL.OQ",
        datetime(2022, 12, 5, 11, 45, 55, 987),
        is_buy=False,
        qty=7,
        price=17,
    )

    ob = OrderBook()
    for o in (buy1, sell1, buy2, sell2, buy3, sell3):
        assert not ob.receive(o), f"Unexpected fill on {o}!"
    assert ob.buy_orders == [
        OrderBookEntry.from_order(o) for o in (buy2, buy1, buy3)
    ]
    assert ob.sell_orders == [
        OrderBookEntry.from_order(o) for o in (sell1, sell3, sell2)
    ]


def test_order_book_simple_fill():
    """Test adding two matching orders to the order book.

    When the second order is added to the order book, it should match and cause
    the first order to also be removed and returned.
    """
    buy_order = Order(
        "AAPL.OQ",
        datetime(2022, 12, 5, 11, 45, 33, 154),
        is_buy=True,
        qty=10,
        price=12,
    )
    sell_order = Order(
        "AAPL.OQ",
        datetime(2022, 12, 5, 11, 45, 33, 241),
        is_buy=False,
        qty=10,
        price=12,
    )

    ob = OrderBook()
    assert not ob.receive(buy_order)
    filled_orders = ob.receive(sell_order)
    assert filled_orders == [
        OrderFill(
            order=buy_order,
            fills=[Fill(timestamp=sell_order.timestamp, qty=10, price=12)],
        ),
        OrderFill(
            order=sell_order,
            fills=[Fill(timestamp=sell_order.timestamp, qty=10, price=12)],
        ),
    ]
    assert not ob.sell_orders
    assert not ob.buy_orders


def test_order_book_entry_partially_fill_existing():
    """Test adding an order that partially fills existing orders on the order
    book, and the incoming order is partially filled so it is also added to the
    order book.
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
        price=12,
    )
    sell_order_3 = Order(
        symbol="AAPL.OQ",
        timestamp=datetime.utcnow(),
        is_buy=False,
        qty=1,
        price=12,
    )
    sell_order_4 = Order(
        symbol="AAPL.OQ",
        timestamp=datetime.utcnow(),
        is_buy=False,
        qty=20,
        price=14,
    )
    buy_order = Order(
        symbol="AAPL.OQ",
        timestamp=datetime.utcnow(),
        is_buy=True,
        qty=20,
        price=13,
    )
    expected_fill_1 = Fill(timestamp=buy_order.timestamp, qty=8, price=10)
    expected_fill_2 = Fill(timestamp=buy_order.timestamp, qty=6, price=12)
    expected_fill_3 = Fill(timestamp=buy_order.timestamp, qty=1, price=12)
    expected_matches = [
        OrderFill(order=sell_order_1, fills=[expected_fill_1]),
        OrderFill(order=sell_order_2, fills=[expected_fill_2]),
        OrderFill(order=sell_order_3, fills=[expected_fill_3]),
    ]
    ob = OrderBook()
    assert not ob.receive(sell_order_1)
    assert not ob.receive(sell_order_2)
    assert not ob.receive(sell_order_3)
    assert not ob.receive(sell_order_4)
    filled_orders = ob.receive(buy_order)
    assert filled_orders == expected_matches
    # 4th sell order price is too high so it stays on the order book unchanged
    assert len(ob.sell_orders) == 1
    assert ob.sell_orders[0] == OrderBookEntry(
        price=14,
        is_buy=False,
        open_orders=[OrderFill(order=sell_order_4)],
    )
    # incoming order is not fully filled so it gets added to the order book
    assert len(ob.buy_orders) == 1
    assert ob.buy_orders[0] == OrderBookEntry(
        price=13,
        is_buy=True,
        open_orders=[
            OrderFill(
                order=buy_order,
                fills=[
                    Fill(buy_order.timestamp, qty=8, price=10),
                    Fill(buy_order.timestamp, qty=7, price=12),
                ],
            )
        ],
    )
