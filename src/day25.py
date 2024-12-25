# Advent of Code 2024, Day 25
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations

FILLED, EMPTY = "#", "."
WIDTH, HEIGHT = 5, 7
SLOT = 5


@print_calls
@print_durations(unit="ms")
def part1(schematics):
    locks, keys = [], []
    for schematic in schematics:
        if is_lock(schematic):
            locks.append(heights(schematic, "lock"))
        else:
            keys.append(heights(schematic, "key"))

    count = 0
    for lock in locks:
        for key in keys:
            if fits(lock, key):
                count += 1

    return count


def is_lock(schematic):
    return all(schematic[c][0] for c in range(WIDTH))


def heights(schematic, type):
    sizes = [-1] * WIDTH
    for c in range(WIDTH):
        it = range(HEIGHT) if type == "lock" else range(HEIGHT - 1, -1, -1)
        for r in it:
            if schematic[c][r]:
                sizes[c] += 1
            else:
                break

    return sizes


def fits(lock, key):
    return all((lock[c] + key[c]) <= SLOT for c in range(WIDTH))


def load(data):
    schematics = []
    for block in data.split("\n\n"):
        schematic = [[False] * HEIGHT for _ in range(WIDTH)]
        for r, line in enumerate(block.splitlines()):
            for c, cell in enumerate(line):
                schematic[c][r] = cell == FILLED
        schematics.append(schematic)

    return schematics


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=25)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 3508
    puzzle.answer_a = ans1
