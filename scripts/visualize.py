#!/usr/bin/env python3
"""CLI script to run interactive Taxi MDP visualization."""
import argparse
import sys
import time
import random
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

from mdp_taxi.core.constants import GRID, GRID_SIZE, PASSENGER_ARRIVAL_PROB
from mdp_taxi.core.states import within_grid


def load_policy(policy_path: str = None):
    """Load policy from file or compute it.

    Args:
        policy_path: Optional path to policy JSON file

    Returns:
        Policy dictionary
    """
    if policy_path:
        import json
        import ast

        print(f"Loading policy from {policy_path}...")
        with open(policy_path, "r") as f:
            json_policy = json.load(f)

        # Convert string keys back to tuples
        policy = {}
        for key_str, action in json_policy.items():
            # Parse the string representation of tuple
            key = ast.literal_eval(key_str)
            policy[key] = action

        print(f"Loaded policy with {len(policy)} states")
        return policy
    else:
        print("Computing policy using value iteration...")
        from mdp_taxi.core.mdp_solver import ValueIterationSolver
        solver = ValueIterationSolver()
        _, policy, metadata = solver.solve(verbose=True)
        print(f"Converged: {metadata['converged']} at iteration {metadata['iterations']}")
        return policy


def step(state, policy):
    """Take one step in the environment.

    Args:
        state: Current state tuple
        policy: Policy dictionary

    Returns:
        New state tuple
    """
    taxi_loc, passenger = state
    action = policy.get(state, "n")  # Default to north if state not found

    if action == "n":
        new_loc = (taxi_loc[0], taxi_loc[1] + 1)
    elif action == "s":
        new_loc = (taxi_loc[0], taxi_loc[1] - 1)
    elif action == "e":
        new_loc = (taxi_loc[0] + 1, taxi_loc[1])
    elif action == "w":
        new_loc = (taxi_loc[0] - 1, taxi_loc[1])
    elif action == "pick":
        if passenger[0] == "waiting" and taxi_loc == passenger[1]:
            return (taxi_loc, ("in_taxi", passenger[2]))
        return state
    elif action == "drop":
        if passenger[0] == "in_taxi" and taxi_loc == passenger[1]:
            return (taxi_loc, ("none", None))
        return state
    else:
        return state

    if not within_grid(new_loc):
        new_loc = taxi_loc

    return (new_loc, passenger)


def main():
    """Run interactive visualization."""
    parser = argparse.ArgumentParser(
        description="Interactive Taxi MDP Visualization",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--policy",
        type=str,
        help="Path to policy JSON file (if not provided, computes policy)",
    )

    parser.add_argument(
        "--speed",
        type=float,
        default=0.4,
        help="Initial delay between steps in seconds",
    )

    parser.add_argument(
        "--no-hud",
        action="store_true",
        help="Disable HUD overlay",
    )

    parser.add_argument(
        "--simple",
        action="store_true",
        help="Use simple visualization (no interactive controls)",
    )

    args = parser.parse_args()

    if not PYGAME_AVAILABLE:
        print("Error: pygame is required for visualization")
        print("Install it with: pip install pygame")
        sys.exit(1)

    # Load or compute policy
    policy = load_policy(args.policy)

    if args.simple:
        run_simple_visualization(policy, args.speed)
    else:
        run_interactive_visualization(policy, args.speed, show_hud=not args.no_hud)


def run_simple_visualization(policy, speed):
    """Run simple visualization without interactive controls.

    Args:
        policy: Policy dictionary
        speed: Delay between steps in seconds
    """
    from mdp_taxi.visualization.renderer import TaxiRenderer

    print("\nStarting simple visualization...")
    print("Close window to exit\n")

    renderer = TaxiRenderer()

    # Initialize state
    origin, destination = random.sample(GRID, 2)
    state = ((0, 0), ("waiting", origin, destination))

    running = True
    while running:
        # Handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw current state
        renderer.draw(state)

        # Print state info
        action = policy.get(state, "n")
        print(f"State: {state}, Action: {action}")

        # Take step
        state = step(state, policy)

        # Handle passenger arrival
        if state[1][0] == "none" and random.random() < PASSENGER_ARRIVAL_PROB:
            origin, destination = random.sample(GRID, 2)
            state = (state[0], ("waiting", origin, destination))

        time.sleep(speed)
        renderer.tick()

    renderer.quit()
    print("\nVisualization ended.")


