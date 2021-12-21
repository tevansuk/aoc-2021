from pathlib import Path
from typing import Optional

from aoc.ds import grids

DrawList = list[int]
BoardList = list["Board"]
CellMatches = set[int]
DIM = 5
BINGOS = [range(x, DIM ** 2, DIM) for x in range(DIM)] + [
    range(y * DIM, y * DIM + DIM) for y in range(DIM)
]


def main(datafile: Path):
    draws, boards = parse_boards(datafile)
    winner = winner_winner_chicken_dinner(draws, boards)
    print(f"Winning board {winner=}")
    print(f"{winner.score=}")

    for b in boards:
        b.reset()

    loser = let_the_wookie_win(draws, boards)
    print(f"Last board to win {loser=}")
    print(f"{loser.score=}")


def parse_boards(datafile: Path) -> tuple[DrawList, BoardList]:
    raw_draws, *raw_boards = datafile.read_text().split("\n\n")
    boards = [Board.parse(board, grids.int_number_value_parser()) for board in raw_boards]
    draws = DrawList(grids.int_number_value_parser(",")(raw_draws))
    return draws, boards


def winner_winner_chicken_dinner(draws, boards) -> "Board":
    for number in draws:
        for board in boards:
            board.draw(number)
            if board.is_bingo:
                return board
    raise Exception("No board won at all - seems unlikely")


def let_the_wookie_win(draws, boards) -> "Board":
    last_winner = None
    for number in draws:
        for board in boards:
            if not board.is_bingo:
                board.draw(number)
                if board.is_bingo:
                    last_winner = board
    if not last_winner:
        raise Exception("No board won last - seems unlikely")
    return last_winner


class Board(grids.Grid[int]):
    matches: CellMatches
    is_bingo = False
    winning_number: Optional[int] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.matches = CellMatches()

    def draw(self, number) -> None:
        if self.is_bingo:
            return
        self.matches.update(pos for pos in range(len(self)) if self[pos] == number)
        if any(all(pos in self.matches for pos in bingo) for bingo in BINGOS):
            self.is_bingo = True
            self.winning_number = number

    @property
    def score(self) -> int:
        if self.winning_number is None:
            return 0
        return self.winning_number * sum(
            self[pos] for pos in range(len(self)) if pos not in self.matches
        )

    def reset(self) -> None:
        self.matches = set()
        self.is_bingo = False
