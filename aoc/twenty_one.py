from collections import Counter
from dataclasses import dataclass
from functools import cache
from itertools import product
from pathlib import Path
from typing import Iterable

Score = int
Position = int
State = tuple[Score, Position, Score, Position]
Count = int


def infinite_die(dN: int = 100) -> Iterable[int]:
    while True:
        yield from range(1, dN + 1)


def three_rolls(dN: int = 100) -> Iterable[int]:
    die = iter(infinite_die())
    while True:
        yield sum((next(die), next(die), next(die)))


@dataclass
class Data:
    start: list[int]

    def play(self) -> tuple[list[int], int]:
        position = self.start[:]
        score = [0, 0]
        rolls = 0
        dice = iter(three_rolls())
        playing = True
        while playing:
            for player in (0, 1):
                rolls += 3
                position[player] = (position[player] + next(dice)) % 10
                score[player] += position[player] + 1
                if score[player] >= 1000:
                    playing = False
                    break
        return score, rolls

    def play_dirac_counter(self) -> list[int]:
        # The return of lanternfish:
        # Track the number of new universes for each possible 3 dice roll
        dice = Counter(sum(dice) for dice in product(range(1, 4), repeat=3))
        # and track the number of universes for each combination of position and score
        games: Counter[State] = Counter({(self.start[0], 0, self.start[1], 0): 1})
        wins = [0, 0]
        while games:
            ngames: Counter[State] = Counter()
            for (p1, s1, p2, s2), num_games in games.items():
                for dice_roll, new_games in dice.items():
                    pos = (p1 + dice_roll) % 10
                    score = s1 + pos + 1
                    if score >= 21:
                        wins[0] += new_games * num_games
                        continue
                    for dice_roll2, new_games2 in dice.items():
                        pos2 = (p2 + dice_roll2) % 10
                        score2 = s2 + pos2 + 1
                        if score2 >= 21:
                            wins[1] += num_games * new_games * new_games2
                            continue
                        ngames[(pos, score, pos2, score2)] += num_games * new_games * new_games2
            games = ngames
        return wins

    def play_dirac_dp(self) -> list[int]:
        dice = Counter(sum(dice) for dice in product(range(1, 4), repeat=3))

        @cache
        def get_winner(pos1, pos2, score1, score2):
            if score1 >= 21 or score2 >= 21:
                return [int(score1 >= 21), int(score2 >= 21)]
            wins = [0, 0]
            for roll, count in dice.items():
                pos = (pos1 + roll) % 10
                score = score1 + pos + 1
                # Now roll for player 2, inverting the arguments
                wins2, wins1 = get_winner(pos2, pos, score2, score)
                wins = [wins[0] + count * wins1, wins[1] + count * wins2]
            return wins

        return get_winner(self.start[0], self.start[1], 0, 0)


def main(datafile: Path) -> None:
    data = parse_data(datafile)
    print(f"Q1: {q1(data) = }")
    print(f"Q2: {q2(data) = }")


def parse_data(datafile: Path) -> Data:
    start_pos = [int(line[-1]) - 1 for line in datafile.read_text().strip().split("\n")]
    return Data(start=start_pos)


def q1(data: Data) -> int:
    score, rolls = data.play()
    return min(score) * rolls


def q2(data: Data) -> int:
    wins = data.play_dirac_dp()
    return max(wins)
