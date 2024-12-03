# Advent of Code 2024, Day 3
# (c) blu3r4y

import re

from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(data):
    muls, _, _ = data
    return sum(a * b for a, b in muls.values())


@print_calls
@print_durations(unit="ms")
def part2(data):
    muls, dos, donts = data
    limit = max(muls.keys() | dos | donts)

    result, disabled = 0, False

    for i in range(limit + 1):
        if i in muls:
            if not disabled:
                a, b = muls[i]
                result += a * b
        elif i in dos:
            disabled = False
        elif i in donts:
            disabled = True

    return result


def load(data):
    muls, dos, donts = dict(), set(), set()

    for match in re.compile(r"mul\((\d{1,3}),(\d{1,3})\)").finditer(data):
        muls[match.start(0)] = tuple(map(int, match.groups()))

    for match in re.compile(r"do\(\)").finditer(data):
        dos.add(match.start(0))

    for match in re.compile(r"don't\(\)").finditer(data):
        donts.add(match.start(0))

    return muls, dos, donts


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=3)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 190604937
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 82857512
    puzzle.answer_b = ans2
