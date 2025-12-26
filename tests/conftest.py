"""Pytest configuration and fixtures for Taxi MDP tests."""
import pytest
import sys
from pathlib import Path

# Add parent directory to path to import main module
sys.path.insert(0, str(Path(__file__).parent.parent))

import main


@pytest.fixture
def small_grid():
    """Fixture for 3x3 grid for faster testing."""
    return [(x, y) for x in range(3) for y in range(3)]


@pytest.fixture
def sample_state():
    """Fixture for a typical state with passenger waiting."""
    return ((1, 1), ('waiting', (0, 0), (2, 2)))


@pytest.fixture
def state_no_passenger():
    """Fixture for state with no passenger."""
    return ((2, 2), ('none', None))


@pytest.fixture
def state_passenger_in_taxi():
    """Fixture for state with passenger in taxi."""
    return ((1, 1), ('in_taxi', (3, 3)))


@pytest.fixture
def grid_size_5():
    """Fixture for default 5x5 grid."""
    return 5


@pytest.fixture
def actions():
    """Fixture for all possible actions."""
    return ['n', 's', 'e', 'w', 'pick', 'drop']
