"""Tests for AoC 14, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202214
import pytest
import numpy as np

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202214.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202214.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    np.testing.assert_array_equal(example1,np.array([[498,   4],
                                                     [498,   5],
                                                     [498,   6],
                                                     [497,   6],
                                                     [496,   6],
                                                     [503,   4],
                                                     [502,   4],
                                                     [502,   5],
                                                     [502,   6],
                                                     [502,   7],
                                                     [502,   8],
                                                     [502,   9],
                                                     [501,   9],
                                                     [500,   9],
                                                     [499,   9],
                                                     [498,   9],
                                                     [497,   9],
                                                     [496,   9],
                                                     [495,   9],
                                                     [494,   9]], dtype=np.int32))


def test_create_rock_structure_part1(example1):
    np.testing.assert_array_equal(aoc202214.create_rock_structure(example1)[0],
                                  np.array([[False, False, False, False, False, False, False, False, False, False],
                                            [False, False, False, False, False, False, False, False, False, False],
                                            [False, False, False, False, False, False, False, False, False, False],
                                            [False, False, False, False, False, False, False, False, False, False],
                                            [False, False, False, False,  True, False, False, False,  True, True],
                                            [False, False, False, False,  True, False, False, False,  True, False],
                                            [False, False,  True,  True,  True, False, False, False,  True, False],
                                            [False, False, False, False, False, False, False, False,  True, False],
                                            [False, False, False, False, False, False, False, False,  True, False],
                                            [True,  True,  True,  True,  True,  True,  True,  True,  True, False]]))

def test_create_rock_structure_part2(example1):
    assert aoc202214.create_rock_structure(example1)[1] == 494


def test_add_grain_part1_0(example1):
    rock_structure,column_min = aoc202214.create_rock_structure(example1)
    
    
    np.testing.assert_array_equal(aoc202214.add_grain(rock_structure,column_min)[0],
                                  np.array([[False, False, False, False, False, False, False, False, False, False],
                                            [False, False, False, False, False, False, False, False, False, False],
                                            [False, False, False, False, False, False, False, False, False, False],
                                            [False, False, False, False, False, False, False, False, False, False],
                                            [False, False, False, False,  True, False, False, False,  True, True],
                                            [False, False, False, False,  True, False, False, False,  True, False],
                                            [False, False,  True,  True,  True, False, False, False,  True, False],
                                            [False, False, False, False, False, False, False, False,  True, False],
                                            [False, False, False, False, False, False, True, False,  True, False],
                                            [True,  True,  True,  True,  True,  True,  True,  True,  True, False]]))

def test_add_grain_part2_0(example1):
    rock_structure,column_min = aoc202214.create_rock_structure(example1)
    assert aoc202214.add_grain(rock_structure,column_min)[1] == False
    
def test_add_grain_part1_1(example1):
    rock_structure,column_min = aoc202214.create_rock_structure(example1)
    
    
    np.testing.assert_array_equal(aoc202214.add_grain(aoc202214.add_grain(rock_structure, column_min)[0],column_min)[0],
                                  np.array([[False, False, False, False, False, False, False, False, False, False],
                                            [False, False, False, False, False, False, False, False, False, False],
                                            [False, False, False, False, False, False, False, False, False, False],
                                            [False, False, False, False, False, False, False, False, False, False],
                                            [False, False, False, False,  True, False, False, False,  True, True],
                                            [False, False, False, False,  True, False, False, False,  True, False],
                                            [False, False,  True,  True,  True, False, False, False,  True, False],
                                            [False, False, False, False, False, False, False, False,  True, False],
                                            [False, False, False, False, False, True, True, False,  True, False],
                                            [True,  True,  True,  True,  True,  True,  True,  True,  True, False]]))

def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202214.part1(example1) == 24


def test_create_rock_structure_part1_part2(example1):
    np.testing.assert_array_equal(aoc202214.create_rock_structure(example1, part1=False)[0],
                                  np.array([[False, False, False, False, False, False, False, False, False, False],
                                            [False, False, False, False, False, False, False, False, False, False],
                                            [False, False, False, False, False, False, False, False, False, False],
                                            [False, False, False, False, False, False, False, False, False, False],
                                            [False, False, False, False,  True, False, False, False,  True, True],
                                            [False, False, False, False,  True, False, False, False,  True, False],
                                            [False, False,  True,  True,  True, False, False, False,  True, False],
                                            [False, False, False, False, False, False, False, False,  True, False],
                                            [False, False, False, False, False, False, False, False,  True, False],
                                            [True,  True,  True,  True,  True,  True,  True,  True,  True, False],
                                            [False, False, False, False, False, False, False, False, False, False],
                                            [True,  True,  True,  True,  True,  True,  True,  True,  True, True]]))


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202214.part2(example1) == 93
    
