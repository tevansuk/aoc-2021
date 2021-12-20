from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Iterable

from aoc.ds.grids import Grid


class IGrid(Grid[int]):
    value_formatter = " █".__getitem__

    def xy2num(self, x: int, y: int, default: int) -> int:
        return sum(
            v << (8 - idx)
            for idx, v in enumerate(
                self._iget(i, j, default) for j in range(y - 1, y + 2) for i in range(x - 1, x + 2)
            )
        )

    def _iget(self, x: int, y: int, default: int) -> int:
        if x < 0 or y < 0 or x >= self.w or y >= self.h:
            return default
        return self[x + y * self.w]


@dataclass
class Data:
    ieh: list[int]
    image: IGrid

    def get_pixel(self, image: IGrid, x: int, y: int, default: int) -> int:
        return self.ieh[image.xy2num(x, y, default)]

    def enhance(self, image: IGrid, step: int) -> IGrid:
        default = self.alternates and int(step % 2) or 0
        nimage = IGrid(
            int,
            (
                self.get_pixel(image, x, y, default)
                for y in range(-1, image.h + 1)
                for x in range(-1, image.w + 1)
            ),
        )
        nimage.w = image.w + 2
        nimage.h = image.h + 2
        return nimage

    @property
    def alternates(self) -> bool:
        # If the first and last ieh rules are light + dark, then the infinite background
        # alternates between light and dark on each step!
        # Bit sneaky, because the test input does not...
        return self.ieh[0] == 1 and self.ieh[-1] == 0


def main(datafile: Path) -> None:
    data = parse_data(datafile)
    print(f"Q1: {q1(data) = }")
    print(f"Q2: {q2(data) = }")


def hash_dot_parser(text: str) -> Iterable[int]:
    return (".#".index(c) for c in text if c in ".#")


def parse_data(datafile: Path) -> Data:
    with datafile.open() as fp:
        ieh_, image_ = fp.read().split("\n\n")
        ieh = list(hash_dot_parser(ieh_))
        image = IGrid.parse(fp=StringIO(image_), parser=hash_dot_parser)
        return Data(ieh=ieh, image=image)


def q1(data: Data) -> int:
    image = data.image
    for i in range(2):
        image = data.enhance(image, i)
    return sum(image)


def q2(data: Data) -> int:
    image = data.image
    for i in range(50):
        image = data.enhance(image, i)
    return sum(image)
