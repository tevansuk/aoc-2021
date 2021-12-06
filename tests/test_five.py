from pathlib import Path

import pytest

from aoc.five import Coord, overlaps, parse_lines, vert_horiz_overlaps


@pytest.fixture
def data():
    return parse_lines(Path(__file__).parent / "five.txt")


def test_parse(data):
    assert len(data) == 10


def test_vert_horiz_overlaps(data):
    assert vert_horiz_overlaps(data) == 5


def test_overlaps(data):
    assert overlaps(data) == 12


def test_points(data):
    line = data[-1]
    assert line.points == [Coord(5, 5), Coord(6, 4), Coord(7, 3), Coord(8, 2)]
