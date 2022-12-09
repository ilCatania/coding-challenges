Order book
==========

A simple order book implementation. Submit orders, match them, keep track of
fills. Example usage:

```python
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
ob.receive(buy_order)
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
```

See the unit tests for further examples.