# Advent of Code 2024, Day 2
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(data):
    safe = 0

    for vals in data:
        if is_save(vals):
            safe += 1

    return safe


@print_calls
@print_durations(unit="ms")
def part2(data):
    safe = 0

    for vals in data:
        dampened = (drop_level(vals, i) for i in range(len(vals)))
        if is_save(vals) or any(is_save(d) for d in dampened):
            safe += 1

    return safe


def is_save(vals):
    diffs = [b - a for a, b in zip(vals, vals[1:])]
    inc = all(1 <= d <= 3 for d in diffs)
    dec = all(1 <= -d <= 3 for d in diffs)
    return inc or dec


def drop_level(vals, i):
    return vals[:i] + vals[i + 1 :]


def load(data):
    pairs = []
    for line in data.splitlines():
        nums = map(int, line.split())
        pairs.append((*nums,))
    return pairs


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=2)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 516
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 561
    puzzle.answer_b = ans2
