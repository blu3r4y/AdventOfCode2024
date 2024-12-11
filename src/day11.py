# Advent of Code 2024, Day 11
# (c) blu3r4y

from functools import cache

from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(stones):
    return sum(blink(stone, n=25) for stone in stones)


@print_calls
@print_durations(unit="ms")
def part2(stones):
    return sum(blink(stone, n=75) for stone in stones)


@cache
def blink(stone, n=1):
    if n == 0:
        return 1

    result = transform(stone)
    if isinstance(result, tuple):
        a, b = result
        return blink(a, n - 1) + blink(b, n - 1)

    return blink(result, n - 1)


@cache
def transform(stone):
    if stone == 0:
        return 1

    text = str(stone)
    if len(text) % 2 == 0:
        left = int(text[: len(text) // 2])
        right = int(text[len(text) // 2 :])
        return left, right

    return stone * 2024


def load(data):
    return tuple(map(int, data.strip().split()))


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=11)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 183435
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 218279375708592
    puzzle.answer_b = ans2
