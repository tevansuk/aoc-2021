from io import StringIO

from aoc.ds.grids import Grid


def test_grid():
    grid = Grid[int].parse(StringIO("123\n456\n789\n"))

    assert len(grid) == 9
    assert grid.w == 3
    assert grid.h == 3

    assert set(grid.surrounding(0)) == {1, 3, 4}
    assert set(grid.surrounding(3)) == {0, 1, 4, 6, 7}
    assert set(grid.surrounding(1)) == {0, 2, 3, 4, 5}
    assert set(grid.surrounding(4)) == {0, 1, 2, 3, 5, 6, 7, 8}
    assert set(grid.surrounding(8)) == {4, 5, 7}

    assert set(grid.adjacent(0)) == {1, 3}
    assert set(grid.adjacent(3)) == {0, 4, 6}
    assert set(grid.adjacent(1)) == {0, 2, 4}
    assert set(grid.adjacent(4)) == {1, 3, 5, 7}
    assert set(grid.adjacent(8)) == {5, 7}

    assert grid.pos2coord(0) == (0, 0)
    assert grid.pos2coord(3) == (0, 1)
    assert grid.pos2coord(4) == (1, 1)
    assert grid.pos2coord(8) == (2, 2)
