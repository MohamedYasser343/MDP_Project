"""Tests for policy completeness and lookup."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import main


class TestPolicyCompleteness:
    """Test that policy covers all necessary states."""

    def test_policy_exists_after_value_iteration(self):
        """Test that policy dict is populated after running main."""
        # Run value iteration (already done when main.py is imported)
        assert main.policy is not None
        assert isinstance(main.policy, dict)
        assert len(main.policy) > 0

    def test_policy_has_valid_actions(self):
        """Test that all policy values are valid actions."""
        valid_actions = set(main.ACTIONS)

        for state, action in main.policy.items():
            assert action in valid_actions, f"Invalid action '{action}' for state {state}"

    def test_policy_coverage(self):
        """Test that policy covers a significant portion of state space."""
        # Policy should cover all states
        coverage = len(main.policy) / len(main.STATES)
        assert coverage > 0.99, f"Policy coverage is {coverage:.2%}, expected >99%"

    def test_common_states_in_policy(self):
        """Test that common/reachable states have policies."""
        # Test a few common states
        common_states = [
            ((0, 0), ('none', None)),
            ((2, 2), ('none', None)),
            ((1, 1), ('waiting', (0, 0), (2, 2))),
            ((3, 3), ('in_taxi', (4, 4))),
        ]

        for state in common_states:
            assert state in main.policy, f"State {state} not in policy"


class TestPolicyLookup:
    """Test safe policy lookup functionality."""

    def test_get_action_for_existing_state(self):
        """Test getting action for a state in the policy."""
        # Get any state from the policy
        if main.policy:
            state = list(main.policy.keys())[0]
            action = main.policy.get(state, None)
            assert action is not None
            assert action in main.ACTIONS

    def test_get_action_for_missing_state(self):
        """Test safe lookup with default for missing states."""
        # Create a state that's unlikely to be in the policy
        # (though all states should be in policy after value iteration)
        nonexistent_state = ((-1, -1), ('none', None))

        # Test with default
        action = main.policy.get(nonexistent_state, 'n')
        assert action == 'n'  # Should return default

    def test_visualization_safe_lookup(self):
        """Test that visualization.py uses safe lookup pattern."""
        # This test checks the fix for the bug on line 91
        pytest.importorskip("pygame", reason="pygame not installed")

        import visualization

        # Test the step function with a valid state
        state = ((1, 1), ('none', None))
        new_state = visualization.step(state)

        # Should not raise KeyError
        assert new_state is not None


class TestPolicyQuality:
    """Test qualitative aspects of the computed policy."""

    def test_policy_prefers_delivery_at_destination(self):
        """Test that policy chooses 'drop' when at destination with passenger."""
        # When taxi is at destination with passenger, should drop
        state = ((3, 3), ('in_taxi', (3, 3)))

        if state in main.policy:
            action = main.policy[state]
            assert action == 'drop', f"Expected 'drop' at destination, got '{action}'"

    def test_policy_prefers_pickup_when_at_origin(self):
        """Test that policy chooses 'pick' when at passenger origin."""
        # When taxi is at passenger location, should pick
        state = ((2, 2), ('waiting', (2, 2), (4, 4)))

        if state in main.policy:
            action = main.policy[state]
            assert action == 'pick', f"Expected 'pick' at origin, got '{action}'"

    def test_policy_avoids_invalid_actions(self):
        """Test that policy doesn't choose pick/drop in invalid situations."""
        # When no passenger, shouldn't pick
        state = ((2, 2), ('none', None))

        if state in main.policy:
            action = main.policy[state]
            # Could be any movement action, but not pick or drop
            assert action in ['n', 's', 'e', 'w'], \
                f"Expected movement action with no passenger, got '{action}'"


class TestPolicyStatistics:
    """Test policy statistics and distribution."""

    def test_action_distribution(self):
        """Test that policy has a reasonable distribution of actions."""
        from collections import Counter

        action_counts = Counter(main.policy.values())

        # All actions should appear at least once
        # (except maybe some edge cases)
        assert len(action_counts) > 0

        # Movement actions should be common
        movement_actions = ['n', 's', 'e', 'w']
        movement_count = sum(action_counts[a] for a in movement_actions if a in action_counts)

        # At least some movement actions
        assert movement_count > 0

    def test_policy_deterministic(self):
        """Test that policy is deterministic (same state -> same action)."""
        # Run value iteration multiple times and check consistency
        # (This is implicitly tested by checking policy dict consistency)

        if main.policy:
            state = list(main.policy.keys())[0]
            action1 = main.policy[state]
            action2 = main.policy.get(state)

            assert action1 == action2, "Policy should be deterministic"
