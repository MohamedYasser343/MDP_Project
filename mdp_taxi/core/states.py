"""State space generation and validation for Taxi MDP."""
from typing import List, Tuple
from .constants import GRID, GRID_SIZE


def generate_states() -> List[Tuple]:
    """Generate all possible states for the Taxi MDP.

    State format: (taxi_location, passenger_status)
    - taxi_location: (x, y) tuple representing position on grid
    - passenger_status: One of:
        - ('none', None) - no passenger present
        - ('waiting', origin, destination) - passenger waiting at origin
        - ('in_taxi', destination) - passenger in taxi heading to destination

    Returns:
        List of all possible state tuples

    Example:
        >>> states = generate_states()
        >>> len(states)  # For 5x5 grid
        16275
    """
    states = []

    for taxi_loc in GRID:
        # State: no passenger
        states.append((taxi_loc, ('none', None)))

        # States: passenger waiting at various locations
        for passenger_loc in GRID:
            for dest_loc in GRID:
                states.append((taxi_loc, ('waiting', passenger_loc, dest_loc)))

            # State: passenger in taxi going to destination
            states.append((taxi_loc, ('in_taxi', passenger_loc)))

    return states


def within_grid(location: Tuple[int, int]) -> bool:
    """Check if a location is within grid boundaries.

    Args:
        location: (x, y) tuple representing a position

    Returns:
        True if location is within grid, False otherwise

    Example:
        >>> within_grid((2, 2))
        True
        >>> within_grid((-1, 0))
        False
        >>> within_grid((10, 10))  # Assuming GRID_SIZE=5
        False
    """
    return 0 <= location[0] < GRID_SIZE and 0 <= location[1] < GRID_SIZE
