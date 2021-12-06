import pytest

from aoc import three


@pytest.fixture
def data():
    return [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ]


@pytest.fixture
def idata(data):
    return [int(d, 2) for d in data]


def test_imlcb(idata):
    assert three.mlcb(idata) == 22
    assert three.mlcb(idata, lcb=True) == 9
    assert three.mlcb(idata, sig=1) == 16
    assert three.mlcb(idata, sig=2) == 16
    assert three.mlcb(idata, sig=3) == 20
    assert three.mlcb(idata, sig=4) == 22
    assert three.mlcb(idata, sig=5) == 22
    assert three.mlcb(idata, lcb=True, sig=1) == 0
    assert three.mlcb(idata, lcb=True, sig=2) == 8
    assert three.mlcb(idata, lcb=True, sig=3) == 8
    assert three.mlcb(idata, lcb=True, sig=4) == 8
    assert three.mlcb(idata, lcb=True, sig=5) == 9


def test_ifind(idata):
    assert three.find(idata) == 23
    assert three.find(idata, lcb=True) == 10
