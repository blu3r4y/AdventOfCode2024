# Advent of Code 2024, Day 18
# (c) blu3r4y

from queue import PriorityQueue

from aocd.models import Puzzle
from funcy import print_calls, print_durations
from tqdm.auto import tqdm


@print_calls
@print_durations(unit="ms")
def part1(data, length=1024):
    coords, bounds = data

    walls = set(coords[:length])
    return astar_search(walls, 0, bounds, bounds)


@print_calls
@print_durations(unit="ms")
def part2(data):
    coords, bounds = data

    walls = set()
    for xy in tqdm(coords):
        if xy in walls:
            continue
        walls.add(xy)

        # check at what point the goal is not reachable anymore
        path = astar_search(walls, 0, bounds, bounds)
        if not path:
            return f"{int(xy.real)},{int(xy.imag)}"


def astar_search(walls, start, goal, bounds):
    closed = {start: 0}
    openpq = PriorityQueue()

    tiebreaker = 0
    openpq.put((0, tiebreaker, start))
    tiebreaker += 1

    while not openpq.empty():
        total_steps, _, current = openpq.get()
        if current == goal:
            return total_steps

        for succ in successor_states(current, walls, bounds):
            new_steps = closed[current] + 1
            if succ not in closed or new_steps < closed[succ]:
                closed[succ] = new_steps
                estimate = new_steps + manhattan_distance(succ, goal)
                openpq.put((estimate, tiebreaker, succ))
                tiebreaker += 1


def successor_states(pos, walls, bounds):
    for nxt in (pos + step for step in (1, 1j, -1, -1j)):
        if within_bounds(nxt, bounds) and nxt not in walls:
            yield nxt


def within_bounds(pos, bounds):
    return 0 <= pos.real <= bounds.real and 0 <= pos.imag <= bounds.imag


def manhattan_distance(a, b) -> int:
    return int(abs(a.imag - b.imag) + abs(a.real - b.real))


def load(data):
    coords, width, height = [], 0, 0

    for line in data.split("\n"):
        x, y = map(int, line.split(","))
        coords.append(complex(x, y))
        if x > width:
            width = x
        if y > height:
            height = y

    bounds = complex(width, height)
    return coords, bounds


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=18)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 326
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == "18,62"
    puzzle.answer_b = ans2
