from aoc.sixteen import Packet, q1, q2


def test_parse_packets() -> None:
    p = Packet.parse("D2FE28")
    assert p.version == 6
    assert p.type == 4
    assert p.val == 2021

    p = Packet.parse("38006F45291200")
    assert p.version == 1
    assert p.type == 6
    assert len(p.packets) == 2
    assert p.packets[0].val == 10
    assert p.packets[1].val == 20

    p = Packet.parse("EE00D40C823060")
    assert p.version == 7
    assert p.type == 3
    assert len(p.packets) == 3
    assert p.packets[0].val == 1
    assert p.packets[1].val == 2
    assert p.packets[2].val == 3


def test_hmm():
    p = Packet.parse("620080001611562C8802118E34")
    assert len(p.packets) == 2
    assert len(p.packets[0].packets) == 2
    assert len(p.packets[1].packets) == 2


def test_q1() -> None:
    assert q1("8A004A801A8002F478") == 16
    assert q1("620080001611562C8802118E34") == 12
    assert q1("C0015000016115A2E0802F182340") == 23
    assert q1("A0016C880162017C3686B18A3D4780") == 31


def test_q2() -> None:
    assert q2("C200B40A82") == 3
    assert q2("04005AC33890") == 54
    assert q2("880086C3E88112") == 7
    assert q2("CE00C43D881120") == 9
    assert q2("D8005AC2A8F0") == 1
    assert q2("F600BC2D8F") == 0
    assert q2("9C005AC2F8F0") == 0
    assert q2("9C0141080250320F1802104A08") == 1
