"""AoC 15, 2022."""

# Standard library imports
import pathlib
import sys
import numpy as np

def parse_data(puzzle_input):
    """Parse input."""
    lines = puzzle_input.split("\n")
    sensor_beacon_pairs = []
    for line in lines:
        sensor,beacon=line.split(':')
        sensor = sensor.split('Sensor at x=')[1]
        sensor_x,sensor_y = sensor.split(', y=')
        
        beacon = beacon.split(' closest beacon is at x=')[1]
        beacon_x,beacon_y = beacon.split(', y=')
        
        sensor_beacon_pairs.append([[int(sensor_x),int(sensor_y)],[int(beacon_x),int(beacon_y)]])
    return(sensor_beacon_pairs)


def part1(data, y=10):
    """Solve part 1."""
    x_coords_max_min = []
    manhatten_dist_vec = []
    for sensor_beacon_pair in data:
        sensor = np.array(sensor_beacon_pair[0])
        beacon = np.array(sensor_beacon_pair[1])
        
        manhatten_dist = np.sum(np.abs(sensor-beacon))
        manhatten_dist_vec.append(manhatten_dist)
        
        x_coords_max_min.append(sensor[0]-manhatten_dist)
        x_coords_max_min.append(sensor[0]+manhatten_dist)

    x_min = np.min(x_coords_max_min)
    x_max = np.max(x_coords_max_min)
    x_len = x_max-x_min+1
    
    beacon_mat = np.zeros([x_len,1], bool)
    no_addtl_beacon_mat = np.zeros([x_len,1],bool)
    xm,ym = np.meshgrid(np.arange(x_min,x_max+1),np.array([y]),indexing='ij')

    for i,sensor_beacon_pair in enumerate(data):
        sensor = np.array(sensor_beacon_pair[0])
        beacon = np.array(sensor_beacon_pair[1])
        beacon_mat[((xm-beacon[0])**2+(ym-beacon[1])**2)==0]=1
        no_addtl_beacon_mat[(np.abs(xm-sensor[0])+np.abs(ym-sensor[1]))<=manhatten_dist_vec[i]]=1
        
    
    return(np.sum(no_addtl_beacon_mat[ym==y])-np.sum(beacon_mat[ym==y]),manhatten_dist_vec)


def full_matrix(data, x_min, x_max, y_min, y_max):


    x_len = x_max-x_min+1
    y_len = y_max-y_min+1
    
    # beacon_mat = np.zeros([x_len,y_len], bool)
    no_addtl_beacon_mat = np.zeros([x_len,y_len],bool)
    xm,ym = np.meshgrid(np.arange(x_min,x_max+1,dtype=np.int32),np.arange(y_min,y_max+1,dtype=np.int32),indexing='ij')

    for i in range(data.shape[0]):
        sensor_beacon_pair = data[i]
        sensor = sensor_beacon_pair[0]
        beacon = sensor_beacon_pair[1]

        manhatten_dist = np.sum(np.abs(sensor-beacon))
        # beacon_mat[((xm-beacon[0])**2+(ym-beacon[1])**2)==0]=1
        no_addtl_beacon_mat[(np.abs(xm-sensor[0])+np.abs(ym-sensor[1]))<=manhatten_dist]=1
        if np.sum(no_addtl_beacon_mat)==np.size(no_addtl_beacon_mat):
            return(no_addtl_beacon_mat,xm,ym)
    
    return(no_addtl_beacon_mat,xm,ym)


