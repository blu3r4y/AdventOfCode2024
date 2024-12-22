# Advent of Code 2024, Day 20
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations

START, END, WALL, EMPTY = "S", "E", "#", "."
UP, DOWN, RIGHT, LEFT = -1j, 1j, 1, -1


@print_calls
@print_durations(unit="ms")
def part1(data):
    walls, start, end = data
    return solve(walls, start, end, 2)


@print_calls
@print_durations(unit="ms")
def part2(data):
    walls, start, end = data
    return solve(walls, start, end, 20)


def solve(walls, start, end, max_skip=2, min_gain=100):
    track = build_track(start, end, walls)

    # lookup table to get index within the track
    track_positions = {pos: i for i, pos in enumerate(track)}

    count_cheats = 0
    for i, pos in enumerate(track):
        targets = cheat_positions(pos, walls, max_skip)
        for target in targets:
            if target not in track_positions:
                continue

            # calculate the saved distance if we would cheat
            j = track_positions[target]
            gain = j - i - distance(pos, target)
            if gain >= min_gain:
                count_cheats += 1

    return count_cheats


def build_track(start, end, walls):
    track = [start]

    while track[-1] != end:
        for move in (UP, DOWN, LEFT, RIGHT):
            pos = track[-1] + move

            # don't hit walls or go back
            if pos in walls:
                continue
            if len(track) > 1 and track[-2] == pos:
                continue

            track.append(pos)
            break

    return track


def cheat_positions(pos, walls, size=2):
    targets = set()

    # get all positions that are reachable from the given position, i.e.,
    # all positions that have a manhattan distance smaller or equal to the given size
    for dx in range(size + 1):
        targets.update(pos + LEFT * dx + UP * dy for dy in range(size + 1 - dx))
        targets.update(pos + LEFT * dx + DOWN * dy for dy in range(size + 1 - dx))
        targets.update(pos + RIGHT * dx + UP * dy for dy in range(size + 1 - dx))
        targets.update(pos + RIGHT * dx + DOWN * dy for dy in range(size + 1 - dx))

    targets -= walls
    return targets


def distance(a, b):
    return abs(a.real - b.real) + abs(a.imag - b.imag)


def load(data):
    gridlines = data.splitlines()

    walls, start, end = set(), None, None
    for r, row in enumerate(gridlines):
        for c, cell in enumerate(row):
            pos = complex(c, r)
            if cell == EMPTY:
                continue
            elif cell == START:
                start = pos
            elif cell == END:
                end = pos
            elif cell == WALL:
                walls.add(pos)

    return walls, start, end


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=20)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 1289
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 982425
    puzzle.answer_b = ans2
