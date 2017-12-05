package it.gcatania.exchange;

import org.junit.*;


public class ExchangeTest {

    @Test
    public void testBasicAdd() {

        Exchange e = new Exchange();
        e.submit(new Order(OrderType.BUY, 1, 1));
        // TODO test


        e.submit(new Order(OrderType.SELL, 1, 1));

    }

    @Test
    public void testMultipleOrdersForPosition() {

        Exchange e = new Exchange();
        e.submit(new Order(OrderType.BUY, 1, 1));
        // TODO test


        e.submit(new Order(OrderType.BUY, 5, 1));

    }



    @Test
    public void testDisplayFlow1() {
        Exchange e = new Exchange();
        e.submit(new Order(OrderType.BUY, 2, 1));
        e.submit(new Order(OrderType.BUY, 3, 2));
        e.submit(new Order(OrderType.BUY, 4, 1));
        String actual = e.currentFlow();

        System.out.println(actual);

        Assert.assertEquals("", ""); // TODO
    }

    @Test
    public void testDisplayFlow2() {
        Exchange e = new Exchange();
        e.submit(new Order(OrderType.BUY, 10, 12.23));
        e.submit(new Order(OrderType.BUY, 20, 12.31));
        e.submit(new Order(OrderType.SELL, 5, 13.55));
        e.submit(new Order(OrderType.BUY, 5, 12.23));
        e.submit(new Order(OrderType.BUY, 15, 12.25));
        e.submit(new Order(OrderType.SELL, 5, 13.31));
        e.submit(new Order(OrderType.BUY, 30, 12.25));
        e.submit(new Order(OrderType.SELL, 5, 13.31));
        String actual = e.currentFlow();

        System.out.println(actual);

        Assert.assertEquals("", ""); // TODO
    }
}
