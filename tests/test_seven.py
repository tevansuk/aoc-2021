from pathlib import Path

import pytest

from aoc.seven import costs, costs2, parse_data, shortest_alignment


@pytest.fixture
def data():
    return parse_data(Path(__file__).parent / "seven.txt")


def test_parse_data(data):
    assert len(data) == 10


def test_shortest_alignment(data):
    cost = costs(data)
    assert shortest_alignment(cost) == 2


def test_costs(data):
    cost = costs(data)
    assert cost[2] == 37
    assert cost[1] == 41
    assert cost[3] == 39
    assert cost[10] == 71


def test_costs2(data):
    cost = costs2(data)
    assert cost[5] == 168
    assert cost[2] == 206
