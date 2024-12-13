# Advent of Code 2024, Day 13
# (c) blu3r4y

from collections import namedtuple
from functools import cache, partial

from aocd.models import Puzzle
from funcy import print_calls, print_durations
from parse import parse
from sympy import Eq, lambdify, solve, symbols

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

    get_n, get_m = generate_solvers()
    for game in games:
        n, m = get_n(game), get_m(game)
        if n is not None and m is not None:
            costs += COST_A * n + COST_B * m

    return costs


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


@cache
def generate_solvers():
    px, py, ax, ay, bx, by, n, m = symbols("px py ax ay bx by n m", integer=True)

    eq = [Eq(px, n * ax + m * bx), Eq(py, n * ay + m * by)]
    sol = solve(eq, (n, m), dict=True, integer=True)
    assert len(sol) == 1

    def _compute(g, fn):
        result = fn(g.prize.x, g.prize.y, g.a.x, g.a.y, g.b.x, g.b.y)
        return int(result) if result.is_integer() and result >= 0 else None

    _lambda_n = lambdify([px, py, ax, ay, bx, by], sol[0][n], modules="math")
    _lambda_m = lambdify([px, py, ax, ay, bx, by], sol[0][m], modules="math")

    # prepare convenience functions to compute n and m for a given game
    _compute_n = partial(_compute, fn=_lambda_n)
    _compute_m = partial(_compute, fn=_lambda_m)
    return _compute_n, _compute_m


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=13)

    # cache the solvers (static, regardless of input)
    generate_solvers()

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 30973
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 95688837203288
    puzzle.answer_b = ans2
