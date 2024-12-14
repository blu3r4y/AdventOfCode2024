# Advent of Code 2024, Day 14
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import count, print_calls, print_durations
from parse import parse


@print_calls
@print_durations(unit="ms")
def part1(robots, w=101, h=103):
    for _ in range(100):
        robots = move(robots, w, h)

    q1, q2, q3, q4 = count_quadrants(robots, w, h)
    return q1 * q2 * q3 * q4


def move(robots, w, h):
    for i, (pos, vel) in enumerate(robots):
        pos = wrap(pos + vel, w, h)
        robots[i] = (pos, vel)
    return robots


def wrap(pos, w, h):
    return complex(pos.real % w, pos.imag % h)


def count_quadrants(robots, w, h):
    midx, midy = w // 2, h // 2

    q1, q2, q3, q4 = 0, 0, 0, 0
    for pos, _ in robots:
        if pos.real < midx and pos.imag < midy:
            q1 += 1
        elif pos.real > midx and pos.imag < midy:
            q2 += 1
        elif pos.real < midx and pos.imag > midy:
            q3 += 1
        elif pos.real > midx and pos.imag > midy:
            q4 += 1

    return q1, q2, q3, q4


@print_calls
@print_durations(unit="ms")
def part2(robots, w=101, h=103):
    for i in count(1):
        robots = move(robots, w, h)
        if tree_heuristic(robots, w, h):
            return i


def tree_heuristic(robots, w, h):
    grid = make_grid(robots, w, h)

    # find the maximum number of consecutive robots for each column
    # so that we can identify long vertical lines of robots
    maxspans = []
    for y in range(h):
        spans = [0]
        for x in range(w):
            if grid[y][x] > 0:
                spans[-1] += 1
            else:
                spans.append(0)

        maxspans.append(max(spans))

    # heuristic to find at least 3 vertical lines (each larger than 5)
    # to hopefully identify a christmas tree, made up of long vertical lines
    return sum(1 for s in maxspans if s >= 5) >= 3


def make_grid(robots, w, h):
    grid = [[0] * w for _ in range(h)]
    for pos, _ in robots:
        grid[int(pos.imag)][int(pos.real)] += 1
    return grid


def load(data):
    robots = []
    for line in data.splitlines():
        p, v = parse("p={} v={}", line)
        px, py = map(int, p.split(","))
        vx, vy = map(int, v.split(","))
        robots.append(((px + py * 1j), (vx + vy * 1j)))
    return robots


def print_grid(robots, w, h):
    grid = make_grid(robots, w, h)

    lines = []
    for row in grid:
        lines.append("".join("#" if num > 0 else "." for num in row))
    image = "\n".join(lines)

    print(image)


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=14)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 224554908
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 6644
    puzzle.answer_b = ans2
