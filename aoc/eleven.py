from pathlib import Path


class Data(list[int]):
    w: int = 10
    h: int = 10

    @classmethod
    def parse(cls, fp):
        return cls(int(num) for num in fp.read() if num.isdigit())

    def flash(self) -> int:
        for pos, val in enumerate(self):
            self[pos] = val + 1
        flashed = set[int]()
        check = set[int](pos for pos, val in enumerate(self) if val == 10)
        while check:
            pos = check.pop()
            flashed.add(pos)
            for adj in self.adjacent(pos):
                self[adj] = self[adj] + 1
                if self[adj] > 9 and adj not in flashed:
                    check.add(adj)
        for pos in flashed:
            self[pos] = 0
        return len(flashed)

    def adjacent(self, pos):
        x, y = pos % self.w, pos // self.w
        return (
            i + j * self.w
            for i in range(x - 1, x + 2)
            for j in range(y - 1, y + 2)
            if i >= 0 and j >= 0 and i < self.w and j < self.h and (i, j) != (x, y)
        )


def main(datafile: Path) -> None:
    data = parse_data(datafile)
    print(f"Q1: {q1(data) = }")
    data = parse_data(datafile)
    print(f"Q2: {q2(data) = }")


def parse_data(datafile: Path) -> Data:
    with datafile.open() as fp:
        return Data.parse(fp)


def q1(data: Data) -> int:
    return sum(data.flash() for _ in range(100))


def q2(data: Data) -> int:
    i = 1
    while True:
        if data.flash() == len(data):
            break
        i += 1
    return i
