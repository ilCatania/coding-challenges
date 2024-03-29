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

public class PositionTest {

    // TODO implement check and enable test
    // @Test(expected = IllegalArgumentException.class)
    public void checkOrderPriceWhenAdding() {
        Position p = new Position(1);
        Order o = new Order(OrderType.BUY, 12, 2);

        p.add(o);
    }

}
