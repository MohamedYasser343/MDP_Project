#!/usr/bin/env python3
"""CLI script to run MDP solver and export policy."""
import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mdp_taxi.core.mdp_solver import ValueIterationSolver
from mdp_taxi.core.policy import Policy


def main():
    """Run value iteration solver with command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Solve Taxi MDP using value iteration",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--iterations",
        type=int,
        default=100,
        help="Maximum number of iterations",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="policy.json",
        help="Output file for policy (JSON format)",
    )

    parser.add_argument(
        "--grid-output",
        type=str,
        help="Optional output file for policy grid visualization",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print progress during value iteration",
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=1e-3,
        help="Convergence threshold for early stopping",
    )

    parser.add_argument(
        "--discount",
        type=float,
        default=0.9,
        help="Discount factor (gamma)",
    )

    args = parser.parse_args()

    # Validate arguments
    if not (0 < args.discount < 1):
        print("Error: Discount factor must be between 0 and 1")
        sys.exit(1)

    if args.threshold <= 0:
        print("Error: Convergence threshold must be positive")
        sys.exit(1)

    # Create solver
    print("Initializing value iteration solver...")
    print(f"  Discount factor: {args.discount}")
    print(f"  Convergence threshold: {args.threshold}")
    print(f"  Max iterations: {args.iterations}")
    print()

    solver = ValueIterationSolver(
        discount_factor=args.discount,
        convergence_threshold=args.threshold,
    )

    # Solve
    print("Running value iteration...")
    values, policy_dict, metadata = solver.solve(
        max_iterations=args.iterations,
        verbose=args.verbose,
    )

    # Display results
    print()
    print("=" * 50)
    print("RESULTS")
    print("=" * 50)
    print(f"Converged: {metadata['converged']}")
    print(f"Iterations: {metadata['iterations']}")
    print(f"Final delta: {metadata['final_delta']:.2e}")
    print()

    # Create policy object
    policy = Policy(policy_dict)

    # Get statistics
    stats = policy.get_statistics()
    print("Policy Statistics:")
    print(f"  Total states: {stats['total_states']}")
    print(f"  Action distribution:")
    for action, count in sorted(stats['action_distribution'].items()):
        percentage = (count / stats['total_states']) * 100
        print(f"    {action}: {count} ({percentage:.1f}%)")
    print()

    # Export policy
    policy.export_to_json(args.output)

    if args.grid_output:
        policy.export_to_grid(args.grid_output)

    print()
    print("Done!")


if __name__ == "__main__":
    main()
