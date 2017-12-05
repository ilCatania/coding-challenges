package it.gcatania.exchange;

import java.util.Comparator;
import java.util.SortedMap;
import java.util.TreeMap;

public class Exchange {

    private final SortedMap<Double, Position> buyPositions = new TreeMap<>(Comparator.reverseOrder());
    private final SortedMap<Double, Position> sellPositions = new TreeMap<>();

    public void submit(Order o) {
        SortedMap<Double, Position> positions = o.type == OrderType.BUY ? buyPositions : sellPositions;

        Position p = positions.get(o.price);
        if (p == null) {
            p = new Position(o);
            positions.put(p.price, p);
            return;
        }
        p.add(o);
    }

    public String currentFlow() {
        return new StringBuilder().append("Buy side:\n")
                .append(positionsAsString(buyPositions)).append("\nSell side:\n")
                .append(positionsAsString(sellPositions)).toString();
    }

    private String positionsAsString(SortedMap<Double, Position> positions) {
        if (positions.isEmpty()) return "EMPTY";
        int i = 0;
        StringBuilder sb = new StringBuilder();
        for (Position p : positions.values()) {
            sb.append(++i).append(") ").append(p).append('\n');
        }
        return sb.toString();
    }

}
