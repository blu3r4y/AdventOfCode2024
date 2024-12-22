# Advent of Code 2024, Day 22
# (c) blu3r4y

from collections import defaultdict
from functools import cache

from aocd.models import Puzzle
from funcy import collecting, partition, print_calls, print_durations
from tqdm.auto import tqdm

NUM_SECRETS = 2000


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

    for s in tqdm(seeds):
        # [3, 0, 6, 5, 4, 4, ...]
        ones = one_digits(s, NUM_SECRETS)
        # [-3, 6, -1, -1, 0, ...]
        deltas = difference(ones)
        # {(-3, 6, -1, -1), (6, -1, -1, 0), ...}
        quadruples = delta_quadruples(deltas)

        # {(-3, 6, -1, -1): 1, (6, -1, -1, 0): 2, ...}
        add_banana_counts(quadruples, deltas, ones, counts)

    return max(counts.values())


def add_banana_counts(sequences, deltas, ones, counts):
    for seq in sequences:
        if (idx := find(deltas, seq)) is not None:
            counts[seq] += ones[idx + 4]


def find(haystack: list[int], needle: tuple[int, int, int, int]) -> int | None:
    # find the first index of the needle in the haystack
    for i in range(len(haystack) - 3):
        if tuple(haystack[i : i + 4]) == needle:
            return i


@collecting
def difference(s):
    for a, b in zip(s, s[1:]):
        yield b - a


def delta_quadruples(nums, size=4):
    return set(map(tuple, partition(size, 1, nums)))


@cache
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
    MASK = (1 << 24) - 1
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
