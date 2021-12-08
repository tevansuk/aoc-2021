from collections import Counter
from pathlib import Path

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
    with datafile.open() as fp:
        return Counter(int(val) for line in fp.readlines() for val in line.split(","))
