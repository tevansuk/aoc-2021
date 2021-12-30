from aoc.alg import dijkstra
from aoc.ds.grids import Grid
from aoc.ds.utils import grid_to_graph


def test_dijkstra():
    # Works with any data structure
    data = """1163751742
1381373672
2136511328
3694931569
7463417191
1319128137
1359912421
3125421639
1293138521
2311944581"""
    grid = Grid[int].parse(data)
    start = 0
    end = len(grid) - 1

    def get_cost(vertex, adjacent):
        return grid[adjacent]

    path, cost = dijkstra(start, end, grid.adjacent, get_cost)
    assert cost == 40
    assert path == [0, 10, 20, 21, 22, 23, 24, 25, 26, 36, 37, 47, 57, 58, 68, 78, 88, 89, 99]

    # And with an adjacency list graph...
    graph = grid_to_graph(grid, grid.adjacent, get_cost)
    npath, ncost = dijkstra(start, end, graph.adjacent, graph.cost)
    assert ncost == cost
    assert npath == path