def split_boxes(all_coords,all_steps):
    all_coords_new=[]
    all_steps_new=[]
    all_coords_corners_new=[]
    
    for i in range(len(all_coords)):
        coords=all_coords[i]
        steps=all_steps[i]
        steps_split_0 = [steps[0]//2,steps[0]-steps[0]//2]
        steps_split_1 = [steps[1]//2,steps[1]-steps[1]//2]
        
        c_i = coords[0]
        c_j = coords[1]
        step_vec = [steps_split_0[0],steps_split_1[0]]
        all_coords_new.append([c_i,c_j])
        all_steps_new.append(step_vec)
        all_coords_corners_new.append([[c_i,c_j],[c_i+step_vec[0],c_j],[c_i,c_j+step_vec[1]],[c_i+step_vec[0],c_j+step_vec[1]]])
        
        c_i = coords[0] + steps_split_0[0]
        c_j = coords[1]
        step_vec = [steps_split_0[1],steps_split_1[0]]
        all_coords_new.append([c_i,c_j])
        all_steps_new.append(step_vec)
        all_coords_corners_new.append([[c_i,c_j],[c_i+step_vec[0],c_j],[c_i,c_j+step_vec[1]],[c_i+step_vec[0],c_j+step_vec[1]]])
        
        c_i = coords[0]
        c_j = coords[1] + steps_split_1[0]
        step_vec = [steps_split_0[0],steps_split_1[1]]
        all_coords_new.append([c_i,c_j])
        all_steps_new.append(step_vec)
        all_coords_corners_new.append([[c_i,c_j],[c_i+step_vec[0],c_j],[c_i,c_j+step_vec[1]],[c_i+step_vec[0],c_j+step_vec[1]]])
        
        c_i = coords[0] + steps_split_0[0]
        c_j = coords[1] + steps_split_1[0]
        step_vec = [steps_split_0[1],steps_split_1[1]]
        all_coords_new.append([c_i,c_j])
        all_steps_new.append(step_vec)
        all_coords_corners_new.append([[c_i,c_j],[c_i+step_vec[0],c_j],[c_i,c_j+step_vec[1]],[c_i+step_vec[0],c_j+step_vec[1]]])
    return(all_coords_new,all_steps_new,all_coords_corners_new)
        

def part2(data, min_coord=0, max_coord=20, step=5):
    """Solve part 2."""
    coords_vec = np.arange(min_coord,max_coord,step)
    step_vec = step*np.ones_like(coords_vec)
    step_vec[-1] = max_coord-coords_vec[-1]+1
    
    all_coords_corners=[]
    all_steps=[]
    all_coords=[]
    for i,c_i in enumerate(coords_vec):
        for j,c_j in enumerate(coords_vec):
            all_coords.append([c_i,c_j])
            all_coords_corners.append([[c_i,c_j],[c_i+step_vec[i],c_j],[c_i,c_j+step_vec[j]],[c_i+step_vec[i],c_j+step_vec[j]]])
            all_steps.append([step_vec[i],step_vec[j]])
    
    for split_step in range(9):
        for j in range(data.shape[0]):
            sensor_beacon_pair = data[j]
            sensor = sensor_beacon_pair[0]
            beacon = sensor_beacon_pair[1]
            manhatten_dist = np.sum(np.abs(sensor-beacon))
            for i in range(len(all_coords_corners)-1,-1,-1):
                coords_corners=all_coords_corners[i]
                eliminate_box = True
                for corner in coords_corners:
                    manhatten_dist_i = np.sum(np.abs(sensor-np.array(corner)))
                    if manhatten_dist_i>manhatten_dist:
                        eliminate_box=False
                if eliminate_box:
                    all_coords_corners.pop(i)
                    all_coords.pop(i)
                    all_steps.pop(i)
        all_coords,all_steps,all_coords_corners = split_boxes(all_coords,all_steps)
    
    for i in range(len(all_coords)):
            no_addtl_beacon_mat, xm, ym = full_matrix(data, all_coords[i][0], all_coords[i][0]+all_steps[i][0], 
                                                      all_coords[i][1], all_coords[i][1]+all_steps[i][1])
            if np.sum(no_addtl_beacon_mat==0)>0:
                inds = np.nonzero(no_addtl_beacon_mat==0)
                x = xm[inds[0][0],inds[1][0]]
                y = ym[inds[0][0],inds[1][0]]
                return(x*4000000+y)


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse_data(puzzle_input)
    part1_sol, manhatten_dist_vec = part1(data, y=2000000)
    yield part1_sol
    data = np.array(data)
    data = data[np.flip(np.argsort(manhatten_dist_vec))]
    yield part2(data, min_coord=0, max_coord=4000000, step=400000)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().rstrip())
        print("\n".join(str(solution) for solution in solutions))
