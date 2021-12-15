from io import StringIO

from aoc.ds import graphs


def test_graph():
    fp = StringIO(
        """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
    )
    graph = graphs.AdjacencyListGraph[str].parse(fp, "-")
    assert set(graph.vertices()) == {"start", "A", "b", "c", "d", "end"}
    assert set(graph.adjacent("start")) == {"A", "b"}
    assert set(graph.adjacent("A")) == {"start", "b", "c", "end"}
