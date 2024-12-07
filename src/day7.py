# Advent of Code 2024, Day 7
# (c) blu3r4y

from itertools import product
from operator import add, mul

from aocd.models import Puzzle
from funcy import print_calls, print_durations
from parse import parse


@print_calls
@print_durations(unit="ms")
def part1(equations):
    operations = [add, mul]
    return solve(equations, operations)


@print_calls
@print_durations(unit="ms")
def part2(equations):
    operations = [add, mul, concat]
    return solve(equations, operations)


def solve(equations, operations):
    total = 0
    for lval, rvals in equations:
        if (res := evaluate(lval, rvals, operations)) is not None:
            total += res

    return total


def evaluate(lval, rvals, ops):
    # test all possible combinations of operator functions
    for ops in product(ops, repeat=len(rvals) - 1):
        result = rvals[0]
        for i, op in enumerate(ops):
            result = op(result, rvals[i + 1])
        if result == lval:
            return lval

    return None


def concat(a, b):
    return int(f"{a}{b}")


def load(data):
    equations = []
    for line in data.split("\n"):
        lval, rvals = parse("{:d}: {}", line)
        rvals = tuple(map(int, rvals.split()))
        equations.append((lval, rvals))

    return equations


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=7)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 1582598718861
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 165278151522644
    puzzle.answer_b = ans2
