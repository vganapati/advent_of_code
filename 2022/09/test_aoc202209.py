"""Tests for AoC 9, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202209
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202209.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202209.parse_data(puzzle_input)

@pytest.fixture
def example3():
    puzzle_input = (PUZZLE_DIR / "example3.txt").read_text().rstrip()
    return aoc202209.parse_data(puzzle_input)

def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == [['R', 4],
                        ['U', 4],
                        ['L', 3],
                        ['D', 1],
                        ['R', 4],
                        ['D', 1],
                        ['L', 5],
                        ['R', 2]]



def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202209.part1(example1) == 13


def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202209.part2(example2) == 36

def test_part2_example3(example3):
    """Test part 2 on example input."""
    assert aoc202209.part2(example3) == 1