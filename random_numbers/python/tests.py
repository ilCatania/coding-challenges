import unittest
from collections import Counter
from random_numbers import RandomGen
from random_numbers_pythonic import random_numbers_gen


class RandomGenTest(unittest.TestCase):

    # the number of calls to be made to next_num()
    ITERATIONS = 10000
    # the maximum delta between expected and observed probabilities
    DELTA = .01
    # static seed value to get repeatable test results
    SEED = 42

    def run_test(self, numbers, probabilities):
        """
        sets up a random generator with the provided arguments,
        then generates a significant amount of random numbers and checks
        that the observed probabilities are close enough to the expected ones.
        """

        # this tests the less pythonic version
        # rnd_gen = RandomGen(numbers, probabilities, self.SEED)
        # counts = Counter((rnd_gen.next_num() for _ in range(
        # self.ITERATIONS)))

        # this tests the more pythonic version
        rnd_gen = random_numbers_gen(numbers, probabilities, seed=self.SEED)
        counts = Counter((next(rnd_gen) for _ in range(self.ITERATIONS)))

        observed_probabilities =\
            {n: (c / self.ITERATIONS) for n,c in counts.items()}
        expected_probabilities = dict(zip(numbers, probabilities))
        self.compare(observed_probabilities, expected_probabilities)

    def compare(self, observed, expected):
        """
        compares two dictionaries expecting them to have the same key set
        and values that differ by at most the configured delta
        """
        self.assertEqual(len(observed), len(expected))
        for key, expected_value in expected.items():
            self.assertAlmostEqual(
                expected_value, observed[key], delta=self.DELTA)

    def test_too_many_probabilities(self):
        numbers = [3.14, 2.71]
        probabilities = [.5, .3, .2]
        with self.assertRaises(ValueError):
            RandomGen(numbers, probabilities)

    def test_too_few_probabilities(self):
        numbers = [3.14, 2.71, 1]
        probabilities = [.7, .3]
        with self.assertRaises(ValueError):
            RandomGen(numbers, probabilities)

    def test_missing_arguments(self):
        numbers = [3.14, 2.71, 1]
        probabilities = [.5, .3, .2]
        with self.assertRaises(ValueError):
            RandomGen(numbers, [])
        with self.assertRaises(ValueError):
            RandomGen([], probabilities)

    def test_probabilities_dont_add_to_one(self):
        """
        assuming input probabilities need to add up to 1 makes mathematical
        sense and makes our life easier too
        """
        numbers = [3.14, 2.71]
        probabilities = [.5, .6]
        with self.assertRaises(ValueError):
            RandomGen(numbers, probabilities)

    def test_single_number(self):
        self.run_test([3.14], [1])

    def test_simple_split(self):
        self.run_test([3.14, 2.71], [.5, .5])

    def test_non_trivial_example(self):
        self.run_test([-1, 0, 1, 2, 3], [.01, .3, .58, .1, .01])


if __name__ == '__main__':
    unittest.main()