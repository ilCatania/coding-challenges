package it.gcatania.exchange;

import java.util.ArrayList;
import java.util.List;

public class Position {

    private final String instrument = "GOLD";
    private int quantity = 0;
    public final double price;
    private final List<Order> orders = new ArrayList<>();

    public Position(double price) {
        this.price = price;
    }

    public Position(Order o) {
        this.price = o.price;
        add(o);
    }

    public void add(Order o) {
        // TODO check whether the price is actually the same
        orders.add(o);
        quantity += o.quantity;
    }

    @Override
    public String toString() {
        return new StringBuilder().append("Price=").append(price)
                .append(", Total units=").append(quantity).toString();
    }
}
