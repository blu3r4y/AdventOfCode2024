# Advent of Code 2024, Day 23
# (c) blu3r4y

import networkx as nx
from aocd.models import Puzzle
from funcy import last, print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(G):
    count = 0

    # cliques are subgraphs with all nodes connected to each other
    # networkx enumerates them all, increasing in size
    for clique in nx.enumerate_all_cliques(G):
        if len(clique) < 3:
            continue
        if len(clique) > 3:
            break
        if not any(n.startswith("t") for n in clique):
            continue

        count += 1

    return count


@print_calls
@print_durations(unit="ms")
def part2(G):
    # the largest clique is the last one in the enumeration
    clique = last(nx.enumerate_all_cliques(G))
    return ",".join(sorted(clique))


def load(data):
    G = nx.Graph()
    for lines in data.splitlines():
        a, b = lines.split("-")
        G.add_edge(a, b)
    return G


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=23)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 1308
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == "bu,fq,fz,pn,rr,st,sv,tr,un,uy,zf,zi,zy"
    puzzle.answer_b = ans2
