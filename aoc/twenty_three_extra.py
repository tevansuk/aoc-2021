import curses
import time
from typing import Any, Iterable

from aoc.twenty_three_base import ABCD, DOORS, Board, Move

Window = Any  # curses is poorly typed...


def move_positions(move: Move) -> Iterable[tuple[int, int]]:
    """(x,y) coords relative to hallway"""
    if move.froom != 0:
        for y in range(move.fidx + 1, -1, -1):
            yield (DOORS[move.froom], y)
        hidx = DOORS[move.froom]
    else:
        hidx = move.fidx
        yield (move.fidx, 0)
    if move.troom != 0:
        htidx = DOORS[move.troom]
    else:
        htidx = move.tidx
    mod = htidx > hidx and 1 or -1
    for x in range(hidx + mod, htidx + mod, mod):
        yield (x, 0)
    if move.troom != 0:
        for y in range(1, move.tidx + 2):
            yield (htidx, y)


def _animate(stdscr: Window, path: list[Board], cost: int):
    curses.curs_set(False)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    stdscr.clear()
    for board in path:
        if board.move:
            _show_move(stdscr, board.move)
        for idx, line in enumerate(str(board).split("\n")):
            stdscr.addstr(idx, 0, line, curses.color_pair(1))
        _show_correct(stdscr, board)
        stdscr.refresh()
        time.sleep(1)
    bsize = len(str(board).split("\n"))
    stdscr.addstr(bsize + 2, 0, f"Puzzle complete! Min cost {cost}")
    stdscr.addstr(bsize + 4, 0, "Press any key to continue")
    stdscr.getkey()


def _show_move(stdscr: Window, move: Move):
    prev = None
    for pos in move_positions(move):
        if prev is not None:
            stdscr.addch(prev[1] + 1, prev[0] + 1, ".", curses.color_pair(2))
        stdscr.addch(pos[1] + 1, pos[0] + 1, ABCD[move.piece], curses.color_pair(2))
        stdscr.refresh()
        prev = pos
        time.sleep(0.2)


def _show_correct(stdscr: Window, board: Board):
    for ridx, room in enumerate(board.rooms):
        if ridx == 0:
            continue
        for idx, val in enumerate(reversed(room)):
            if val != ridx:
                break
            stdscr.addch(len(room) + 1 - idx, DOORS[ridx] + 1, ABCD[val], curses.color_pair(3))


def animate_solution(path: list[Board], cost: int):
    def _wrapper(stdscreen: Window):
        return _animate(stdscreen, path, cost)

    curses.wrapper(_wrapper)
