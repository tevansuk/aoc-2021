from aoc.ds import graphs


def test_graph():
    data = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
    graph = graphs.AdjacencyListGraph[str].parse(data, "-")
    assert set(graph.vertices()) == {"start", "A", "b", "c", "d", "end"}
    assert set(graph.adjacent("start")) == {"A", "b"}
    assert set(graph.adjacent("A")) == {"start", "b", "c", "end"}
