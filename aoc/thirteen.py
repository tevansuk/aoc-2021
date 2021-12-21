from pathlib import Path

from aoc.ds import grids

Point = tuple[int, int]
Fold = tuple[bool, int]


class Data:
    points: set[Point]
    folds: list[Fold]

    def __init__(self):
        self.points = set[Point]()
        self.folds = list[Fold]()

    @classmethod
    def parse_data(cls, text: str) -> "Data":
        data = cls()
        points, folds = text.strip().split("\n\n")
        data.points = set(
            (int(xy[0]), int(xy[1])) for line in points.split("\n") if (xy := line.split(","))
        )
        data.folds = list(
            (dp[0] == "x", int(dp[1]))
            for line in folds.split("\n")
            if (dp := line.split()[2].split("="))
        )
        data.folds.reverse()
        return data

    def fold(self) -> bool:
        if not self.folds:
            return False
        x_fold, fold = self.folds.pop()
        points = set[Point]()
        for point in self.points:
            if x_fold and fold < point[0]:
                points.add((2 * fold - point[0], point[1]))
            elif not x_fold and fold < point[1]:
                points.add((point[0], 2 * fold - point[1]))
            else:
                points.add(point)
        self.points = points
        return True

    def __str__(self) -> str:
        return "\n".join(
            "".join(
                grids.block_formatter(bool((x, y) in self.points))
                for x in range(max(p[0] for p in self.points) + 1)
            )
            for y in range(max(p[1] for p in self.points) + 1)
        )


def main(datafile: Path) -> None:
    data = parse_data(datafile)
    print(f"Q1: {q1(data) = }")
    q2(data)
    print(f"Q2:\n{data}")


def parse_data(datafile: Path) -> Data:
    return Data.parse_data(datafile.read_text())


def q1(data: Data) -> int:
    data.fold()
    return len(data.points)


def q2(data: Data) -> None:
    while data.fold():
        pass
