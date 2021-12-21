from collections import Counter
from functools import reduce
from pathlib import Path
from typing import Optional

Data = list[str]

CLOSES_SCORE = {
    ")": (3, 1),
    "]": (57, 2),
    "}": (1197, 3),
    ">": (25137, 4),
}
TO_CLOSE = {
    "{": "}",
    "[": "]",
    "<": ">",
    "(": ")",
}


def main(datafile: Path) -> None:
    data = parse_data(datafile)
    print(f"Q1: {q1(data) = }")
    print(f"Q2: {q2(data) = }")


def parse_data(datafile: Path) -> Data:
    return datafile.read_text().strip().split("\n")


def q1(data: Data) -> int:
    c = Counter(char for line in data if (char := illegal_incomplete(line)))
    return sum(CLOSES_SCORE[k][0] * v for k, v in c.items())


def q2(data: Data) -> int:
    scores = sorted(
        score(expected) for line in data if (expected := illegal_incomplete(line, incomplete=True))
    )
    return scores[len(scores) // 2]


def illegal_incomplete(line: str, incomplete: bool = False) -> Optional[str]:
    expected = list[str]()
    for char in line:
        if char in CLOSES_SCORE:
            if expected[-1] != char:
                return None if incomplete else char
            expected.pop()
        else:
            expected.append(TO_CLOSE[char])
    return "".join(expected[::-1]) if (incomplete and expected) else None


def score(expected: str) -> int:
    return reduce(lambda score, char: score * 5 + CLOSES_SCORE[char][1], expected, 0)
