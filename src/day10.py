# Advent of Code 2024, Day 10
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(data):
    graph, limits = data
    return solve(graph, limits, distinct_ends=True)


@print_calls
@print_durations(unit="ms")
def part2(data):
    graph, limits = data
    return solve(graph, limits)


def solve(graph, limits, distinct_ends=False):
    num_distinct = 0
    for th in find_trailheads(graph):
        paths = traverse(th, graph, limits)
        if distinct_ends:  # only count end points
            paths = {path[-1] for path in paths}

        num_distinct += len(paths)

    return num_distinct


def find_trailheads(graph):
    return [k for k, v in graph.items() if v == 0]


def traverse(start, graph, limits, paths=0, currpath=None):
    paths = paths or set()
    currpath = (start,) if currpath is None else currpath + (start,)

    # check if we reached the end
    if graph[start] == 9:
        return paths | {currpath}

    # check and branch to neighbors
    curr = graph[start]
    for pos in neighbors(start, limits):
        if graph[pos] != curr + 1:
            continue  # must increment by 1
        paths |= traverse(pos, graph, limits, paths, currpath)

    return paths


def neighbors(pos, limits):
    points = (pos + d for d in [1, -1, 1j, -1j])
    return (p for p in points if 0 <= p.real < limits[1] and 0 <= p.imag < limits[0])


def load(data):
    graph = dict()

    rows = data.splitlines()
    for r, row in enumerate(data.splitlines()):
        for c, cell in enumerate(row):
            graph[complex(c, r)] = int(cell)

    limits = len(rows), len(rows[0])
    return graph, limits


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=10)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 688
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 1459
    puzzle.answer_b = ans2
