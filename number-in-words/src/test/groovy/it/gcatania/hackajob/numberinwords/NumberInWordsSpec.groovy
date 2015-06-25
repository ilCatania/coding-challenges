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
        388500611009L || 'three hundred eighty-eight billion five million six hundred eleven thousand nine'
    }
}
