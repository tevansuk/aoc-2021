from pathlib import Path

import pytest

from aoc.fifteen import Data, parse_data, q1, q2


@pytest.fixture
def data() -> Data:
    return parse_data(Path(__file__).parent / "fifteen.txt")


@pytest.fixture
def magnified() -> Data:
    return parse_data(Path(__file__).parent / "fifteen-magnified.txt")


def test_parse_data(data: Data) -> None:
    assert len(data.grid) == 100


def test_q1(data: Data) -> None:
    assert q1(data) == 40


def test_magnify(data: Data, magnified: Data) -> None:
    assert len(magnified.grid) == 2500
    big = data.magnify(5)
    assert len(magnified.grid) == len(big.grid)
    for pos in range(len(magnified.grid)):
        assert magnified.grid[pos] == big.grid[pos]


def test_q2(data: Data) -> None:
    assert q2(data) == 315
