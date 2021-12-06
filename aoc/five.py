from collections import Counter
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def points(self, other: "Coord") -> list["Coord"]:
        # .. or cmp(other.x, self.x) in other words
        dx = (other.x > self.x) - (other.x < self.x)
        dy = (other.y > self.y) - (other.y < self.y)
        return [
            Coord(self.x + r * dx, self.y + r * dy)
            for r in range(max(abs(self.x - other.x), abs(self.y - other.y)) + 1)
        ]


@dataclass
class Line:
    p1: Coord
    p2: Coord

    @property
    def is_vertical(self) -> bool:
        return self.p1.x == self.p2.x

    @property
    def is_horizontal(self) -> bool:
        return self.p1.y == self.p2.y

    @property
    def points(self) -> list[Coord]:
        return self.p1.points(self.p2)


def main(datafile: Path) -> None:
    lines = parse_lines(datafile)
    vh_overlaps = vert_horiz_overlaps(lines)
    print(f"{vh_overlaps=}")

    overlap = overlaps(lines)
    print(f"{overlap=}")


def vert_horiz_overlaps(lines: list[Line]) -> int:
    return overlaps(line for line in lines if line.is_vertical or line.is_horizontal)


def overlaps(lines: list[Line]) -> int:
    c = Counter(coord for line in lines for coord in line.points)
    return sum(1 for v in c.values() if v > 1)


def parse_lines(datafile: Path) -> list[Line]:
    with datafile.open() as fp:
        return [
            Line(*(Coord(*map(int, val.split(","))) for val in line.split(" -> ")))
            for line in fp.readlines()
        ]
