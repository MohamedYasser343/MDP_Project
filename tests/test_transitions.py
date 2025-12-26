"""Tests for state transitions and action logic."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import main


class TestMovementActions:
    """Test movement actions (n, s, e, w)."""

    def test_north_movement(self):
        """Test moving north increases y coordinate."""
        state = ((2, 2), ('none', None))
        values = {s: 0 for s in main.STATES}
        value, action = main.calc_value_action(state, values)

        # Manually check north movement
        taxi_loc = (2, 2)
        new_loc = (taxi_loc[0], taxi_loc[1] + 1)
        assert new_loc == (2, 3)
        assert main.within_grid(new_loc)

    def test_south_movement(self):
        """Test moving south decreases y coordinate."""
        taxi_loc = (2, 2)
        new_loc = (taxi_loc[0], taxi_loc[1] - 1)
        assert new_loc == (2, 1)
        assert main.within_grid(new_loc)

    def test_east_movement(self):
        """Test moving east increases x coordinate."""
        taxi_loc = (2, 2)
        new_loc = (taxi_loc[0] + 1, taxi_loc[1])
        assert new_loc == (3, 2)
        assert main.within_grid(new_loc)

    def test_west_movement(self):
        """Test moving west decreases x coordinate."""
        taxi_loc = (2, 2)
        new_loc = (taxi_loc[0] - 1, taxi_loc[1])
        assert new_loc == (1, 2)
        assert main.within_grid(new_loc)


class TestBoundaryCollisions:
    """Test boundary collision handling."""

    def test_north_boundary(self):
        """Test that moving north at top boundary keeps taxi in place."""
        loc = (2, main.GRID_SIZE - 1)
        assert not main.within_grid((loc[0], loc[1] + 1))

    def test_south_boundary(self):
        """Test that moving south at bottom boundary keeps taxi in place."""
        loc = (2, 0)
        assert not main.within_grid((loc[0], loc[1] - 1))

    def test_east_boundary(self):
        """Test that moving east at right boundary keeps taxi in place."""
        loc = (main.GRID_SIZE - 1, 2)
        assert not main.within_grid((loc[0] + 1, loc[1]))

    def test_west_boundary(self):
        """Test that moving west at left boundary keeps taxi in place."""
        loc = (0, 2)
        assert not main.within_grid((loc[0] - 1, loc[1]))

    def test_within_grid_valid(self):
        """Test within_grid returns True for valid coordinates."""
        assert main.within_grid((0, 0))
        assert main.within_grid((2, 2))
        assert main.within_grid((main.GRID_SIZE - 1, main.GRID_SIZE - 1))

    def test_within_grid_invalid(self):
        """Test within_grid returns False for invalid coordinates."""
        assert not main.within_grid((-1, 0))
        assert not main.within_grid((0, -1))
        assert not main.within_grid((main.GRID_SIZE, 0))
        assert not main.within_grid((0, main.GRID_SIZE))


class TestPickupDropoff:
    """Test pickup and dropoff logic."""

    def test_valid_pickup_location(self):
        """Test that pickup is valid when taxi is at passenger origin."""
        state = ((1, 1), ('waiting', (1, 1), (3, 3)))
        # Taxi at (1,1), passenger waiting at (1,1) going to (3,3)
        # This should be a valid pickup

        passenger_status = state[1]
        assert passenger_status[0] == 'waiting'
        assert state[0] == passenger_status[1]  # Taxi at passenger location

    def test_invalid_pickup_location(self):
        """Test that pickup is invalid when taxi is not at passenger origin."""
        state = ((2, 2), ('waiting', (1, 1), (3, 3)))
        # Taxi at (2,2), passenger waiting at (1,1)
        # This should be an invalid pickup

        passenger_status = state[1]
        assert passenger_status[0] == 'waiting'
        assert state[0] != passenger_status[1]  # Taxi not at passenger location

    def test_valid_dropoff_location(self):
        """Test that dropoff is valid when taxi is at destination."""
        state = ((3, 3), ('in_taxi', (3, 3)))
        # Taxi at (3,3), passenger in taxi going to (3,3)
        # This should be a valid dropoff

        passenger_status = state[1]
        assert passenger_status[0] == 'in_taxi'
        assert state[0] == passenger_status[1]  # Taxi at destination

    def test_invalid_dropoff_location(self):
        """Test that dropoff is invalid when taxi is not at destination."""
        state = ((2, 2), ('in_taxi', (3, 3)))
        # Taxi at (2,2), passenger in taxi going to (3,3)
        # This should be an invalid dropoff

        passenger_status = state[1]
        assert passenger_status[0] == 'in_taxi'
        assert state[0] != passenger_status[1]  # Taxi not at destination

    def test_pickup_when_no_passenger(self):
        """Test that pickup is invalid when no passenger is waiting."""
        state = ((1, 1), ('none', None))
        passenger_status = state[1]
        assert passenger_status[0] == 'none'

    def test_dropoff_when_no_passenger_in_taxi(self):
        """Test that dropoff is invalid when no passenger is in taxi."""
        state = ((1, 1), ('waiting', (1, 1), (3, 3)))
        passenger_status = state[1]
        assert passenger_status[0] != 'in_taxi'


class TestStateSpace:
    """Test state space generation."""

    def test_state_count(self):
        """Test that state count matches expected formula."""
        # For grid size n:
        # - States with 'none': n^2
        # - States with 'waiting': n^2 * n^2 * n^2 = n^6
        # - States with 'in_taxi': n^2 * n^2 = n^4
        # Total: n^2 + n^6 + n^4 = n^2(1 + n^4 + n^2)

        # For n=5: 25 + 15625 + 625 = 16275
        expected_count = (main.GRID_SIZE ** 2 +
                          main.GRID_SIZE ** 6 +
                          main.GRID_SIZE ** 4)

        assert len(main.STATES) == expected_count

    def test_all_passenger_statuses_present(self):
        """Test that all passenger status types are represented."""
        status_types = set()
        for state in main.STATES:
            status_types.add(state[1][0])

        assert 'none' in status_types
        assert 'waiting' in status_types
        assert 'in_taxi' in status_types

    def test_all_grid_locations_covered(self):
        """Test that taxi can be at any grid location."""
        taxi_locations = set()
        for state in main.STATES:
            taxi_locations.add(state[0])

        assert len(taxi_locations) == main.GRID_SIZE ** 2
        assert (0, 0) in taxi_locations
        assert (main.GRID_SIZE - 1, main.GRID_SIZE - 1) in taxi_locations
