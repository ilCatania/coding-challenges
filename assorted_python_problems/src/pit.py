"""
Find the maximum pit depth in an array of integers.
"""
from typing import List, Optional


def pit_depth(start, bottom, end):
    """The pit depth."""
    return min(start - bottom, end - bottom)


def get_state(curr: int, next: int) -> Optional[str]:
    if next < curr:
        return "down"
    elif next > curr:
        return "up"
    else:
        return None


def solution(A: List[int]) -> int:
    max_depth = -1
    if not A:
        return max_depth
    curr = A[0]
    top = curr
    bottom = None
    curr_state = None
    for next in A[1:]:
        next_state = get_state(curr, next)

        if (
            curr_state == "up"
            and next_state != "up"
            and top is not None
            and bottom is not None
        ):
            # we're at the end of a pit
            curr_depth = pit_depth(top, bottom, curr)
            max_depth = max(max_depth, curr_depth)
        if curr_state != "down" and next_state == "down":
            # we're at the top
            top = curr
        elif curr_state == "down" and next_state == "up":
            # we're at the bottom
            bottom = curr
        curr_state = next_state
        curr = next

    if curr_state == "up" and top is not None and bottom is not None:
        # pit at the end
        curr_depth = pit_depth(top, bottom, curr)
        max_depth = max(max_depth, curr_depth)
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
