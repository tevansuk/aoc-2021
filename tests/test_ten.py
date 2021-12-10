from pathlib import Path

import pytest

from aoc.ten import Data, illegal_incomplete, parse_data, q1, q2, score


@pytest.fixture
def data() -> Data:
    return parse_data(Path(__file__).parent / "ten.txt")


def test_parse_data(data: Data) -> None:
    assert len(data) == 10


def test_q1(data: Data) -> None:
    assert q1(data) == 26397


def test_q2(data: Data) -> None:
    assert q2(data) == 288957


def test_illegal_char(data: Data) -> None:
    char = illegal_incomplete(data[8])
    assert char == ">"


def test_incomplete(data: Data) -> None:
    to_complete = illegal_incomplete(data[0], True)
    assert to_complete == "}}]])})]"
    assert score(to_complete) == 288957
