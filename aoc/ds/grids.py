from collections.abc import MutableSequence
from typing import Callable, Iterable, Optional, TextIO, Type, TypeVar

T = TypeVar("T", int, str)
B = TypeVar("B", bound="Grid")
ValueParser = Callable[[str], Iterable[T]]


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
        return (int(c) for line in text.split("\n") for c in line.split(separator))

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
        return (val for line in text.split("\n") for val in line.split(separator))

    return parser


class Grid(list[T], MutableSequence[T]):
    w: int
    h: int
    value_type: Type[T]
    output_separator: str = ""
    value_formatter: Callable[[int], str] = str

    def __init__(self, value_type: Type[T], *args, **kwargs):
        self.value_type = value_type
        super().__init__(*args, **kwargs)

    @classmethod
    def parse(
        cls: Type[B],
        fp: TextIO,
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
        grid = cls(value_type, parser(fp.readline()))
        grid.w = len(grid)
        grid.extend(parser(fp.read()))
        grid.h = len(grid) // grid.w
        return grid

    def adjacent(self, pos: int):
        """
        The points in the grid that are above, below, left and right of the pos
        """
        x, y = self.pos2coord(pos)
        if x > 0:
            yield pos - 1
        if x + 1 < self.w:
            yield pos + 1
        if y > 0:
            yield pos - self.w
        if y + 1 < self.h:
            yield pos + self.w

    def surrounding(self, pos: int):
        """
        The points surrounding the pos, eg adjacent() + diagonals
        """
        x, y = self.pos2coord(pos)
        return (
            i + j * self.w
            for i in range(x - 1, x + 2)
            for j in range(y - 1, y + 2)
            if i >= 0 and j >= 0 and i < self.w and j < self.h and (i, j) != (x, y)
        )

    def pos2coord(self, pos: int) -> tuple[int, int]:
        """position to cartesian coordinates"""
        return pos % self.w, pos // self.w

    def positions(self) -> Iterable[int]:
        return range(len(self))

    def copy(self: B) -> B:
        copy = self.__class__(self)
        copy.w = self.w
        copy.h = self.h
        return copy

    def __str__(self):
        return "\n".join(
            (
                self.output_separator.join(
                    self.value_formatter(v) for v in self[j * self.w : j * self.w + self.w]
                )
                for j in range(self.h)
            )
        )
