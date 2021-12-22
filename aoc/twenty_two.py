import re
from dataclasses import dataclass
from itertools import product
from math import prod
from pathlib import Path
from typing import Optional

POINTS = list(p[0] + p[1] for p in product("xyz", "01"))


@dataclass
class Cube:
    x0: int
    x1: int
    y0: int
    y1: int
    z0: int
    z1: int
    on: bool = True

    @classmethod
    def parse(cls, inp: str) -> "Cube":
        x0, x1, y0, y1, z0, z1 = [
            c for coord in re.findall(r"(-?\d+)\.\.(-?\d+)", inp) for c in sorted(map(int, coord))
        ]
        return cls(x0, x1, y0, y1, z0, z1, on=inp[1] == "n")

    @property
    def initial(self) -> bool:
        return all((abs(getattr(self, c)) <= 50 for c in POINTS))

    @property
    def size(self) -> int:
        return prod(
            c[1] - c[0] + 1 for c in ((self.x0, self.x1), (self.y0, self.y1), (self.z0, self.z1))
        )

    def no_overlaps(self, other: "Cube") -> bool:
        """Check if other overlaps with this cube"""
        return any(
            (
                self.x0 > other.x1,
                self.x1 < other.x0,
                self.y0 > other.y1,
                self.y1 < other.y0,
                self.z0 > other.z1,
                self.z1 < other.z0,
            )
        )

    def remove_overlaps(self, other) -> list["Cube"]:
        """Create a list of cubes that are other - this cube"""
        cubes = []
        x0, x1, y0, y1, z0, z1 = other.x0, other.x1, other.y0, other.y1, other.z0, other.z1
        if self.x0 > x0:
            cubes.append(Cube(x0, self.x0 - 1, y0, y1, z0, z1))
        if self.x1 < x1:
            cubes.append(Cube(self.x1 + 1, x1, y0, y1, z0, z1))
        x0, x1 = (max(self.x0, x0), min(self.x1, x1))
        if self.y0 > y0:
            cubes.append(Cube(x0, x1, y0, self.y0 - 1, z0, z1))
        if self.y1 < y1:
            cubes.append(Cube(x0, x1, self.y1 + 1, y1, z0, z1))
        y0, y1 = (max(self.y0, y0), min(self.y1, y1))
        if self.z0 > z0:
            cubes.append(Cube(x0, x1, y0, y1, z0, self.z0 - 1))
        if self.z1 < z1:
            cubes.append(Cube(x0, x1, y0, y1, self.z1 + 1, z1))
        return cubes


class Data(list[Cube]):
    def reboot_reactor(self, all_cubes=False) -> int:
        on_cubes: list[Optional[Cube]] = []
        for cube in self:
            if cube.initial or all_cubes:
                for idx in range(len(on_cubes)):
                    other = on_cubes[idx]
                    if not other or cube.no_overlaps(other):
                        continue
                    on_cubes[idx] = None
                    if cubes := cube.remove_overlaps(other):
                        on_cubes.extend(cubes)
                if cube.on:
                    on_cubes.append(cube)
        return sum(c.size for c in on_cubes if c)


def main(datafile: Path) -> None:
    data = parse_data(datafile)
    print(f"Q1: {q1(data) = }")
    print(f"Q2: {q2(data) = }")


def parse_data(datafile: Path) -> Data:
    return Data(Cube.parse(line) for line in datafile.read_text().strip().split("\n"))


def q1(data: Data) -> int:
    return data.reboot_reactor()


def q2(data: Data) -> int:
    return data.reboot_reactor(True)
