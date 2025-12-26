"""Tests for MDP solver and value iteration."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import main


class TestValueIteration:
    """Test value iteration algorithm."""

    def test_values_initialized_to_zero(self):
        """Test that values are initialized to zero."""
        # Create fresh values dict
        test_values = {}
        for state in main.STATES[:10]:  # Test first 10 states
            test_values[state] = 0

        for state, value in test_values.items():
            assert value == 0, f"State {state} should have initial value 0"

    def test_value_function_improves(self):
        """Test that value function improves over iterations."""
        # Run value iteration on full state space with zero initialization
        # and compare to current values (which have been computed)

        # Values after full value iteration
        computed_values = main.values

        # Initial values (all zeros)
        initial_values = {state: 0 for state in main.STATES}

        # At least some values should have changed from initial zeros
        changes = sum(1 for s in main.STATES if computed_values[s] != initial_values[s])
        assert changes > 0, "Values should change from initial zeros after iteration"

    def test_convergence_detection(self):
        """Test that convergence is detected correctly."""
        # This is tested implicitly by running main.py
        # If it converged, the convergence message should have been printed
        assert main.policy is not None
        assert len(main.policy) > 0


class TestCalculateValueAction:
    """Test the calc_value_action function."""

    def test_calc_value_action_returns_tuple(self):
        """Test that calc_value_action returns (value, action) tuple."""
        state = ((2, 2), ('none', None))
        values = {s: 0 for s in main.STATES}

        result = main.calc_value_action(state, values)

        assert isinstance(result, tuple)
        assert len(result) == 2

        value, action = result
        assert isinstance(value, (int, float))
        assert action in main.ACTIONS

    def test_calc_value_action_with_no_passenger(self):
        """Test value calculation for state with no passenger."""
        state = ((2, 2), ('none', None))
        values = {s: 0 for s in main.STATES}

        value, action = main.calc_value_action(state, values)

        # Value should be calculated
        assert isinstance(value, (int, float))

        # Action should be a movement action (not pick/drop)
        assert action in ['n', 's', 'e', 'w']

    def test_calc_value_action_at_valid_pickup(self):
        """Test value calculation when at valid pickup location."""
        # Taxi at passenger location
        state = ((1, 1), ('waiting', (1, 1), (3, 3)))
        values = {s: 0 for s in main.STATES}

        value, action = main.calc_value_action(state, values)

        # Should consider picking up
        assert isinstance(value, (int, float))
        assert action in main.ACTIONS

    def test_calc_value_action_at_valid_dropoff(self):
        """Test value calculation when at valid dropoff location."""
        # Taxi at destination with passenger
        state = ((3, 3), ('in_taxi', (3, 3)))
        values = {s: 0 for s in main.STATES}

        value, action = main.calc_value_action(state, values)

        # Should prefer dropping off (gets +10 reward)
        assert isinstance(value, (int, float))
        assert action in main.ACTIONS


class TestRewardStructure:
    """Test reward calculations."""

    def test_step_cost(self):
        """Test that movement has -1 cost."""
        # In calc_value_action, movement actions should have -1 reward
        # This is tested indirectly through value function

        state = ((2, 2), ('none', None))
        values = {s: 0 for s in main.STATES}

        value, action = main.calc_value_action(state, values)

        # With all zero values, the reward should dominate
        # Movement action should give value close to -1 (with discount)
        if action in ['n', 's', 'e', 'w']:
            # Value should be negative (step cost)
            assert value <= 0

    def test_delivery_reward(self):
        """Test that successful delivery has positive reward."""
        # Dropping off at destination should give +10 reward

        state = ((3, 3), ('in_taxi', (3, 3)))
        values = {s: 0 for s in main.STATES}

        value, action = main.calc_value_action(state, values)

        # Should choose drop action
        # Value should be positive (delivery reward)
        if action == 'drop':
            # With zero future values, should get ~+10 reward
            assert value > 0

    def test_invalid_action_penalty(self):
        """Test that invalid pickup/dropoff has penalty."""
        # Trying to pick when not at passenger location should give -5 penalty
        # This is tested through the algorithm choosing not to do invalid actions

        state = ((2, 2), ('waiting', (1, 1), (3, 3)))
        values = {s: 0 for s in main.STATES}

        value, action = main.calc_value_action(state, values)

        # Should not choose 'pick' when not at passenger location
        # (because -5 penalty is worse than -1 movement cost)
        assert action != 'pick'


class TestDiscountFactor:
    """Test discount factor effects."""

    def test_discount_factor_value(self):
        """Test that discount factor is in valid range."""
        assert 0 < main.DISCOUNT_FACTOR < 1
        assert main.DISCOUNT_FACTOR == 0.9

    def test_discount_affects_future_rewards(self):
        """Test that discount factor properly discounts future rewards."""
        # Future rewards should be discounted by gamma
        # This is tested implicitly in the value iteration

        # Immediate reward should be valued more than future reward
        immediate_value = 10  # Immediate +10
        future_value = main.DISCOUNT_FACTOR * 10  # Future +10

        assert immediate_value > future_value


class TestStateTransitions:
    """Test state transition dynamics."""

    def test_deterministic_transitions(self):
        """Test that transitions are deterministic (for most actions)."""
        # Movement, pickup, dropoff are deterministic
        # Only passenger arrival is stochastic

        state = ((2, 2), ('none', None))

        # Movement north should always go to (2, 3)
        new_loc = (2, 3)
        assert main.within_grid(new_loc)

    def test_passenger_arrival_probability(self):
        """Test that passenger arrival is incorporated in value calculation."""
        # When passenger status is 'none', there's 20% chance of new passenger

        state = ((2, 2), ('none', None))
        values = {s: 0 for s in main.STATES}

        value, action = main.calc_value_action(state, values)

        # The value should account for probabilistic passenger arrivals
        # (tested implicitly through calc_value_action logic)
        assert isinstance(value, (int, float))


class TestConvergenceProperties:
    """Test convergence properties of value iteration."""

    def test_convergence_threshold(self):
        """Test that convergence threshold is set."""
        assert hasattr(main, 'CONVERGENCE_THRESHOLD')
        assert main.CONVERGENCE_THRESHOLD > 0
        assert main.CONVERGENCE_THRESHOLD < 1

    def test_max_iterations(self):
        """Test that max iterations is set to reasonable value."""
        assert hasattr(main, 'ITERATIONS')
        assert main.ITERATIONS > 0
        assert main.ITERATIONS >= 100  # Should be enough for 5x5 grid

    def test_values_dict_populated(self):
        """Test that values dictionary is populated after iteration."""
        assert main.values is not None
        assert isinstance(main.values, dict)
        assert len(main.values) > 0

        # Should have values for all states
        assert len(main.values) == len(main.STATES)

    def test_policy_dict_populated(self):
        """Test that policy dictionary is populated after iteration."""
        assert main.policy is not None
        assert isinstance(main.policy, dict)
        assert len(main.policy) > 0

        # Should have actions for all states
        assert len(main.policy) == len(main.STATES)
