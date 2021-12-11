from pathlib import Path

import pytest

from aoc.eleven import Data, parse_data, q1, q2


@pytest.fixture
def data() -> Data:
    return parse_data(Path(__file__).parent / "eleven.txt")


def test_parse_data(data: Data) -> None:
    assert len(data) == 100


def test_q1(data: Data) -> None:
    assert q1(data) == 1656


def test_q2(data: Data) -> None:
    assert q2(data) == 195


def test_adj(data: Data) -> None:
    assert set(data.adjacent(0)) == {1, 10, 11}
    assert set(data.adjacent(10)) == {0, 1, 20, 21, 11}
    assert set(data.adjacent(1)) == {0, 2, 10, 11, 12}
    assert set(data.adjacent(11)) == {0, 1, 2, 10, 12, 20, 21, 22}
    assert set(data.adjacent(99)) == {88, 89, 98}


def test_flash(data: Data) -> None:
    assert data.flash() == 0
