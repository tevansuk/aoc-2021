from functools import reduce
from operator import mul
from pathlib import Path
from typing import Iterable

from .ds.grids import Grid


class Data(Grid[int]):
    def lowpoints(self) -> Iterable[int]:
        return (
            pos
            for pos, val in enumerate(self)
            if all(val < self[adj] for adj in self.adjacent(pos))
        )

    def basin(self, pos: int) -> set[int]:
        basin = {pos}
        check = {pos}
        while check:
            pos = check.pop()
            for adj in self.adjacent(pos):
                if self[pos] < self[adj] < 9 and adj not in basin:
                    basin.add(adj)
                    check.add(adj)
        return basin


def main(datafile: Path) -> None:
    with datafile.open() as fp:
        data = Data.parse(fp)
    print(f"Q1: {q1(data) = }")
    print(f"Q2: {q2(data) = }")


def q1(data: Data) -> int:
    return sum(1 + data[pos] for pos in data.lowpoints())


def q2(data: Data) -> int:
    basin_sizes = [len(data.basin(pos)) for pos in data.lowpoints()]
    return reduce(mul, sorted(basin_sizes, reverse=True)[:3])
