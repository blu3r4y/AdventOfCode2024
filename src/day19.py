# Advent of Code 2024, Day 19
# (c) blu3r4y

from functools import cache

from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(data):
    patterns, designs = data

    # can each design be made from the patterns?
    matcher = make_matcher(patterns)
    count = sum(1 for design in designs if matcher(design))

    return count


def make_matcher(patterns):
    @cache
    def matcher(design):
        if not design:
            return True
        for pattern in patterns:
            if design.startswith(pattern):
                if matcher(design[len(pattern) :]):
                    return True
        return False

    return matcher


@print_calls
@print_durations(unit="ms")
def part2(data):
    patterns, designs = data

    # how many options are there to make each design?
    counter = make_counter(patterns)
    count = sum(map(counter, designs))

    return count


def make_counter(patterns):
    @cache
    def counter(design):
        if not design:
            return 1
        count = 0
        for pattern in patterns:
            if design.startswith(pattern):
                count += counter(design[len(pattern) :])
        return count

    return counter


def load(data):
    a, b = data.split("\n\n")
    patterns = a.split(", ")
    designs = b.splitlines()

    return set(patterns), designs


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=19)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 300
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 624802218898092
    puzzle.answer_b = ans2
