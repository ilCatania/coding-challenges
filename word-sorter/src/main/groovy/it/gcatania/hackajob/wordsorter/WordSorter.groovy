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
package it.gcatania.hackajob.wordsorter

import java.util.regex.Matcher
import java.util.regex.Pattern


/**
 * @author ilCatania
 *
 */
class WordSorter
{

    private static final Pattern WORD_CAPTURE_PATTERN = ~/\w+/

    static String sortWords(String text)
    {
        Matcher m = WORD_CAPTURE_PATTERN.matcher(text)
        StringListValuedIntegerMap wordsByLength = new StringListValuedIntegerMap()
        while(m.find())
        {
            String word = m.group()
            int length = word.length()
            wordsByLength.add(length, word)
        }
        return wordsByLength.descendingMap().collect(
                { int length, List<String> words ->
                    words.collect(
                            { String word -> "$word - $length" })
                }).flatten().join('\n')
    }

    /**
     * helper class. of course it could be easily generalized
     */
    private static class StringListValuedIntegerMap extends TreeMap<Integer, List<String>>
    {

        void add(Integer key, String value)
        {
            List<String> l = super.get(key)
            if(l == null)
            {
                l = new ArrayList<String>()
                super.put(key, l)
            }
            l.add(value)
        }
    }
}