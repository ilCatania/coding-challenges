"""
There are N bulbs linked to their respective switches. A bulb is on only
if all the previous bulbs are on. Given an array of numbers corresponding to
switches being turned on, write a function returning the number of moments in
which all turned on switches correspond to turned on bulbs.

Switch indices in the input array are 1-based.
"""
from typing import List, Optional


def solution(A: List[int]) -> int:
    if not A:
        return 0
    switches = [False] * len(A)
    bulbs = [False] * len(A)
    moments = 0
    for k_ in A:
        k = k_ - 1  # A is 1-based
        switches[k] = True
        if k == 0 or bulbs[k - 1]:
            bulbs[k] = True
            for n in range(k + 1, len(A)):
                if switches[n]:
                    bulbs[n] = True
                else:
                    break
        if switches == bulbs:
            moments += 1
    return moments


assert solution([]) == 0, "empty"
assert solution([1]) == 1, "single bulb, single moment"
assert solution([1, 2]) == 2, "two bulbs, two moments"
assert solution([2, 1]) == 1, "two bulbs, one moment"
assert solution([2, 3, 1]) == 1, "three bulbs, one moment"
assert solution([2, 1, 3]) == 2, "three bulbs, two moments"
assert solution([2, 1, 3, 5, 4]) == 3, "example from original problem statement"
