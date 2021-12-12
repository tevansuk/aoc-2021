from collections import defaultdict
from pathlib import Path
from typing import TextIO

Vertex = str
AdjacencyList = list[Vertex]
GraphPath = list[Vertex]
_Stack = list[tuple[Vertex, GraphPath, bool]]


class Graph(defaultdict[Vertex, AdjacencyList]):
    @classmethod
    def parse_graph(cls, fp: TextIO):
        graph = cls(AdjacencyList)
        for line in fp.readlines():
            v_from, v_to = line.strip().split("-")
            graph[v_from].append(v_to)
            graph[v_to].append(v_from)
        return graph

    def routes_small_once(self, more_small: bool = False) -> list[GraphPath]:
        paths = list[GraphPath]()
        stack = _Stack([("start", GraphPath(), more_small)])
        while stack:
            vertex, path, more_small = stack.pop()
            path.append(vertex)
            if vertex == "end":
                paths.append(path)
            else:
                for adjacent in self[vertex]:
                    if adjacent not in path or adjacent.isupper():
                        stack.append((adjacent, path.copy(), more_small))
                    elif more_small:
                        if adjacent in ("start", "end"):
                            continue
                        stack.append((adjacent, path.copy(), False))
        return paths

    def routes_small_once_recursive(self, more_small: bool = False) -> list[GraphPath]:
        paths = list[GraphPath]()
        self._df_visit("start", GraphPath(), paths, more_small)
        return paths

    def _df_visit(
        self, vertex: Vertex, path: GraphPath, paths: list[GraphPath], more_small: bool
    ) -> None:
        path.append(vertex)
        if vertex == "end":
            paths.append(path)
        else:
            for adjacent in self[vertex]:
                if adjacent not in path or adjacent.isupper():
                    self._df_visit(adjacent, path.copy(), paths, more_small)
                elif more_small:
                    if adjacent in ("start", "end"):
                        continue
                    self._df_visit(adjacent, path.copy(), paths, False)


def main(datafile: Path) -> None:
    graph = parse_graph(datafile)
    print(f"Q1: {q1(graph) = }")
    print(f"Q2: {q2(graph) = }")


def parse_graph(datafile: Path) -> Graph:
    with datafile.open() as fp:
        return Graph.parse_graph(fp)


def q1(graph: Graph) -> int:
    return len(graph.routes_small_once())


def q2(graph: Graph) -> int:
    return len(graph.routes_small_once(True))