def run_interactive_visualization(policy, initial_speed, show_hud=True):
    """Run interactive visualization with full controls.

    Args:
        policy: Policy dictionary
        initial_speed: Initial delay between steps
        show_hud: Whether to show HUD overlay
    """
    from mdp_taxi.visualization.renderer import TaxiRenderer
    from mdp_taxi.visualization.controls import SimulationController
    from mdp_taxi.visualization.display import HUDDisplay

    print("\nStarting interactive visualization...")
    print("Controls:")
    print("  SPACE: Pause/Resume")
    print("  UP/DOWN: Adjust speed")
    print("  RIGHT: Step (when paused)")
    print("  R: Reset simulation")
    print("  H: Toggle help")
    print("  Q/ESC: Quit")
    print()

    renderer = TaxiRenderer()
    controller = SimulationController(initial_speed)
    hud = HUDDisplay(renderer.screen) if show_hud else None

    # Initialize state and statistics
    origin, destination = random.sample(GRID, 2)
    state = ((0, 0), ("waiting", origin, destination))
    step_count = 0
    total_reward = 0
    deliveries = 0
    last_step_time = time.time()

    while not controller.quit_requested:
        # Handle events
        controller.handle_events()

        # Handle reset
        if controller.reset_requested:
            origin, destination = random.sample(GRID, 2)
            state = ((0, 0), ("waiting", origin, destination))
            step_count = 0
            total_reward = 0
            deliveries = 0
            print("Simulation reset")

        # Draw current state
        renderer.draw(state)

        # Get current action
        action = policy.get(state, "n")

        # Draw HUD if enabled
        if hud and show_hud:
            hud.draw_legend()
            hud.draw_state_info(state, action)
            hud.draw_statistics(step_count, total_reward, deliveries)
            hud.draw_controls_hint(controller.paused, controller.speed)

            if controller.show_help:
                hud.draw_help_overlay(controller.get_help_text())

        pygame.display.flip()

        # Check if we should advance
        current_time = time.time()
        time_since_step = current_time - last_step_time
        should_step = (
            controller.should_advance() and
            (time_since_step >= controller.speed or controller.step_mode)
        )

        if should_step:
            # Calculate reward
            old_passenger = state[1]

            # Take step
            state = step(state, policy)
            step_count += 1
            last_step_time = current_time

            # Calculate reward
            new_passenger = state[1]
            if old_passenger[0] == "in_taxi" and new_passenger[0] == "none":
                # Successful delivery
                total_reward += 10
                deliveries += 1
                print(f"Delivery completed! Total: {deliveries}")
            elif action in ("pick", "drop"):
                if old_passenger == new_passenger:
                    # Invalid pick/drop
                    total_reward -= 5
                else:
                    # Successful pickup
                    total_reward += 0
            else:
                # Movement
                total_reward -= 1

            # Handle passenger arrival
            if state[1][0] == "none" and random.random() < PASSENGER_ARRIVAL_PROB:
                origin, destination = random.sample(GRID, 2)
                state = (state[0], ("waiting", origin, destination))
                print(f"New passenger arrived: {origin} -> {destination}")

        renderer.tick(60)

    renderer.quit()
    print(f"\nSimulation ended.")
    print(f"Final statistics:")
    print(f"  Steps: {step_count}")
    print(f"  Deliveries: {deliveries}")
    print(f"  Total reward: {total_reward:.1f}")
    if step_count > 0:
        print(f"  Average reward/step: {total_reward / step_count:.2f}")


if __name__ == "__main__":
    main()
