from collections import Counter
from pathlib import Path

import pytest

from aoc.fourteen import Data, q1, q2


@pytest.fixture
def data() -> Data:
    return Data.parse((Path(__file__).parent / "fourteen.txt").read_text())


def test_parse_data(data: Data) -> None:
    assert data.polymer == "NNCB"
    assert len(data.mutations) == 16


def test_polymer(data: Data):
    data.step()
    assert data.polymer == "NCNBCHB"
    data.step()
    assert data.polymer == "NBCCNBBBCBHCB"
    data.step()
    assert data.polymer == "NBBBCNCCNBBNBNBBCHBHHBCHB"
    data.step()
    assert data.polymer == "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"


def test_cstep(data: Data) -> None:
    assert data.cstep(1) == Counter(c for c in "NCNBCHB")
    assert data.cstep(2) == Counter(c for c in "NBCCNBBBCBHCB")
    assert data.cstep(3) == Counter(c for c in "NBBBCNCCNBBNBNBBCHBHHBCHB")
    assert data.cstep(4) == Counter(c for c in "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB")
    c = data.cstep(10)
    counts = c.values()
    assert max(counts) - min(counts) == 1588


def test_q1(data: Data) -> None:
    assert q1(data) == 1588


def test_q2(data: Data) -> None:
    assert q2(data) == 2188189693529
