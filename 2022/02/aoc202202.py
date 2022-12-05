"""AoC 2, 2022."""

# Standard library imports
import pathlib
import sys
import numpy as np

def parse_data(puzzle_input):
    """Parse input."""
    games = puzzle_input.split("\n")
    return [[player[0] for player in game.split(" ")] for game in games]

def part1(data):
    """Solve part 1."""
    data = np.array(data)
    
    '''points for the object chosen'''
    my_objects = np.zeros_like(data[:,1], dtype=np.int32)
    my_objects[data[:,1]=='X'] = 1
    my_objects[data[:,1]=='Y'] = 2
    my_objects[data[:,1]=='Z'] = 3
    
    object_points = np.sum(my_objects)
    
    '''points for win/loss/draw'''
    
    # opponent choices to numpy array
    opp_objects = np.zeros_like(data[:,0], dtype=np.int32)
    opp_objects[data[:,0]=='A'] = 1
    opp_objects[data[:,0]=='B'] = 2
    opp_objects[data[:,0]=='C'] = 3
    
    results = np.zeros_like(data[:,0], dtype=np.int32)
    # results[my_objects<opp_objects] = 0 # losses
    results[my_objects>opp_objects] = 6 # wins
    results[my_objects==opp_objects] = 3 #draws
    results[(my_objects==1) & (opp_objects==3)] = 6 # correct for rock beating scissors
    results[(my_objects==3) & (opp_objects==1)] = 0 # correct for rock beating scissors
    
    points_results = np.sum(results)
    
    total_points = object_points + points_results
    return(total_points, opp_objects, my_objects)
    

def part2(data):
    """Solve part 2."""
    _, opp_objects, my_choices = part1(data)
    
    '''points for win/loss/draw'''
    my_points = np.zeros_like(my_choices)
    # my_points[my_choices==1]=0 # lose
    my_points[my_choices==2]=3 # draw
    my_points[my_choices==3]=6 # win
    
    points_results = np.sum(my_points)

    '''points for object chosen'''
    
    # determine which objects were chosen for desired result
    my_objects = np.zeros_like(my_choices)
    my_objects[my_choices==1] = opp_objects[my_choices==1]-1 # lose 
    my_objects[my_choices==2] = opp_objects[my_choices==2] # draw
    my_objects[my_choices==3] = opp_objects[my_choices==3]+1 # win

    my_objects[(my_objects==0)] = 3 # correct losses for rock beating scissors
    my_objects[(my_objects==4)] = 1 # correct wins for rock beating scissors
    
    object_points = np.sum(my_objects)
    total_points = object_points + points_results
    return(total_points)

def solve(puzzle_input):
    """Solve the puzzle for the given input."""    
    data = parse_data(puzzle_input)
    yield part1(data)[0]
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))
