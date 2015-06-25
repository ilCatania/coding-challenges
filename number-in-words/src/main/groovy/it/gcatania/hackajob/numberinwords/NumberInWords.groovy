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


/**
 * @author ilCatania
 *
 */
class NumberInWords
{
    static final Map<Long, String> MAGNITUDES = [1: '', 1000L: 'thousand', 1000000: 'million', 1000000000: 'billion']
    static final Map<Integer, String> UNITS = [
        1: 'one', 2: 'two', 3: 'three',
        4: 'four', 5: 'five', 6: 'six',
        7: 'seven', 8: 'eight', 9: 'nine']
    // let's also keep corner cases for eleven, twelve, etc. here
    static final Map<Integer, String> TENS = [
        10: 'ten', 11: 'eleven', 12: 'twelve',
        13: 'thirteen', 14: 'fourteen', 15: 'fifteen',
        16: 'sixteen', 17: 'seventeen', 18: 'eighteen',
        19: 'nineteen', 20: 'twenty', 30: 'thirty',
        40: 'forty', 50: 'fifty', 60: 'sixty',
        70: 'seventy', 80: 'eighty', 90: 'ninety']


    /**
     * returns the word version of an input number, for example:
     * <dl>
     * <dt>0</dt><dd>zero</dd>
     * <dt>23</dt><dd>twenty-three</dd>
     * <dt>28711</dt><dd>twenty-eight thousand seven hundred eleven</dd>
     * </dl>
     * @param n the number
     * @return the word version
     */
    static String inWords(Number n)
    {
        if(n.longValue() == 0L) return 'zero'
        return MAGNITUDES.collect(
                { long magnitude, String magnitudeName ->
                    long upperMagnitude = magnitude * 1000
                    int digitsForMagnitude = (n.longValue() % upperMagnitude) / magnitude
                    return wordGroup(digitsForMagnitude, magnitudeName)
                }).findAll({!it.empty}).reverse().join(' ')
    }

    private static String wordGroup(int digitsForMagnitude, String magnitudeName) {
        if(digitsForMagnitude == 0) return ''
        StringBuilder output = new StringBuilder()
        boolean outputEmpty = true
        int hundreds = digitsForMagnitude / 100
        if(hundreds > 0) {
            output.append(UNITS.get(hundreds)).append(' ').append('hundred')
            outputEmpty = false
        }
        int tens = digitsForMagnitude % 100
        if(tens > 0) {
            if(!outputEmpty) output.append(' ')
            String singleTensWord = TENS.get(tens)
            if(singleTensWord != null) {
                output.append(singleTensWord)
            }
            else {
                // if we are here, it's guaranteed that the tens digits are in the form tens-units (e.g. seventy-three)
                // otherwise a single tens word would have been found
                int tensFirstDigit = tens / 10
                if(tensFirstDigit > 0) {
                    output.append(TENS.get(tensFirstDigit*10)).append('-')
                }
                int tensSecondDigit = tens % 10
                // this will always be nonzero, otherwise TENS.get() above would have returned something
                output.append(UNITS.get(tensSecondDigit))
            }
        }
        if(!magnitudeName.empty) output.append(' ').append(magnitudeName)
        return output.toString()
    }

}