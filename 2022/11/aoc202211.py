"""AoC 11, 2022."""

# Standard library imports
import pathlib
import sys
from dataclasses import dataclass
import numpy as np

def parse_data(puzzle_input):
    """Parse input."""
    data = {}
    monkey_list = puzzle_input.split("\n\n")
    for monkey in monkey_list:
        lines = monkey.split("\n")
        data[(lines[0][:-1]).strip()]={}
        for line_ind in range(1,len(lines)):
            if line_ind==1:
                data[lines[0][:-1]][(lines[line_ind].split(":")[0]).strip()] = [int(item) for item in (lines[line_ind].split(":")[1].strip()).split(',')]
            else:
                data[lines[0][:-1]][(lines[line_ind].split(":")[0]).strip()] = lines[line_ind].split(":")[1].strip()
    return(data)

@dataclass
class Monkey:
    name: str
    starting_items: list
    operation: str
    test: str
    if_true: str
    if_false: str
    items_inspected: int = 0
    
    def perform_operation(self, value):
        lhs = self.operation.split(" = ")[-1].split(" ")
        
        if lhs[1]=='+':
            if lhs[-1] == 'old':
                new_value = value + value
            else:
                new_value = value + int(lhs[-1])
        else:
            if lhs[-1] == 'old':
                new_value = value * value
            else:
                new_value = value * int(lhs[-1])
        return(new_value)
        
    def find_factor(self):
        return(int(self.test.split(" ")[-1]))
    
    def perform_test(self, value):
        self.items_inspected += 1
        factor = self.find_factor()
        if (value % factor) == 0:
            return(self.if_true.split("throw to ")[-1].capitalize())
        else:
            return(self.if_false.split("throw to ")[-1].capitalize())

def single_round(monkey_objects_list, common_multiple=None, divide_by_three=True):
    for monkey in monkey_objects_list:
        for item in monkey.starting_items:
            value = monkey.perform_operation(item)
            if divide_by_three:
                value = value//3
            else:
                value = value%common_multiple
            throw_to = monkey.perform_test(value)
            monkey_objects_list[int(throw_to.split(" ")[-1])].starting_items.append(value)
        monkey.starting_items = []
    
    final_dict = {}
    for monkey in monkey_objects_list:
        final_dict[monkey.name] = monkey.starting_items
    return(final_dict)

def create_monkey_objects_list(data):
    monkey_objects_list = []
    for i in range(len(data.keys())):
        monkey_name = 'Monkey ' + str(i)
        monkey_obj = Monkey(name=monkey_name,
                            starting_items = data[monkey_name]['Starting items'],
                            operation = data[monkey_name]['Operation'],
                            test = data[monkey_name]['Test'],
                            if_true = data[monkey_name]['If true'],
                            if_false = data[monkey_name]['If false'])
        monkey_objects_list.append(monkey_obj)
    return(monkey_objects_list)

def part1(data, num_rounds=20):
    """Solve part 1."""
    monkey_objects_list = create_monkey_objects_list(data)
    for i in range(num_rounds):
        single_round(monkey_objects_list)
    
    items_inspected_list = []
    for monkey in monkey_objects_list:
        items_inspected_list.append(monkey.items_inspected)
    
    return(np.prod(np.sort(items_inspected_list)[-2:]))
        

def part2(data, num_rounds=10000):
    """Solve part 2."""
    monkey_objects_list = create_monkey_objects_list(data)
    factor_list = []
    for monkey in monkey_objects_list:
        factor_list.append(monkey.find_factor())
        
    for i in range(num_rounds):
        single_round(monkey_objects_list,common_multiple=np.prod(factor_list), divide_by_three=False)
    
    items_inspected_list = []
    for monkey in monkey_objects_list:
        items_inspected_list.append(monkey.items_inspected)
    
    return(np.prod(np.sort(items_inspected_list)[-2:]))

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
