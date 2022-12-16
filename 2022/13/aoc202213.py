"""AoC 13, 2022."""

# Standard library imports
import pathlib
import sys
import ast
import numpy as np

def parse_data(puzzle_input):
    """Parse input."""
    return([[ast.literal_eval(l) for l in line.split("\n")] for line in puzzle_input.split("\n\n")])
    
def compare(data_pair):
    element_0, element_1 = data_pair
    order = None
    
    for i in range(len(element_0)):
        order = None
        
        try:
            a = element_0[i]
            b = element_1[i]
            if type(a)==int and type(b)==int:
                if a<b:
                    order=True
                elif a>b:
                    order=False
            else:
                if type(a)==int:
                    # convert to list
                    a = [a]
                if type(b)==int:
                    # convert to list
                    b = [b]
                order = compare([a,b])
        except IndexError:
            order=False
        if order is not None:
            break
    
    if order is None:
        if len(element_0)<len(element_1):
            order=True
    return(order)
        
def part1(data):
    """Solve part 1."""
    compare_vec = []
    for data_pair in data:
        compare_vec.append(compare(data_pair))
        
    return(np.sum(np.arange(1,len(compare_vec)+1)[np.array(compare_vec)]))
    
        
def merge_sort_items(all_items):

    if len(all_items)==1:
        return(all_items)
    elif len(all_items)==2:
        order = compare(all_items)
        if order==True:
            return(all_items)
        else:
            return([all_items[1], all_items[0]])
    else:
        # split list and sort
        all_items_0_sorted = merge_sort_items(all_items[0:len(all_items)//2])
        all_items_1_sorted = merge_sort_items(all_items[len(all_items)//2:])
        
        
        #combine sorted sub-lists
        all_items_sorted = []
        flag = True
        a_ind=0
        b_ind=0

        while flag:
            a_item = all_items_0_sorted[a_ind] 
            b_item = all_items_1_sorted[b_ind]
            
            order = compare([a_item,b_item])
            if order==True:
                all_items_sorted.append(a_item)
                a_ind += 1
            else:
                all_items_sorted.append(b_item)
                b_ind += 1
            
            if (a_ind == len(all_items_0_sorted)) or (b_ind == len(all_items_1_sorted)):
                flag=False
                
        if a_ind<=(len(all_items_0_sorted)-1):
            for i in range(a_ind,len(all_items_0_sorted)):
                all_items_sorted.append(all_items_0_sorted[i])

        if b_ind<=(len(all_items_1_sorted)-1):
            for i in range(b_ind,len(all_items_1_sorted)):
                all_items_sorted.append(all_items_1_sorted[i])
                
        return(all_items_sorted)
        
def preprocess_part2(data):
    all_items =[]
    for data_pair in data:
        all_items.append(data_pair[0])
        all_items.append(data_pair[1])
    all_items.append([[2]])
    all_items.append([[6]])
    return(all_items)

def part2(data):
    """Solve part 2."""
    all_items = preprocess_part2(data)
    all_items_sorted = merge_sort_items(all_items)
    
    # find the decoder keys
    ind_0 = all_items_sorted.index([[2]])
    ind_1 = all_items_sorted.index([[6]])
    
    return((ind_0+1)*(ind_1+1))
    

    

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
