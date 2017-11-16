from random import Random
from math import fsum


class RandomGen(object):
    # Values that may be returned by next_num()
    _random_nums = []
    # Probability of the occurrence of random_nums
    _probabilities = []
    # Our own random instance to allow seeding
    _rnd = Random()

    def __init__(self, numbers, probabilities, seed=None):
        """
        Initializes a new random number generator
        :param numbers: the numbers to return upon calling ``next_num()``
        :param probabilities: the probabilities associated to the respective
        number. Probabilities should add to ``1``
        :param seed: an optional seed value for the random generator
        """
        if not numbers:
            raise ValueError("No numbers provided!")
        if not probabilities:
            raise ValueError("No probabilities provided!")
        if len(numbers) != len(probabilities):
            raise ValueError("{} numbers but {} probabilities provided!"
                    .format(len(numbers), len(probabilities)))
        if 1 != fsum(probabilities):
            raise ValueError("Probabilities: {} should add to 1, not {}!"
                             .format(probabilities, fsum(probabilities)))
        self._random_nums = numbers
        # TODO for better performance we should probably store the
        # cumulative probabilites directly
        self._probabilities = probabilities
        self._rnd.seed(seed)

    def seed(self, seed_value):
        self._rnd.seed(seed_value)

    def next_num(self):
        """
        Returns one of the randomNums. When this method is called
        multiple times over a long period, it should return the
        numbers roughly with the initialized probabilities.
        :return: a number chosen from this instance's random numbers
        according to their probability distribution
        :raises RuntimeError: should never be raised unless the code is
        somehow buggy
        """
        roll = self._rnd.random()
        cumulative = 0
        for index, prob in enumerate(self._probabilities):
            cumulative += prob
            if roll < cumulative:
                return self._random_nums[index]
        # should never reach this point
        raise RuntimeError(
            "Invalid state! Numbers: {}, probabilities: {}, rolled: {}"
                .format(self._random_nums, self._probabilities, roll))
