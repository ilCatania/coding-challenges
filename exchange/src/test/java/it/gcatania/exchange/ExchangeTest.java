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
