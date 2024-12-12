# Advent of Code 2024

My solutions for the [AoC 2024](https://adventofcode.com/2024) challenges, written in Python.

🎄 🎄 🎄

## Puzzles

| Day | 🧩 Puzzle                                                        | 🐍 Solution              | ⏳ Duration A | ⏳ Duration B |
| --: | :--------------------------------------------------------------- | :----------------------- | ------------: | ------------: |
|   1 | **[Historian Hysteria](https://adventofcode.com/2024/day/1)**    | [day1.py](src/day1.py)   |             - |             - |
|   2 | **[Red-Nosed Reports](https://adventofcode.com/2024/day/2)**     | [day2.py](src/day2.py)   |             - |             - |
|   3 | **[Mull It Over](https://adventofcode.com/2024/day/3)**          | [day3.py](src/day3.py)   |             - |             - |
|   4 | **[Ceres Search](https://adventofcode.com/2024/day/4)**          | [day4.py](src/day4.py)   |         13 ms |         59 ms |
|   5 | **[Print Queue](https://adventofcode.com/2024/day/5)**           | [day5.py](src/day5.py)   |         14 ms |         62 ms |
|   6 | **[Guard Gallivant](https://adventofcode.com/2024/day/6)**       | [day6.py](src/day6.py)   |             - |     39.193 ms |
|   7 | **[Bridge Repair](https://adventofcode.com/2024/day/7)**         | [day7.py](src/day7.py)   |        119 ms |     12.479 ms |
|   8 | **[Resonant Collinearity](https://adventofcode.com/2024/day/8)** | [day8.py](src/day8.py)   |             - |             - |
|   9 | **[Disk Fragmenter](https://adventofcode.com/2024/day/9)**       | [day9.py](src/day9.py)   |             - |      4.989 ms |
|  10 | **[Hoof It](https://adventofcode.com/2024/day/10)**              | [day10.py](src/day10.py) |         12 ms |         12 ms |
|  11 | **[Plutonian Pebbles](https://adventofcode.com/2024/day/11)**    | [day11.py](src/day11.py) |             - |         84 ms |
|  12 | **[Garden Groups](https://adventofcode.com/2024/day/12)**        | [day12.py](src/day12.py) |        135 ms |        230 ms |

Timings are measured on my computer in a non-scientific way.
Empty durations indicate a runtime of less than ten milliseconds.
Bold durations indicate a runtime of more than one minute.

## Requirements

### Python 3.13

Package requirements are specified in the **[requirements.txt](requirements.txt)** file.

```sh
pip install -r requirements.txt
```

You should install the pre-commit hooks and its dependencies to format the code before committing.

```sh
pip install pre-commit ruff
pre-commit install
```
