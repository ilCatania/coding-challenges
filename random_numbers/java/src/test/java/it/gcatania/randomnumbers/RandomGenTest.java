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
package it.gcatania.randomnumbers;

import org.junit.Test;

import static org.junit.Assert.*;

import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class RandomGenTest {

    private static final int ITERATIONS = 1000000;
    private static final double DELTA = .001;
    private static final int SEED = 42;

    private static void runTest(int[] numbers, double[] probabilities) {
        RandomGen randomGen = new RandomGen(numbers, probabilities, SEED);

        Map<Integer, Long> counts = IntStream.range(0, ITERATIONS)
                .mapToObj(i -> randomGen.nextNum())
                .collect(Collectors.groupingBy(Function.identity(),
                        Collectors.counting()));

        Map<Integer, Double> observedProbabilities = counts.entrySet()
                .parallelStream().collect(Collectors.toMap(
                        e -> e.getKey(),
                        e -> (double) e.getValue() / ITERATIONS));
        Map<Integer, Double> expectedProbabilities = IntStream
                .range(0, numbers.length).boxed()
                .collect(Collectors.toMap(
                        i -> numbers[i],
                        i -> probabilities[i]));
        compare(observedProbabilities, expectedProbabilities);
    }

    private static void compare(Map<Integer, Double> obs, Map<Integer, Double> exp) {
        assertEquals(exp.size(), obs.size());
        obs.forEach((n, observed) -> assertEquals(exp.get(n), observed, DELTA));
    }

    @Test(expected = IllegalArgumentException.class)
    public void tooManyProbabilities() {
        int[] numbers = { 3, 2 };
        double[] probabilities = { .5, .3, .2 };
        runTest(numbers, probabilities);
    }

    @Test(expected = IllegalArgumentException.class)
    public void tooFewProbabilities() {
        int[] numbers = { 3, 2, 1 };
        double[] probabilities = { .7, .3 };
        runTest(numbers, probabilities);
    }

    @Test(expected = NullPointerException.class)
    public void missingArguments() {
        double[] probabilities = { .5, .3, .2 };
        runTest(null, probabilities);
    }

    @Test(expected = IllegalArgumentException.class)
    public void probabilitiesDontAddToOne() {
        int[] numbers = { 3, 2, 1 };
        double[] probabilities = { .5, .3, .1 };
        runTest(numbers, probabilities);
    }

    @Test
    public void singleNumber() {
        runTest(new int[] { 3 }, new double[] { 1 });
    }

    @Test
    public void simpleSplit() {
        runTest(new int[] { 3, 4 }, new double[] { .5, .5 });
    }

    @Test
    public void nonTrivialCase() {
        runTest(new int[] { -1, 0, 1, 2, 3 }, new double[] { .01, .3, .58, .1, .01 });
    }
}
