from collections import Counter
from pathlib import Path

from aoc.ds.grids import int_number_value_parser

N = [7, 5, 4, 3, 2, 1, 0]


def main(datafile: Path) -> None:
    data = parse_data(datafile)
    day_80 = age(data, 80)
    print(f"Q1: {sum(day_80.values())}")
    day_256 = age(data, 256)
    print(f"Q2: {sum(day_256.values())}")


def age(data: Counter, days: int) -> Counter:
    for day in range(1, days + 1):
        data = Counter({8: data[0], 6: data[0] + data[7]} | {k: data[k + 1] for k in N})
    return data


def parse_data(datafile: Path) -> Counter:
    return Counter(int_number_value_parser(",")(datafile.read_text()))
