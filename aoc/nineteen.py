from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Iterator, TextIO

Coord = tuple[int, int, int]
Beacons = set[Coord]


@dataclass
class Scanner:
    id: int
    readings: list[list[Coord]]
    orientation: int = -1
    origin: tuple[int, int, int] = (0, 0, 0)

    @classmethod
    def parse(cls, fp: TextIO, sid: int) -> "Scanner":
        readings = []
        while (line := fp.readline().strip()) != "":
            x, y, z = map(int, line.strip().split(","))
            readings.append(all_rotations((x, y, z)))
        return cls(id=sid, readings=[*zip(*readings)])  # type: ignore

    def orientate(self, other: "Scanner") -> Beacons:
        opoints = other.readings[other.orientation]
        opoints_set = set(opoints)
        for idx in range(24):
            points = self.readings[idx]
            for (a, b, c), (d, e, f) in product(opoints, points):
                gen = ((x - d + a, y - e + b, z - f + c) for x, y, z in points)
                if len(opoints_set.intersection(gen)) >= 12:
                    self.orientation = idx
                    self.origin = (
                        other.origin[0] + d - a,
                        other.origin[1] + e - b,
                        other.origin[2] + f - c,
                    )
                    return {
                        (x - self.origin[0], y - self.origin[1], z - self.origin[2])
                        for x, y, z in self.readings[self.orientation]
                    }
        return set()


class Scanners(list[Scanner]):
    @classmethod
    def parse(cls, fp: TextIO) -> "Scanners":
        scanners = cls()
        while line := fp.readline():
            sid = int(line.split()[2])
            scanners.append(Scanner.parse(fp, sid))
        return scanners

    def orientate_scanners(self) -> Beacons:
        self[0].orientation = 0
        self[0].origin = (0, 0, 0)
        all_beacons = set(self[0].readings[0])
        tried: defaultdict[int, set[int]] = defaultdict(set)

        for scanner in self.unoriented():
            for other in self.oriented():
                if other.id in tried[scanner.id]:
                    continue
                beacons = scanner.orientate(other)
                if beacons:
                    all_beacons |= beacons
                    break
                tried[scanner.id].add(other.id)
        return all_beacons

    def unoriented(self) -> Iterator[Scanner]:
        more = True
        while more:
            more = False
            for s in self:
                if s.orientation == -1:
                    more = True
                    yield s

    def oriented(self) -> Iterator[Scanner]:
        for s in self:
            if s.orientation >= 0:
                yield s


def main(datafile: Path) -> None:
    data = parse_data(datafile)
    print(f"Q1: {q1(data) = }")
    print(f"Q2: {q2(data) = }")


def parse_data(datafile: Path) -> Scanners:
    with datafile.open() as fp:
        return Scanners.parse(fp)


def q1(scanners: Scanners) -> int:
    beacons = scanners.orientate_scanners()
    return len(beacons)


def q2(scanners: Scanners) -> int:
    return max(
        sum(abs(i - j) for i, j in zip(s1.origin, s2.origin))
        for s1, s2 in product(scanners, repeat=2)
    )


def _rotate(x: int, y: int, z: int) -> Coord:
    return (x, z, -y)


def _turn(x: int, y: int, z: int) -> Coord:
    return (-y, x, z)


def all_rotations(vect: Coord) -> list[Coord]:
    combis = []
    for _ in range(2):
        for _ in range(3):
            vect = _rotate(*vect)
            combis.append(vect)
            for _ in range(3):
                vect = _turn(*vect)
                combis.append(vect)
        vect = _rotate(*_turn(*_rotate(*vect)))
    return combis
