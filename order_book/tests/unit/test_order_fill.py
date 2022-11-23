from datetime import datetime, timezone
from order_book.model import Order, OrderFill, OrderFillStatus
import pytest


@pytest.fixture
def fake_order() -> Order:
    return Order(
        "VOD.L", datetime(2022, 3, 2, 11, 33, 12, 55, timezone.utc), True, 120, 46.3
    )


def test_order_fill_zero(fake_order):
    of = OrderFill(fake_order)
    assert of.fill_qty == 0
    assert of.status == OrderFillStatus.NONE


def test_order_fill_single(fake_order):
    of = OrderFill(fake_order)
    of.register_fill(datetime.utcnow(), 120, 46.3)
    assert of.fill_qty == 120
    assert of.avg_fill_price == 46.3
    assert of.status == OrderFillStatus.FILLED


def test_order_fill_single(fake_order):
    of = OrderFill(fake_order)
    of.register_fill(datetime.utcnow(), 120, 46.3)
    assert of.fill_qty == 120
    assert of.avg_fill_price == 46.3
    assert of.status == OrderFillStatus.FILLED


def test_order_fill_multiple(fake_order):
    of = OrderFill(fake_order)
    of.register_fill(datetime.utcnow(), 110, 40)
    assert of.fill_qty == 110
    assert of.status == OrderFillStatus.PARTIALLY_FILLED
    of.register_fill(datetime.utcnow(), 10, 46.3)
    assert of.fill_qty == 120
    assert of.avg_fill_price == 40.525
    assert of.status == OrderFillStatus.FILLED


def test_order_invalid_fill(fake_order):
    of = OrderFill(fake_order)
    with pytest.raises(ValueError, match="Invalid fill price"):
        of.register_fill(datetime.utcnow(), 110, 50)
    with pytest.raises(ValueError, match="Invalid fill quantity"):
        of.register_fill(datetime.utcnow(), 130, 40)
