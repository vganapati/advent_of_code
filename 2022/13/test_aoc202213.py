"""Tests for AoC 13, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202213
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202213.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202213.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == [[[1,1,3,1,1],
                        [1,1,5,1,1]],
                        [[[1],[2,3,4]],
                        [[1],4]],
                        [[9],
                        [[8,7,6]]],
                        [[[4,4],4,4],
                        [[4,4],4,4,4]],
                        [[7,7,7,7],
                        [7,7,7]],
                        [[],
                        [3]],
                        [[[[]]],
                        [[]]],
                        [[1,[2,[3,[4,[5,6,7]]]],8,9],
                        [1,[2,[3,[4,[5,6,0]]]],8,9]]]


def test_compare_0(example1):
    """Test part 1 on example input."""
    assert aoc202213.compare(example1[0]) == True

def test_compare_1(example1):
    """Test part 1 on example input."""
    assert aoc202213.compare(example1[1]) == True
    
def test_compare_2(example1):
    """Test part 1 on example input."""
    assert aoc202213.compare(example1[2]) == False
    
def test_compare_3(example1):
    """Test part 1 on example input."""
    assert aoc202213.compare(example1[3]) == True

def test_compare_4(example1):
    """Test part 1 on example input."""
    assert aoc202213.compare(example1[4]) == False

def test_compare_5(example1):
    """Test part 1 on example input."""
    assert aoc202213.compare(example1[5]) == True

def test_compare_6(example1):
    """Test part 1 on example input."""
    assert aoc202213.compare(example1[6]) == False
    
def test_compare_7(example1):
    """Test part 1 on example input."""
    assert aoc202213.compare(example1[7]) == False

def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202213.part1(example1) == 13

def test_part1_example2(example2):
    """Test part 1 on example input."""
    assert aoc202213.part1(example2) == 0
    
def test_merge_sort_items(example1):
    all_items = aoc202213.preprocess_part2(example1)
    assert aoc202213.merge_sort_items(all_items) == [[],
                                                     [[]],
                                                     [[[]]],
                                                     [1,1,3,1,1],
                                                     [1,1,5,1,1],
                                                     [[1],[2,3,4]],
                                                     [1,[2,[3,[4,[5,6,0]]]],8,9],
                                                     [1,[2,[3,[4,[5,6,7]]]],8,9],
                                                     [[1],4],
                                                     [[2]],
                                                     [3],
                                                     [[4,4],4,4],
                                                     [[4,4],4,4,4],
                                                     [[6]],
                                                     [7,7,7],
                                                     [7,7,7,7],
                                                     [[8,7,6]],
                                                     [9]]

def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202213.part2(example1) == 140

