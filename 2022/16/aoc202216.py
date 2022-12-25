"""AoC 16, 2022."""

# Standard library imports
import pathlib
import sys
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path

def parse_data(puzzle_input):
    """Parse input."""
    
    valve_dict={}
    lines = puzzle_input.split('\n')
    for ind,line in enumerate(lines):
        valve_name, flow_rate = line.split('Valve ')[1].split(' has flow rate=')
        flow_rate=int(flow_rate.split(';')[0])
        try:
            connections = line.split('tunnels lead to valves ')[1]
        except IndexError:
            connections = line.split('tunnel leads to valve ')[1]
        connections_list = connections.split(', ')
        valve_dict[valve_name]={'flow':flow_rate, 'connect':connections_list, 'ind':ind}
    return(valve_dict)


def create_graph_mat(valve_dict):
    graph_mat = np.zeros([len(valve_dict),len(valve_dict)], dtype=bool)
    for key in valve_dict.keys():
        ind = valve_dict[key]['ind']
        connections_list = valve_dict[key]['connect']
        for connection in connections_list:
            connect_ind = valve_dict[connection]['ind']
            graph_mat[ind,connect_ind]=1
    return(graph_mat)
        
def create_shortest_path_mat(graph_mat):
    graph_mat_sparse = csr_matrix(graph_mat)     
    dist_mat = shortest_path(graph_mat_sparse, method='auto', directed=True, 
                             return_predecessors=False, unweighted=False, overwrite=False, indices=None)
    dist_mat += 1
    return(dist_mat)

def trim_shortest_path_mat(dist_mat, valve_dict):
    """Remove nodes with flow_rate==0"""
    start_ind = valve_dict['AA']['ind']
    start_node = 'AA'
    start_flow = valve_dict['AA']['flow']
    keep_inds=[start_ind]
    keep_nodes=[start_node]
    keep_nodes_flow_rate=[start_flow]
    for key in valve_dict.keys():
        ind = valve_dict[key]['ind']
        flow_rate = valve_dict[key]['flow']
        if flow_rate > 0:
            keep_inds.append(ind)
            keep_nodes.append(key)
            keep_nodes_flow_rate.append(flow_rate)
            
    dist_mat = dist_mat[keep_inds,:][:,keep_inds]
    return(dist_mat,keep_inds,keep_nodes, keep_nodes_flow_rate)

def get_all_paths(dist_mat,keep_inds,keep_nodes_flow_rate,total_time=30):
    
    paths=[[0]]
    pressure_released=[0]
    time_per_path=[0]
    done = [False]

    while False in done:
        additional_paths=[]
        additional_pressure_released=[]
        additional_time_per_path=[]
        additional_done=[]
        delete_paths=[]
        for i,path in enumerate(paths):
            flag=False
            if time_per_path[i]<total_time:
                for j,k in enumerate(keep_inds):
                    if j not in path:
                        distance = dist_mat[path[-1],j]
                        time_elapsed = distance+time_per_path[i] #XXX
                        if time_elapsed<=total_time:
                            flag=True # delete the original path
                            new_path = path + [j]
                            additional_paths.append(new_path)
                            flow_rate=keep_nodes_flow_rate[j]
                            new_pressure_released = pressure_released[i]+(total_time - time_elapsed)*flow_rate
                            additional_pressure_released.append(new_pressure_released)
                            additional_time_per_path.append(time_elapsed)
                            additional_done.append(False)
            done[i]=not(flag)
            delete_paths.append(flag)
        for i in range(len(paths)-1,-1,-1):
            if delete_paths[i]:
                paths.pop(i)
                pressure_released.pop(i)
                time_per_path.pop(i)
                done.pop(i)
        paths = paths + additional_paths
        pressure_released = pressure_released + additional_pressure_released
        time_per_path = time_per_path + additional_time_per_path
        done = done + additional_done
    
    max_pressure_released = int(np.max(pressure_released))
    return(max_pressure_released,paths,pressure_released,time_per_path)    

def get_time_steps(path,dist_mat):
    
    current_time=0    
    time_steps=[current_time] # time the valve is opened at
    
    for i in range(1,len(path)):
        start_pt = path[i-1] # starting point
        end_pt = path[i]
        current_time += dist_mat[start_pt,end_pt]
        time_steps.append(current_time)
        
    return(time_steps)

def get_elephant_paths(human_path, keep_inds, dist_mat, keep_nodes_flow_rate, total_time=26):
    
    time_steps = get_time_steps(human_path,dist_mat)
    
    elephant_paths = [[0]]
    time_per_path = [0]
    pressure_from_elephant = [0]
    done=[False]
    
    while False in done:
        delete_paths=[]
        additional_paths=[]
        additional_pressure_from_elephant=[]
        additional_time_per_path=[]
        additional_done = []
        
        for i,path in enumerate(elephant_paths):
            delete=False
            previous = path[-1]
            for j in range(len(keep_inds)):
                add_path=False
                if j not in path:
                    elephant_valve_open_time = time_per_path[i]+dist_mat[previous,j]
                    try:
                        human_ind = human_path.index(j)
                        human_valve_open_time = time_steps[human_ind]
                        if elephant_valve_open_time<human_valve_open_time:
                            add_path=True
                    except ValueError:
                        if elephant_valve_open_time<total_time:
                            human_valve_open_time=total_time
                            add_path=True
                    if add_path:
                        delete=True
                        additional_paths.append(path+[j])
                        additional_pressure_from_elephant.append(pressure_from_elephant[i]+(human_valve_open_time-elephant_valve_open_time)*keep_nodes_flow_rate[j])                       
                        additional_done.append(False)
                        additional_time_per_path.append(elephant_valve_open_time)                        
            done[i]=not(add_path)
            delete_paths.append(delete)
        for i in range(len(elephant_paths)-1,-1,-1):
            if delete_paths[i]:
                elephant_paths.pop(i)
                time_per_path.pop(i)
                pressure_from_elephant.pop(i)
                done.pop(i)
        elephant_paths = elephant_paths + additional_paths
        pressure_from_elephant = pressure_from_elephant + additional_pressure_from_elephant
        time_per_path = time_per_path + additional_time_per_path
        done = done + additional_done
        
    return(np.max(pressure_from_elephant))
    

def part1(data):
    """Solve part 1."""
    valve_dict = data
    graph_mat = create_graph_mat(valve_dict)
    dist_mat = create_shortest_path_mat(graph_mat)
    dist_mat,keep_inds,keep_nodes, keep_nodes_flow_rate = trim_shortest_path_mat(dist_mat, valve_dict)
    max_pressure_released = get_all_paths(dist_mat,keep_inds,keep_nodes_flow_rate)[0]
    return(max_pressure_released)

def part2(data):
    """Solve part 2."""
    valve_dict = data
    graph_mat = create_graph_mat(valve_dict)
    dist_mat = create_shortest_path_mat(graph_mat)
    dist_mat,keep_inds,keep_nodes, keep_nodes_flow_rate = trim_shortest_path_mat(dist_mat, valve_dict)
    max_pressure_released,paths,pressure_released,time_per_path = get_all_paths(dist_mat,keep_inds,keep_nodes_flow_rate,total_time=26)


    
    additional_pressure_vec=[]
    final_pressure=[]
    
    for i in range(len(paths)):
        # print(i)
        human_path=paths[i]
        additional_pressure = get_elephant_paths(human_path, keep_inds, dist_mat, keep_nodes_flow_rate, total_time=26)
        final_pressure.append(additional_pressure+pressure_released[i])
        additional_pressure_vec.append(additional_pressure)

    return(int(np.max(final_pressure)))
    
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
