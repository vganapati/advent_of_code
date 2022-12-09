"""AoC 6, 2022."""

# Standard library imports
import pathlib
import sys
import numpy as np
import scipy.signal as signal
import itertools

def parse_data(puzzle_input):
    """Parse input."""
    data = [letter for letter in puzzle_input]
    return(data)

def create_filters(filter_length):
    filters = []
    for comb in itertools.combinations(np.arange(filter_length),2):
        filter_0 = np.zeros(filter_length,dtype=np.int32)
        filter_0[comb[0]]=1
        filter_0[comb[1]]=-1
        filters.append(filter_0)
    filters=np.stack(filters)
    return(filters)

def part1(data, filter_length=4):
    """Solve part 1."""
    filters = create_filters(filter_length)
    data = np.array([ord(letter) for letter in data])
    filtered_data = np.array([signal.convolve(data,filters[i],mode='valid') for i in range(len(filters))])
    filtered_data_bool = np.any(1-filtered_data.astype(bool),axis=0) # find the first place with a distinct 4 character string
    ind = np.nonzero(filtered_data_bool==False)[0][0]
    ind += len(filters[0])
    return(ind)

def part2(data, filter_length=14):
    """Solve part 2."""
    return(part1(data, filter_length=filter_length))

    


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
