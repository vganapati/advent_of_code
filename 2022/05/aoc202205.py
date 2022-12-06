"""AoC 5, 2022."""

# Standard library imports
import pathlib
import sys
import numpy as np
from dataclasses import dataclass

def parse_data(puzzle_input):
    """Parse input."""
    data = puzzle_input.split("\n\n")
    
    stacks = data[0]
    stacks = [[item for item in row] for row in stacks.split("\n")]
    stacks = stacks[:-1] # remove last row, just a numbering row
    stacks = np.fliplr(np.transpose(stacks))
    stacks = stacks[1::4]
    stacks=[stack[stack != ' '].tolist() for stack in stacks]
    
    procedure = data[1]
    procedure = procedure.split("\n")
    procedure = [line.split(" ") for line in procedure]
    procedure = np.array(procedure)
    procedure = procedure[:,1::2]
    procedure = [[int(item) for item in row] for row in procedure]
    
    return [stacks, procedure]

@dataclass
class CrateStack:
    memory: list[list[str]]
    program: list[list[int]]

    def run(self,crane_type=0):
        """Run the program."""
        current_line = 0
        
        while current_line < len(self.program):
            program_line = self.program[current_line]
            num_boxes = program_line[0]
            start_stack = program_line[1]-1 # -1 for 0 indexing
            end_stack = program_line[2]-1 # -1 for 0 indexing
            
            if crane_type==0:
                for i in range(num_boxes):
                    self.memory[end_stack].append(self.memory[start_stack].pop())
            else:
                self.memory[end_stack] = self.memory[end_stack] + self.memory[start_stack][-num_boxes:]
                self.memory[start_stack] = self.memory[start_stack][:-num_boxes]
            current_line+=1
            
            
def part1(data, crane_type=0):
    """Solve part 1."""
    [stacks,procedure]=data
    state_machine = CrateStack(
        stacks, program=procedure
    )
    state_machine.run(crane_type=crane_type)
    new_stacks = state_machine.memory
    top_boxes = [stack[-1] for stack in new_stacks]
    return ''.join(top_boxes)
    

def part2(data):
    """Solve part 2."""
    return part1(data,crane_type=1)


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
    yield part1(data)
    data = parse_data(puzzle_input) # reset to beginning
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
