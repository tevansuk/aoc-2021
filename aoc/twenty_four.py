import operator
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Iterable


@dataclass
class Stack:
    w: int = 0
    x: int = 0
    y: int = 0
    z: int = 0

    def eval(self, register):
        if register in "wxyz":
            return getattr(self, register)
        return int(register)


@dataclass(frozen=True)
class Op:
    ins: str
    r1: str
    r2: str


OPS = {
    "add": operator.add,
    "mul": operator.mul,
    "div": operator.floordiv,
    "mod": operator.mod,
    "eql": operator.eq,
}


@dataclass(frozen=True)
class Program:
    ops: tuple[Op, ...]

    @classmethod
    def parse(cls, lines: list[str]) -> list["Program"]:
        ops = []
        progs = []
        for line in lines:
            try:
                ins, r1, r2 = line.split()
                ops.append(Op(ins, r1, r2))
            except ValueError:
                if ops:
                    progs.append(cls(tuple(ops)))
                    ops = []
                ins, register = line.split()
                ops.append(Op(ins, register, ""))
        if ops:
            progs.append(cls(tuple(ops)))
        return progs

    def run(self, inp: int, stack: Stack) -> Stack:
        for op in self.ops:
            if op.ins == "inp":
                val = inp
            else:
                val = OPS[op.ins](getattr(stack, op.r1), stack.eval(op.r2))
            setattr(stack, op.r1, int(val))
        return stack


def run(programs: list[Program], inp: int | list[int]) -> Stack:
    if isinstance(inp, int):
        inp = [int(c) for c in str(inp)]
    stack = Stack()
    for idx, prog in enumerate(programs):
        stack = prog.run(inp[idx], stack)
    return stack


def main(datafile: Path) -> None:
    prog = parse_data(datafile)
    print(f"Q1: {q1(prog) = }")
    print(f"Q2: {q2(prog) = }")


def parse_data(datafile: Path) -> list[Program]:
    return Program.parse(datafile.read_text().strip().split("\n"))


def solve(progs: list[Program], search_range: Iterable[int]) -> int:
    # The entire program is basically 14 different programs
    # Each of those 14 programs is in one of two styles
    # To tell them apart, op 4 either divides z by 1 or 26
    # The differences:
    # Type1+2: op5 adds A to x
    # Type1+2: op15 adds B to y
    # Type1+2: inputs are digit (w), z, A, B - x and y are zeroed
    # There are ten rounds of type 1, then 4 rounds of type
    # For type 2 blocks, if we calculate x and its not in the range 1-10, its no
    # good and we can just skip it
    # For z to end up as 0 after final type2:
    #   x==0 => iz % 26 + a == w
    #   iz < 26
    # => w - a = iz
    # a = -10, therefore for final step iz = w + 10 (therefore 11 < iz <= 25)
    # The previous 3 type2 either decrease z by facter of 1 or 26, therefore
    # the range of iz that the first type2 stage gets needs to be in the range
    # 26 ** 3 (interesting, but ultimately not relevant, cache is good enough!)
    progv = tuple((int(p.ops[5].r2), int(p.ops[15].r2), int(p.ops[4].r2)) for p in progs)

    @cache
    def block(w, z, abc):
        a, b, c = abc
        x = int((z % 26) + a != w)
        z = z // c
        z *= (25 * x) + 1
        return z + ((w + b) * x)

    @cache
    def solve_serial(idx, iz):
        if idx == 13:
            for num in search_range:
                if block(num, iz, progv[idx]) == 0:
                    return num
            return 0
        else:
            if progv[idx][2] == 1:
                nums = search_range
            else:
                # Optimisation: calculate x - if  0 < x < 10 then check just x
                # otherwise, its no good
                x = (iz % 26) + progv[idx][0]
                if not 0 < x < 10:
                    return 0
                nums = range(x, x + 1)
            for num in nums:
                res = solve_serial(idx + 1, block(num, iz, progv[idx]))
                if res > 0:
                    return num * (10 ** (13 - idx)) + res
            return 0
        return 0

    return solve_serial(0, 0)


def q1(progs):
    serial = solve(progs, range(9, 0, -1))
    assert run(progs, serial).z == 0
    return serial


def q2(progs) -> int:
    serial = solve(progs, range(1, 10))
    assert run(progs, serial).z == 0
    return serial
