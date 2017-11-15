package it.gcatania.randomnumbers;

public class RandomGen {
    // Values that may be returned by nextNum()
    private int[] randomNums;
    // Probability of the occurence of randomNums
    private float[] probabilities;
    /**
     Returns one of the randomNums. When this method is called
     multiple times over a long period, it should return the
     numbers roughly with the initialized probabilities.
     */
    public int nextNum() {
        return 0;
    }

    public static void main(String[] args) {
        System.out.println(new RandomGen().nextNum());
    }
}