"""AoC 12, 2022."""

# Standard library imports
import pathlib
import sys
import numpy as np

def parse_data(puzzle_input):
    """Parse input."""
    data = [[l for l in line] for line in puzzle_input.split("\n")]
    return(data)

def check_in_bounds(data_row, data_col, ind):
    in_bounds=True
    if ind[0]<0 or ind[0]>=data_row:
        in_bounds=False
    if ind[1]<0 or ind[1]>=data_col:
        in_bounds=False
    return(in_bounds)

def get_neighbor_value(data,neighbor_ind):
    flag=False
    if data[neighbor_ind[0],neighbor_ind[1]] == 'E':
        neighbor_val = ord('z')
        flag=True
    elif data[neighbor_ind[0],neighbor_ind[1]] == 'S':
        neighbor_val = ord('a')
    else:
        neighbor_val = ord(data[neighbor_ind[0],neighbor_ind[1]])
    return(neighbor_val, flag)
    
def part1(data):
    """Solve part 1."""
    data = np.array(data)
    visited = np.zeros_like(data, bool)
    start_ind = np.argwhere(data=='S')[0]
    paths = [[start_ind]]
    
    visited[start_ind[0], start_ind[1]] = True
    data_row, data_col = data.shape
    found_end=False
    while found_end==False:
        new_paths = []
        for path in paths:
            current_ind = path[-1]
                
            current_val = data[current_ind[0],current_ind[1]]
            if current_val == 'S':
                current_val = 'a'


            right_ind = current_ind + [0,1]
            if check_in_bounds(data_row, data_col, right_ind):
                if visited[right_ind[0],right_ind[1]] == False:
                    right_value, flag = get_neighbor_value(data,right_ind)
                    if right_value <= (ord(current_val)+1):
                        visited[right_ind[0],right_ind[1]]=True
                        new_paths.append(path + [right_ind])
                        if flag:
                            found_end=True
            if found_end:
                break
            

            left_ind = current_ind + [0,-1]
            if check_in_bounds(data_row, data_col, left_ind):
                if visited[left_ind[0],left_ind[1]] == False:
                    left_value, flag = get_neighbor_value(data,left_ind)
                    if left_value <= (ord(current_val)+1):
                        visited[left_ind[0],left_ind[1]]=True
                        new_paths.append(path + [left_ind])
                        if flag:
                            found_end=True
            if found_end:
                break
            
            top_ind = current_ind + [-1,0]
            if check_in_bounds(data_row, data_col, top_ind):
                if visited[top_ind[0],top_ind[1]] == False:
                    top_value, flag = get_neighbor_value(data,top_ind)
                    if top_value <= (ord(current_val)+1):
                        visited[top_ind[0],top_ind[1]]=True
                        new_paths.append(path + [top_ind])
                        if flag:
                            found_end=True
            if found_end:
                break
            
            bottom_ind = current_ind + [1,0]
            if check_in_bounds(data_row, data_col, bottom_ind):
                if visited[bottom_ind[0],bottom_ind[1]] == False:  
                    bottom_value, flag = get_neighbor_value(data,bottom_ind)
                    if bottom_value <= (ord(current_val)+1):
                        visited[bottom_ind[0],bottom_ind[1]]=True
                        new_paths.append(path + [bottom_ind])
                        if flag:
                            found_end=True
            if found_end:
                break
         
        paths = new_paths
    shortest_path = len(paths[-1])-1
    return(shortest_path)
         
def part2(data):
    """Solve part 2."""
    start_ind = np.argwhere(np.array(data)=='S')[0]
    data[start_ind[0]][start_ind[1]]='a'  
    end_ind = np.argwhere(np.array(data)=='E')[0]
    data[end_ind[0]][end_ind[1]] = 'z'
    alpha_dict = {}
    for i in range(26):
        alpha_dict[chr(i+97)]=chr(122-i) 
        
    # switch letters
    data = [[alpha_dict[i] for i in d] for d in data]
    data = np.array(data)


    data[end_ind[0]][end_ind[1]] = 'S'
    data[data=='z']='E'
    return(part1(data))


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
    yield part1(data)
    data = parse_data(puzzle_input)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
