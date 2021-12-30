import importlib
import os
import subprocess
import sys
from pathlib import Path

from num2words import num2words


def main():
    if len(sys.argv) < 2:
        print("Usage: poetry day [N]")
        sys.exit(-1)
    day = int(sys.argv[1])
    args = sys.argv[2:]
    print(f"Yo its day {day}")
    dayw = num2words(day).replace("-", "_")
    module_name = f"aoc.{dayw}"
    input_file = Path(__file__).parent.parent / "resources" / f"{dayw}.txt"
    try:
        mod = importlib.import_module(module_name)
        func = getattr(mod, "main")
    except (ModuleNotFoundError, AttributeError):
        print(f"No such module/function {module_name}.main")
        sys.exit(-1)
    print(f"Running {module_name}.main")
    sys.exit(func(input_file, *args))


def make_my_day():
    if len(sys.argv) != 2:
        print("Usage: poetry mkday [N]")
        sys.exit(-1)
    dayw = num2words(int(sys.argv[1])).replace("-", "_")
    root = Path(__file__).parent.parent
    pyfile = root / "aoc" / f"{dayw}.py"
    if not pyfile.exists():
        pyfile.write_text(
            """from pathlib import Path

Data = list[str]


def main(datafile: Path) -> None:
    data = parse_data(datafile)
    print(f"Q1: {q1(data) = }")
    print(f"Q2: {q2(data) = }")


def parse_data(datafile: Path) -> Data:
    return datafile.read_text().strip().split("\\n")


def q1(data: Data) -> int:
    return 0


def q2(data: Data) -> int:
    return 0
"""
        )
    testfile = root / "tests" / f"test_{dayw}.py"
    if not testfile.exists():
        testfile.write_text(
            f"""from pathlib import Path

import pytest

from aoc.{dayw} import Data, parse_data, q1, q2


@pytest.fixture
def data() -> Data:
    return parse_data(Path(__file__).parent / "{dayw}.txt")


def test_parse_data(data: Data) -> None:
    assert len(data) == 10


def test_q1(data: Data) -> None:
    assert q1(data) == 0


def test_q2(data: Data) -> None:
    assert q2(data) == 0
"""
        )
    testdata = root / "tests" / f"{dayw}.txt"
    if not testdata.exists():
        testdata.write_text("")
    files = [pyfile, testfile, testdata]
    if os.environ.get("EDITOR") == "vim":
        subprocess.check_call(["vim", "-o", *files])
    else:
        print("Created the following files:", *files, sep="\n")
