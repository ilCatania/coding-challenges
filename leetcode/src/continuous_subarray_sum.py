"""
https://leetcode.com/problems/continuous-subarray-sum/
Given an integer array nums and an integer k, return true if nums has a
continuous subarray of size at least two whose elements sum up to a multiple of
k, or false otherwise.

An integer x is a multiple of k if there exists an integer n such that
x = n * k. 0 is always a multiple of k.
"""
from typing import List


class Solution:
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        for i in range(len(nums)):
            for j in range(i + 2, len(nums) + 1):
                if not (sum(nums[i:j]) % k):
                    return True
        return False


s = Solution()
assert not s.checkSubarraySum([], 6)
assert not s.checkSubarraySum([12], 6)
assert not s.checkSubarraySum([5, 4], 6)
assert s.checkSubarraySum([4, 2], 6)
assert s.checkSubarraySum([23, 2, 4, 6, 7], 6)
assert not s.checkSubarraySum([23, 2, 6, 4, 7], 13)
