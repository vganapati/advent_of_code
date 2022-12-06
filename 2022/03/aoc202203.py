"""AoC 3, 2022."""

# Standard library imports
import pathlib
import sys
import numpy as np

def parse_data(puzzle_input):
    """Parse input."""
    all_rucksacks = puzzle_input.split("\n")
    return [[item for item in items_per_rucksack] for items_per_rucksack in all_rucksacks]

def ord_to_priority(letter):
    '''
    ord('A') == 65
    ord('Z') == 90
    
    ord('a') == 97
    ord('z') == 122
    '''
    if ord(letter)<91: # capital letter
        return(ord(letter)-38)
    else: # lowercase letter
        return(ord(letter)-96)
      
    

def part1(data):
    """Solve part 1."""
    
    # split each rucksack into 2 compartments
    data = [np.array_split(rucksack,2) for rucksack in data]

    # find the item that is the same in both rucksack
    data = [np.intersect1d(compartments[0],compartments[1]) for compartments in data]
    
    '''
    Find the priorities for each of the common items:
    Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52.
    '''
    return np.sum([ord_to_priority(i[0][0]) for i in data])
    
    
def part2(data):
    """Solve part 2."""
    
    # indices corresponding to groups of 3
    inds = np.arange(0,len(data),3)
    data = [np.intersect1d(np.intersect1d(data[ind],data[ind+1]),data[ind+2]) for ind in inds]
    
    return np.sum([ord_to_priority(i[0][0]) for i in data])


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
