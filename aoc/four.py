from dataclasses import dataclass
from pathlib import Path
from typing import Optional

DrawList = list[int]
BoardList = list["Board"]
Cells = list[int]
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
    with datafile.open() as fp:
        draws = [int(draw) for draw in fp.readline().split(",")]
        cells = [int(num) for num in fp.read().split()]
    boards = [
        Board(cells=cells[pos : pos + DIM ** 2], matches=set())
        for pos in range(0, len(cells), DIM ** 2)
    ]
    return draws, boards


def winner_winner_chicken_dinner(draws, boards) -> Optional["Board"]:
    for number in draws:
        for board in boards:
            board.draw(number)
            if board.is_bingo:
                return board


def let_the_wookie_win(draws, boards) -> Optional["Board"]:
    last_winner = None
    for number in draws:
        for board in boards:
            if not board.is_bingo:
                board.draw(number)
                if board.is_bingo:
                    last_winner = board
    return last_winner


@dataclass
class Board:
    cells: Cells
    matches: CellMatches
    is_bingo = False
    winning_number: Optional[int] = None

    def draw(self, number) -> None:
        if self.is_bingo:
            return
        self.matches.update(pos for pos in range(DIM ** 2) if self.cells[pos] == number)
        if any(all(pos in self.matches for pos in bingo) for bingo in BINGOS):
            self.is_bingo = True
            self.winning_number = number

    @property
    def score(self) -> int:
        if not self.is_bingo:
            return 0
        return self.winning_number * sum(
            self.cells[pos] for pos in range(DIM ** 2) if pos not in self.matches
        )

    def reset(self) -> None:
        self.matches = set()
        self.is_bingo = False
