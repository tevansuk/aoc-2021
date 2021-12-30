from itertools import count
from pathlib import Path
from typing import Iterable

from .ds.grids import Grid

EMPTY_RIGHT_DOWN = ".>v"
EMPTY = 0
RIGHT = 1
DOWN = 2


def erd_parser(text: str) -> Iterable[int]:
    return (EMPTY_RIGHT_DOWN.index(c) for c in text if c in EMPTY_RIGHT_DOWN)


class Board(Grid[int]):
    value_formatter = EMPTY_RIGHT_DOWN.__getitem__

    @classmethod
    def parse(cls, data, *args) -> "Board":
        return super(cls, cls).parse(data, erd_parser, int)

    def move(self) -> int:
        nmoves = 0
        for (direction, mod) in [(RIGHT, (1, 0)), (DOWN, (0, 1))]:
            moves: list[tuple[int, int]] = []
            node_iter = iter(enumerate(self))
            for pos, val in node_iter:
                if val == direction:
                    x, y = self.pos2coord(pos)
                    npos = self.coord2pos((x + mod[0]) % self.w, (y + mod[1]) % self.h)
                    if self[npos] == EMPTY:
                        moves.append((pos, npos))
            for (pos, npos) in moves:
                self[pos] = EMPTY
                self[npos] = direction
            nmoves += len(moves)
        return nmoves


def main(datafile: Path) -> None:
    board = parse_data(datafile)
    print(f"Q1: {q1(board) = }")


def parse_data(datafile: Path) -> Board:
    return Board.parse(datafile.read_text())


def q1(board: Board) -> int:
    for step in count(start=1, step=1):
        if board.move() == 0:
            return step
    return -1
