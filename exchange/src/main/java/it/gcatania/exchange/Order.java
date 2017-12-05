package it.gcatania.exchange;

public class Order {

    public final OrderType type;
    public final String instrument = "GOLD";
    public final int quantity;
    public final double price;

    public Order(OrderType type, int quantity, double price) {
        this.type = type;
        this.quantity = quantity;
        this.price = price;
    }

    // toString
    // equals
    // hashcode

}