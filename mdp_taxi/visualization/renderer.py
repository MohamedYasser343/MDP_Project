"""Pygame rendering logic for Taxi MDP visualization."""
from typing import Tuple, Optional
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

from ..core.constants import (
    GRID_SIZE,
    CELL_SIZE,
    COLOR_WHITE,
    COLOR_BLACK,
    COLOR_BLUE,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_YELLOW,
)


class TaxiRenderer:
    """Handles all drawing operations for taxi simulation.

    Attributes:
        cell_size: Size of each grid cell in pixels
        grid_size: Number of cells in each dimension
        width: Total window width
        height: Total window height
        screen: Pygame display surface
    """

    def __init__(self, cell_size: int = CELL_SIZE, grid_size: int = GRID_SIZE):
        """Initialize the renderer.

        Args:
            cell_size: Size of each cell in pixels
            grid_size: Number of cells in grid (grid_size x grid_size)

        Raises:
            ImportError: If pygame is not available
        """
        if not PYGAME_AVAILABLE:
            raise ImportError("pygame is required for visualization")

        self.cell_size = cell_size
        self.grid_size = grid_size
        self.width = cell_size * grid_size
        self.height = cell_size * grid_size

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Taxi MDP")
        self.clock = pygame.time.Clock()

    def draw(self, state: Tuple, show_hud: bool = False, hud_info: Optional[dict] = None) -> None:
        """Draw the current state to screen.

        Args:
            state: State tuple (taxi_location, passenger_status)
            show_hud: Whether to show HUD overlay
            hud_info: Optional dict with HUD information
        """
        self.screen.fill(COLOR_WHITE)
        self._draw_grid()
        self._draw_taxi(state[0])
        self._draw_passenger(state)
        pygame.display.flip()

    def _draw_grid(self) -> None:
        """Draw grid lines."""
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                rect = pygame.Rect(
                    x * self.cell_size,
                    (self.grid_size - 1 - y) * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, COLOR_BLACK, rect, 2)

    def _draw_taxi(self, taxi_loc: Tuple[int, int]) -> None:
        """Draw taxi at specified location.

        Args:
            taxi_loc: (x, y) coordinates of taxi
        """
        tx, ty = taxi_loc
        taxi_x = tx * self.cell_size + self.cell_size * 0.25
        taxi_y = (self.grid_size - 1 - ty) * self.cell_size + self.cell_size * 0.25
        taxi_size = self.cell_size * 0.5

        taxi_rect = pygame.Rect(taxi_x, taxi_y, taxi_size, taxi_size)
        pygame.draw.rect(self.screen, COLOR_BLUE, taxi_rect)

    def _draw_passenger(self, state: Tuple) -> None:
        """Draw passenger and destination based on state.

        Args:
            state: Full state tuple (taxi_location, passenger_status)
        """
        taxi_loc, passenger = state
        taxi_size = self.cell_size * 0.5

        # Draw destination (red square)
        if passenger[0] == "waiting":
            dest_x = passenger[2][0] * self.cell_size + self.cell_size * 0.25
            dest_y = (self.grid_size - 1 - passenger[2][1]) * self.cell_size + self.cell_size * 0.25
            dest_rect = pygame.Rect(dest_x, dest_y, taxi_size, taxi_size)
            pygame.draw.rect(self.screen, COLOR_RED, dest_rect)

            # Draw waiting passenger (green circle)
            px, py = passenger[1]
            pygame.draw.circle(
                self.screen,
                COLOR_GREEN,
                (
                    px * self.cell_size + self.cell_size // 2,
                    (self.grid_size - 1 - py) * self.cell_size + self.cell_size // 2,
                ),
                self.cell_size // 8,
            )

        elif passenger[0] == "in_taxi":
            # Draw destination (red square)
            dest_x = passenger[1][0] * self.cell_size + self.cell_size * 0.25
            dest_y = (self.grid_size - 1 - passenger[1][1]) * self.cell_size + self.cell_size * 0.25
            dest_rect = pygame.Rect(dest_x, dest_y, taxi_size, taxi_size)
            pygame.draw.rect(self.screen, COLOR_RED, dest_rect)

            # Draw passenger in taxi (yellow circle inside taxi)
            tx, ty = taxi_loc
            taxi_x = tx * self.cell_size + self.cell_size * 0.25
            taxi_y = (self.grid_size - 1 - ty) * self.cell_size + self.cell_size * 0.25
            pygame.draw.circle(
                self.screen,
                COLOR_YELLOW,
                (
                    int(taxi_x + taxi_size / 2),
                    int(taxi_y + taxi_size / 2),
                ),
                self.cell_size // 8,
            )

    def tick(self, fps: int = 60) -> None:
        """Limit frame rate.

        Args:
            fps: Target frames per second
        """
        self.clock.tick(fps)

    def quit(self) -> None:
        """Clean up pygame resources."""
        pygame.quit()
