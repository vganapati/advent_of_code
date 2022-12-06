"""AoC 4, 2022."""

# Standard library imports
import pathlib
import sys

def parse_data(puzzle_input):
    """Parse input."""
    all_pairs = puzzle_input.split("\n")
    return [[[int(item) for item in elf.split("-")] for elf in pair.split(",")] for pair in all_pairs]

def part1(data):
    """Solve part 1."""
    count=0
    for pair in data:
        elf_0 = pair[0]
        elf_1 = pair[1]

        if (elf_0[0]==elf_1[0]) or (elf_0[1]==elf_1[1]):
            # print('same start or end index')
            count+=1
        elif (elf_0[0]<elf_1[0]):
            if elf_1[1]<elf_0[1]:
                # print('second is enclosed in first')
                count+=1
        else:
          if elf_0[1]<elf_1[1]:
              # print('first is enclosed in second')
            count+=1
            
    return count
        
    

def part2(data):
    """Solve part 2."""
    total_pairs = len(data)
    count=0 # no overlap at all
    for pair in data:
        elf_0 = pair[0]
        elf_1 = pair[1]
        if (elf_0[0]>elf_1[1]) or (elf_1[0]>elf_0[1]):
            count+=1
    return(total_pairs-count)
            


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
