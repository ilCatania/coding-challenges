import random

class RandomGen(object):
    # Values that may be returned by next_num()
    _random_nums = []
    # Probability of the occurence of random_nums
    _probabilities = []
    _rnd = random.Random()

    def __init__(self, numbers, probabilities, seed=None):
        self._random_nums = numbers
        self._probabilities = probabilities
        self._rnd.seed(seed)

    def seed(self, seed_value):
        self._rnd.seed(seed_value)

    def next_num(self):
        """
        Returns one of the randomNums. When this method is called
        multiple times over a long period, it should return the
        numbers roughly with the initialized probabilities.
        """
        pass
