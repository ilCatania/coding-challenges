from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Tree:
    x: int
    l: "Tree"
    r: "Tree"

    @staticmethod
    def create_tree(t: Tuple) -> Optional["Tree"]:
        if t is None:
            return None
        return Tree(t[0], Tree.create_tree(t[1]), Tree.create_tree(t[2]))
