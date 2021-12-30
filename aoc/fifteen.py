from pathlib import Path

from .alg import dijkstra
from .ds.grids import Grid


class Data(Grid[int]):
    def cheapest_path(self) -> int:
        _, score = dijkstra(0, len(self) - 1, self.adjacent, self.get_cost)
        return score

    def get_cost(self, from_pos: int, to_pos: int):
        return self[to_pos]

    def magnify(self, size: int) -> "Data":
        data = self.__class__(int, [0] * len(self) * size ** 2)
        data.w = self.w * size
        data.h = self.h * size
        for pos in range(len(self)):
            x, y = self.pos2coord(pos)
            for ym in range(size):
                for xm in range(size):
                    npos = (x + (xm * self.w)) + (y + (ym * self.h)) * data.w
                    cost = self[pos] + ym + xm
                    while cost >= 10:
                        cost -= 9
                    data[npos] = cost
        return data


def main(datafile: Path) -> None:
    data = Data.parse(datafile.read_text())
    print(f"Q1: {q1(data) = }")
    print(f"Q2: {q2(data) = }")


def q1(data: Data) -> int:
    score = data.cheapest_path()
    return score


def q2(data: Data) -> int:
    full = data.magnify(5)
    score = full.cheapest_path()
    return score
