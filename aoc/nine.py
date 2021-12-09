from functools import reduce
from operator import mul
from pathlib import Path
from typing import Iterable, TextIO


class Data(list[int]):
    width: int

    @classmethod
    def read(cls, fp: TextIO) -> "Data":
        data = cls(int(c) for c in fp.readline().strip())
        data.width = len(data)
        data.extend(int(c) for c in fp.read() if c.isdigit())
        return data

    def adjacent(self, pos: int) -> Iterable[int]:
        if pos % self.width > 0:
            yield pos - 1
        if (pos + 1) % self.width:
            yield pos + 1
        if pos >= self.width:
            yield pos - self.width
        if pos + self.width < len(self):
            yield pos + self.width

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
    data = parse_data(datafile)
    print(f"Q1: {q1(data) = }")
    print(f"Q2: {q2(data) = }")


def parse_data(datafile: Path) -> Data:
    with datafile.open() as fp:
        return Data.read(fp)


def q1(data: Data) -> int:
    return sum(1 + data[pos] for pos in data.lowpoints())


def q2(data: Data) -> int:
    basin_sizes = [len(data.basin(pos)) for pos in data.lowpoints()]
    return reduce(mul, sorted(basin_sizes, reverse=True)[:3])
