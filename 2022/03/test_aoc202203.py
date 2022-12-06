"""Tests for AoC 3, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202203
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc202203.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc202203.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == [['v','J','r','w','p','W','t','w','J','g','W','r','h','c','s','F','M','M','f','F','F','h','F','p'],
                        ['j','q','H','R','N','q','R','j','q','z','j','G','D','L','G','L','r','s','F','M','f','F','Z','S','r','L','r','F','Z','s','S','L'],
                        ['P','m','m','d','z','q','P','r','V','v','P','w','w','T','W','B','w','g'],
                        ['w','M','q','v','L','M','Z','H','h','H','M','v','w','L','H','j','b','v','c','j','n','n','S','B','n','v','T','Q','F','n'],
                        ['t','t','g','J','t','R','G','J','Q','c','t','T','Z','t','Z','T'],
                        ['C','r','Z','s','J','s','P','P','Z','s','G','z','w','w','s','L','w','L','m','p','w','M','D','w']]


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202203.part1(example1) == 157


def test_ord_to_priority1():
    assert aoc202203.ord_to_priority('a') == 1


def test_ord_to_priority2():
    assert aoc202203.ord_to_priority('A') == 27

  
def test_ord_to_priority3():
    assert aoc202203.ord_to_priority('z') == 26

  
def test_ord_to_priority4():
    assert aoc202203.ord_to_priority('Z') == 52

  
@pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202203.part2(example1) == ...


def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc202203.part2(example2) == 70
