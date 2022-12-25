"""Tests for AoC 16, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202216
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202216.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202216.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == {'AA':{'flow':0, 'connect':['DD', 'II', 'BB'], 'ind':0},
                        'BB':{'flow':13, 'connect':['CC', 'AA'], 'ind':1},
                        'CC':{'flow':2, 'connect':['DD', 'BB'], 'ind':2},
                        'DD':{'flow':20, 'connect':['CC', 'AA', 'EE'], 'ind':3},
                        'EE':{'flow':3, 'connect':['FF', 'DD'], 'ind':4},
                        'FF':{'flow':0, 'connect':['EE', 'GG'], 'ind':5},
                        'GG':{'flow':0, 'connect':['FF', 'HH'], 'ind':6},
                        'HH':{'flow':22, 'connect':['GG'], 'ind':7},
                        'II':{'flow':0, 'connect':['AA', 'JJ'], 'ind':8},
                        'JJ':{'flow':21, 'connect':['II'], 'ind':9}}


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202216.part1(example1) == 1651


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202216.part2(example1) == 1707
