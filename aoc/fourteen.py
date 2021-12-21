from collections import Counter
from pathlib import Path
from typing import Iterable


class Data:
    polymer: str
    mutations: dict[str, str]

    @classmethod
    def parse(cls, text: str) -> "Data":
        data = cls()
        data.polymer, _, *mut = text.strip().split("\n")
        data.mutations = {p[0]: p[1] for m in mut if (p := m.split(" -> "))}
        return data

    def step(self) -> None:
        npolymer = []
        for pair in self.pairs():
            if insert := self.mutations.get(pair):
                npolymer.append(pair[0] + insert)
            else:
                npolymer.append(pair[0])
        npolymer.append(self.polymer[-1])
        self.polymer = "".join(npolymer)

    def cstep(self, steps: int) -> Counter[str]:
        pairs = Counter(self.pairs())
        for _ in range(steps):
            for pair, count in pairs.copy().items():
                if mut := self.mutations.get(pair):
                    pairs[pair] -= count
                    pairs[pair[0] + mut] += count
                    pairs[mut + pair[1]] += count
        chars = Counter[str](self.polymer[0])
        for pair, count in pairs.items():
            chars[pair[1]] += count
        return chars

    def pairs(self) -> Iterable[str]:
        return (a + b for a, b in zip(self.polymer, self.polymer[1:]))


def main(datafile: Path) -> None:
    data = Data.parse(datafile.read_text())
    print(f"Q1: {q1(data) = }")
    data = Data.parse(datafile.read_text())
    print(f"Q2: {q2(data) = }")


def q1(data: Data) -> int:
    for _ in range(10):
        data.step()
    c = Counter(char for char in data.polymer)
    counts = c.values()
    return max(counts) - min(counts)


def q2(data: Data) -> int:
    c = data.cstep(40)
    counts = c.values()
    return max(counts) - min(counts)
