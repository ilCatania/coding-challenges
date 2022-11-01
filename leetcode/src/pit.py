"""
Find the maximum pit depth in an array of integers.
"""
from typing import List


def pit_depth(start, bottom, end):
    """The pit depth."""
    return min(start - bottom, end - bottom)


def solution(A: List[int]) -> int:
    max_depth = -1
    state = None
    if not A:
        return max_depth
    prev = A[0]
    last_top = prev
    last_bottom = None
    for curr in A[1:]:
        if curr < prev:
            next_state = "down"
        elif curr > prev:
            next_state = "up"
        else:
            next_state = None
        if (
            state == "up"
            and next_state != "up"
            and last_top is not None
            and last_bottom is not None
        ):
            # prev ends a pit
            curr_depth = pit_depth(last_top, last_bottom, prev)
            max_depth = max(max_depth, curr_depth)
        if state != "down" and next_state == "down":
            # we were at the top
            last_top = prev
        elif state == "down" and next_state == "up":
            # we were at the bottom
            last_bottom = prev
        state = next_state
        prev = curr

    if state == "up" and last_top is not None and last_bottom is not None:
        # pit at the end
        curr_depth = pit_depth(last_top, last_bottom, prev)
        max_depth = max(max_depth, curr_depth)
    print(f"Input: {A}, solution: {max_depth}")
    return max_depth


assert solution([]) == -1
assert solution([0]) == -1
assert solution([5, 4, 1, -3]) == -1  # no pit, just monotone decreasing
assert solution([0, 2, 3]) == -1  # no pit, just monotone increasing
assert solution([-1, 0, 0, 1]) == -1  # not a pit because not strictly <>
assert solution([1, 2, 1]) == -1  # not a pit because it goes upwards
assert solution([1, 0, 1]) == 1  # simple pit
assert solution([0, 0, 1, 0, 1]) == 1  # simple pit with rubbish before
assert solution([1, 0, 1, 0, 0]) == 1  # simple pit with rubbish after
assert solution([2, 0, 3]) == 2  # asymmetric pit
assert solution([2, 0, -1, 5]) == 3  # long pit
assert solution([5, 3, 8, 0, 1]) == 2  # two pits sharing delimiter, min 1st
assert solution([5, 3, 8, 0, 9]) == 8  # two pits sharing delimiter, min last
assert solution([0, 1, 3, -2, 0, 1, 0, -3, 2, 3]) == 4
