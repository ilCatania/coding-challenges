package it.gcatania.randomnumbers;

import java.util.Arrays;
import java.util.Random;
import java.util.stream.DoubleStream;

public class RandomGen {
    // Values that may be returned by nextNum()
    private final int[] randomNums;
    // Cumulative probabilities of the occurences of randomNums
    private final double[] cumulatives;
    private final Random random;


    public RandomGen(int[] randomNums, double[] probabilities, long seed) {
        this.randomNums = randomNums;
        if(1 != DoubleStream.of(probabilities).sum()) {
            throw new IllegalArgumentException("Probabilities don't add to 1!");
        }
        if(randomNums.length != probabilities.length) {
            throw new IllegalArgumentException(
                    "Length mismatch between numbers and probabilities!");
        }
        random = new Random(seed);
        cumulatives = new double[probabilities.length];
        double cumulative = 0d;
        for(int i = 0; i < probabilities.length; i++) {
            cumulative += probabilities[i];
            cumulatives[i] = cumulative;
        }
    }

    public RandomGen(int[] randomNums, double[] probabilities) {
        this(randomNums, probabilities, System.currentTimeMillis());
    }

    /**
     Returns one of the randomNums. When this method is called
     multiple times over a long period, it should return the
     numbers roughly with the initialized probabilities.
     */
    public int nextNum() {
        double roll = random.nextDouble();
        int found = Arrays.binarySearch(cumulatives, roll);
        return randomNums[-found-1];
    }

    public static void main(String[] args) {
        if(args.length<2) {
            System.out.println("must provide 2 arguments, " +
                    "each a list of numbers separated by commas\n" +
                    "example: 4,12,44 .6,.2,.2");
            return;
        }

        int[] n = Arrays.stream(args[0].split(","))
                .mapToInt(Integer::parseInt).toArray();
        double[] p = Arrays.stream(args[1].split(","))
                .mapToDouble(Double::parseDouble).toArray();
        System.out.println(new RandomGen(n, p).nextNum());
    }
}