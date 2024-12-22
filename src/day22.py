# Advent of Code 2024, Day 22
# (c) blu3r4y

from collections import defaultdict
from functools import cache

from aocd.models import Puzzle
from funcy import collecting, partition, print_calls, print_durations

NUM_SECRETS = 2000
MASK = (1 << 24) - 1


@print_calls
@print_durations(unit="ms")
def part1(seeds):
    result = 0
    for s in seeds:
        result += secret_sequence(s, NUM_SECRETS)[-1]

    return result


@print_calls
@print_durations(unit="ms")
def part2(seeds):
    counts = defaultdict(int)
    for s in seeds:
        # [3, 0, 6, 5, 4, 4, ...]
        digits = one_digits(s, NUM_SECRETS)
        # [-3, 6, -1, -1, 0, ...]
        deltas = difference(digits)
        # {(-3, 6, -1, -1): +1, (6, -1, -1, 0): +2, ...}
        add_banana_counts(deltas, digits, counts)

    return max(counts.values())


def add_banana_counts(deltas, digits, counts):
    visited = set()
    for i, quad in enumerate(partition(4, 1, deltas)):
        quad = tuple(quad)

        # only count the first occurrence
        if quad in visited:
            continue

        counts[quad] += digits[i + 4]
        visited.add(quad)


@collecting
def difference(s):
    for a, b in zip(s, s[1:]):
        yield b - a


def one_digits(s, n=1):
    # only the ones digit of each element in the secret sequence
    return [s % 10 for s in secret_sequence(s, n)]


@cache
@collecting
def secret_sequence(s, n=1):
    yield s
    for _ in range(n):
        s = advance(s)
        yield s


@cache
def advance(s):
    s = ((s << 6) ^ s) & MASK  #  ((s * 64) XOR s) mod 2^24
    s = ((s >> 5) ^ s) & MASK  #  ((s // 32) XOR s) mod 2^24
    s = ((s << 11) ^ s) & MASK  # ((s * 2048) XOR s) mod 2^24
    return s


def load(data):
    return list(map(int, data.splitlines()))


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=22)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 17724064040
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 1998
    puzzle.answer_b = ans2
