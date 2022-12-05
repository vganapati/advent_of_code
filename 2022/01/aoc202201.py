"""AoC 1, 2022: Calorie Counting."""

# Standard library imports
import pathlib
import sys
import numpy as np

def parse_data(puzzle_input):
    """Parse input."""
    cal_list_per_elf = puzzle_input.split("\n\n")
    return [[int(cal) for cal in cal_list_single_elf.split("\n")] for cal_list_single_elf in cal_list_per_elf]
    

def part1(data):
    """Solve part 1."""
    return np.max([np.sum(cal_list_single_elf) for cal_list_single_elf in data])


def part2(data):
    """Solve part 2."""
    return np.sum(np.sort([np.sum(cal_list_single_elf) for cal_list_single_elf in data])[-3:])


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))
