package it.gcatania.exchange;

import org.junit.*;


public class PositionTest {

    // TODO implement check and enable test
    // @Test(expected = IllegalArgumentException.class)
    public void checkOrderPriceWhenAdding() {
        Position p = new Position(1);
        Order o = new Order(OrderType.BUY, 12, 2);

        p.add(o);
    }



}
