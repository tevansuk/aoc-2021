from pathlib import Path

import pytest

from aoc.twenty_two import Data, parse_data, q1, q2


@pytest.fixture
def data() -> Data:
    return parse_data(Path(__file__).parent / "twenty_two.txt")


@pytest.fixture
def data_large() -> Data:
    return parse_data(Path(__file__).parent / "twenty_two_large.txt")


@pytest.fixture
def data_monster() -> Data:
    return parse_data(Path(__file__).parent / "twenty_two_monster.txt")


def test_parse_data(data: Data) -> None:
    assert len(data) == 4
    assert data[0].on
    assert not data[2].on
    assert data[0].size == 27


def test_parse_data_large(data_large):
    assert len(data_large) == 22
    assert data_large[-1].initial is False
    assert data_large[0].x0 == -20
    assert len([c for c in data_large if c.initial]) == 20
    for cube in data_large:
        assert cube.size > 0


def test_q1(data: Data) -> None:
    assert q1(data) == 39


def test_q1_large(data_large: Data) -> None:
    assert q1(data_large) == 590784


def test_q2(data_monster: Data) -> None:
    assert q2(data_monster) == 2758514936282235
