"""AoC 19, 2022."""

# Standard library imports
import pathlib
import sys
import functools
import numpy as np


def parse_data(puzzle_input):
    """Parse input."""
    lines = puzzle_input.split('\n')
    blueprints = {}
    for line in lines:
        blueprint_number = int(line.split('Blueprint ')[1].split(':')[0])
        robot_costs = line.split(': ')[1].split('. ')
        assert len(robot_costs) == 4
        # cost for each robot type is [ore, clay, obsidian, geode]
        ore_robot = [int(robot_costs[0].split('costs ')[-1].split(' ore')[0]), 0, 0, 0]
        clay_robot = [int(robot_costs[1].split('costs ')[-1].split(' ore')[0]), 0, 0, 0]
        obsidian_robot = [int(robot_costs[2].split(' ore')[0].split(' ')[-1]), int(robot_costs[2].split(' clay')[0].split(' ')[-1]), 0, 0]
        geode_robot = [int(robot_costs[3].split(' ore')[0].split(' ')[-1]), 0, int(robot_costs[3].split(' obsidian')[0].split(' ')[-1]), 0]

        ore_robot = np.array(ore_robot)
        clay_robot = np.array(clay_robot)
        obsidian_robot = np.array(obsidian_robot)
        geode_robot = np.array(geode_robot)

        blueprints[blueprint_number] = {'ore_robot': ore_robot, 'clay_robot': clay_robot, 'obsidian_robot': obsidian_robot, 'geode_robot': geode_robot}
    return(blueprints)


def get_purchase_options(resources, blueprint):
    # XXX need to redo
    purchase_options = [np.array([0,0,0,0])]

    for previous_purchase in purchase_options:
        purchase_options.append(add_option(resources, previous_purchase))
    """
    returns purchase array of [ore, clay, obsidian, geode]
    """
    def add_option(resources, previous_purchase):
        if np.min(resources - blueprint['ore_robot']) >= 0:
            return add_option(resources - blueprint['ore_robot'], previous_purchase + np.array([1, 0, 0, 0]))
        elif np.min(resources - blueprint['clay_robot']) >= 0:
            return add_option(resources - blueprint['clay_robot'], previous_purchase + np.array([0, 1, 0, 0]))
        elif np.min(resources - blueprint['obsidian_robot']) >= 0:
            return add_option(resources - blueprint['obsidian_robot'], previous_purchase + np.array([0, 0, 1, 0]))    
        elif np.min(resources - blueprint['geode_robot']) >= 0:
            return add_option(resources - blueprint['geode_robot'], previous_purchase + np.array([0, 0, 0, 1]))
        else: # base case: cannot purchase anything
            return previous_purchase

@functools.cache
def find_max_geodes(blueprint, time, resources, robots):
    if time == 24:
        geodes = resources[3]
        return geodes
    else:
        resources, additional_robots = make_purchase(resources)
        resources = resources + robots
        robots = robots + additional_robots
        return max(find_max_geodes(blueprint, time+1, resources, robots))

def part1(blueprint):
    """Solve part 1."""
    resources = np.zeros(4) # ore, clay, obsidian, geodes
    robots = np.array([1, 0, 0, 0]) # ore, clay, obsidian, geode




def part2(data):
    """Solve part 2."""


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
