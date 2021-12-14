from pathlib import Path

import pytest

from aoc.thirteen import Data, parse_data, q1, q2


@pytest.fixture
def data() -> Data:
    return parse_data(Path(__file__).parent / "thirteen.txt")


def test_parse_data(data: Data) -> None:
    assert len(data.points) == 18
    assert max([p[0] for p in data.points]) == 10
    assert max([p[1] for p in data.points]) == 14


def test_q1(data: Data) -> None:
    assert q1(data) == 17
    q2(data)
    assert len(data.points) == 16
