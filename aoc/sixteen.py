from functools import reduce
from operator import mul
from pathlib import Path


class Packet:
    version: int
    type: int
    val: int
    packets: list["Packet"]

    def __init__(self):
        self.version = 0
        self.type = 0
        self.val = 0
        self.packets = []

    @classmethod
    def parse(cls, val: str) -> "Packet":
        bits = format(int(val, 16), f"0{len(val) * 4}b")
        p = Packet()
        p._parse(bits)
        return p

    def value(self) -> int:
        if self.type == 4:
            return self.val
        elif self.type == 0:
            return sum(p.value() for p in self.packets)
        elif self.type == 1:
            return reduce(mul, (p.value() for p in self.packets))
        elif self.type == 2:
            return min(p.value() for p in self.packets)
        elif self.type == 3:
            return max(p.value() for p in self.packets)
        elif self.type == 5:
            return int(self.packets[0].value() > self.packets[1].value())
        elif self.type == 6:
            return int(self.packets[0].value() < self.packets[1].value())
        elif self.type == 7:
            return int(self.packets[0].value() == self.packets[1].value())
        return 0

    def _parse(self, bits: str) -> str:
        self.version = int(bits[0:3], 2)
        self.type = int(bits[3:6], 2)
        if self.type == 4:
            return self._parse_value(bits)
        else:
            return self._parse_sub_packets(bits)

    def _parse_sub_packets(self, bits: str) -> str:
        rem = ""
        npackets = 0
        if int(bits[6], 2):
            npackets = int(bits[7:18], 2)
            pdata = bits[18:]
        else:
            tlen = int(bits[7:22], 2)
            pdata = bits[22 : 22 + tlen]
            rem = bits[22 + tlen :]
        while pdata:
            p = Packet()
            pdata = p._parse(pdata)
            self.packets.append(p)
            if npackets and len(self.packets) == npackets:
                rem = pdata
                break
        return rem

    def _parse_value(self, bits: str) -> str:
        pval = ""
        idx = 6
        while bits[idx] == "1":
            pval += bits[idx + 1 : idx + 5]
            idx += 5
        pval += bits[idx + 1 : idx + 5]
        self.val = int(pval, 2)
        return bits[idx + 5 :]


def main(datafile: Path) -> None:
    with datafile.open() as fp:
        data = fp.readline().strip()
    print(f"Q1: {q1(data) = }")
    print(f"Q2: {q2(data) = }")


def q1(value: str) -> int:
    p = Packet.parse(value)
    vsum = 0
    stack = [p]
    while stack:
        p = stack.pop()
        vsum += p.version
        stack.extend(p.packets)
    return vsum


def q2(value: str) -> int:
    p = Packet.parse(value)
    return p.value()
