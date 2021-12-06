from pathlib import Path

import pytest

from aoc.four import let_the_wookie_win, parse_boards, winner_winner_chicken_dinner


@pytest.fixture
def data():
    return parse_boards(Path(__file__).parent / "four.txt")


def test_draw(data):
    board = data[1][2]
    board.draw(14)
    assert 0 in board.matches


def test_winner(data):
    boards = data[1]
    winner = winner_winner_chicken_dinner(*data)
    assert winner == boards[2]
    assert winner.score == 4512


def test_loser(data):
    boards = data[1]
    assert len(boards) == 3
    loser = let_the_wookie_win(*data)
    assert loser.score == 1924
