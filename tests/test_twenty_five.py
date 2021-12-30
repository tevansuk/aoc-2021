from pathlib import Path

import pytest

from aoc.twenty_five import Board, parse_data, q1


@pytest.fixture
def board() -> Board:
    return parse_data(Path(__file__).parent / "twenty_five.txt")


def test_parse_data(board: Board) -> None:
    assert len(board) == 90
    assert board.w == 10
    assert board.h == 9


def test_move_simple():
    b = Board.parse(
        """...>...
.......
......>
v.....>
......>
.......
..vvv.."""
    )
    b.move()
    assert (
        str(b)
        == """..vv>..
.......
>......
v.....>
>......
.......
....v.."""
    )
    b.move()
    assert (
        str(b)
        == """....v>.
..vv...
.>.....
......>
v>.....
.......
......."""
    )
    b.move()
    assert (
        str(b)
        == """......>
..v.v..
..>v...
>......
..>....
v......
......."""
    )
    b.move()
    assert (
        str(b)
        == """>......
..v....
..>.v..
.>.v...
...>...
.......
v......"""
    )


def test_move(board: Board) -> None:
    expected1 = """....>.>v.>
v.v>.>v.v.
>v>>..>v..
>>v>v>.>.v
.>v.v...v.
v>>.>vvv..
..v...>>..
vv...>>vv.
>.v.v..v.v"""
    assert board.move() == 24
    assert str(board) == expected1
    board.move()
    expected2 = """>.v.v>>..v
v.v.>>vv..
>v>.>.>.v.
>>v>v.>v>.
.>..v....v
.>v>>.v.v.
v....v>v>.
.vv..>>v..
v>.....vv."""
    assert str(board) == expected2


def test_q1(board: Board) -> None:
    assert q1(board) == 58
