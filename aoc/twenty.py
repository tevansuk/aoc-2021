from dataclasses import dataclass
from pathlib import Path

from aoc.ds import grids


class IGrid(grids.Grid[int]):
    value_formatter = grids.block_formatter

    def xy2num(self, x: int, y: int, default: int) -> int:
        return sum(
            v << (8 - idx)
            for idx, v in enumerate(
                self.get(i, j, default) for i, j in self.xycontaining(x, y, outside=True)
            )
        )


@dataclass
class Data:
    ieh: list[int]
    image: IGrid

    def enhance(self, image: IGrid, step: int) -> IGrid:
        default = self.alternates and int(step % 2) or 0
        nimage = IGrid(
            int,
            (
                self.ieh[image.xy2num(x, y, default)]
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


def parse_data(datafile: Path) -> Data:
    ieh_, image_ = datafile.read_text().split("\n\n")
    ieh = list(grids.hash_dot_parser(ieh_))
    image = IGrid.parse(image_, parser=grids.hash_dot_parser)
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
