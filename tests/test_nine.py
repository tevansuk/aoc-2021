from pathlib import Path

import pytest

from aoc.nine import Data, q1, q2


@pytest.fixture
def data() -> Data:
    with (Path(__file__).parent / "nine.txt").open() as fp:
        return Data.parse(fp)


def test_parse_data(data: Data) -> None:
    assert len(data) == 50


def test_q1(data: Data) -> None:
    assert q1(data) == 15


def test_q2(data: Data) -> None:
    assert q2(data) == 1134


def test_basin(data: Data) -> None:
    assert data.basin(1) == {0, 1, 10}
    assert data.basin(9) == {5, 6, 7, 8, 9, 16, 18, 19, 29}
