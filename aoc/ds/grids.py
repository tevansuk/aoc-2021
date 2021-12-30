from collections.abc import MutableSequence
from itertools import product
from typing import Callable, Iterable, Optional, Type, TypeVar

T = TypeVar("T", int, str)
B = TypeVar("B", bound="Grid")
ValueParser = Callable[[str], Iterable[T]]
Coord = tuple[int, int]
_3X3 = list(product([-1, 0, 1], repeat=2))
_ADJ = [(0, -1), (-1, 0), (1, 0), (0, 1)]


def int_digit_value_parser(text: str) -> Iterable[int]:
    """
    For parsing grids like:
        123
        456
        789
    """
    return (int(c) for c in text if c.isdigit())


def int_number_value_parser(separator: Optional[str] = None) -> ValueParser:
    """
    For parsing grids like:
        1 2 3
        4 5 6
        7 8 9
    or
        1,2,3
        4,5,6
        7,8,9
    """

    def parser(text: str) -> Iterable[int]:
        return (int(c) for line in text.strip().split("\n") for c in line.split(separator))

    return parser


def char_value_parser(text: str) -> Iterable[str]:
    """
    For parsing grids like:
        abc
        def
        ghi
    """
    return (c for c in text if not c.isspace())


def str_value_parser(separator: Optional[str] = None) -> ValueParser:
    """
    For parsing grids like:
        a b c
        d e f
        g h i
    or
        a,b,c
        d,e,f
        g,h,i
    """

    def parser(text: str) -> Iterable[str]:
        return (val for line in text.strip().split("\n") for val in line.split(separator))

    return parser


def hash_dot_parser(text: str) -> Iterable[int]:
    return (".#".index(c) for c in text if c in ".#")


block_formatter = " █".__getitem__


class Grid(list[T], MutableSequence[T]):
    w: int
    h: int
    value_type: Type[T]
    output_separator: str = ""
    value_formatter: Callable[[T], str] = str

    def __init__(self, value_type: Type[T], *args, **kwargs):
        self.value_type = value_type
        super().__init__(*args, **kwargs)

    @classmethod
    def parse(
        cls: Type[B],
        data: str,
        parser: ValueParser = int_digit_value_parser,
        value_type: Type[T] = int,
    ) -> B:
        """
        Read a grid from input. The grid should be laid out as a grid in the input.
        Eg:
            012
            345
            678
        """
        lines = data.strip().split("\n", 1)
        grid = cls(value_type, parser(lines[0]))
        grid.w = len(grid)
        if len(lines) > 1:
            grid.extend(parser(lines[1]))
        grid.h = len(grid) // grid.w
        return grid

    def adjacent(self, pos: int) -> Iterable[int]:
        """
        The points in the grid that are above, below, left and right of the pos
        """
        return (i + j * self.w for i, j in self.xyadjacent(*self.pos2coord(pos)))

    def surrounding(self, pos: int) -> Iterable[int]:
        """
        The points surrounding the pos, eg adjacent() + diagonals
        """
        return self.containing(pos, False)

    def containing(self, pos: int, include_pos=True) -> Iterable[int]:
        """
        3x3 grid positions surrounding pos. Inside the grid only - use xycontaining
        for positions outside the grid
        """
        x, y = self.pos2coord(pos)
        return (
            i + j * self.w
            for i, j in self.xycontaining(x, y, outside=False, include_self=include_pos)
        )

    def xycontaining(
        self, x: int, y: int, outside: bool = False, include_self: bool = True
    ) -> Iterable[Coord]:
        """
        3x3 grid positions surrounding (x,y).
            outside: include positions outside the grid.
            include_self: include (x,y)
        """
        return (
            ij
            for (dy, dx) in _3X3
            if (ij := (x + dx, y + dy))
            and (outside or (0 <= ij[0] < self.w and 0 <= ij[1] < self.h))
            and (include_self or ij != (x, y))
        )

    def xyadjacent(self, x: int, y: int, outside: bool = False) -> Iterable[Coord]:
        return (
            ij
            for (dy, dx) in _ADJ
            if (ij := (x + dx, y + dy))
            and (outside or (0 <= ij[0] < self.w and 0 <= ij[1] < self.h))
        )

    def pos2coord(self, pos: int) -> Coord:
        """position to cartesian coordinates"""
        return pos % self.w, pos // self.w

    def coord2pos(self, x: int, y: int) -> int:
        return y * self.w + x

    def positions(self) -> Iterable[int]:
        return range(len(self))

    def copy(self: B) -> B:
        copy = self.__class__(self.value_type, self)
        copy.w = self.w
        copy.h = self.h
        return copy

    def get(self, x: int, y: int, default: T = None) -> T:
        """Get using x,y co-ords, returning a default if outside the grid"""
        if any((x < 0, y < 0, x >= self.w, y >= self.h)):
            return default
        return self[x + y * self.w]

    def __str__(self) -> str:
        return "\n".join(
            (
                self.output_separator.join(
                    self.value_formatter(v) for v in self[j * self.w : (j + 1) * self.w]
                )
                for j in range(self.h)
            )
        )
