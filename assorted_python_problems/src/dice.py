"""
Given an array representing ordinary 6-sided dice and the number showing on
their top side, count the number of moves needed to have them all show the same
number on top.
"""
from typing import List, Optional
from collections import Counter


def solution(A: List[int]) -> int:
    # count the occurrence for each number from 1 to 6
    count = Counter(A)
    # at most we have to move every die once
    min_n_moves = len(A)
    for n in range(1, 7):
        # for each number n, the moves required to get all dice to show that
        # number are:
        # 0 for all dice already showing that face
        # 2 for all dice showing the opposite face 7-n
        # 1 for every other dice
        n_moves = len(A) + count[7 - n] - count[n]
        min_n_moves = min(min_n_moves, n_moves)
    return min_n_moves


assert solution([]) == 0, "empty"
assert solution([1]) == 0, "single die"
assert solution([1, 1]) == 0, "multiple dice, same face"
assert solution([1, 2]) == 1, "two dice, one move"
assert solution([1, 6]) == 2, "two dice, two moves"
assert solution([1, 1, 6]) == 2, "three dice, two numbers, two moves"
assert solution([1, 2, 5]) == 2, "three dice, three numbers, two moves"
assert solution([1, 2, 3]) == 2, "1st example from problem statement"
assert solution([1, 1, 6]) == 2, "2nd example from problem statement"
assert solution([1, 6, 2, 3]) == 3, "3rd example from problem statement"
