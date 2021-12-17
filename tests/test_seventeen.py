from pathlib import Path

import pytest

from aoc.seventeen import Target, find_all_launch_speeds, parse_data, q1, q2


@pytest.fixture
def target() -> Target:
    return parse_data(Path(__file__).parent / "seventeen.txt")


def test_parse_data(target: Target) -> None:
    xmin, xmax, ymin, ymax = target
    assert xmin == 20
    assert xmax == 30
    assert ymin == -10
    assert ymax == -5


def test_q1(target: Target) -> None:
    all_launch_speeds = find_all_launch_speeds(*target)
    assert q1(all_launch_speeds) == 45


def test_q2(target: Target) -> None:
    all_launch_speeds = find_all_launch_speeds(*target)
    assert q2(all_launch_speeds) == 112
