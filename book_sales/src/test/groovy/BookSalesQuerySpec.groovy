/*
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
import groovy.sql.Sql
import spock.lang.Shared
import spock.lang.Specification

import java.time.LocalDate

class BookSalesQuerySpec extends Specification {
    // use jdbc:h2:mem:;TRACE_LEVEL_SYSTEM_OUT=2 for sql logs
    @Shared sql = Sql.newInstance("jdbc:h2:mem:", "org.h2.Driver")

    def setupSpec() {
        sql.execute(this.class.getResource('/sql/schema.sql').text)

        LocalDate today = LocalDate.now()
        LocalDate threeYearsAgo = today.minusYears(3)
        LocalDate fiveMonthsAgo = today.minusMonths(5)
        sql.withBatch(this.class.getResource('/sql/insert_product_template.sql').text, { s ->
            s.addBatch(id: 1, name: 'yes; base case', from: today.minusWeeks(12))
            s.addBatch(id: 2, name: 'yes; more copies sold in previous years', from: threeYearsAgo)
            s.addBatch(id: 3, name: 'yes; an order with zero copies sold exists', from: threeYearsAgo)
            s.addBatch(id: 4, name: 'yes; no copies sold ever', from: threeYearsAgo)
            s.addBatch(id: 5, name: 'yes; more copies due to be sold in the future', from: threeYearsAgo)
            s.addBatch(id: 11, name: 'no; available within last month', from: today.minusDays(8))
            s.addBatch(id: 12, name: 'no; not yet available', from: today.plusDays(5))
            s.addBatch(id: 13, name: 'no; more than 10 copies sold in year', from: threeYearsAgo)
            s.addBatch(id: 14, name: 'no; exactly 10 copies sold in year', from: threeYearsAgo)
        })
        int orderId = 0
        sql.withBatch(this.class.getResource('/sql/insert_order_template.sql').text, { s ->
            s.addBatch(id: orderId++, prodId: 1, qty: 3, dispatched: fiveMonthsAgo)
            s.addBatch(id: orderId++, prodId: 1, qty: 2, dispatched: today.minusWeeks(10))
            s.addBatch(id: orderId++, prodId: 1, qty: 4, dispatched: today.minusDays(1))
            s.addBatch(id: orderId++, prodId: 2, qty: 8, dispatched: fiveMonthsAgo)
            s.addBatch(id: orderId++, prodId: 2, qty: 3, dispatched: threeYearsAgo)
            s.addBatch(id: orderId++, prodId: 3, qty: 0, dispatched: fiveMonthsAgo)
            s.addBatch(id: orderId++, prodId: 5, qty: 1, dispatched: fiveMonthsAgo)
            s.addBatch(id: orderId++, prodId: 5, qty: 12, dispatched: today.plusWeeks(5))
            s.addBatch(id: orderId++, prodId: 11, qty: 7, dispatched: today.minusDays(6))
            s.addBatch(id: orderId++, prodId: 12, qty: 8, dispatched: today.plusDays(12))
            s.addBatch(id: orderId++, prodId: 13, qty: 6, dispatched: fiveMonthsAgo)
            s.addBatch(id: orderId++, prodId: 13, qty: 8, dispatched: today.minusWeeks(3))
            s.addBatch(id: orderId++, prodId: 14, qty: 10, dispatched: fiveMonthsAgo)
        })
    }

    def 'none of the wrong books are returned'() {
        expect:
        result['NAME'].startsWith('yes')

        where:
        result << sql.rows(this.class.getResource('/sql/query.sql').text)
    }

    def 'all of the right books are returned'() {
        when:
        def rows = sql.rows(this.class.getResource('/sql/query.sql').text)

        then:
        rows.size() == 5
    }
}