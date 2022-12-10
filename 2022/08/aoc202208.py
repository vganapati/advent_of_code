"""AoC 8, 2022."""

# Standard library imports
import pathlib
import sys
import numpy as np

def parse_data(puzzle_input):
    """Parse input."""
    data = puzzle_input.split("\n")
    return([[int(r) for r in row] for row in data])

def part1(data):
    """Solve part 1."""

    data = np.array(data)
    
    visible=0
    visible_mat = np.zeros_like(data)
    for i in range(1,data.shape[0]-1):
        for j in range(1,data.shape[1]-1):
            diff = data-data[i,j]
            bool_mat = np.zeros_like(diff,bool)
            bool_mat[diff<0]=True
            top = np.all(bool_mat[i,0:j])
            bottom = np.all(bool_mat[i,j+1:])
            left = np.all(bool_mat[0:i,j])
            right = np.all(bool_mat[i+1:,j])
            if top or bottom or left or right:
                visible+=1
                visible_mat[i,j]=1      
    
    # border trees
    visible += data.shape[0]*2+data.shape[1]*2 - 4
    
    return(visible)
    
def scenic_score_vector(vec):
    score=1
    for i in vec:
        if i==True:
            score+=1
        else:
            break
    if score>len(vec):
        score-=1
    return(score)

def part2(data):
    """Solve part 2."""
    data = np.array(data)
    scenic_score_mat = np.zeros_like(data)
    
    for i in range(1,data.shape[0]-1):
        for j in range(1,data.shape[1]-1):
            diff = data-data[i,j]
            bool_mat = np.zeros_like(diff,bool)
            bool_mat[diff<0]=True
            top = scenic_score_vector(np.flip(bool_mat[i,0:j]))
            bottom = scenic_score_vector(bool_mat[i,j+1:])
            left = scenic_score_vector(np.flip(bool_mat[0:i,j]))
            right = scenic_score_vector(bool_mat[i+1:,j])
            scenic_score_mat[i,j] = top*bottom*left*right
    
            
    return(np.max(scenic_score_mat))
    


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
