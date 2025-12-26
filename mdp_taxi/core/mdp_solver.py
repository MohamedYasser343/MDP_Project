"""MDP solver using value iteration with convergence checking."""
import logging
from typing import Dict, Tuple, Any
from .constants import (
    ACTIONS,
    DISCOUNT_FACTOR,
    MAX_ITERATIONS,
    CONVERGENCE_THRESHOLD,
    REWARD_STEP,
    REWARD_INVALID_ACTION,
    REWARD_SUCCESSFUL_PICKUP,
    REWARD_SUCCESSFUL_DELIVERY,
    PASSENGER_ARRIVAL_PROB,
    GRID,
)
from .states import generate_states, within_grid

logger = logging.getLogger(__name__)


class ValueIterationSolver:
    """Solves Taxi MDP using value iteration algorithm.

    Attributes:
        discount_factor: Discount factor for future rewards (gamma)
        convergence_threshold: Threshold for early stopping
        states: List of all possible states
        actions: List of all possible actions
    """

    def __init__(
        self,
        discount_factor: float = DISCOUNT_FACTOR,
        convergence_threshold: float = CONVERGENCE_THRESHOLD,
    ):
        """Initialize the value iteration solver.

        Args:
            discount_factor: Discount factor (0 < gamma < 1)
            convergence_threshold: Stop when max value change < threshold
        """
        self.discount_factor = discount_factor
        self.convergence_threshold = convergence_threshold
        self.states = generate_states()
        self.actions = ACTIONS

    def solve(
        self, max_iterations: int = MAX_ITERATIONS, verbose: bool = False
    ) -> Tuple[Dict, Dict, Dict[str, Any]]:
        """Run value iteration to compute optimal policy.

        Args:
            max_iterations: Maximum number of iterations
            verbose: If True, print progress every 5 iterations

        Returns:
            Tuple of (values, policy, metadata) where:
            - values: Dict mapping states to their values
            - policy: Dict mapping states to optimal actions
            - metadata: Dict with convergence info (iterations, converged, final_delta)
        """
        # Initialize values
        values = {state: 0.0 for state in self.states}
        policy = {}

        for iteration in range(max_iterations):
            new_values = values.copy()

            # Update value for each state
            for state in self.states:
                new_values[state], policy[state] = self._calc_value_action(
                    state, values
                )

            # Check convergence
            max_delta = max(abs(new_values[s] - values[s]) for s in self.states)

            if verbose and iteration % 5 == 0:
                logger.info(f"Iteration {iteration}: max_delta={max_delta:.6f}")
                print(f"Iteration {iteration}: max_delta={max_delta:.6f}")

            if max_delta < self.convergence_threshold:
                if verbose:
                    logger.info(f"Converged at iteration {iteration}")
                    print(f"Converged at iteration {iteration} (delta={max_delta:.2e})")
                return values, policy, {
                    "iterations": iteration,
                    "converged": True,
                    "final_delta": max_delta,
                }

            values = new_values

        logger.warning(f"Did not converge after {max_iterations} iterations")
        if verbose:
            print(f"Did not converge after {max_iterations} iterations")

        return values, policy, {
            "iterations": max_iterations,
            "converged": False,
            "final_delta": max_delta,
        }

    def _calc_value_action(
        self, state: Tuple, values: Dict
    ) -> Tuple[float, str]:
        """Calculate the best action and value for a given state.

        Uses the Bellman equation to compute Q-values for all actions
        and returns the action with maximum expected value.

        Args:
            state: State tuple (taxi_location, passenger_status)
            values: Current value estimates for all states

        Returns:
            Tuple of (max_value, best_action)
        """
        max_value = float("-inf")
        best_action = None

        for action in self.actions:
            value = self._calculate_q_value(state, action, values)

            if value > max_value:
                max_value = value
                best_action = action

        return max_value, best_action

    def _calculate_q_value(
        self, state: Tuple, action: str, values: Dict
    ) -> float:
        """Calculate Q-value for a state-action pair.

        Args:
            state: Current state
            action: Action to evaluate
            values: Current value estimates

        Returns:
            Expected value of taking action in state
        """
        taxi_loc, passenger = state
        reward = REWARD_STEP  # Default step cost

        # Determine next state and reward based on action
        if action == "n":
            new_state = ((taxi_loc[0], taxi_loc[1] + 1), passenger)
        elif action == "s":
            new_state = ((taxi_loc[0], taxi_loc[1] - 1), passenger)
        elif action == "e":
            new_state = ((taxi_loc[0] + 1, taxi_loc[1]), passenger)
        elif action == "w":
            new_state = ((taxi_loc[0] - 1, taxi_loc[1]), passenger)
        elif action == "pick":
            if passenger[0] == "waiting" and taxi_loc == passenger[1]:
                reward = REWARD_SUCCESSFUL_PICKUP
                new_state = (taxi_loc, ("in_taxi", passenger[2]))
            else:
                reward = REWARD_INVALID_ACTION
                new_state = state
        elif action == "drop":
            if passenger[0] == "in_taxi" and taxi_loc == passenger[1]:
                reward = REWARD_SUCCESSFUL_DELIVERY
                new_state = (taxi_loc, ("none", None))
            else:
                reward = REWARD_INVALID_ACTION
                new_state = state
        else:
            new_state = state

        # Check grid boundaries for movement actions
        if action in ["n", "s", "e", "w"]:
            if not within_grid(new_state[0]):
                new_state = state

        # Calculate expected value
        if new_state[1][0] == "none":
            # Handle probabilistic passenger arrivals
            arrival_value = 0.0
            for origin in GRID:
                for dest in GRID:
                    if origin != dest:
                        arrival_state = (new_state[0], ("waiting", origin, dest))
                        arrival_value += values[arrival_state]
            arrival_value /= len(GRID) * (len(GRID) - 1)

            # 80% stay empty, 20% new passenger arrives
            value = 0.8 * (reward + self.discount_factor * values[new_state]) + 0.2 * (
                reward + self.discount_factor * arrival_value
            )
        else:
            # Deterministic transition
            value = reward + self.discount_factor * values[new_state]

        return value
