from aoc.twenty_four import Program, run


def test_simple_prog() -> None:
    p = Program.parse(
        """inp z
inp x
mul z 3
eql z x
""".strip().split(
            "\n"
        )
    )
    state = run(p, [10, 30])
    assert state.z == 1
    state = run(p, [9, 30])
    assert state.z == 0
