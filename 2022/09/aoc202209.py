"""AoC 9, 2022."""

# Standard library imports
import pathlib
import sys
import numpy as np

def parse_data(puzzle_input):
    """Parse input."""
    data = puzzle_input.split("\n")
    return([[line.split(" ")[0],int(line.split(" ")[1])] for line in data])

direction_dict={'R':np.array([0,1]),
                'L':np.array([0,-1]),
                'U':np.array([1,0]),
                'D':np.array([-1,0])}

possible_movements_diagonal = np.array([[1,1],
                                        [1,-1],
                                        [-1,1],
                                        [-1,-1]])

possible_movements_up_down = np.array([[0,1],
                                       [0,-1],
                                       [1,0],
                                       [-1,0]])

def check_diagonal(position_head,position_tail):
    diagonal=False
    for move in possible_movements_diagonal:
        if np.all((position_head+move) == position_tail):
            diagonal=True
    return(diagonal)

def check_up_down(position_head,position_tail):
    up_down=False
    for move in possible_movements_up_down:
        if np.all((position_head+move) == position_tail):
            up_down=True
    return(up_down)


def single_step(direction,position_head,position_tail):
    """Follow the leader"""
    position_head_new = position_head + direction_dict[direction]
    if np.all(position_head == position_tail): # overlapping initially
        position_tail_new = position_tail # no change
    elif np.all(position_head_new == position_tail): # becomes overlapping
        position_tail_new = position_tail # no change
    elif np.all(position_head_new == (position_tail+direction_dict[direction]*2)): # behind the head and it moves 1 ahead in that direction
        position_tail_new = position_tail + direction_dict[direction] # same movement as head
    elif check_diagonal(position_head, position_tail): 
        if check_up_down(position_head_new,position_tail): # start diagonal, then head moves next to or overlapping tail
            position_tail_new = position_tail # tail doesn't move
        else: # start diagonal and move away
            # tail moves diagonally to be next to head
            position_tail_new = position_head
    elif check_up_down(position_head,position_tail):
        if check_diagonal(position_head_new,position_tail):
            position_tail_new = position_tail # tail doesn't move

    return(position_head_new, position_tail_new)
    
def move_to_touch(position_head, position_tail):
    # first try diagonal movements
    for move in possible_movements_diagonal:
        position_tail_new = position_tail+move
        if check_up_down(position_head,position_tail_new):
            return(position_tail_new)
    # then try up-down-left-right movements
    for move in possible_movements_up_down:
        position_tail_new = position_tail+move
        if check_up_down(position_head,position_tail_new):
            return(position_tail_new)
        
    # first try diagonal movements
    for move in possible_movements_diagonal:
        position_tail_new = position_tail+move
        if check_diagonal(position_head,position_tail_new):
            return(position_tail_new)
    # then try up-down-left-right movements
    for move in possible_movements_up_down:
        position_tail_new = position_tail+move
        if check_diagonal(position_head,position_tail_new):
            return(position_tail_new)
    
def single_step_follow(position_head_new,position_tail):
    """Follow the knot ahead"""
    if np.all(position_head_new == position_tail): # knots are overlapping
        position_tail_new = position_tail
    elif check_diagonal(position_head_new,position_tail): # knots are touching
        position_tail_new = position_tail
    elif check_up_down(position_head_new, position_tail): # knots are touching
        position_tail_new = position_tail
    else: # knots are no longer touching
        position_tail_new = move_to_touch(position_head_new, position_tail)
    return(position_tail_new)

def max_direction(steps_vec, directions_vec, direction):
    """Maximum movement in a direction"""
    return(1+np.sum(steps_vec[directions_vec==direction]))

def part1(data):
    """Solve part 1."""
    directions_vec = np.array(data)[:,0]
    steps_vec = np.array(data)[:,1].astype(np.int32)
    position_head = np.array([0,0],dtype=np.int32)
    position_tail = np.array([0,0],dtype=np.int32)
    
    # make grid of max dimensions
    max_R = max_direction(steps_vec, directions_vec, 'R')
    max_U = max_direction(steps_vec, directions_vec, 'U')

    visited_grid = np.zeros([max_U,max_R],dtype=bool)
    visited_grid[position_tail[0],position_tail[1]]=True
    for i in range(len(directions_vec)):
        direction = directions_vec[i]
        num_steps = steps_vec[i]
        for j in range(num_steps):
            position_head, position_tail = single_step(direction, position_head,position_tail)
            visited_grid[position_tail[0],position_tail[1]]=True
    # print(visited_grid)
    return(np.sum(visited_grid))

def print_positions(positions, max_U, max_R):
    grid = np.zeros([max_U,max_R],dtype=str)
    grid[:]='.'
    for p in np.flip(np.arange(len(positions))):
        position = positions[p]
        grid[position[0],position[1]]=str(p)
    print(np.flipud(grid))
    
def part2(data, num_knots=9, verbose=False):
    """Solve part 2."""
    directions_vec = np.array(data)[:,0]
    steps_vec = np.array(data)[:,1].astype(np.int32)
    positions=np.array([np.array([0,0],dtype=np.int32) for knot in range(num_knots+1)])
    
    # make grid of max dimensions
    max_R = max_direction(steps_vec, directions_vec, 'R')
    max_U = max_direction(steps_vec, directions_vec, 'U')

    if verbose:
        print_positions(positions, max_U, max_R)
    
    visited_grid = np.zeros([max_U,max_R],dtype=bool)
    visited_grid[positions[-1,0],positions[-1,1]]=True
    
    for i in range(len(directions_vec)):
        direction = directions_vec[i]
        num_steps = steps_vec[i]
        for j in range(num_steps):
            positions_new = np.zeros_like(positions)
            (positions_new[0],positions_new[1]) = single_step(direction, positions[0], positions[1])
            for k in range(2,num_knots+1):
                positions_new[k] = single_step_follow(positions_new[k-1],positions[k]) 
            if verbose:
                print_positions(positions_new, max_U, max_R)
            positions=positions_new
            visited_grid[positions[-1,0],positions[-1,1]]=True
    # print(visited_grid)
    return(np.sum(visited_grid))

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
