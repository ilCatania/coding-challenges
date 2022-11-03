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
    moments = 0
    rightmost_on_switch = 0
    for i, k in enumerate(A):
        rightmost_on_switch = max(rightmost_on_switch, k)
        if rightmost_on_switch == i + 1:  # positions in A are 1-based
            moments += 1
    return moments


assert solution([]) == 0, "empty"
assert solution([1]) == 1, "single bulb, single moment"
assert solution([1, 2]) == 2, "two bulbs, two moments"
assert solution([2, 1]) == 1, "two bulbs, one moment"
assert solution([2, 3, 1]) == 1, "three bulbs, one moment"
assert solution([2, 1, 3]) == 2, "three bulbs, two moments"
assert solution([2, 1, 3, 5, 4]) == 3, "example from original problem statement"
