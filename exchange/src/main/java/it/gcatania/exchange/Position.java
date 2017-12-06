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
