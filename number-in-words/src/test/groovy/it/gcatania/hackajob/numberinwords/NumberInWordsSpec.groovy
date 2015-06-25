/*
 * Copyright 2015 Gabriele Catania <gabriele.ctn@gmail.com>
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
package it.gcatania.hackajob.numberinwords

import spock.lang.Specification
import spock.lang.Unroll


/**
 * @author ilCatania
 */
class NumberInWordsSpec extends Specification
{

    @Unroll
    def "number #n in words is #w"()
    {
        expect: NumberInWords.inWords(n) == w

        where:
        n || w
        0 || 'zero'
        2 || 'two'
        11 || 'eleven'
        20 || 'twenty'
        21 || 'twenty-one'
        44 || 'forty-four'
        100 || 'one hundred'
        101 || 'one hundred one'
        113 || 'one hundred thirteen'
        174 || 'one hundred seventy-four'
        7000L || 'seven thousand'
        6000000L || 'six million'
        2000000000L || 'two billion'
        123456789L || 'one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine'
        388500611003L || 'three hundred eighty-eight billion five hundred million six hundred eleven thousand three'
    }
}
