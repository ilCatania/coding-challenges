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

import spock.lang.Specification


/**
 * @author ilCatania
 */
class WordSorterSpec extends Specification
{

    def "test sorting words"()
    {
        expect: WordSorter.sortWords(text) == sortedWords.collect({word-> "$word - ${word.length()}"}).join('\n')

        where:
        text || sortedWords
        '!"£$%' || []
        'se tu ci sei nel mio domani' || [
            'domani',
            'sei',
            'nel',
            'mio',
            'se',
            'tu',
            'ci'
        ]
        'guarda come dondolo' || ['dondolo', 'guarda', 'come']
        'Hi, world!' || ['world', 'Hi']
        'this is a test... is it not?' || [
            'this',
            'test',
            'not',
            'is',
            'is',
            'it',
            'a'
        ]
    }
}
