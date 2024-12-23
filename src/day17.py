# Advent of Code 2024, Day 17
# (c) blu3r4y

import random

from aocd.models import Puzzle
from funcy import count, print_calls, print_durations
from parse import parse


@print_calls
@print_durations(unit="ms")
def part1(data):
    program, a, b, c = data
    result = interpret(program, a, b, c)
    return ",".join(map(str, result))


def interpret(program: list[int], a: int, b: int, c: int) -> list[int]:
    ip, output = 0, []

    while ip < len(program) - 1:
        ins = program[ip]
        lit = program[ip + 1]

        # decipher combo operand
        cmb = None
        if 0 <= lit <= 3:
            cmb = lit
        elif lit == 4:
            cmb = a
        elif lit == 5:
            cmb = b
        elif lit == 6:
            cmb = c

        # execute instruction
        if ins == 0:
            a = a // pow(2, cmb)
        elif ins == 1:
            b = b ^ lit
        elif ins == 2:
            b = cmb % 8
        elif ins == 3:
            if a != 0:
                ip = lit
                continue
        elif ins == 4:
            b = b ^ c
        elif ins == 5:
            output.append(cmb % 8)
        elif ins == 6:
            b = a // pow(2, cmb)
        elif ins == 7:
            c = a // pow(2, cmb)

        ip += 2

    return output


@print_calls
@print_durations(unit="ms")
def part2(data, verbose=True):
    program, _, _, _ = data

    best = None
    for i in count(1):
        print(f"ATTEMPT {i} {f"(with constraint < {best:,d})" if best else ''}")

        # take multiple rounds to find the smallest solution, where,
        # in each round, we punish solutions that are larger than the previous one
        fitness = make_fitness_function(program, best)

        # the first run uses a random population, subsequent runs have a
        # population that is centered around the previous solution
        population = (
            biased_population(best, POPULATION_SIZE)
            if best is not None
            else random_population(POPULATION_SIZE)
        )

        solution = genetic_solver(fitness, population, verbose=verbose)
        if solution is None and best is not None:
            break  # not the first try, so take the previous best

        assert solution is not None
        assert interpret(program, solution, 0, 0) == program
        best = solution

    return best


def random_population(size):
    return [random.randrange(0, 2**64) for _ in range(size)]


def biased_population(center, size):
    return [max(0, center + random.randrange(-(2**16), 2**16)) for _ in range(size)]


# number of individuals in each generation
POPULATION_SIZE = 100
# the rate at which we flip a bit (with higher probability for lower bits)
MINOR_RATE = 0.5
# the rate at which we flip a bit (with equal probability for all bits)
MAJOR_RATE = 0.02
# the strength of the bias towards flipping least significant bits in minor mutations
MINOR_LSB_BIAS = 1.2
# maximum number of generations to run until we give up
MAX_GENERATIONS = 30_000


def genetic_solver(fitness, initial_population, verbose=False):
    population = initial_population
    best, best_score = None, -float("inf")

    g = 0
    while best_score < fitness.optimal_score and g < MAX_GENERATIONS:
        if verbose and g % (MAX_GENERATIONS / 100) == 0:
            print(f"\r{g:6d}: {"":7s}{population[0]:40,d}", end="\r")

        # evaluate fitness and update best solution
        scores = [fitness(a) for a in population]
        for value, score in zip(population, scores):
            if score > best_score:
                best, best_score = value, score
                if verbose:
                    progress = best_score / fitness.optimal_score
                    print(f"{g:6d}: {progress:6.1%} {best:40,d}")

        # re-sample new generation based on fitness
        parents = random.choices(population, weights=scores, k=POPULATION_SIZE)

        # there are two types of mutations:
        # - minor mutations are always applied. they flip individual bits,
        #   but with a bias towards least significant bits to avoid large jumps
        # - major mutations are more likely when the fitness is low. they flip
        #   all bits with equal probability, resulting in more drastic changes
        r = MAJOR_RATE * (1 - (best_score / fitness.optimal_score))
        children = []
        for child in parents:
            child = major_mutation(child, r)
            child = minor_mutation(child, MINOR_RATE)
            children.append(child)

        population = children
        g += 1

    if verbose:
        print()

    if best_score == fitness.optimal_score:
        return best


def minor_mutation(a: int, rate: float) -> int:
    for i in range(a.bit_length()):
        # exponentially higher probability for lower bits
        bit_rate = rate * (1.0 / (MINOR_LSB_BIAS**i))
        if random.random() < bit_rate:
            a ^= 1 << i
    return a


def major_mutation(a: int, rate: float) -> int:
    for i in range(a.bit_length()):
        if random.random() < rate:
            a ^= 1 << i
    return a


def make_fitness_function(program: list[int], threshold: int | None = None) -> callable:
    program_size = len(program)

    def fitness_function(a: int) -> int:
        result = interpret(program, a, 0, 0)

        # special case that punishes results above a certain threshold
        if threshold is not None and a >= threshold:
            return 0.001

        # length mismatches shall lead to very low scores
        result_size = len(result)
        if result_size != program_size:
            return 1 / abs(result_size - program_size)

        # score each digit, left to right, stop on first mismatch
        score = 1
        for x, y in zip(reversed(result), reversed(program)):
            if x != y:
                break
            score += 1

        return score

    optimal_score = float(1 + program_size)
    fitness_function.optimal_score = optimal_score

    return fitness_function


def load(data):
    reg, prog = data.split("\n\n")
    a, b, c = [parse("Register {}: {:d}", line)[1] for line in reg.splitlines()]
    program = list(map(int, parse("Program: {}", prog)[0].split(",")))

    return program, a, b, c


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=17)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == "7,3,5,7,5,7,4,3,0"
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 105734774294938
    puzzle.answer_b = ans2
