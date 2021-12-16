from pathlib import Path

from aoc.ds.graphs import AdjacencyListGraph, GraphPath

_Stack = list[tuple[str, GraphPath, bool]]


class Graph(AdjacencyListGraph[str]):
    def routes_small_once(self, more_small: bool = False) -> list[GraphPath]:
        paths = list[GraphPath]()
        stack = _Stack([("start", GraphPath(), more_small)])
        while stack:
            vertex, path, more_small = stack.pop()
            path.append(vertex)
            if vertex == "end":
                paths.append(path)
            else:
                for adjacent in self.adjacent(vertex):
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
        self, vertex: str, path: GraphPath, paths: list[GraphPath], more_small: bool
    ) -> None:
        path.append(vertex)
        if vertex == "end":
            paths.append(path)
        else:
            for adjacent in self.adjacent(vertex):
                if adjacent not in path or adjacent.isupper():
                    self._df_visit(adjacent, path.copy(), paths, more_small)
                elif more_small:
                    if adjacent in ("start", "end"):
                        continue
                    self._df_visit(adjacent, path.copy(), paths, False)


def main(datafile: Path) -> None:
    with datafile.open() as fp:
        graph = Graph.parse(fp, "-")
    print(f"Q1: {q1(graph) = }")
    print(f"Q2: {q2(graph) = }")


def q1(graph: Graph) -> int:
    return len(graph.routes_small_once())


def q2(graph: Graph) -> int:
    return len(graph.routes_small_once(True))
