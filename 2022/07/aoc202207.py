"""AoC 7, 2022."""

# Standard library imports
import pathlib
import sys
from anytree import AnyNode,PreOrderIter
import numpy as np

def parse_data(puzzle_input):
    """Parse input."""
    data = puzzle_input.split("\n")
    return(data)

def total_size(data):
    file_total=0
    for dat in data:
        if (dat[0] != '$') and (dat[:3] != 'dir'):
            size,node_id = dat.split(" ")
            file_total += int(size)
    return(file_total)

    
def create_tree(data):
    nodes = []
    
    parent = AnyNode(id='root')
    nodes.append(parent)
    
    count = 0
    while count<len(data):
        if data[count] == '$ ls':
            # keep reading lines until a '$'
            count+=1
            while count<len(data) and data[count][0] != '$' :
                if data[count][:3] == 'dir':
                    pass
                else:
                    size,node_id = data[count].split(" ")
                    node = AnyNode(id=node_id,parent=parent,size=int(size),folder=False)
                    nodes.append(node)
                count+=1
        elif data[count][:7] == '$ cd ..':
            parent = parent.parent
            count+=1
        elif data[count][:4] == '$ cd':
            node_id = data[count][5:]
            node = AnyNode(id=node_id, parent=parent, folder=True, size=0)
            nodes.append(node)
            parent=node
            count+=1  
    return(nodes)

def get_size(node):
    size = np.sum([node.size for node in node.children])
    for node in node.children:
        if node.folder == True:
            size+=get_size(node)
    return(size)
        

def part1(data):
    """Solve part 1."""
    nodes=create_tree(data)
    total=0
    for node in PreOrderIter(nodes[1]):
        if node.folder == True:
            size = get_size(node)
            if size<=100000:
                total+=size
    return(total)
            

    

def part2(data):
    """Solve part 2."""
    nodes=create_tree(data)
    size_list=[]
    for node in PreOrderIter(nodes[1]):
        if node.folder == True:
            size = get_size(node)
            size_list.append(size)

    size_list = np.array(size_list)
    desired_unused_space = 30000000
    unused_space_vec = 70000000 - size_list[0] + size_list # unused space if we remove that directory
    return(np.min(size_list[unused_space_vec >= desired_unused_space]))


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
