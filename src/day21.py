# Advent of Code 2024, Day 21
# (c) blu3r4y

from functools import cache

import networkx as nx
from aocd.models import Puzzle
from funcy import pairwise, print_calls, print_durations

UP, DOWN, LEFT, RIGHT, ACTION = "^", "v", "<", ">", "A"

ROBO_KEYPAD: nx.Graph = None
DOOR_KEYPAD: nx.Graph = None

ROBO_SHORTEST_PATHS: dict[dict[any, any]] = None
DOOR_SHORTEST_PATHS: dict[dict[any, any]] = None

ROBO_DISTANCES: dict[dict[any, int]] = None
DOOR_DISTANCES: dict[dict[any, int]] = None


@print_calls
@print_durations(unit="ms")
def part1(codes):
    return solve(codes, 2)


@print_calls
@print_durations(unit="ms")
def part2(codes):
    return solve(codes, 25)


def solve(codes, max_depth):
    lengths = []
    for code in codes:
        robo_sequences = indirect_door_keypad((ACTION,) + code)
        shortest_length = dfs(robo_sequences, depth=max_depth)
        lengths.append(shortest_length)

    return compute_complexity(codes, lengths)


@cache
def dfs(sequences, depth=1):
    length = 0
    for seq in sequences:
        # indirect this sequence and get its length (possibly recursively)
        indirect_seqs = indirect_robo_keypad((ACTION,) + seq)
        length += len(indirect_seqs) if depth == 0 else dfs(indirect_seqs, depth - 1)

    return length


def indirect_door_keypad(buttons):
    # return the shortest indirect sequences on the numeric (door) keypad
    seqs = all_indirect_sequences(DOOR_KEYPAD, DOOR_SHORTEST_PATHS, buttons)
    seqs = pick_optimal_paths(seqs)
    return tuple(seqs)


@cache
def indirect_robo_keypad(buttons):
    # return the shortest indirect sequences on the directional (roboter) keypad
    seqs = all_indirect_sequences(ROBO_KEYPAD, ROBO_SHORTEST_PATHS, buttons)
    seqs = pick_optimal_paths(seqs)
    return tuple(seqs)


def all_indirect_sequences(G, shortest_paths, buttons):
    sequences = []

    # sequentially indirect each button press
    for a, b in pairwise(buttons):
        sequence = []
        for path in shortest_paths[a][b]:
            edges = nx.path_graph(path).edges()
            moves = [G.edges[edge]["move"] for edge in edges]

            # end with an ACTION since we need to press the button
            sequence.append(tuple(moves) + (ACTION,))

        # a sequence holds one or more (!) consecutive button presses
        # that all lead to the next button (all of the same length)
        assert all(len(s) == len(sequence[0]) for s in sequence)
        sequences.append(sequence)

    return sequences


def pick_optimal_paths(sequences):
    optimal = []
    for sequence in sequences:
        if len(sequence) == 1:
            optimal.append(sequence[0])
            continue  # only one path

        # add up how far an indirect robot would have to travel to
        # traverse each path in the sequence - then, pick the shortest
        dist = sequence_distance(sequence)
        optimal.append(sequence[dist.index(min(dist))])

    return optimal


def sequence_distance(segment):
    # distance of each path in the segment
    return list(map(path_distance, segment))


def path_distance(buttons):
    distance = 0
    for a, b in pairwise(buttons):
        distance += ROBO_DISTANCES[a][b]

    return distance


def compute_complexity(codes, lengths):
    complexity = 0
    for code, length in zip(codes, lengths):
        codeno = int("".join(map(str, code[:-1])))
        complexity += codeno * length

    return complexity


def make_numeric_keypad():
    # +---+---+---+
    # | 7 | 8 | 9 |
    # +---+---+---+
    # | 4 | 5 | 6 |
    # +---+---+---+
    # | 1 | 2 | 3 |
    # +---+---+---+
    #     | 0 | A |
    #     +---+---+

    G = nx.DiGraph()

    G.add_edge(7, 8, move=RIGHT)
    G.add_edge(7, 4, move=DOWN)

    G.add_edge(8, 7, move=LEFT)
    G.add_edge(8, 9, move=RIGHT)
    G.add_edge(8, 5, move=DOWN)

    G.add_edge(9, 8, move=LEFT)
    G.add_edge(9, 6, move=DOWN)

    G.add_edge(4, 7, move=UP)
    G.add_edge(4, 5, move=RIGHT)
    G.add_edge(4, 1, move=DOWN)

    G.add_edge(5, 8, move=UP)
    G.add_edge(5, 4, move=LEFT)
    G.add_edge(5, 6, move=RIGHT)
    G.add_edge(5, 2, move=DOWN)

    G.add_edge(6, 9, move=UP)
    G.add_edge(6, 5, move=LEFT)
    G.add_edge(6, 3, move=DOWN)

    G.add_edge(1, 4, move=UP)
    G.add_edge(1, 2, move=RIGHT)

    G.add_edge(2, 5, move=UP)
    G.add_edge(2, 1, move=LEFT)
    G.add_edge(2, 3, move=RIGHT)
    G.add_edge(2, 0, move=DOWN)

    G.add_edge(3, 6, move=UP)
    G.add_edge(3, 2, move=LEFT)
    G.add_edge(3, ACTION, move=DOWN)

    G.add_edge(0, 2, move=UP)
    G.add_edge(0, ACTION, move=RIGHT)

    G.add_edge(ACTION, 3, move=UP)
    G.add_edge(ACTION, 0, move=LEFT)

    return G


def make_directional_keypad():
    #     +---+---+
    #     | ^ | A |
    # +---+---+---+
    # | < | v | > |
    # +---+---+---+

    G = nx.DiGraph()

    G.add_edge(UP, ACTION, move=RIGHT)
    G.add_edge(UP, DOWN, move=DOWN)

    G.add_edge(ACTION, UP, move=LEFT)
    G.add_edge(ACTION, RIGHT, move=DOWN)

    G.add_edge(LEFT, DOWN, move=RIGHT)

    G.add_edge(DOWN, UP, move=UP)
    G.add_edge(DOWN, LEFT, move=LEFT)
    G.add_edge(DOWN, RIGHT, move=RIGHT)

    G.add_edge(RIGHT, ACTION, move=UP)
    G.add_edge(RIGHT, DOWN, move=LEFT)

    return G


def init():
    global DOOR_KEYPAD, ROBO_KEYPAD
    DOOR_KEYPAD = make_numeric_keypad()
    ROBO_KEYPAD = make_directional_keypad()

    global DOOR_SHORTEST_PATHS, ROBO_SHORTEST_PATHS
    DOOR_SHORTEST_PATHS = dict(nx.all_pairs_all_shortest_paths(DOOR_KEYPAD))
    ROBO_SHORTEST_PATHS = dict(nx.all_pairs_all_shortest_paths(ROBO_KEYPAD))

    global DOOR_DISTANCES, ROBO_DISTANCES
    DOOR_DISTANCES = dict(nx.all_pairs_shortest_path_length(DOOR_KEYPAD))
    ROBO_DISTANCES = dict(nx.all_pairs_shortest_path_length(ROBO_KEYPAD))


def load(data):
    codes = []
    for line in data.splitlines():
        codes.append(tuple(map(int, line[:-1])) + (ACTION,))
    return codes


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=21)

    init()

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 212488
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 258263972600402
    puzzle.answer_b = ans2
