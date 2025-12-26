"""Backward compatibility wrapper for main.py

This file maintains the original interface while using the new modular package.
New code should use: python scripts/solve_mdp.py
"""
import warnings

# Import from new package
from mdp_taxi.core.constants import (
    GRID_SIZE,
    GRID,
    ACTIONS,
    DISCOUNT_FACTOR,
    MAX_ITERATIONS as ITERATIONS,
    CONVERGENCE_THRESHOLD,
)
from mdp_taxi.core.states import generate_states, within_grid
from mdp_taxi.core.mdp_solver import ValueIterationSolver
from mdp_taxi.core.policy import Policy as PolicyClass

# Show deprecation warning
warnings.warn(
    "main.py is deprecated and will be removed in version 3.0. "
    "Use 'python scripts/solve_mdp.py' instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Generate states (backward compatibility)
STATES = generate_states()


# Backward compatibility function
def calc_value_action(state, values):
    """Calculate value and action for a state (backward compatibility).

    This wraps the new ValueIterationSolver._calculate_q_value method.
    """
    solver = ValueIterationSolver()
    return solver._calc_value_action(state, values)


# Run value iteration
print("Running value iteration (using new modular package)...")
solver = ValueIterationSolver(
    discount_factor=DISCOUNT_FACTOR,
    convergence_threshold=CONVERGENCE_THRESHOLD,
)

values, policy_dict, metadata = solver.solve(
    max_iterations=ITERATIONS,
    verbose=True,
)

# Create policy object but also maintain dict for backward compat
policy = policy_dict  # For visualization.py compatibility
policy_obj = PolicyClass(policy_dict)

# Display results
print()
if metadata['converged']:
    print("Value iteration complete. Final policy computed.")
else:
    print(f"Did not converge after {metadata['iterations']} iterations")

# Export for inspection
if __name__ == "__main__":
    stats = policy_obj.get_statistics()
    print(f"\nPolicy covers {stats['total_states']} states")
    print("Action distribution:")
    for action, count in sorted(stats['action_distribution'].items()):
        percentage = (count / stats['total_states']) * 100
        print(f"  {action}: {count:5d} ({percentage:4.1f}%)")
