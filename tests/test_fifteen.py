from pathlib import Path

import pytest

from aoc.fifteen import Data, q1, q2


@pytest.fixture
def data() -> Data:
    with (Path(__file__).parent / "fifteen.txt").open() as fp:
        return Data.parse(fp)


@pytest.fixture
def magnified() -> Data:
    with (Path(__file__).parent / "fifteen-magnified.txt").open() as fp:
        return Data.parse(fp)


def test_parse_data(data: Data) -> None:
    assert len(data) == 100


def test_q1(data: Data) -> None:
    assert q1(data) == 40


def test_magnify(data: Data, magnified: Data) -> None:
    assert len(magnified) == 2500
    big = data.magnify(5)
    assert len(magnified) == len(big)
    for pos in range(len(magnified)):
        assert magnified[pos] == big[pos]


def test_q2(data: Data) -> None:
    assert q2(data) == 315
