"""Tests for AoC 17, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202217
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202217.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202217.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == ['>','>','>','<','<','>','<','>','>','<','<','<','>','>','<','>','>',
                        '>','<','<','<','>','>','>','<','<','<','>','<','<','<','>','>','<',
                        '>','>','<','<','>','>']


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202217.part1(example1) == 3068


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202217.part2(example1) == 1514285714288
