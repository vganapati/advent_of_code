"""AoC 14, 2022."""

# Standard library imports
import pathlib
import sys
import numpy as np
import matplotlib.pyplot as plt

def parse_data(puzzle_input):
    """Parse input."""
    rock_paths = puzzle_input.split("\n")
    all_points = []
    for ii,path in enumerate(rock_paths):
        points = path.split(" -> ")
        points = [[point.split(",")[0], point.split(",")[1]] for point in points]
        
        for i in range(len(points[:-1])):
            start = np.array(points[i]).astype(np.int32)
            
            if i==0:
                all_points.append([start])
                
            end = np.array(points[i+1]).astype(np.int32)
            changing_axis = np.argmax(np.abs(end-start))
            unchanging_axis = int(not(changing_axis))
            step = end-start
            step = step[changing_axis]/np.abs(step[changing_axis])
            changed_pts = np.arange(start[changing_axis]+step,end[changing_axis]+step,step,dtype=np.int32)
            unchanged_pts = start[unchanging_axis]*np.ones_like(changed_pts)
            
            all_points_i = np.zeros_like(changed_pts, shape=[len(changed_pts),2])
            all_points_i[:,unchanging_axis] = unchanged_pts
            all_points_i[:,changing_axis] = changed_pts
            
            # if len(all_points_i)>0:
            all_points.append(all_points_i)
            
    all_points=np.concatenate(all_points)
    return(all_points)

def create_rock_structure(data, part1=True):
    column_min = np.min(data[:,0])  
    column_max = np.max(data[:,0])
    
    row_min = 0 # np.min(data[:,1])
    if part1:
        row_max = np.max(data[:,1])
    else:
        row_max = np.max(data[:,1])+2
                
    
    rock_structure = np.zeros([row_max-row_min+1,column_max-column_min+1],dtype=bool)
    data[:,0] -= column_min
    # data[:,1] -= row_min
    rock_structure[data[:,1],data[:,0]] = True
    
    if not(part1): # part2
        rock_structure[-1,:]=True
        
    return(rock_structure,column_min)

def add_grain(rock_structure,column_min):
    falling=True
    void=False
    
    # grain enters at row 0, column 500
    grain_position=np.array([0,500]) - np.array([0,column_min])
    
    while falling and not(void):
        # try to move grain down
        grain_position_i = grain_position + np.array([1,0])
        if grain_position_i[0]>=rock_structure.shape[0]: 
            # if grain is moved off the rock structure, void is set to True 
            void = True
        elif rock_structure[grain_position_i[0],grain_position_i[1]]==False:
            grain_position = grain_position_i
        else:
            # try to move grain down and left
            grain_position_i = grain_position + np.array([1,-1])
            if grain_position_i[1]<0:
                # if grain is moved off the rock structure, void is set to True 
                void=True
            elif rock_structure[grain_position_i[0],grain_position_i[1]]==False:
                grain_position = grain_position_i
            else:
                # try to move grain down and right
                grain_position_i = grain_position + np.array([1,1])
                if grain_position_i[1]>=rock_structure.shape[1]:
                    # if grain is moved off the rock structure, void is set to True 
                    void=True
                elif rock_structure[grain_position_i[0],grain_position_i[1]]==False:
                    grain_position = grain_position_i
                else:
                    # if no movement is possible, falling is set to False and grain is added to rock structure
                    falling=False
                    rock_structure[grain_position[0],grain_position[1]] = True
        
    return(rock_structure,void)



def move_left(rock_structure, grain_position_i, column_min):
    column_to_add = np.zeros([rock_structure.shape[0],1],dtype=bool)
    column_to_add[-1]=True
    add_col = False
    # try to move grain down and left
    grain_position_ii = grain_position_i + np.array([1,-1])
    if grain_position_ii[1]<0:
        # if grain is moved off the rock structure, add an extra column
        rock_structure = np.concatenate((column_to_add, rock_structure),axis=1)

        # update grain_position_i
        grain_position_ii = grain_position_ii+np.array([0,1])
        # update column_min
        column_min -=1
        
        if rock_structure[grain_position_ii[0],grain_position_ii[1]]==False:
            grain_position_i = grain_position_ii
            moved=True
        else:
            add_col = True
            moved=False
    elif rock_structure[grain_position_ii[0],grain_position_ii[1]]==False:
        # found unoccupied spot
        grain_position_i = grain_position_ii
        moved=True
    else:
        moved=False
    return(rock_structure,grain_position_i,column_min,moved,add_col)
            
def move_right(rock_structure, grain_position_i, column_min):
    column_to_add = np.zeros([rock_structure.shape[0],1],dtype=bool)
    column_to_add[-1]=True
    
    # try to move grain down and right
    grain_position_ii = grain_position_i + np.array([1,1])
    if grain_position_ii[1]>=rock_structure.shape[1]:
        # if grain is moved off the rock structure, add an extra column
        rock_structure = np.concatenate((rock_structure,column_to_add),axis=1)
        # column_min stays the same
        # update grain_position_i
        if rock_structure[grain_position_ii[0],grain_position_ii[1]]==False:
            grain_position_i = grain_position_ii
    elif rock_structure[grain_position_ii[0],grain_position_ii[1]]==False:
        # found unoccupied spot
        grain_position_i = grain_position_ii
    return(rock_structure,grain_position_i,column_min)
        
def add_grain_part2(rock_structure,column_min):
    falling=True
    final_grain=False
    
    # grain enters at row 0, column 500
    grain_position_0=np.array([0,500]) - np.array([0,column_min])
    grain_position=np.copy(grain_position_0)
    
    

    while falling:

        # try to move grain down
        grain_position_j = grain_position + np.array([1,0])
        if rock_structure[grain_position_j[0],grain_position_j[1]]==False:
            grain_position = grain_position_j
        else:
            # try to move grain down and left
            rock_structure,grain_position_j,column_min,moved,add_col = move_left(rock_structure, grain_position, column_min)
            if not(moved) and add_col:
                grain_position = grain_position + np.array([0,1])
            if not(moved):
                # try to move grain down and right
                rock_structure,grain_position_j,column_min = move_right(rock_structure, grain_position, column_min)
                if np.all(grain_position==grain_position_j):
                    # if no movement is possible, falling is set to False and grain is added to rock structure
                    falling=False
                    rock_structure[grain_position[0],grain_position[1]] = True
                else:
                    grain_position = grain_position_j
            else:
                grain_position = grain_position_j
    

    # if grain can't move from the original position, it is the final grain to be added  
    if np.all(grain_position==grain_position_0):
        final_grain=True
    

    return(rock_structure, final_grain, column_min)

def part1(data):
    """Solve part 1."""
    rock_structure, column_min = create_rock_structure(data)
    void=False
    count=0
    while not(void):
        # print(count)
        rock_structure,void = add_grain(rock_structure,column_min)
        if not(void):
            count+=1
    return(count)

    

def part2(data):
    """Solve part 2."""

    rock_structure, column_min = create_rock_structure(data, part1=False)

    final_grain=False
    count=0
    while not(final_grain):
        rock_structure, final_grain, column_min = add_grain_part2(rock_structure,column_min)        
        count+=1

    return(count)



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
