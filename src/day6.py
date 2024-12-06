# Advent of Code 2024, Day 6
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations
from tqdm.auto import tqdm

GUARD = "^"
WALL = "#"
FREE = "."


@print_calls
@print_durations(unit="ms")
def part1(data):
    walls, guard, limits = data

    visited = set()
    heading = -1j

    while within_bounds(guard, limits):
        visited.add(guard)
        while guard + heading in walls:
            heading *= 1j  # turn right
        guard += heading

    return len(visited)


@print_calls
@print_durations(unit="ms")
def part2(data):
    walls, guard, limits = data
    width, height = limits

    obstructions = 0

    pbar = tqdm(total=width * height)
    for r in range(width):
        for c in range(height):
            cell = cmplx(r, c)
            if cell == guard or cell in walls:
                continue

            new_walls = walls.copy()
            new_walls[cell] = WALL
            if is_guard_looping(new_walls, guard, limits):
                obstructions += 1

            pbar.update(1)

    return obstructions


def within_bounds(pos, limits):
    height, width = limits
    return 0 <= pos.imag < height and 0 <= pos.real < width


def is_guard_looping(walls, guard, limits):
    visited = []
    heading = -1j

    while within_bounds(guard, limits):
        if len(visited) % 10_000 == 0:
            if detect_cycle(visited):
                return True

        visited.append((guard, heading))
        while guard + heading in walls:
            heading *= 1j  # turn right
        guard += heading

    # out of bounds, no cycle
    return False


def detect_cycle(visited):
    if len(visited) < 2:
        return False

    # Floyd's Tortoise and Hare algorithm
    tortoise, hare = 0, 0
    while True:
        if hare + 1 >= len(visited) or hare + 2 >= len(visited):
            return False

        tortoise += 1
        hare += 2

        if visited[tortoise] == visited[hare]:
            return True


def cmplx(r, c):
    return 1j * r + c


def load(data):
    walls, guard = {}, None

    rows = data.splitlines()
    for r, row in enumerate(data.splitlines()):
        for c, cell in enumerate(row):
            pos = cmplx(r, c)
            if cell == WALL:
                walls[pos] = cell
            elif cell == GUARD:
                guard = pos

    limits = len(rows), len(rows[0])
    return walls, guard, limits


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=6)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 5242
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 1424
    puzzle.answer_b = ans2
