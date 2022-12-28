"""AoC 18, 2022."""

# Standard library imports
import pathlib
import sys
import numpy as np

def parse_data(puzzle_input):
    """Parse input."""
    lines = puzzle_input.split('\n')
    return([[int(p) for p in line.split(',')] for line in lines])

def get_axis_size(data, axis=0):
    x_min = np.min(data[:,axis])
    x_max = np.max(data[:,axis])
    x_length = x_max - x_min + 1
    return(x_min,x_max,x_length)

def get_sides(lava_shape_mat, x_length, y_length, z_length, row, return_empty_neighbors=False):
    sides=[]
    empty_neighbors = []
    
    if row[0] != x_length-1:
        lava_pix = lava_shape_mat[row[0]+1,row[1],row[2]]
        sides.append(lava_pix)
        if not(lava_pix):
            empty_neighbors.append([row[0]+1,row[1],row[2]])
    if row[0] != 0:
        lava_pix = lava_shape_mat[row[0]-1,row[1],row[2]]
        sides.append(lava_pix)
        if not(lava_pix):
            empty_neighbors.append([row[0]-1,row[1],row[2]])
        
    if row[1] != y_length-1:
        lava_pix = lava_shape_mat[row[0],row[1]+1,row[2]]
        sides.append(lava_pix)
        if not(lava_pix):
            empty_neighbors.append([row[0],row[1]+1,row[2]])
    if row[1] != 0:
        lava_pix = lava_shape_mat[row[0],row[1]-1,row[2]]
        sides.append(lava_pix)
        if not(lava_pix):
            empty_neighbors.append([row[0],row[1]-1,row[2]])

        
    if row[2] != z_length-1:
        lava_pix = lava_shape_mat[row[0],row[1],row[2]+1]
        sides.append(lava_pix)
        if not(lava_pix):
            empty_neighbors.append([row[0],row[1],row[2]+1])
    if row[2] != 0:
        lava_pix = lava_shape_mat[row[0],row[1],row[2]-1]
        sides.append(lava_pix)
        if not(lava_pix):
            empty_neighbors.append([row[0],row[1],row[2]-1])
    if return_empty_neighbors:
        return(empty_neighbors)
    else:
        return(sides)

def part1(data, extra_output=False):
    """Solve part 1."""
    data = np.array(data)
    
    x_min,x_max,x_length = get_axis_size(data, axis=0)
    y_min,y_max,y_length = get_axis_size(data, axis=1)
    z_min,z_max,z_length = get_axis_size(data, axis=2)

    data[:,0] = data[:,0]-x_min
    data[:,1] = data[:,1]-y_min
    data[:,2] = data[:,2]-z_min
    
    lava_shape_mat = np.zeros([x_length,y_length,z_length],dtype=bool)
    
    exposed_sides = 0
    
    for row in data:
        sides = get_sides(lava_shape_mat, x_length, y_length, z_length, row)
        lava_shape_mat[row[0],row[1],row[2]]=1

        total_touching_sides = np.sum(sides)    
        exposed_sides += 6-2*total_touching_sides

    if extra_output:
        return(exposed_sides, lava_shape_mat)
    else:
        return(exposed_sides)


def get_exterior_pix(lava_shape_mat):
    
    x_length, y_length, z_length = lava_shape_mat.shape
    
    start_pix = [0,0,0]
    ext_pix = [start_pix]
    ext_pix_status = [False]
    
    while False in ext_pix_status:
        ext_pix_additional = []
        ext_pix_status_additional = []
        for i,pix in enumerate(ext_pix):
            if ext_pix_status[i]==False:
                ext_pix_status[i]=True
                empty_neighbors = get_sides(lava_shape_mat, x_length, y_length, z_length, pix, return_empty_neighbors=True)
                for neighbor in empty_neighbors:
                    if (neighbor not in ext_pix) and (neighbor not in ext_pix_additional):
                        ext_pix_additional.append(neighbor)
                        ext_pix_status_additional.append(False)
        ext_pix = ext_pix + ext_pix_additional
        ext_pix_status = ext_pix_status + ext_pix_status_additional

    
    
    ## recursive approach fails due to exceeding max recursion depth
    # def get_exterior_pix_i(start_pix):
    #     # get neighbors of start pix that are not lava pixels
    #     empty_neighbors = get_sides(lava_shape_mat, x_length, y_length, z_length, start_pix, return_empty_neighbors=True)
    #     for neighbor in empty_neighbors:
    #         if neighbor in ext_pix:
    #             pass
    #         else:
    #             ext_pix.append(neighbor)
    #             get_exterior_pix_i(neighbor)
        
    # get_exterior_pix_i(start_pix)   
    

    return(ext_pix)

def part2(data):
    """Solve part 2."""
    
    exposed_sides, lava_shape_mat = part1(data, extra_output=True)
    lava_shape_mat = np.pad(lava_shape_mat,1)
    ext_pix = get_exterior_pix(lava_shape_mat)
       
    x,y,z = np.nonzero(lava_shape_mat==0)
    
    for i in range(len(x)):
        row = [x[i],y[i],z[i]]
        if row not in ext_pix: # interior point
            # print(row)
            sides = get_sides(lava_shape_mat, lava_shape_mat.shape[0], lava_shape_mat.shape[1], lava_shape_mat.shape[2], row)
            exposed_sides -= np.sum(sides)
    return(exposed_sides)

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
