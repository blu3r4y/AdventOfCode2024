# Advent of Code 2024, Day 4
# (c) blu3r4y

import numpy as np
from aocd.models import Puzzle
from funcy import lmap, print_calls, print_durations

MAIN_DIAGONAL = ((-1, -1), (0, 0), (1, 1))
ANTI_DIAGONAL = ((-1, 1), (0, 0), (1, -1))


@print_calls
@print_durations(unit="ms")
def part1(data):
    counts = 0
    for yield_fn in YIELD_FUNCTIONS:
        for line in yield_fn(data):
            counts += line.count("XMAS")
            counts += line.count("SAMX")

    return counts


@print_calls
@print_durations(unit="ms")
def part2(data):
    grid_size = len(data)

    counts = 0
    for x in range(grid_size):
        for y in range(grid_size):
            if is_xmas(data, x, y, grid_size):
                counts += 1

    return counts


def is_xmas(data, x, y, grid_size):
    left_text = text_at(data, x, y, grid_size, MAIN_DIAGONAL)
    right_text = text_at(data, x, y, grid_size, ANTI_DIAGONAL)
    return left_text in ("MAS", "SAM") and right_text in ("MAS", "SAM")


def text_at(grid, x, y, grid_size, offsets):
    indexes = [(x + dx, y + dy) for dx, dy in offsets]
    if all(0 <= x < grid_size and 0 <= y < grid_size for x, y in indexes):
        return "".join(grid[x][y] for x, y in indexes)


def yield_horizontal(data):
    for row in data:
        yield row


def yield_vertical(data):
    grid_size = len(data)
    for col in range(grid_size):
        yield "".join(row[col] for row in data)


def yield_main_diagonal(data):
    grid_size = len(data)
    data = np.array(lmap(list, data))
    for i in range(-grid_size + 1, grid_size):
        yield "".join(data.diagonal(i))


def yield_anti_diagonal(data):
    grid_size = len(data)
    data = np.array(lmap(list, data))
    for i in range(-grid_size + 1, grid_size):
        yield "".join(np.fliplr(data).diagonal(i))


YIELD_FUNCTIONS = [
    yield_horizontal,
    yield_vertical,
    yield_main_diagonal,
    yield_anti_diagonal,
]


def load(data):
    return data.splitlines()


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=4)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 2434
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 1835
    puzzle.answer_b = ans2
