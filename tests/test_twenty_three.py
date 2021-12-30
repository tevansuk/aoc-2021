from pathlib import Path

import pytest

from aoc.twenty_three import parse_data, q1, q2
from aoc.twenty_three_base import Board, Move


@pytest.fixture
def start() -> Board:
    return parse_data(Path(__file__).parent / "twenty_three.txt")


def test_parse_data(start: Board) -> None:
    assert len(start.rooms) == 5
    assert len(start.rooms[0]) == 11
    assert start.rooms[1] == (2, 1)
    assert start.rooms[2] == (3, 4)
    assert start.rooms[3] == (2, 3)
    assert start.rooms[4] == (4, 1)


@pytest.fixture
def almost() -> Board:
    rooms = [[0] * 11, [0, 1], [2, 2], [3, 3], [4, 4]]
    rooms[0][9] = 1
    return Board(rooms=tuple(tuple(r) for r in rooms))


@pytest.fixture
def almost2() -> Board:
    rooms = [[0] * 11, [0, 1], [2, 2], [3, 3], [4, 4]]
    rooms[0][0] = 1
    return Board(rooms=tuple(tuple(r) for r in rooms))


@pytest.fixture
def direct() -> Board:
    rooms = [[0] * 11, [1, 1], [3, 2], [0, 3], [4, 4]]
    rooms[0][0] = 2
    return Board(rooms=tuple(tuple(r) for r in rooms))


def test_room_moves(start, direct) -> None:
    assert start.room_to_room_moves() == []
    moves = direct.room_to_room_moves()
    assert len(moves) == 1
    assert moves[0] == Move(3, 2, 0, 3, 0)
    assert moves[0].cost() == 400


def test_hallway_to_room_moves(almost: Board, almost2: Board) -> None:
    moves = almost.hallway_to_room_moves()
    assert len(moves) == 1
    assert moves[0] == Move(1, 0, 9, 1, 0)
    assert moves[0].cost() == 8
    moves = almost2.hallway_to_room_moves()
    assert len(moves) == 1
    assert moves[0] == Move(1, 0, 0, 1, 0)
    assert moves[0].cost() == 3


def test_room_to_hallway_moves(start: Board) -> None:
    moves = start.room_to_hallway_moves()
    assert len(moves) == 28
    assert moves[0] == Move(2, 1, 0, 0, 1)
    assert moves[0].cost() == 20
    assert moves[1] == Move(2, 1, 0, 0, 0)
    assert moves[1].cost() == 30


def test_q1(start: Board) -> None:
    assert q1(start) == 12521


def test_q2(start: Board) -> None:
    assert q2(start) == 44169
