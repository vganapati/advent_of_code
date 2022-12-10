"""Tests for AoC 7, 2022."""

# Standard library imports
import pathlib

# Third party imports
import aoc202207
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().rstrip()
    return aoc202207.parse_data(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().rstrip()
    return aoc202207.parse_data(puzzle_input)


@pytest.fixture
def example3():
    puzzle_input = (PUZZLE_DIR / "example3.txt").read_text().rstrip()
    return aoc202207.parse_data(puzzle_input)

def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == ['$ cd /',
                        '$ ls',
                        'dir a',
                        '14848514 b.txt',
                        '8504156 c.dat',
                        'dir d',
                        '$ cd a',
                        '$ ls',
                        'dir e',
                        '29116 f',
                        '2557 g',
                        '62596 h.lst',
                        '$ cd e',
                        '$ ls',
                        '584 i',
                        '$ cd ..',
                        '$ cd ..',
                        '$ cd d',
                        '$ ls',
                        '4060174 j',
                        '8033020 d.log',
                        '5626152 d.ext',
                        '7214296 k']



def test_parse_example2(example2):
    """Test that input is parsed properly."""
    assert example2 == ['$ cd /',
                        '$ ls',
                        'dir ccjp',
                        '328708 hglnvs.bsh',
                        'dir hpsnpc',
                        'dir pcb',
                        'dir pntzm',
                        'dir pzg',
                        'dir thfgwwsp',
                        '$ cd ccjp',
                        '$ ls',
                        '159990 dlz',
                        'dir mbtsvblj',
                        '165076 nppbjl.qhg',
                        '$ cd mbtsvblj',
                        '$ ls',
                        '34806 frqsf.nsv',
                        'dir ppq',
                        'dir ptht',
                        'dir rgmvdwt',
                        '$ cd ppq',
                        '$ ls',
                        '10 dhzp',
                        '$ cd ..',
                        '$ cd ptht']

def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc202207.part1(example1) == 95437

def test_part1_example2(example2):
    """Test part 1 on example input."""
    assert aoc202207.part1(example2) == 34826

def test_total_size(example1):
    assert aoc202207.total_size(example1) == 48381165

def test_part1_example3(example3):
    """Test part 1 on example input."""
    assert aoc202207.part1(example3) == 81645

def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc202207.part2(example1) == 24933642

