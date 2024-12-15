# Advent of Code 2024, Day 15
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations

ROBOT, BOX, WALL, EMPTY = "@", "O", "#", "."
BOX_START, BOX_END = "[", "]"


@print_calls
@print_durations(unit="ms")
def part1(data):
    grid, moves, robot, _ = data
    for move in moves:
        grid, robot = perform_simple_move(grid, robot, move)

    return score_boxes(grid)


def perform_simple_move(grid, oldpos, move):
    pos = oldpos + move
    if grid.get(pos) == WALL:
        return grid, oldpos  # blocked

    # find the last box in the direction of the move
    lastbox = oldpos
    while grid.get(lastbox + move) in (BOX, BOX_START, BOX_END):
        lastbox += move
    if grid.get(lastbox + move) == WALL:
        return grid, oldpos  # cannot push

    # move all boxes
    while lastbox != oldpos:
        grid[lastbox + move] = grid[lastbox]
        del grid[lastbox]
        lastbox -= move

    # move the robot
    grid[pos] = ROBOT
    del grid[oldpos]

    return grid, pos


@print_calls
@print_durations(unit="ms")
def part2(data):
    grid, moves, robot, _ = data
    for move in moves:
        assert move is not None
        grid, robot = perform_complex_move(grid, robot, move)

    return score_boxes(grid)


def perform_complex_move(grid, oldpos, move):
    # use simple logic for horizontal moves
    if abs(move.real) > 0:
        return perform_simple_move(grid, oldpos, move)

    # collect all boxes in the direction of the move, if any
    boxes = collect_boxes(grid, oldpos + move, move)
    if boxes is None:
        return grid, oldpos  # cannot push

    # clear, then move all boxes
    for box in boxes:
        grid[box] = EMPTY
        grid[box + 1] = EMPTY
    for box in boxes:
        grid[box + move] = BOX_START
        grid[box + 1 + move] = BOX_END

    # move the robot
    pos = oldpos + move
    grid[pos] = ROBOT
    del grid[oldpos]

    return grid, pos


def collect_boxes(grid, pos, move, boxes=None):
    boxes = boxes or list()

    # cannot push, invalid end position
    if grid.get(pos) == WALL:
        return None

    # valid end position, return collected boxes, if any
    if grid.get(pos, EMPTY) == EMPTY:
        return boxes

    # touching other boxes, continue collecting
    if grid.get(pos) in (BOX_START, BOX_END):
        if grid.get(pos) == BOX_END:
            pos -= 1

        # collect boxes to the left and right of the current box
        left, right = pos + move, pos + 1 + move
        left_boxes = collect_boxes(grid, left, move, boxes + [pos])
        right_boxes = collect_boxes(grid, right, move, boxes + [pos])

        # cannot push, because at least one path is blocked
        if not left_boxes or not right_boxes:
            return None

        return boxes + left_boxes + right_boxes


def score_boxes(grid):
    score = 0
    for pos, cell in grid.items():
        if cell == BOX or cell == BOX_START:
            score += 100 * int(pos.imag) + int(pos.real)
    return score


def load(data, large=False):
    block_a, block_b = data.split("\n\n")
    block_b = block_b.replace("\n", "")

    if large:  # enlarge the grid for the second part
        block_a = block_a.replace(WALL, WALL + WALL)
        block_a = block_a.replace(BOX, BOX_START + BOX_END)
        block_a = block_a.replace(EMPTY, EMPTY + EMPTY)
        block_a = block_a.replace(ROBOT, ROBOT + EMPTY)

    gridlines = block_a.splitlines()

    grid, robot = dict(), None
    for r, row in enumerate(gridlines):
        for c, cell in enumerate(row):
            pos = complex(c, r)
            if cell == EMPTY:
                continue
            if cell == ROBOT:
                robot = pos
            grid[pos] = cell

    mapping = {"^": -1j, "v": 1j, "<": -1, ">": 1}
    moves = tuple(map(mapping.get, block_b))

    limits = len(gridlines[0]), len(gridlines)
    return grid, moves, robot, limits


def print_grid(grid, limits):
    width, height = limits
    for r in range(height):
        for c in range(width):
            pos = complex(c, r)
            print(grid.get(pos, EMPTY), end="")
        print()


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=15)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 1478649
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data, large=True))
    assert ans2 == 1495455
    puzzle.answer_b = ans2
