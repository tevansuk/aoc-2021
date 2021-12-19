from pathlib import Path

import pytest

from aoc.nineteen import Scanners, parse_data, q1, q2


@pytest.fixture
def scanners() -> Scanners:
    return parse_data(Path(__file__).parent / "nineteen.txt")


def test_parse_data(scanners) -> None:
    assert len(scanners) == 5
    assert len(scanners[0].readings) == 24
    assert len(scanners[0].readings[0]) == 25


def test_q1(scanners) -> None:
    assert q1(scanners) == 79


def test_q2(scanners) -> None:
    scanners.orientate_scanners()
    assert q2(scanners) == 3621
