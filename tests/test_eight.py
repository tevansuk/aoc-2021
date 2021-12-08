from pathlib import Path

import pytest

from aoc.eight import (
    calculate_output_reading,
    count_simple_outputs,
    parse_data,
    sum_output_readings,
)


@pytest.fixture
def data():
    return parse_data(Path(__file__).parent / "eight.txt")


def test_parse_data(data):
    assert len(data) == 10
    assert len(data[0]) == 2
    assert len(data[0][0]) == 10
    assert len(data[0][1]) == 4
    assert data[0][0][3] == {"f", "e", "c", "a", "d", "g"}


def test_count_simple_outputs(data):
    assert count_simple_outputs(data[:2]) == 5
    assert count_simple_outputs(data) == 26


def test_calculate_output_reading(data):
    assert calculate_output_reading(*data[0]) == 8394


def test_sum_output_readings(data):
    assert sum_output_readings(data) == 61229
