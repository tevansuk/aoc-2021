from pathlib import Path

import pytest

from aoc.twenty_one import Data, parse_data, q1, q2


@pytest.fixture
def data() -> Data:
    return parse_data(Path(__file__).parent / "twenty_one.txt")


def test_parse_data(data: Data) -> None:
    assert data.start == [3, 7]


def test_q1(data: Data) -> None:
    assert q1(data) == 739785


def test_q2(data: Data) -> None:
    assert q2(data) == 444356092776315


def test_q2_counter(data: Data) -> None:
    assert max(data.play_dirac_counter()) == 444356092776315
