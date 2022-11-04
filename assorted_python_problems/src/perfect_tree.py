from extratypes import Tree

from collections import deque

# import networkx as nx  # ModuleNotFoundError: No module named 'networkx' (sad)


def perfect_tree_size(t: Tree) -> int:
    """
    Return the size of the biggest perfect subtree having the input root.

    Also caches the size on the objects to avoid navigating the tree
    multiple times.
    """
    if t is None:
        return 0
    if not hasattr(t, "_size"):  # speed!
        t._size = 1
        l_size = perfect_tree_size(t.l)
        r_size = perfect_tree_size(t.r)
        if l_size == r_size:
            # two perfect subtrees with the same size, meaning the resulting
            # tree is also perfect
            t._size += 2 * l_size
    return t._size


def solution(T):
    # I'm going to do it with recursion even though I know it will not be
    # performing enough, because I'm not smart enough to do it iteratively
    stack = deque([T])
    max_size = 0
    while stack:
        t = stack.pop()
        s = perfect_tree_size(t)
        if s:
            max_size = max(max_size, s)
        if t.l:
            stack.append(t.l)
        if t.r:
            stack.append(t.r)
    return max_size


for t, (expected, msg) in {
    (1, None, None): (1, "one node"),
    (1, (2, None, None), None): (1, "two nodes (left)"),
    (1, None, (2, None, None)): (1, "two nodes (right)"),
    (1, (2, None, None), (3, None, None)): (3, "three nodes"),
    (1, (2, (4, None, None), None), (3, None, None)): (3, "four nodes"),
    (0, (1, (2, None, None), (3, None, None)), None): (3, "four nodes (top)"),
    (
        1,
        (2, None, (4, None, None)),
        (
            3,
            (5, (7, None, None), (8, None, None)),
            (6, (9, None, None), (10, (11, None, None), None)),
            None,
        ),
    ): (7, "from problem statement"),
}.items():
    assert solution(Tree.create_tree(t)) == expected, msg
