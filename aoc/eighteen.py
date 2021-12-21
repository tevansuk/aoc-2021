import json
import re
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from math import ceil
from operator import add
from pathlib import Path
from typing import Generator, Optional, Type, TypeVar

from aoc.utils.timing import catchtime

NumT = TypeVar("NumT", bound="Number")


class Number(ABC):
    @classmethod
    @abstractmethod
    def parse(cls: Type[NumT], inp: str) -> NumT:
        ...

    @property
    @abstractmethod
    def magnitude(self: NumT) -> int:
        ...

    @abstractmethod
    def __add__(self: NumT, other: NumT) -> NumT:
        ...

    @abstractmethod
    def __iadd__(self: NumT, other: NumT) -> NumT:
        ...

    @abstractmethod
    def explode(self: NumT) -> bool:
        ...

    @abstractmethod
    def split(self: NumT) -> bool:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...


# I think this is my preferred solution - a simple binary tree
# I think this presents the logic for all the different components in the cleanest
# possible way. Its also the slowest version!
@dataclass(eq=False)
class Node:
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    value: Optional[int] = None

    @classmethod
    def parse(cls, inp: list | int) -> "Node":
        if isinstance(inp, list):
            a, b = inp
            return cls(left=cls.parse(a), right=cls.parse(b))
        else:
            return cls(value=inp)

    @property
    def leaf(self) -> bool:
        return self.value is not None

    def split(self) -> bool:
        if self.leaf and self.value is not None and self.value > 9:
            left = self.value // 2
            self.left = Node(value=left)
            self.right = Node(value=self.value - left)
            self.value = None
            return True
        elif self.left is not None and self.right is not None:
            return self.left.split() or self.right.split()
        return False

    @property
    def magnitude(self) -> int:
        if self.value is not None:  # Yes I know thats what .leaf is, but mypy does not
            return self.value
        if self.left is None or self.right is None:
            raise Exception("Broken tree")
        return 3 * self.left.magnitude + 2 * self.right.magnitude

    def __str__(self) -> str:
        if self.leaf:
            return str(self.value)
        return f"[{self.left},{self.right}]"

    def __iter__(self):
        if self.left is not None:
            yield from self.left
        if self.value is not None:
            yield self
        if self.right is not None:
            yield from self.right

    def _find_leaf_node_pair_parent(self, depth=0, min_depth=4):
        if self.leaf:
            return
        if self.left is not None:
            yield from self.left._find_leaf_node_pair_parent(depth=depth + 1, min_depth=min_depth)
        if depth >= min_depth and self.left.leaf and self.right.leaf:
            yield self
        if self.right is not None:
            yield from self.right._find_leaf_node_pair_parent(depth=depth + 1, min_depth=min_depth)


class NumberTree(Number):
    root: Node

    def __init__(self):
        self.root = Node()

    @classmethod
    def parse(cls, inp: str) -> "NumberTree":
        t = cls()
        t.root = Node.parse(json.loads(inp))
        return t

    @property
    def magnitude(self) -> int:
        return self.root.magnitude

    def __str__(self):
        return str(self.root)

    def __repr__(self):
        return f"NumberTree({self.root})"

    def __add__(self, other: "NumberTree") -> "NumberTree":
        t = self.__class__()
        t.root.left = deepcopy(self.root)
        t.root.right = deepcopy(other.root)
        t._reduce()
        return t

    def __iadd__(self, other: "NumberTree") -> "NumberTree":
        self.root = Node(left=self.root, right=deepcopy(other.root))
        self._reduce()
        return self

    def _reduce(self) -> None:
        while self.explode() or self.split():
            pass

    def explode(self) -> bool:
        bomb = next(self.root._find_leaf_node_pair_parent(), None)
        if not bomb:
            return False
        prev = None
        node_iter = iter(self.root)
        for node in node_iter:
            if node == bomb.left:
                break
            prev = node
        if prev:
            prev.value += bomb.left.value
        next(node_iter)
        if next_node := next(node_iter, None):
            next_node.value += bomb.right.value
        bomb.value = 0
        bomb.left = None
        bomb.right = None
        return True

    def split(self) -> bool:
        return self.root.split()


