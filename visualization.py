"""Backward compatibility wrapper for visualization.py

This file maintains the original interface while using the new modular package.
For new code, use: python scripts/visualize.py

New features available in scripts/visualize.py:
- Interactive controls (pause, speed, step-through)
- HUD overlay with statistics
- Load policy from file
- Reset simulation
"""
import warnings

warnings.warn(
    "visualization.py is deprecated and will be removed in version 3.0. "
    "Use 'python scripts/visualize.py' for interactive visualization.",
    DeprecationWarning,
    stacklevel=2,
)

import pygame
import time
import random

# Import from new modular package
from mdp_taxi.core.constants import (
    GRID_SIZE,
    GRID,
    CELL_SIZE,
    COLOR_WHITE,
    COLOR_BLACK,
    COLOR_BLUE,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_YELLOW,
    PASSENGER_ARRIVAL_PROB,
    DEFAULT_STEP_DELAY,
    FPS,
)
from mdp_taxi.core.states import within_grid

# Import policy from main (which now uses new package)
from main import policy

# Initialize pygame
pygame.init()

# Setup display
WIDTH = HEIGHT = CELL_SIZE * GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Taxi MDP (Legacy Mode)")

clock = pygame.time.Clock()

# Initial state
state = ((0, 0), ('none', None))


def draw(state):
    """Draw the current state to screen."""
    screen.fill(COLOR_WHITE)

    # Draw grid
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(
                x * CELL_SIZE,
                (GRID_SIZE - 1 - y) * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, COLOR_BLACK, rect, 2)

    taxi_loc, passenger = state
    tx, ty = taxi_loc

    taxi_x = tx * CELL_SIZE + CELL_SIZE * 0.25
    taxi_y = (GRID_SIZE - 1 - ty) * CELL_SIZE + CELL_SIZE * 0.25
    taxi_size = CELL_SIZE * 0.5

    # Draw taxi (blue square)
    taxi_rect = pygame.Rect(taxi_x, taxi_y, taxi_size, taxi_size)
    pygame.draw.rect(screen, COLOR_BLUE, taxi_rect)

    # Draw destination (red square)
    if passenger[0] == 'waiting':
        dest_x = passenger[2][0] * CELL_SIZE + CELL_SIZE * 0.25
        dest_y = (GRID_SIZE - 1 - passenger[2][1]) * CELL_SIZE + CELL_SIZE * 0.25
        dest_rect = pygame.Rect(dest_x, dest_y, taxi_size, taxi_size)
        pygame.draw.rect(screen, COLOR_RED, dest_rect)
    if passenger[0] == 'in_taxi':
        dest_x = passenger[1][0] * CELL_SIZE + CELL_SIZE * 0.25
        dest_y = (GRID_SIZE - 1 - passenger[1][1]) * CELL_SIZE + CELL_SIZE * 0.25
        dest_rect = pygame.Rect(dest_x, dest_y, taxi_size, taxi_size)
        pygame.draw.rect(screen, COLOR_RED, dest_rect)

    # Draw passenger
    if passenger[0] == 'waiting':
        # Green circle for waiting passenger
        px, py = passenger[1]
        pygame.draw.circle(
            screen,
            COLOR_GREEN,
            (
                px * CELL_SIZE + CELL_SIZE // 2,
                (GRID_SIZE - 1 - py) * CELL_SIZE + CELL_SIZE // 2
            ),
            CELL_SIZE // 8
        )
    elif passenger[0] == 'in_taxi':
        # Yellow circle for passenger in taxi
        pygame.draw.circle(
            screen,
            COLOR_YELLOW,
            (
                int(taxi_x + taxi_size / 2),
                int(taxi_y + taxi_size / 2)
            ),
            CELL_SIZE // 8
        )

    pygame.display.flip()


def step(state):
    """Take one step using the policy."""
    taxi_loc, passenger = state
    action = policy.get(state, 'n')  # Safe lookup with default

    if action == 'n':
        new_loc = (taxi_loc[0], taxi_loc[1] + 1)
    elif action == 's':
        new_loc = (taxi_loc[0], taxi_loc[1] - 1)
    elif action == 'e':
        new_loc = (taxi_loc[0] + 1, taxi_loc[1])
    elif action == 'w':
        new_loc = (taxi_loc[0] - 1, taxi_loc[1])
    elif action == 'pick':
        if passenger[0] == 'waiting' and taxi_loc == passenger[1]:
            return (taxi_loc, ('in_taxi', passenger[2]))
        return state
    elif action == 'drop':
        if passenger[0] == 'in_taxi' and taxi_loc == passenger[1]:
            return (taxi_loc, ('none', None))
        return state
    else:
        return state

    if not within_grid(new_loc):
        new_loc = taxi_loc

    return (new_loc, passenger)


# Main loop
if __name__ == "__main__":
    print("Running legacy visualization...")
    print("For interactive mode, use: python scripts/visualize.py")
    print()

    origin, destination = random.sample(GRID, 2)
    state = ((0, 0), ('waiting', origin, destination))
    draw(state)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        state = step(state)
        draw(state)
        print(state, policy.get(state, 'n'))

        if state[1][0] == 'none' and random.random() < PASSENGER_ARRIVAL_PROB:
            origin, destination = random.sample(GRID, 2)
            state = (state[0], ('waiting', origin, destination))

        time.sleep(DEFAULT_STEP_DELAY)
        clock.tick(FPS)

    pygame.quit()
