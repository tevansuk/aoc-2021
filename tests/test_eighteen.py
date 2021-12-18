from pathlib import Path
from typing import Type

import pytest

from aoc.eighteen import NUMBER_TYPES, Number, NumberDumb, q1, q2


@pytest.fixture
def data() -> list[str]:
    with (Path(__file__).parent / "eighteen.txt").open() as fp:
        return [line.strip() for line in fp.readlines()]


@pytest.mark.parametrize("Number", NUMBER_TYPES.values())
def test_add_basic(data: list[str], Number: Type[Number]) -> None:
    s = Number.parse("[[[[4,3],4],4],[7,[[8,4],9]]]")
    s += Number.parse("[1,1]")
    assert str(s) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"

    val = Number.parse(data[0])
    for num in data[1:]:
        val += Number.parse(num)
    assert str(val) == "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"
    assert val.magnitude == 4140


@pytest.mark.parametrize("Number", NUMBER_TYPES.values())
def test_explode(Number: Type[Number]):
    s = Number.parse("[[6,[5,[4,[3,2]]]],1]")
    assert s.explode()
    assert str(s) == "[[6,[5,[7,0]]],3]"


@pytest.mark.parametrize("Number", NUMBER_TYPES.values())
def test_split(Number: Type[Number]):
    s = Number.parse("[[[[0,7],4],[15,[0,13]]],[1,1]]")
    assert s.split()
    assert str(s) == "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"


@pytest.mark.parametrize("Number", NUMBER_TYPES.values())
def test_str_format(Number: Type[Number], data: list[str]):
    for line in data:
        assert str(Number.parse(line)) == line


@pytest.mark.parametrize("Number", NUMBER_TYPES.values())
def test_add(Number: Type[Number]):
    s = Number.parse("[1,1]")
    assert str(s) == "[1,1]"
    s += Number.parse("[2,2]")
    assert str(s) == "[[1,1],[2,2]]"
    s += Number.parse("[3,3]")
    assert str(s) == "[[[1,1],[2,2]],[3,3]]"
    s += Number.parse("[4,4]")
    assert str(s) == "[[[[1,1],[2,2]],[3,3]],[4,4]]"

    s += Number.parse("[5,5]")
    assert str(s) == "[[[[3,0],[5,3]],[4,4]],[5,5]]"

    s += Number.parse("[6,6]")
    assert str(s) == "[[[[5,0],[7,4]],[5,5]],[6,6]]"

    s = Number.parse("[[[[4,3],4],4],[7,[[8,4],9]]]")
    s += Number.parse("[1,1]")
    assert str(s) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"


@pytest.mark.parametrize("Number", NUMBER_TYPES.values())
def test_add_complex(Number: Type[Number]):
    s = Number.parse("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]")
    s += Number.parse("[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]")
    assert str(s) == "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"

    s += Number.parse("[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]")
    assert str(s) == "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]"
    s += Number.parse("[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]")
    assert str(s) == "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]"
    s += Number.parse("[7,[5,[[3,8],[1,4]]]]")
    s += Number.parse("[[2,[2,2]],[8,[8,1]]]")
    s += Number.parse("[2,9]")
    s += Number.parse("[1,[[[9,3],9],[[9,0],[0,7]]]]")
    s += Number.parse("[[[5,[7,4]],7],1]")
    s += Number.parse("[[[[4,2],2],6],[8,7]]")
    assert str(s) == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"


@pytest.mark.parametrize(
    "nums,expected",
    [
        (
            [[6, [5, [4, [3, 2]]]], 1],
            [
                (6, [0, 0]),
                (5, [0, 1, 0]),
                (4, [0, 1, 1, 0]),
                (3, [0, 1, 1, 1, 0]),
                (2, [0, 1, 1, 1, 1]),
                (1, [1]),
            ],
        ),
    ],
)
def test_nums_to_loc(nums, expected):
    assert list(NumberDumb._nums_to_loc(nums, [])) == expected


@pytest.mark.parametrize("Number", NUMBER_TYPES.values())
@pytest.mark.parametrize(
    "inp,magnitude",
    [
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
    ],
)
def test_magnitude(Number: Type[Number], inp: str, magnitude: int):
    assert Number.parse(inp).magnitude == magnitude


@pytest.mark.parametrize("Number", NUMBER_TYPES.values())
def test_q1(Number: Type[Number], data: list[str]) -> None:
    assert q1([Number.parse(num) for num in data]) == 4140


@pytest.mark.parametrize("Number", NUMBER_TYPES.values())
def test_q2(Number: Type[Number], data: list[str]) -> None:
    assert q2([Number.parse(num) for num in data]) == 3993
