from collections import Counter
from pathlib import Path

import pytest

from aoc.six import age, parse_data


@pytest.fixture
def data() -> Counter:
    return parse_data(Path(__file__).parent / "six.txt")


def test_parse_data(data) -> None:
    assert len(data) == 4


def test_age(data) -> None:
    day_1 = age(data, 1)
    assert day_1.total() == 5
    day_5 = age(data, 5)
    assert day_5.total() == 10
    day_256 = age(data, 256)
    assert day_256.total() == 26984457539
