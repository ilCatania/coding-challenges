"""
https://leetcode.com/problems/median-of-two-sorted-arrays/
Given two sorted arrays nums1 and nums2 of size m and n respectively, return the
median of the two sorted arrays.
"""
from statistics import median
from typing import List


def sorted_values(nums1: List[int], nums2: List[int]):
    """Return values from two arrays in sorted order."""
    i1 = 0
    i2 = 0
    while True:
        if i1 == len(nums1):
            if i2 < len(nums2):
                yield from nums2[i2:]
            return
        elif i2 == len(nums2):
            yield from nums1[i1:]
            return
        elif nums1[i1] < nums2[i2]:
            yield nums1[i1]
            i1 += 1
        else:
            yield nums2[i2]
            i2 += 1


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        if not nums1:
            return median(nums2) if nums2 else None
        if not nums2:
            return median(nums1)
        i1 = 0
        i2 = 0
        tot_len = len(nums1) + len(nums2)
        prev = None
        last = None
        for i, v in enumerate(sorted_values(nums1, nums2)):
            if i >= 1 + (tot_len // 2):
                break
            prev = last
            last = v

        if tot_len % 2:  # odd
            return last
        else:  # even
            return (last + prev) / 2


s = Solution()
assert s.findMedianSortedArrays([], []) is None
assert s.findMedianSortedArrays([1], []) == 1
assert s.findMedianSortedArrays([1, 3, 5], []) == 3
assert s.findMedianSortedArrays([1, 4], []) == 2.5
assert s.findMedianSortedArrays([], [1, 4]) == 2.5
assert s.findMedianSortedArrays([1], [4]) == 2.5
assert s.findMedianSortedArrays([4], [1]) == 2.5
assert s.findMedianSortedArrays([1, 3], [2]) == 2
assert s.findMedianSortedArrays([1, 2], [3, 4]) == 2.5
assert s.findMedianSortedArrays([1, 3], [2, 5, 6]) == 3
assert s.findMedianSortedArrays([1, 3], [2, 4, 5, 6]) == 3.5
