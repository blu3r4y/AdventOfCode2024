# Advent of Code 2024, Day 8
# (c) blu3r4y

from itertools import combinations

from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(data):
    antennas, limits = data
    return solve(antennas, limits)


@print_calls
@print_durations(unit="ms")
def part2(data):
    antennas, limits = data
    return solve(antennas, limits, harmonics=True)


def solve(antennas, limits, harmonics=False):
    antinodes = set()

    for antenna in set(antennas.values()):
        locs = [pos for pos, a in antennas.items() if a == antenna]

        if harmonics:
            # each antenna is an antinode then
            antinodes.update(locs)

        for a, b in combinations(locs, 2):
            dist = b - a

            while within_bounds(a := a - dist, limits):
                antinodes.add(a)
                if not harmonics:
                    break  # once per pair

            while within_bounds(b := b + dist, limits):
                antinodes.add(b)
                if not harmonics:
                    break  # once per pair

    return len(antinodes)


def within_bounds(pos, limits):
    return 0 <= pos.real < limits[1] and 0 <= pos.imag < limits[0]


def load(data):
    antennas = dict()

    rows = data.splitlines()
    for r, row in enumerate(data.splitlines()):
        for c, cell in enumerate(row):
            pos = complex(c, r)
            if cell != ".":
                antennas[pos] = cell

    limits = len(rows), len(rows[0])
    return antennas, limits


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=8)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 289
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 1030
    puzzle.answer_b = ans2
