# Advent of Code 2024, Day 16
# (c) blu3r4y

import networkx as nx
from aocd.models import Puzzle
from funcy import print_calls, print_durations

START, END, WALL, EMPTY = "S", "E", "#", "."

NORTH, SOUTH, EAST, WEST = -1j, 1j, 1, -1
TURN_RIGHT, TURN_LEFT = 1j, -1j

STEP_COST, TURN_COST = 1, 1000


@print_calls
@print_durations(unit="ms")
def part1(data):
    walls, start, end, limits = data
    graph = build_graph(walls, limits)

    score, _ = find_best_paths(graph, start, end)
    return score


@print_calls
@print_durations(unit="ms")
def part2(data):
    walls, start, end, limits = data
    graph = build_graph(walls, limits)

    _, paths = find_best_paths(graph, start, end)

    # all unique positions on any best path
    vistas = set()
    for path in paths:
        vistas.update((p for p, _ in path))
    return len(vistas)


def find_best_paths(graph, start, end):
    paths, scores = [], []

    # get all shortest paths, ending in any orientation
    for orient in [NORTH, SOUTH, EAST, WEST]:
        it = nx.all_shortest_paths(graph, (start, EAST), (end, orient), "weight")
        for path in it:
            paths.append(path)
            scores.append(path_score(path))

    best_score = min(scores)
    best_paths = [p for p, s in zip(paths, scores) if s == best_score]
    return best_score, best_paths


def path_score(path):
    score = 0
    for (_, a), (_, b) in zip(path, path[1:]):
        score += STEP_COST if a == b else TURN_COST
    return score


def build_graph(walls, limits):
    width, height = limits

    graph = nx.DiGraph()
    for h in range(height):
        for w in range(width):
            pos = complex(w, h)
            if pos in walls:
                continue

            for orient in [NORTH, SOUTH, EAST, WEST]:
                curr = (pos, orient)

                # allow moving forward in this orientation
                if pos + orient not in walls:
                    graph.add_edge(curr, (pos + orient, orient), weight=STEP_COST)

                # allow turning right or left on the spot
                for turn in [TURN_RIGHT, TURN_LEFT]:
                    graph.add_edge(curr, (pos, orient * turn), weight=TURN_COST)

    return graph


def load(data):
    walls, start, end = set(), None, None

    rows = data.splitlines()
    for r, row in enumerate(rows):
        for c, cell in enumerate(row):
            pos = complex(c, r)
            if cell == START:
                start = pos
            if cell == END:
                end = pos
            if cell == WALL:
                walls.add(pos)

    limits = len(rows[0]), len(rows)
    return walls, start, end, limits


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=16)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 88416
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 442
    puzzle.answer_b = ans2
