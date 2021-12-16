from pathlib import Path

import pytest

from aoc.twelve import Graph, q1, q2


@pytest.fixture
def graph() -> Graph:
    with (Path(__file__).parent / "twelve.txt").open() as fp:
        return Graph.parse(fp, "-")


@pytest.fixture
def graph_big() -> Graph:
    with (Path(__file__).parent / "twelve-1.txt").open() as fp:
        return Graph.parse(fp, "-")


@pytest.fixture
def graph_bigger() -> Graph:
    with (Path(__file__).parent / "twelve-2.txt").open() as fp:
        return Graph.parse(fp, "-")


def test_parse_graph(graph: Graph) -> None:
    assert len(graph) == 6


def test_q1(graph: Graph, graph_big: Graph, graph_bigger: Graph) -> None:
    assert q1(graph) == 10
    assert q1(graph_big) == 19
    assert q1(graph_bigger) == 226


def test_q2(graph: Graph, graph_big: Graph, graph_bigger: Graph) -> None:
    assert q2(graph) == 36
    assert q2(graph_big) == 103
    assert q2(graph_bigger) == 3509


def test_recursive(graph: Graph) -> None:
    assert len(graph.routes_small_once_recursive()) == 10
    assert len(graph.routes_small_once_recursive(True)) == 36
