import heapq
from collections import defaultdict
from math import inf
from random import random
from typing import Callable, Iterable, Optional, TypeVar

Vertex = TypeVar("Vertex")
Path = list[Vertex]
Cost = int
GetCost = Callable[[Vertex, Vertex], Cost]
GetNeighbours = Callable[[Vertex], Iterable[Vertex]]
GetNeighboursAndCost = Callable[[Vertex], Iterable[tuple[Vertex, Cost]]]
_StableSort = float
_Heap = list[tuple[Cost, _StableSort, Vertex]]
_Seen = set[Vertex]


def dijkstra(
    start: Vertex,
    end: Vertex,
    get_neighbours: GetNeighbours,
    get_cost: GetCost,
) -> tuple[Path, Cost]:
    """
    Generic Dijkstra's shortest path algorithm.

    The Vertex type needs to be hashable.

    Args:
        start: The start vertex
        end: The end vertex
        get_vertices: Callable returning the full set of vertices in the graph
        get_neighbours: Callable returning the neighbours for a given vertex
        get_cost: Callable returning the cost to go from one vertex to another
    """
    dist: defaultdict[Vertex, Cost] = defaultdict(lambda: inf, {start: 0})
    prev: defaultdict[Vertex, Optional[Vertex]] = defaultdict(lambda: None)
    heap = _Heap([(0, random(), start)])
    seen = _Seen()
    cost = 0
    while heap:
        cost, _, vertex = heapq.heappop(heap)
        if vertex in seen:
            continue
        seen.add(vertex)
        if vertex == end:
            end = vertex
            break
        for adjacent in get_neighbours(vertex):
            alt = cost + get_cost(vertex, adjacent)
            if alt < dist[adjacent]:
                dist[adjacent] = alt
                prev[adjacent] = vertex
                heapq.heappush(heap, (alt, random(), adjacent))
    path = []
    vertex = end
    if prev[vertex] is not None or vertex == start:
        while vertex is not None:
            path.insert(0, vertex)
            vertex = prev.get(vertex)
    return path, cost


def dijkstra2(
    start: Vertex,
    end: Vertex,
    get_neighbours_and_cost: GetNeighboursAndCost,
) -> tuple[Path, Cost]:
    """
    Generic Dijkstra's shortest path algorithm.

    The Vertex type needs to be hashable.

    Args:
        start: The start vertex
        end: The end vertex
        get_neighbours_and_cost: Callable returning the neighbours for a given vertex
    """
    dist: defaultdict[Vertex, Cost] = defaultdict(lambda: inf, {start: 0})
    prev: defaultdict[Vertex, Optional[Vertex]] = defaultdict(lambda: None)
    heap = _Heap([(0, random(), start)])
    seen = _Seen()
    cost = 0
    while heap:
        cost, _, vertex = heapq.heappop(heap)
        if vertex in seen:
            continue
        seen.add(vertex)
        if vertex == end:
            end = vertex
            break
        for adjacent, ncost in get_neighbours_and_cost(vertex):
            alt = cost + ncost
            if alt < dist[adjacent]:
                dist[adjacent] = alt
                prev[adjacent] = vertex
                heapq.heappush(heap, (alt, random(), adjacent))
    path = []
    vertex = end
    if prev[vertex] is not None or vertex == start:
        while vertex is not None:
            path.insert(0, vertex)
            vertex = prev.get(vertex)
    return path, cost
