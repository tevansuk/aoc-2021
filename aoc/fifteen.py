import heapq
from pathlib import Path
from random import random
from typing import Iterable, TextIO

Grid = list[int]
_Heap = list[tuple[int, float, int]]
_Seen = set[int]


class Data:
    grid: Grid
    sx: int
    sy: int

    @classmethod
    def parse(cls, fp: TextIO) -> "Data":
        data = cls()
        data.grid = [int(c) for c in fp.readline() if c.isdigit()]
        data.sx = len(data.grid)
        data.grid.extend(int(c) for c in fp.read() if c.isdigit())
        data.sy = len(data.grid) // data.sx
        return data

    def adjacent(self, pos: int) -> Iterable[int]:
        x, y = pos % self.sx, pos // self.sx
        if x > 0:
            yield pos - 1
        if (pos + 1) % self.sx:
            yield pos + 1
        if y > 1:
            yield pos - self.sx
        if y < self.sy - 1:
            yield pos + self.sx

    def cheapest_path(self) -> int:
        end = len(self.grid) - 1
        heap = _Heap([(0, random(), 0)])
        seen = _Seen()
        while heap:
            score, _, pos = heapq.heappop(heap)
            if pos in seen:
                continue
            seen.add(pos)
            if pos == end:
                return score
            for adjacent in self.adjacent(pos):
                heapq.heappush(heap, (score + self.grid[adjacent], random(), adjacent))
        return -1

    def magnify(self, size: int) -> "Data":
        data = self.__class__()
        data.grid = [0] * len(self.grid) * size ** 2
        data.sx = self.sx * size
        data.sy = self.sy * size
        for pos in range(len(self.grid)):
            x, y = pos % self.sx, pos // self.sx
            for ym in range(size):
                for xm in range(size):
                    npos = (x + (xm * self.sx)) + (y + (ym * self.sy)) * data.sx
                    cost = self.grid[pos] + ym + xm
                    while cost >= 10:
                        cost -= 9
                    data.grid[npos] = cost
        return data


def main(datafile: Path) -> None:
    data = parse_data(datafile)
    print(f"Q1: {q1(data) = }")
    print(f"Q2: {q2(data) = }")


def parse_data(datafile: Path) -> Data:
    with datafile.open() as fp:
        return Data.parse(fp)


def q1(data: Data) -> int:
    score = data.cheapest_path()
    return score


def q2(data: Data) -> int:
    full = data.magnify(5)
    return full.cheapest_path()
