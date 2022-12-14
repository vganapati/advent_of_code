"""Tests for AoC 11, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202211
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202211.parse_data(puzzle_input)


def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == {'Monkey 0':{'Starting items': [79,98],
                                    'Operation': 'new = old * 19',
                                    'Test': 'divisible by 23',
                                    'If true':'throw to monkey 2',
                                    'If false':'throw to monkey 3'},
                        'Monkey 1':{'Starting items': [54, 65, 75, 74],
                                    'Operation': 'new = old + 6',
                                    'Test': 'divisible by 19',
                                    'If true':'throw to monkey 2',
                                    'If false':'throw to monkey 0'},
                        'Monkey 2':{'Starting items': [79, 60, 97],
                                    'Operation': 'new = old * old',
                                    'Test': 'divisible by 13',
                                    'If true':'throw to monkey 1',
                                    'If false':'throw to monkey 3'},
                        'Monkey 3':{'Starting items': [74],
                                    'Operation': 'new = old + 3',
                                    'Test': 'divisible by 17',
                                    'If true':'throw to monkey 0',
                                    'If false':'throw to monkey 1'},
                        }


def test_single_round_example1(example1):
    """Test part 1 on example input."""
    monkey_objects_list = aoc202211.create_monkey_objects_list(example1)
    assert aoc202211.single_round(monkey_objects_list) == {'Monkey 0': [20, 23, 27, 26],
                                                           'Monkey 1': [2080, 25, 167, 207, 401, 1046],
                                                           'Monkey 2': [],
                                                           'Monkey 3': []}


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202211.part1(example1) == 10605

def test_part2_example1_0(example1,num_rounds=20):
    """Test part 2 on example input."""
    assert aoc202211.part2(example1,num_rounds=num_rounds) == 10197

def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202211.part2(example1) == 2713310158