# OK, getting silly now, this is version 4, as a flat tree modelled by a list
# its a bit of 1 + 3, but explode() is a lot more complex because we dont have
# any node references


@dataclass(eq=False)
class NumberFlatTree(Number):
    nums: list

    @classmethod
    def parse(cls, inp: str) -> "NumberFlatTree":
        return cls(nums=json.loads(inp))

    def __add__(self, other: "NumberFlatTree") -> "NumberFlatTree":
        new_val = self.__class__(nums=[deepcopy(self.nums), deepcopy(other.nums)])
        new_val.reduce()
        return new_val

    def __iadd__(self, other: "NumberFlatTree") -> "NumberFlatTree":
        self.nums = [self.nums, deepcopy(other.nums)]
        self.reduce()
        return self

    @property
    def magnitude(self) -> int:
        return self._magnitude(self.nums)

    @classmethod
    def _magnitude(cls, nums) -> int:
        total = 0
        left, right = nums
        if isinstance(left, int):
            total += 3 * left
        else:
            total += 3 * cls._magnitude(left)
        if isinstance(right, int):
            total += 2 * right
        else:
            total += 2 * cls._magnitude(right)
        return total

    def reduce(self) -> None:
        while self.explode() or self.split():
            pass

    @classmethod
    def _node_iterator(cls, node, depth=1):
        left, right = node
        if isinstance(left, list):
            yield from cls._node_iterator(left, depth=depth + 1)
        else:
            yield left, node, depth, 0
        if isinstance(right, list):
            yield from cls._node_iterator(right, depth=depth + 1)
        else:
            yield right, node, depth, 1

    def __iter__(self):
        yield from self._node_iterator(self.nums, depth=1)

    def explode(self) -> bool:
        prev = None
        node_iter = iter(self)
        for (lnum, lsubtree, ldepth, ll_r) in node_iter:
            if ldepth >= 5:
                break
            prev = (lnum, lsubtree, ldepth, ll_r)
        else:
            return False
        rnum, _, _, _ = next(node_iter)
        next_node = next(node_iter, None)
        # The subtree containing the bomb to replace with 0 may be in either
        # psubtree or nsubtree
        if prev and prev[1][int(not prev[3])] == [lnum, rnum]:
            prev[1][int(not prev[3])] = 0
        elif next_node and next_node[1][int(not next_node[3])] == [lnum, rnum]:
            next_node[1][int(not next_node[3])] = 0
        else:
            # If its not, its a bit more complex, its the sibling of either psubtree
            # or nsubtree, so we need to walk the tree one more time to find it
            for pair in self._pair_iterator(self.nums):
                if next_node and pair == [[lnum, rnum], next_node[1]]:
                    pair[0] = 0
                    break
                elif prev and pair == [prev[1], [lnum, rnum]]:
                    pair[1] = 0
                    break
            else:
                raise Exception("Unexpected")
        if prev:
            prev[1][prev[3]] = prev[0] + lnum
        if next_node:
            next_node[1][next_node[3]] = next_node[0] + rnum
        return True

    @classmethod
    def _pair_iterator(cls, node):
        left, right = node
        if isinstance(left, list):
            yield from cls._pair_iterator(left)
            if isinstance(right, list):
                yield node
        if isinstance(right, list):
            yield from cls._pair_iterator(right)

    def split(self) -> bool:
        for num, subtree, _, l_r in self:
            if num > 9:
                subtree[l_r] = [num // 2, num - num // 2]
                return True
        return False

    def __str__(self) -> str:
        return str(self.nums).replace(" ", "")


# This was my second version. It builds a list of (effectively) tuples of (depth, value)
# and then operates on that list. This makes explode and split relatively simple to
# deal with, but __str__ and magnitude are bloody stupid.
# Annoyingly, its also the most efficient


@dataclass
class SPart:
    depth: int
    value: int


@dataclass
class NumberList(Number):
    nums: list[SPart]

    @classmethod
    def parse(cls, inp: str) -> "NumberList":
        depth = 0
        num = cls(nums=[])
        for elem in re.split(r"([\[\],])", inp):
            if elem == "[":
                depth += 1
            elif elem == "]":
                depth -= 1
            elif elem.isdigit():
                num.nums.append(SPart(depth=depth, value=int(elem)))
        return num

    def __add__(self, other: "NumberList") -> "NumberList":
        num = self.__class__(deepcopy(self.nums))
        num.nums.extend(deepcopy(other.nums))
        for n in num.nums:
            n.depth += 1
        num.reduce()
        return num

    def __iadd__(self, other: "NumberList") -> "NumberList":
        self.nums.extend(deepcopy(other.nums))
        for n in self.nums:
            n.depth += 1
        self.reduce()
        return self

    def reduce(self) -> None:
        while self.explode() or self.split():
            pass

    def explode(self) -> bool:
        bomb = next(((idx, num) for idx, num in enumerate(self.nums) if num.depth == 5), None)
        if not bomb:
            return False
        idx, num = bomb
        if idx > 0:
            self.nums[idx - 1].value += num.value
        if idx < len(self.nums) - 2:
            self.nums[idx + 2].value += self.nums[idx + 1].value
        self.nums[idx + 1] = SPart(value=0, depth=num.depth - 1)
        del self.nums[idx]
        return True

    def split(self) -> bool:
        split = next(((idx, num) for idx, num in enumerate(self.nums) if num.value > 9), None)
        if not split:
            return False
        idx, num = split
        self.nums[idx] = SPart(value=num.value // 2, depth=num.depth + 1)
        self.nums.insert(idx + 1, SPart(value=ceil(num.value / 2), depth=num.depth + 1))
        return True

    @property
    def magnitude(self) -> int:
        mags = deepcopy(self.nums)
        while (max_depth := max(val.depth for val in mags)) != 0:
            part_iter = iter(enumerate(mags))
            for idx, val in part_iter:
                if val.depth == max_depth:
                    mags[idx] = SPart(
                        value=3 * val.value + 2 * next(part_iter)[1].value, depth=val.depth - 1
                    )
                    del mags[idx + 1]
                    break
        return mags[0].value

    def __str__(self) -> str:
        def _str_iter():
            depth = 0
            nv = [0]
            for num in self.nums:
                while num.depth > depth:
                    yield "["
                    nv.append(0)
                    depth += 1
                yield str(num.value)
                nv[-1] += 1
                while nv and nv[-1] == 2:
                    yield "]"
                    depth -= 1
                    nv.pop()
                    if nv:
                        nv[-1] += 1
                yield ","

        return "".join(_str_iter())[:-1]


# This was my initial version. It simplifies parsing - the tree is just the list
# of values. I don't like this one quite so much, each explode/split requires
# turning the tree into a list of (number, indexes). I especially didn't like
# _add_to_loc / _replace_loc, so ugly.
# After getting this working, I immediately wrote the NumberList version, which
# I also disliked!


@dataclass
class NumberDumb(Number):
    nums: list

    @classmethod
    def parse(cls, inp: str) -> "NumberDumb":
        return cls(nums=json.loads(inp))

    def __add__(self, other: "NumberDumb") -> "NumberDumb":
        new_val = self.__class__([deepcopy(self.nums), deepcopy(other.nums)])
        new_val.reduce()
        return new_val

    def __iadd__(self, other: "NumberDumb") -> "NumberDumb":
        self.nums = [self.nums, deepcopy(other.nums)]
        self.reduce()
        return self

    @property
    def magnitude(self) -> int:
        return self._magnitude(self.nums)

    def reduce(self) -> None:
        while self.explode() or self.split():
            pass

    def explode(self) -> bool:
        nums = list(self._nums_to_loc(self.nums, []))
        for idx in range(len(nums)):
            n, loc = nums[idx]
            if len(loc) == 5:
                if idx > 0:
                    self._add_to_loc(n, nums[idx - 1][1])
                if idx < len(nums) - 2:
                    self._add_to_loc(nums[idx + 1][0], nums[idx + 2][1])
                self.nums[loc[0]][loc[1]][loc[2]][loc[3]] = 0
                return True
        return False

    def split(self) -> bool:
        nums = list(self._nums_to_loc(self.nums, []))
        for idx in range(len(nums)):
            n, loc = nums[idx]
            if n >= 10:
                repl = [n // 2, ceil(n / 2)]
                self._replace_loc(repl, loc)
                return True
        return False

    def _add_to_loc(self, n: int, loc: list[int]) -> None:
        if len(loc) == 5:
            self.nums[loc[0]][loc[1]][loc[2]][loc[3]][loc[4]] += n
        elif len(loc) == 4:
            self.nums[loc[0]][loc[1]][loc[2]][loc[3]] += n
        elif len(loc) == 3:
            self.nums[loc[0]][loc[1]][loc[2]] += n
        elif len(loc) == 2:
            self.nums[loc[0]][loc[1]] += n
        elif len(loc) == 1:
            self.nums[loc[0]] += n
        else:
            raise Exception("Unexpected")

    def _replace_loc(self, repl: list[int], loc: list[int]) -> None:
        if len(loc) == 4:
            self.nums[loc[0]][loc[1]][loc[2]][loc[3]] = repl
        elif len(loc) == 3:
            self.nums[loc[0]][loc[1]][loc[2]] = repl
        elif len(loc) == 2:
            self.nums[loc[0]][loc[1]] = repl
        elif len(loc) == 1:
            self.nums[loc[0]] = repl
        else:
            raise Exception("Unexpected")

    @classmethod
    def _magnitude(cls, nums: list) -> int:
        if isinstance(nums[0], int):
            left = 3 * nums[0]
        else:
            left = 3 * cls._magnitude(nums[0])
        if isinstance(nums[1], int):
            right = 2 * nums[1]
        else:
            right = 2 * cls._magnitude(nums[1])
        return left + right

    @classmethod
    def _nums_to_loc(
        cls, nums: list, depth: list[int]
    ) -> Generator[tuple[int, list[int]], None, None]:
        for i in range(2):
            if isinstance(nums[i], int):
                yield nums[i], depth + [i]
            else:
                for num in cls._nums_to_loc(nums[i], depth + [i]):
                    yield num

    def __str__(self) -> str:
        return str(self.nums).replace(" ", "")


NUMBER_TYPES: dict[str, Type[Number]] = {
    "dumb": NumberDumb,
    "list": NumberList,
    "tree": NumberTree,
    "flat_tree": NumberFlatTree,
}


def main(datafile: Path, num_type=None) -> None:
    for ntype in NUMBER_TYPES:
        if num_type is None or ntype == num_type:
            all_nums = parse_data(datafile, ntype)
            with catchtime(f"Q1: Number class {ntype} took: ") as timer:
                print(f"Q1: {q1(all_nums) = }")
            print(timer)
            with catchtime(f"Q2: Number class {ntype} took: ") as timer:
                print(f"Q2: {q2(all_nums) = }")
            print(timer)


def parse_data(datafile: Path, num_type) -> list[Number]:
    Number = NUMBER_TYPES[num_type]
    return [Number.parse(line) for line in datafile.read_text().strip().split("\n")]


def q1(all_nums: list[Number]) -> int:
    return reduce(add, all_nums).magnitude


def q2(all_nums: list[Number]) -> int:
    return max((n1 + n2).magnitude for n1 in all_nums for n2 in all_nums if n1 is not n2)
