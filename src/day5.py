# Advent of Code 2024, Day 5
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(data):
    rules, books = data

    result = 0
    for pages in books:
        if satisfies(pages, rules):
            result += middle(pages)

    return result


@print_calls
@print_durations(unit="ms")
def part2(data):
    rules, books = data

    incorrect = set()
    for i, pages in enumerate(books):
        while not satisfies(pages, rules):
            incorrect.add(i)
            fixup(pages, rules)

    result = 0
    for i in incorrect:
        result += middle(books[i])

    return result


def satisfies(num, rules):
    for a, b in rules:
        if a not in num or b not in num:
            continue

        apos, bpos = num.index(a), num.index(b)
        if apos > bpos:
            return False

    return True


def middle(num):
    return num[len(num) // 2]


def fixup(num, rules):
    for a, b in rules:
        if a not in num or b not in num:
            continue

        apos, bpos = num.index(a), num.index(b)
        if apos > bpos:
            num[apos], num[bpos] = num[bpos], num[apos]


def load(data):
    rules, books = [], []
    sectiona, sectionb = data.split("\n\n")

    for line in sectiona.splitlines():
        rules.append(tuple(map(int, line.split("|"))))

    for line in sectionb.splitlines():
        books.append(list(map(int, line.split(","))))

    return rules, books


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=5)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 6384
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 5353
    puzzle.answer_b = ans2
