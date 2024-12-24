# Advent of Code 2024, Day 24
# (c) blu3r4y

from collections import namedtuple

from aocd.models import Puzzle
from funcy import print_calls, print_durations
from parse import parse

Gate = namedtuple("Gate", "op x y out")


@print_calls
@print_durations(unit="ms")
def part1(data):
    wires, gates = data

    # evaluate output gates
    znames = gate_names(gates, "z")
    values = [eval_gate(z, wires, gates) for z in znames]

    # convert binary list to integer
    binary = "".join(str(z) for z in reversed(values))
    return int(binary, 2)


@print_calls
@print_durations(unit="ms")
def part2(data):
    wires, gates = data

    xnames = wire_names(wires, "x")
    ynames = wire_names(wires, "y")
    *znames, _ = gate_names(gates, "z")  # ignore last output (carry)
    assert len(xnames) == len(ynames) == len(znames)

    # check full adder structure
    errors = set()
    for x, y, z in zip(xnames, ynames, znames):
        errs = check_full_adder(x, y, z, gates, ignore_carry=(x == "x00"))
        errors.update(errs)

    return ",".join(sorted(errors))


def gate_names(gates, prefix):
    return sorted((g for g in gates if g.startswith(prefix)))


def wire_names(wires, prefix):
    return sorted((w for w in wires if w.startswith(prefix)))


def check_full_adder(x, y, z, gates, ignore_carry=False):
    # check structural constraints of a full adder
    # https://en.wikipedia.org/wiki/File:Full-adder_logic_diagram.svg
    #   with A, B = x, y (the inputs)
    #   with C_in, C_out = cin, cout (the carry input and output)
    #   with S = z (the output)

    errors = set()

    # XOR of the first half-adder (assume correctly-wired inputs)
    xor1_x = get_gate(x, "XOR", gates)
    xor1_y = get_gate(y, "XOR", gates)
    assert xor1_x == xor1_y != None, f"input {x} and {y} don't share an XOR gate"
    xor1 = xor1_x

    # AND of the first half-adder (assume correctly-wired inputs)
    and1_x = get_gate(x, "AND", gates)
    and1_y = get_gate(y, "AND", gates)
    assert and1_x == and1_y != None, f"input {x} and {y} don't share an AND gate"
    and1 = and1_x

    # XOR of the second half-adder (via z output)
    xor2z = gates[z]
    if xor2z.op != "XOR":
        errors.add(z)

    # XOR of the second half-adder (via cin, xor1)
    xor2_xor1 = get_gate(xor1.out, "XOR", gates)
    if not ignore_carry and xor2_xor1 is None:
        errors.add(xor1.out)
    if xor2_xor1 is not None and xor2_xor1.out != z:
        errors.add(xor2_xor1.out)

    # AND of the second half-adder (via cin, xor1)
    and2_xor1 = get_gate(xor1.out, "AND", gates)
    if not ignore_carry and and2_xor1 is None:
        errors.add(xor1.out)

    # OR of the two AND gates (via and1)
    or_and1 = get_gate(and1.out, "OR", gates)
    if not ignore_carry and or_and1 is None:
        errors.add(and1.out)

    return errors


def get_gate(name, op, gates):
    result = []
    for g in gates.values():
        if g.op == op and (g.x == name or g.y == name):
            result.append(g)

    assert len(result) <= 1, f"multiple {op} gates with input {name}"
    return result[0] if result else None


def eval_gate(name, wires, gates):
    if name in wires:
        return wires[name]

    # evaluate gate inputs
    g = gates[name]
    x = eval_gate(g.x, wires, gates)
    y = eval_gate(g.y, wires, gates)

    # evaluate gate
    if g.op == "AND":
        return x & y
    elif g.op == "OR":
        return x | y
    elif g.op == "XOR":
        return x ^ y


def load(data):
    a, b = data.split("\n\n")

    wires = dict()
    for line in a.splitlines():
        w, val = line.split(":")
        wires[w] = int(val.strip())

    gates = dict()
    for line in b.splitlines():
        x, op, y, out = parse("{:w} {:w} {:w} -> {:w}", line)
        gates[out] = Gate(op, x, y, out)

    return wires, gates


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=24)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 55920211035878
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == "btb,cmv,mwp,rdg,rmj,z17,z23,z30"
    puzzle.answer_b = ans2
