# Advent of Code 2024, Day 1
# (c) blu3r4y

from collections import Counter

from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(data):
    left, right = data
    left, right = sorted(left), sorted(right)

    distances = 0
    for l, r in zip(left, right):
        distances += abs(l - r)

    return distances


@print_calls
@print_durations(unit="ms")
def part2(data):
    left, right = data
    counts = Counter(right)

    similarity = 0
    for l in left:
        similarity += l * counts[l]

    return similarity


def load(data):
    pairs = []
    for line in data.splitlines():
        nums = map(int, line.split())
        pairs.append((*nums,))
    return zip(*pairs)


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=1)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 1765812
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 20520794
    puzzle.answer_b = ans2
