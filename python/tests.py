import unittest
from collections import Counter
from random_numbers import RandomGen

class RandomGenTest(unittest.TestCase):

    # the number of calls to be made to next_num()
    ITERATIONS = 10000
    # the maximum delta between expected and observed probabilities
    DELTA = .01
    # static seed value to get repeatable test results
    SEED = 42

    def setUp(self):
        # TODO might actually not be needed
        pass

    def run_test(self, numbers, probabilities):
        """
        sets up a random generator with the provided arguments, then
        generates a significant amount of random numbers and checks
        that the observed probabilities are close enough to the
        expected ones.
        """
        rnd_gen = RandomGen(numbers, probabilities, self.SEED)
        counts = Counter([rnd_gen.next_num() for _ in range(self.ITERATIONS)])
        observed_probabilities = {n: c / self.ITERATIONS for n, c in counts.items()}
        expected_probabilities = dict(zip(numbers, probabilities))
        self.compare(observed_probabilities, expected_probabilities)

    def compare(self, observed, expected):
        """
        compares two dictionaries expecting them to have the same
        key set and values that differ by at most the configured
        delta
        """
        self.assertEqual(len(observed), len(expected))
        for key, expected in expected.items():
            self.assertAlmostEqual(expected, observed[key], delta=self.DELTA)

    def test_probabilities_dont_add_to_one(self):
        # assuming input probabilities need to add up to 1 makes
        # mathematical sense and makes our life easier too
        # TODO implement
        pass

    def test_invalid_arguments(self):
        # TODO implement
        pass

    def test_single_number(self):
        # TODO implement
        pass

    def test_simple_split(self):
        # TODO implement
        pass

    def test_non_trivial_example(self):
        # TODO implement
        pass

if __name__ == '__main__':
    unittest.main()