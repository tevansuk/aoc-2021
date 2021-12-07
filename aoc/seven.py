from pathlib import Path


def main(datafile: Path) -> None:
    data = parse_data(datafile)
    print(f"Q1: {min(costs(data))=}")
    print(f"Q2: {min(costs2(data))=}")


def shortest_alignment(costs: list[int]) -> int:
    return costs.index(min(costs))


def costs(data: list[int]) -> list[int]:
    return [sum(abs(cpos - pos) for cpos in data) for pos in range(max(data) + 1)]


def costs2(data: list[int]) -> list[int]:
    return [
        sum((n * (n + 1)) // 2 for cpos in data if (n := abs(cpos - pos)))
        for pos in range(max(data) + 1)
    ]


def parse_data(datafile: Path) -> list[int]:
    with datafile.open() as fp:
        return [int(val) for line in fp.readlines() for val in line.split(",")]
