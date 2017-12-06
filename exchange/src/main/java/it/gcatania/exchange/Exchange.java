/**
 * Copyright 2017 Gabriele Catania <gabriele.ctn@gmail.com>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
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
