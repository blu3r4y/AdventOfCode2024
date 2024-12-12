# Advent of Code 2024, Day 12
# (c) blu3r4y

from collections import Counter, defaultdict

from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(data):
    grid, limits = data
    return solve(grid, limits)


@print_calls
@print_durations(unit="ms")
def part2(data):
    grid, limits = data
    return solve(grid, limits, count_sides=True)


def solve(grid, limits, count_sides=False):
    result = 0

    areas = find_areas(grid, limits)
    for area_list in areas.values():
        for area in area_list:
            perimeter = find_perimeter(area)

            if count_sides:
                sides = get_number_of_sides(perimeter)
                result += len(area) * sides
            else:
                result += len(area) * len(perimeter)

    return result


def find_areas(grid, limits):
    areas = defaultdict(list)
    visited = set()

    def _flood_fill(pos):
        visited.add(pos)
        name = grid[pos]

        neighbors = get_neighbors(pos, grid, limits)
        positions = {pos, *neighbors}

        # try adding to existing area, in reverse order
        # because it was the most recently created area
        for area in reversed(areas[name]):
            if any(p in area for p in positions):
                area.update(positions)
                break

        else:  # create new area
            areas[name].append(positions)

        # recursively fill neighbors
        for n in neighbors:
            if n not in visited:
                _flood_fill(n)

    for pos in grid:
        if pos not in visited:
            _flood_fill(pos)

    # the list of areas, keyed by name
    return areas


def get_neighbors(pos, grid, limits):
    width, height = limits
    name = grid[pos]

    # all neighbors of the same name
    new = (pos + d for d in [1, -1, 1j, -1j])
    new = (p for p in new if 0 <= p.real < width and 0 <= p.imag < height)
    new = (p for p in new if grid[p] == name)
    return list(new)


def find_perimeter(area):
    borders = Counter()
    for pos in area:
        borders.update(get_borders(pos))

    # the perimeter of the entire area is made up unique cell borders,
    # because a unique border can only be at the perimeter of the area
    borders = [e for e, c in borders.items() if c == 1]
    return borders


def get_borders(pos):
    return (pos + d for d in [0.5, -0.5, 0.5j, -0.5j])


def get_number_of_sides(perimeter):
    def is_crossing(p1, p2):
        horizontal = p1.imag == p2.imag
        vertical = p1.real == p2.real
        assert vertical ^ horizontal

        if vertical:  # mirror, to avoid duplicate code
            p1, p2 = flip(p1), flip(p2)

        if p1.real > p2.real:
            p1, p2 = p2, p1

        # calculate two vertical borders from two horizontal borders
        real = p1.real + 0.5
        c1, c2 = complex(real, p1.imag - 0.5), complex(real, p1.imag + 0.5)

        if vertical:  # mirror result
            c1, c2 = flip(c1), flip(c2)

        return c1 in perimeter and c2 in perimeter

    def flip(c):
        return complex(c.imag, c.real)

    sides = 0

    segments = set(perimeter)
    while segments:
        this = segments.pop()

        # horizontal border segments have no fractional part
        horizontal = this.real.is_integer()

        parallel_offsets = [1, -1] if horizontal else [1j, -1j]

        # traverse all neighbors parallel to the current segment,
        # as all of them are part of the same side
        fringe = {this}
        while fringe:
            curr = fringe.pop()
            neighbors = [curr + d for d in parallel_offsets]
            for n in neighbors:
                if is_crossing(curr, n):
                    continue  # crossing points break the side

                if n in segments:
                    fringe.add(n)
                    segments.remove(n)

        sides += 1

    return sides


def load(data):
    grid = dict()

    rows = data.splitlines()
    for r, row in enumerate(data.splitlines()):
        for c, cell in enumerate(row):
            pos = complex(c, r)
            grid[pos] = cell

    limits = len(rows[0]), len(rows)
    return grid, limits


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=12)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 1375574
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 830566
    puzzle.answer_b = ans2
