# Advent of Code 2024, Day 13
# (c) blu3r4y

from collections import namedtuple

from aocd.models import Puzzle
from funcy import print_calls, print_durations
from parse import parse
from sympy import Eq, solve, symbols

COST_A, COST_B = 3, 1
INC = 10000000000000

Point = namedtuple("Point", ["x", "y"])
Game = namedtuple("Game", ["a", "b", "prize"])


@print_calls
@print_durations(unit="ms")
def part1(games):
    return compute_costs(games)


@print_calls
@print_durations(unit="ms")
def part2(games):
    games = [Game(g.a, g.b, Point(g.prize.x + INC, g.prize.y + INC)) for g in games]
    return compute_costs(games)


def compute_costs(games):
    costs = 0

    for game in games:
        if solution := solve_game(game):
            n, m = solution
            costs += COST_A * n + COST_B * m

    return costs


def solve_game(game):
    # n and m are the number of button presses to reach the prize
    n, m = symbols("n m", integer=True, nonnegative=True)

    eq = [
        Eq(game.prize.x, n * game.a.x + m * game.b.x),
        Eq(game.prize.y, n * game.a.y + m * game.b.y),
    ]

    # solve in integer domain
    if sol := solve(eq, (n, m), dict=True, integer=True):
        return int(sol[0][n]), int(sol[0][m])

    return None


def load(data):
    blocks = data.split("\n\n")
    games = []

    for block in blocks:
        a, b, p = block.splitlines()
        ax, ay = parse("Button A: X+{:d}, Y+{:d}", a)
        bx, by = parse("Button B: X+{:d}, Y+{:d}", b)
        px, py = parse("Prize: X={:d}, Y={:d}", p)

        game = Game(Point(ax, ay), Point(bx, by), Point(px, py))
        games.append(game)

    return games


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=13)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 30973
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 95688837203288
    puzzle.answer_b = ans2
