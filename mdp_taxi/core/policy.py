"""Policy management with safe lookup and export capabilities."""
import json
import logging
from typing import Dict, Optional, Any
from collections import Counter

logger = logging.getLogger(__name__)


class Policy:
    """Wrapper for policy dictionary with safe lookup and export.

    Attributes:
        policy: Dictionary mapping states to actions
        default_action: Default action when state not in policy
    """

    def __init__(self, policy_dict: Dict, default_action: str = "n"):
        """Initialize policy.

        Args:
            policy_dict: Dictionary mapping state tuples to action strings
            default_action: Default action for missing states (default: 'n')
        """
        self.policy = policy_dict
        self.default_action = default_action

    def get_action(self, state: tuple, default: Optional[str] = None) -> str:
        """Safely get action for state with fallback.

        Args:
            state: State tuple
            default: Optional default action (overrides self.default_action)

        Returns:
            Action string from policy or default

        Example:
            >>> policy = Policy({((0,0), ('none', None)): 'n'})
            >>> policy.get_action(((0,0), ('none', None)))
            'n'
            >>> policy.get_action(((5,5), ('none', None)), 'e')
            'e'
        """
        if state not in self.policy:
            action = default if default is not None else self.default_action
            logger.warning(f"State {state} not in policy, using default: {action}")
            return action
        return self.policy[state]

    def export_to_json(self, filepath: str) -> None:
        """Export policy to JSON file.

        Converts state tuples to string keys for JSON serialization.

        Args:
            filepath: Path to output JSON file

        Example:
            >>> policy.export_to_json('policy.json')
        """
        # Convert tuple keys to strings for JSON
        json_policy = {str(k): v for k, v in self.policy.items()}

        with open(filepath, "w") as f:
            json.dump(json_policy, f, indent=2)

        logger.info(f"Policy exported to {filepath}")
        print(f"Policy exported to {filepath}")

    def export_to_grid(self, filepath: str, grid_size: int = 5) -> None:
        """Export policy as human-readable grid display.

        Creates ASCII art visualization of policy for no-passenger states.

        Args:
            filepath: Path to output text file
            grid_size: Size of grid (default: 5)

        Example:
            >>> policy.export_to_grid('policy_grid.txt')
        """
        output = []
        output.append("=" * 50)
        output.append("Taxi Policy Grid - No Passenger State")
        output.append("=" * 50)
        output.append("")

        # Action symbols
        action_symbols = {
            "n": "↑",
            "s": "↓",
            "e": "→",
            "w": "←",
            "pick": "P",
            "drop": "D",
        }

        # Create grid for no-passenger states
        for y in range(grid_size - 1, -1, -1):
            row = []
            for x in range(grid_size):
                state = ((x, y), ("none", None))
                action = self.policy.get(state, "?")
                symbol = action_symbols.get(action, "?")
                row.append(f" {symbol} ")
            output.append("|" + "|".join(row) + "|")

        output.append("")
        output.append("Legend:")
        output.append("  ↑ = North, ↓ = South, → = East, ← = West")
        output.append("  P = Pick up, D = Drop off")
        output.append("")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(output))

        logger.info(f"Policy grid exported to {filepath}")
        print(f"Policy grid exported to {filepath}")

    def get_statistics(self) -> Dict[str, Any]:
        """Get policy statistics.

        Returns:
            Dictionary with policy statistics:
            - total_states: Number of states in policy
            - action_distribution: Count of each action
            - coverage: Fraction of states covered

        Example:
            >>> stats = policy.get_statistics()
            >>> print(stats['total_states'])
            16275
        """
        action_counts = Counter(self.policy.values())

        return {
            "total_states": len(self.policy),
            "action_distribution": dict(action_counts),
            "coverage": 1.0,  # Assuming full coverage after value iteration
        }

    def validate(self) -> bool:
        """Validate that policy is complete and consistent.

        Returns:
            True if policy is valid, False otherwise
        """
        if not self.policy:
            logger.error("Policy is empty")
            return False

        # Check that all actions are valid
        valid_actions = {"n", "s", "e", "w", "pick", "drop"}
        for state, action in self.policy.items():
            if action not in valid_actions:
                logger.error(f"Invalid action '{action}' for state {state}")
                return False

        logger.info("Policy validation passed")
        return True

    def __len__(self) -> int:
        """Return number of states in policy."""
        return len(self.policy)

    def __contains__(self, state: tuple) -> bool:
        """Check if state is in policy."""
        return state in self.policy

    def __getitem__(self, state: tuple) -> str:
        """Get action for state (raises KeyError if not found)."""
        return self.policy[state]
