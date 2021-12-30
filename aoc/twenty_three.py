from pathlib import Path
from typing import Iterable, Optional

from aoc.alg.dijkstra import dijkstra2
from aoc.twenty_three_base import Board
from aoc.twenty_three_extra import animate_solution


def get_adj_costs(board: Board) -> Iterable[tuple[Board, int]]:
    for move in board.moves():
        yield board.apply(move), move.cost()


def main(datafile: Path, animate_: Optional[str] = None) -> None:
    start = parse_data(datafile)
    animate = bool(animate_)
    print(f"Q1: {q1(start, animate) = }")
    print(f"Q2: {q2(start, animate) = }")


def parse_data(datafile: Path) -> Board:
    return Board.parse(datafile.read_text().strip().split("\n"))


def q1(start: Board, animate: bool = False) -> int:
    end = Board(rooms=((0,) * 11, (1, 1), (2, 2), (3, 3), (4, 4)))
    path, cost = dijkstra2(start, end, get_adj_costs)
    if animate:
        animate_solution(path, cost)
    return cost


def extra_rows(start: Board) -> Board:
    # D#C#B#A#
    # D#B#A#C#
    rooms = list(list(r) for r in start.rooms)
    rooms[1] = rooms[1][:1] + [4, 4] + rooms[1][-1:]
    rooms[2] = rooms[2][:1] + [3, 2] + rooms[2][-1:]
    rooms[3] = rooms[3][:1] + [2, 1] + rooms[3][-1:]
    rooms[4] = rooms[4][:1] + [1, 3] + rooms[4][-1:]
    return Board(rooms=tuple((tuple(r) for r in rooms)))


def q2(start: Board, animate: bool = False) -> int:
    end = Board(rooms=((0,) * 11, (1, 1, 1, 1), (2, 2, 2, 2), (3, 3, 3, 3), (4, 4, 4, 4)))
    start = extra_rows(start)
    path, cost = dijkstra2(start, end, get_adj_costs)
    if animate:
        animate_solution(path, cost)
    return cost
