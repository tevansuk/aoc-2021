from pathlib import Path

import pytest

from aoc.eleven import Data, q1, q2


@pytest.fixture
def data() -> Data:
    return Data.parse((Path(__file__).parent / "eleven.txt").read_text())


def test_parse_data(data: Data) -> None:
    assert len(data) == 100


def test_q1(data: Data) -> None:
    assert q1(data) == 1656


def test_q2(data: Data) -> None:
    assert q2(data) == 195


def test_flash(data: Data) -> None:
    assert data.flash() == 0
