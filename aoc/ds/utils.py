from typing import Callable, Iterable, TypeVar

from . import graphs
from .grids import Grid

GetEdges = Callable[[int], Iterable[int]]
GetCost = Callable[[int, int], graphs.Cost]
T = TypeVar("T", int, str)


def grid_to_graph(grid: Grid[T], get_edges: GetEdges, get_cost: GetCost) -> graphs.Graph:
    graph = graphs.AdjacencyListGraph[T]()
    for pos in grid.positions():
        for adj in get_edges(pos):
            graph[pos][adj] = get_cost(pos, adj)
    return graph
