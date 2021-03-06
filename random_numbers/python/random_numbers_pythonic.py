from random import Random
from math import fsum
from itertools import accumulate
from bisect import bisect_left


def random_numbers_gen(numbers, probabilities, seed=None):
    """
    :param numbers: a list of random numbers
    :param probabilities: the probabilities of returning each of the
    respective ``numbers``. Probabilities should add to ``1``
    :param seed: an optional seed value for the random generator
    :return: a generator returning each of ``numbers`` according to their
    ``probabilities``
    """
    if 1 != fsum(probabilities):
        raise ValueError("Probabilities: {} should add to 1, not {}!"
                         .format(probabilities, fsum(probabilities)))
    rnd = Random()
    rnd.seed(seed)
    cumulatives = list(accumulate(probabilities))
    while True:
        roll = rnd.random()
        i = bisect_left(cumulatives, roll)
        yield numbers[i]