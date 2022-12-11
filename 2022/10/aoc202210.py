"""AoC 10, 2022."""

# Standard library imports
import pathlib
import sys
import numpy as np
import matplotlib.pyplot as plt

def parse_data(puzzle_input):
    """Parse input."""
    data = puzzle_input.split("\n")
    return(data)

def get_register_values(data):
    
    register_values = []
    
    cycle = 0
    register = 1
        
    for line in range(len(data)):
        
        instruction = data[line]
        if instruction == 'noop':
            cycle += 1
            register_values.append([cycle,register])
        else:
            cycle += 1
            register_values.append([cycle,register])
            cycle += 1
            register_values.append([cycle,register])
            value = int(data[line].split(" ")[1])
            register += value

    return(register_values)

def part1(data):
    """Solve part 1."""
    register_values = get_register_values(data)
    register_values_trimmed = np.array(register_values)[19::40,:]
    return(np.sum(register_values_trimmed[:,0]*register_values_trimmed[:,1]))
    


def part2(data):
    """Solve part 2."""
    register_values = np.array(get_register_values(data))

    sprites = np.zeros([40,len(register_values)],dtype=np.int32)
    sprites[register_values[:,1][(register_values[:,1]<=39) & (register_values[:,1]>=0)],register_values[:,0][(register_values[:,1]<=39) & (register_values[:,1]>=0)]-1]=1
    sprites[register_values[:,1][(register_values[:,1]<=40) & (register_values[:,1]>=1)]-1,register_values[:,0][(register_values[:,1]<=40) & (register_values[:,1]>=1)]-1]=1
    sprites[register_values[:,1][(register_values[:,1]<=38) & (register_values[:,1]>=-1)]+1,register_values[:,0][(register_values[:,1]<=38) & (register_values[:,1]>=-1)]-1]=1

    crt = sprites[(register_values[:,0]-1)%40,register_values[:,0]-1]
    crt = np.reshape(crt,[len(register_values)//40,40])
    plt.figure()
    plt.imshow(crt)
    plt.show()
    return(crt.tolist())

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
