from pathlib import Path

import pytest

from aoc.twenty import Data, parse_data, q1, q2


@pytest.fixture
def data() -> Data:
    return parse_data(Path(__file__).parent / "twenty.txt")


def test_parse_data(data: Data) -> None:
    assert len(data.ieh) == 512
    assert data.image.w == 5
    assert data.image.h == 5
    assert len(data.image) == 25


def test_xy2num(data):
    assert data.image.xy2num(2, 2, 0) == 34
    assert data.image.xy2num(0, 0, 0) == 18
    assert data.get_pixel(data.image, 2, 2, 0) == 1


def test_q1(data: Data) -> None:
    assert q1(data) == 35


def test_q2(data: Data) -> None:
    assert q2(data) == 3351
