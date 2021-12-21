from collections import defaultdict
from collections.abc import MutableMapping
from typing import Iterable, Type, TypeVar

Vertex = TypeVar("Vertex", int, str)
Cost = int
AdjacencyList = dict[Vertex, Cost]
GraphPath = list[Vertex]
Graph = TypeVar("Graph", bound="BaseGraph")


class BaseGraph(MutableMapping[Vertex, AdjacencyList]):
    def vertices(self) -> Iterable[Vertex]:
        return self.keys()

    def adjacent(self, vertex: Vertex) -> Iterable[Vertex]:
        return self[vertex].keys()

    def cost(self, vertex: Vertex, to: Vertex) -> Cost:
        return self[vertex][to]


class AdjacencyListGraph(defaultdict[Vertex, AdjacencyList], BaseGraph):
    def __init__(self, *args, **kwargs):
        super().__init__(AdjacencyList, *args, **kwargs)

    @classmethod
    def parse(
        cls: Type[Graph],
        data: str,
        split: str,
        bidi: bool = True,
        vertex_type: Type[Vertex] = str,
    ) -> Graph:
        graph = cls()
        for line in data.strip().split("\n"):
            v_from, v_to = line.strip().split(split)
            graph[vertex_type(v_from)][vertex_type(v_to)] = 0
            if bidi:
                graph[vertex_type(v_to)][vertex_type(v_from)] = 0
        return graph

    @classmethod
    def parse_with_costs(
        cls: Type[Graph], data: str, split: str, vertex_type: Type[Vertex] = str
    ) -> Graph:
        graph = cls()
        for line in data.strip().split("\n"):
            v_from, v_to, cost = line.strip().split(split)
            graph[vertex_type(v_from)][vertex_type(v_to)] = Cost(cost)
        return graph
