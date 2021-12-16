from pathlib import Path

from .ds.grids import Grid


class Data(Grid[int]):
    def flash(self) -> int:
        for pos, val in enumerate(self):
            self[pos] = val + 1
        flashed = set[int]()
        check = set[int](pos for pos, val in enumerate(self) if val == 10)
        while check:
            pos = check.pop()
            flashed.add(pos)
            for adj in self.surrounding(pos):
                self[adj] = self[adj] + 1
                if self[adj] > 9 and adj not in flashed:
                    check.add(adj)
        for pos in flashed:
            self[pos] = 0
        return len(flashed)


def main(datafile: Path) -> None:
    with datafile.open() as fp:
        data = Data.parse(fp)
    data2 = data.copy()
    print(f"Q1: {q1(data) = }")
    print(f"Q2: {q2(data2) = }")


def q1(data: Data) -> int:
    return sum(data.flash() for _ in range(100))


def q2(data: Data) -> int:
    i = 1
    while True:
        if data.flash() == len(data):
            break
        i += 1
    return i
