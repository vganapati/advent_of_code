"""AoC 17, 2022."""

# Standard library imports
import pathlib
import sys
import numpy as np
import matplotlib.pyplot as plt


def parse_data(puzzle_input):
    """Parse input."""
    data = [p for p in puzzle_input]
    return(data)

def check_blocked(rock_structure, block_top_corner_new,block):
    blocked = np.any(rock_structure[block_top_corner_new[0]:block_top_corner_new[0]+block.shape[0],
                                    block_top_corner_new[1]:block_top_corner_new[1]+block.shape[1]])
    return(blocked)

def move(block,block_top_corner,rock_structure, movement='down'):
    if movement=='down':
        block_top_corner_new = block_top_corner + np.array([1,0])
    elif movement=='right':
        block_top_corner_new = block_top_corner + np.array([0,1])
    elif movement=='left':
        block_top_corner_new = block_top_corner + np.array([0,-1])
    
    if np.any(block_top_corner_new<0):
        blocked=True
    else:
        shape_0 = rock_structure[block_top_corner_new[0]:block_top_corner_new[0]+block.shape[0],
                                        block_top_corner_new[1]:block_top_corner_new[1]+block.shape[1]].shape
        if shape_0 == block.shape:
            blocked = np.any(rock_structure[block_top_corner_new[0]:block_top_corner_new[0]+block.shape[0],
                                            block_top_corner_new[1]:block_top_corner_new[1]+block.shape[1]] * block)
        else:
            blocked = True
    if not(blocked):
        block_top_corner = block_top_corner_new
    return(blocked, block_top_corner)


def single_fall(rock_structure, blocks, block_ind, jet_pattern, jet_ind):
    block = blocks[block_ind%len(blocks)]
    block_height = block.shape[0]
    rock_structure = np.concatenate((np.zeros([block_height+3,rock_structure.shape[1]],dtype=bool),rock_structure),axis=0)
    block_top_corner = np.array([0,2])
    done=False

    count = 0
    while not(done):
        if count%2==0:
            if jet_pattern[jet_ind%len(jet_pattern)]=='>':
                movement='right'
            elif jet_pattern[jet_ind%len(jet_pattern)]=='<':
                movement='left'
            jet_ind += 1
        else:
            movement='down'
            
        blocked, block_top_corner = move(block,block_top_corner,rock_structure,movement=movement)
        if (movement == 'down') and blocked:
            done=True
        count += 1

    rock_structure[block_top_corner[0]:block_top_corner[0]+block.shape[0],
                   block_top_corner[1]:block_top_corner[1]+block.shape[1]] = rock_structure[block_top_corner[0]:block_top_corner[0]+block.shape[0],
                                  block_top_corner[1]:block_top_corner[1]+block.shape[1]] + block
    
    # remove blank rows
    first_nonzero_ind=np.argmax(np.sum(rock_structure,axis=1)>0)
    rock_structure = rock_structure[first_nonzero_ind:,:]
    
    block_top_corner = block_top_corner+np.array([first_nonzero_ind,0])
    return(rock_structure, jet_ind, block_top_corner)
    
def part1(jet_pattern, num_steps=2022):
    """Solve part 1."""
    
    block_0 = np.array([[1,1,1,1]],dtype=bool)

    block_1 = np.array([[0,1,0],
                        [1,1,1],
                        [0,1,0]],dtype=bool)

    block_2 = np.array([[0,0,1],
                        [0,0,1],
                        [1,1,1]],dtype=bool)

    block_3 = np.array([[1],
                        [1],
                        [1],
                        [1]],dtype=bool)

    block_4 = np.array([[1,1],
                        [1,1]],dtype=bool)


    blocks=[block_0,block_1,block_2,block_3,block_4]
    
    jet_ind = 0
    rock_structure = np.array([[1,1,1,1,1,1,1]], dtype=bool)
    
    for block_ind in range(num_steps):
        rock_structure, jet_ind, _ = single_fall(rock_structure, blocks, block_ind, jet_pattern, jet_ind)
        
    max_height = rock_structure.shape[0]-1
    return(int(max_height))
        


def part2(jet_pattern, num_steps=1000000000000):
    
    """Solve part 2."""
    block_0 = np.array([[1,1,1,1]],dtype=bool)

    block_1 = np.array([[0,1,0],
                        [1,1,1],
                        [0,1,0]],dtype=bool)

    block_2 = np.array([[0,0,1],
                        [0,0,1],
                        [1,1,1]],dtype=bool)

    block_3 = np.array([[1],
                        [1],
                        [1],
                        [1]],dtype=bool)

    block_4 = np.array([[1,1],
                        [1,1]],dtype=bool)


    blocks=[block_0,block_1,block_2,block_3,block_4]
    
    jet_ind = 0
    rock_structure = np.array([[1,1,1,1,1,1,1]], dtype=bool)
    jet_ind_vec = [jet_ind%len(jet_pattern)]
    block_ind_vec = [0%len(blocks)]
    top_of_structure_current = np.zeros_like(rock_structure[0])
    removed_rows = 0
    top_of_structure_vec = np.expand_dims(top_of_structure_current, axis=1)
    height_vec = [0]
    flag = True
    done = False
    block_ind = 0
    
    while not(done):
        
        rock_structure, jet_ind, block_top_corner = single_fall(rock_structure, blocks, block_ind, jet_pattern, jet_ind)
        top_of_structure_current = np.argmax(rock_structure,axis=0)
        remove_rows_i = rock_structure.shape[0] - np.max(top_of_structure_current)-1
        rock_structure = rock_structure[0:np.max(top_of_structure_current)+1]
        removed_rows += remove_rows_i
        
        
        row_matches = np.abs(np.sum(top_of_structure_vec-np.expand_dims(top_of_structure_current,axis=1),axis=0))
        
        row_inds = row_matches == 0
        jet_inds = np.array(jet_ind_vec)[row_inds]==jet_ind%len(jet_pattern)
        matches = np.array(block_ind_vec)[row_inds][jet_inds] == (block_ind+1)%len(blocks)
        
        # print(block_ind)
        # print(np.any(row_inds))
        # print()
        
        height_vec.append(removed_rows + rock_structure.shape[0]-1)
        
        if np.any(matches) and flag:
            # print('Found repeating loop')
            match_ind = np.arange(0,block_ind+1)[row_inds][jet_inds][matches]
            loop_length = block_ind+1 - match_ind
            num_loops =  (num_steps - match_ind - 1)//loop_length - 1
            height_from_loops = num_loops*(height_vec[block_ind+1] - height_vec[match_ind[0]])
            final_step_ind = num_steps - loop_length*(num_loops) - 1
            flag = False
            
        
        if flag==False and block_ind == final_step_ind[0]:
            done=True
            
        
        
        if block_ind != num_steps-1:
            top_of_structure_vec = np.concatenate((top_of_structure_vec,np.expand_dims(top_of_structure_current, axis=1)),axis=1)
            jet_ind_vec.append(jet_ind%len(jet_pattern))
            block_ind_vec.append((block_ind+1)%len(blocks))
        
        block_ind += 1
            
    max_height = removed_rows + rock_structure.shape[0]-1 + height_from_loops
    return(int(max_height))

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    jet_pattern = parse_data(puzzle_input)
    yield part1(jet_pattern, num_steps=2022)
    yield part2(jet_pattern, num_steps=1000000000000)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
