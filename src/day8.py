# Advent of Code 2024, Day 8
# (c) blu3r4y

import numpy as np
from aocd.models import Puzzle
from funcy import print_calls, print_durations
from parse import parse


@print_calls
@print_durations(unit="ms")
def part1(data):
    return data


@print_calls
@print_durations(unit="ms")
def part2(data):
    return data


def load(data):
    return data.split("\n")


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=8)

    example1 = """TODO"""

    ex1 = part1(load(example1))
    assert ex1 == -1

    ans1 = part1(load(puzzle.input_data))
    # assert ans1 == -1
    puzzle.answer_a = ans1

    ex2 = part2(load(example1))
    assert ex2 == -1

    ans2 = part2(load(puzzle.input_data))
    # assert ans2 == -1
    puzzle.answer_b = ans2
