# Advent of Code 2024, Day 9
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(data):
    blocks = make_blocks(data)
    move_blocks(blocks)
    return checksum_blocks(blocks)


def make_blocks(data):
    blocks = []

    free, fid = False, 0
    for fsize in data:
        if free:
            blocks.extend([None] * fsize)
        else:
            blocks.extend([fid] * fsize)
            fid += 1
        free = not free

    assert len(blocks) == sum(data)
    return blocks


def move_blocks(data):
    front, back = 0, len(data) - 1
    dst, src = None, None

    while front < back:
        # take first non-empty block from the back
        if src is None:
            if data[back] is not None:
                src = back
            else:
                back -= 1

        # take first empty block from the front
        if dst is None:
            if data[front] is None:
                dst = front
            else:
                front += 1

        # swap blocks if both are found
        if dst is not None and src is not None:
            data[dst], data[src] = data[src], data[dst]
            dst, src = None, None
            back -= 1
            front += 1


def checksum_blocks(data):
    result = 0
    for bid, bsize in enumerate(data):
        if bsize is not None:
            result += bid * bsize

    return result


@print_calls
@print_durations(unit="ms")
def part2(data):
    blocks = make_files(data)
    move_files(blocks)
    return checksum_files(blocks)


def make_files(data):
    blocks = []

    free, fid = False, 0
    for fsize in data:
        if free:
            blocks.append((None, fsize))
        else:
            blocks.append((fid, fsize))
            fid += 1
        free = not free

    return blocks


def move_files(blocks):
    # defragment in order of decreasing file id
    fid = max(fid for fid, _ in blocks if fid is not None)

    while fid > 0:
        # index and size of next file block
        fi, fsize = next((i, size) for i, (k, size) in enumerate(blocks) if k == fid)

        # check for a large enough spot from left to right
        for ei, (eid, esize) in enumerate(blocks):
            if eid is not None:
                continue  # not a free block
            if ei > fi:
                break  # don't move blocks to the right

            if esize >= fsize:
                blocks[fi] = (None, fsize)  # old
                blocks[ei] = (fid, fsize)  # new
                if esize - fsize > 0:
                    blocks.insert(ei + 1, (None, esize - fsize))  # leftover
                break

        fid -= 1


def checksum_files(blocks):
    result = 0

    pos = 0
    for fid, fsize in blocks:
        if fid is not None:
            result += sum(fid * i for i in range(pos, pos + fsize))
        pos += fsize

    return result


def load(data):
    return list(map(int, data.strip()))


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=9)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 6337367222422
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 6361380647183
    puzzle.answer_b = ans2
