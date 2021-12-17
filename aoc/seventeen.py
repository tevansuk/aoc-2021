import re
from collections import defaultdict
from itertools import product
from pathlib import Path
from typing import Tuple

TargetSteps = defaultdict[int, set[int]]
XAnyStep = set[int]
Velocities = set[tuple[int, int]]
Target = Tuple[int, ...]


def tri(n: int) -> int:
    return (n * (n + 1)) // 2


def parse_data(datafile: Path) -> Target:
    with datafile.open() as fp:
        return tuple(map(int, re.findall(r"[-\d]+", fp.readline())))


def main(datafile: Path):
    all_launch_speeds = find_all_launch_speeds(*parse_data(datafile))
    print(f"Q1: {q1(all_launch_speeds) = }")
    print(f"Q2: {q2(all_launch_speeds) = }")


def q1(all_launch_speeds) -> int:
    max_y_speed = max(v[1] for v in all_launch_speeds)
    return tri(max_y_speed)


def q2(all_launch_speeds) -> int:
    return len(all_launch_speeds)


def find_all_launch_speeds(xmin: int, xmax: int, ymin: int, ymax: int) -> Velocities:
    x_steps, x_any_step = find_x_steps(xmin, xmax)
    y_steps = find_y_steps(ymin, ymax)
    return combine(x_steps, y_steps, x_any_step)


def find_x_steps(xmin: int, xmax: int) -> tuple[TargetSteps, XAnyStep]:
    x_steps = TargetSteps(set)
    x_any_step = XAnyStep()
    for xspeed in range(xmax + 1):
        max_x = tri(xspeed)
        if max_x < xmin:
            continue
        if max_x <= xmax:
            x_any_step.add(xspeed)
        cx = max_x
        for step in range(xspeed):
            cx -= step
            if xmin <= cx <= xmax:
                x_steps[xspeed - step].add(xspeed)
            elif cx < xmin:
                break
    return x_steps, x_any_step


def find_y_steps(ymin: int, ymax: int) -> TargetSteps:
    y_steps = TargetSteps(set)
    for yspeed in range(ymin, abs(ymin + ymax)):
        dy = yspeed
        cy = 0
        step = 0
        while True:
            if ymin <= cy <= ymax:
                y_steps[step].add(yspeed)
            elif cy < ymin:
                break
            cy += dy
            dy -= 1
            step += 1
    return y_steps


def combine(x_steps: TargetSteps, y_steps: TargetSteps, x_any_step: XAnyStep) -> Velocities:
    launch_velocities = Velocities()
    for step in set(x_steps.keys()) & set(y_steps.keys()):
        launch_velocities.update(product(x_steps[step], y_steps[step]))
    for x_any in x_any_step:
        for step, y_speeds in y_steps.items():
            if step >= x_any:
                launch_velocities.update((x_any, y_speed) for y_speed in y_speeds)
    return launch_velocities
