"""
https://leetcode.com/problems/check-if-two-string-arrays-are-equivalent/

Given two string arrays word1 and word2, return true if the two arrays represent the same string, and false otherwise.

A string is represented by an array if the array elements concatenated in order forms the string.

"""
from itertools import chain, zip_longest
from typing import List

class Solution:
    def arrayStringsAreEqual(self, word1: List[str], word2: List[str]) -> bool:
        for c1, c2 in zip_longest(chain(*word1), chain(*word2)):
            if c1 != c2:
                return False
        return True
        
s = Solution()
assert s.arrayStringsAreEqual(["ab", "c"], ["a", "bc"])