"""HUD overlay with state info, legend, and statistics."""
from typing import Dict, Optional, Tuple, List
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

from ..core.constants import (
    COLOR_WHITE,
    COLOR_BLACK,
    COLOR_BLUE,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_YELLOW,
)


class HUDDisplay:
    """Displays on-screen information overlay.

    Provides visual feedback for:
    - Current state (taxi position, passenger status)
    - Current action being taken
    - Statistics (steps, rewards, deliveries)
    - Control hints
    - Color legend

    Attributes:
        screen: Pygame display surface
        font: Font for text rendering
        small_font: Smaller font for secondary text
    """

    def __init__(self, screen, font_size: int = 24, small_font_size: int = 18):
        """Initialize HUD display.

        Args:
            screen: Pygame display surface
            font_size: Size for main text
            small_font_size: Size for secondary text
        """
        if not PYGAME_AVAILABLE:
            raise ImportError("pygame is required for HUD display")

        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.Font(None, font_size)
        self.small_font = pygame.font.Font(None, small_font_size)

        # Colors
        self.bg_color = (0, 0, 0, 180)  # Semi-transparent black
        self.text_color = COLOR_WHITE
        self.highlight_color = COLOR_YELLOW

    def draw_legend(self, x: int = 10, y: int = 10) -> None:
        """Draw color legend in top-left corner.

        Args:
            x: X position for legend
            y: Y position for legend
        """
        legend_items = [
            (COLOR_BLUE, "Taxi"),
            (COLOR_GREEN, "Passenger (waiting)"),
            (COLOR_YELLOW, "Passenger (in taxi)"),
            (COLOR_RED, "Destination"),
        ]

        # Draw semi-transparent background
        padding = 5
        line_height = 20
        max_width = 180
        bg_height = len(legend_items) * line_height + padding * 2 + 20

        bg_surface = pygame.Surface((max_width, bg_height), pygame.SRCALPHA)
        bg_surface.fill(self.bg_color)
        self.screen.blit(bg_surface, (x, y))

        # Draw title
        title = self.small_font.render("LEGEND", True, self.highlight_color)
        self.screen.blit(title, (x + padding, y + padding))

        # Draw legend items
        for i, (color, label) in enumerate(legend_items):
            item_y = y + padding + 20 + i * line_height

            # Draw color square
            pygame.draw.rect(self.screen, color, (x + padding, item_y, 15, 15))
            pygame.draw.rect(self.screen, COLOR_WHITE, (x + padding, item_y, 15, 15), 1)

            # Draw label
            text = self.small_font.render(label, True, self.text_color)
            self.screen.blit(text, (x + padding + 20, item_y))

    def draw_state_info(
        self,
        state: Tuple,
        action: Optional[str],
        x: int = 10,
        y: int = 120
    ) -> None:
        """Draw current state and action information.

        Args:
            state: Current state tuple
            action: Current action being taken
            x: X position
            y: Y position
        """
        taxi_loc, passenger = state

        # Format state info
        lines = [
            f"Taxi: ({taxi_loc[0]}, {taxi_loc[1]})",
        ]

        if passenger[0] == "none":
            lines.append("Passenger: None")
        elif passenger[0] == "waiting":
            lines.append(f"Passenger: Waiting at ({passenger[1][0]}, {passenger[1][1]})")
            lines.append(f"Destination: ({passenger[2][0]}, {passenger[2][1]})")
        elif passenger[0] == "in_taxi":
            lines.append("Passenger: In taxi")
            lines.append(f"Destination: ({passenger[1][0]}, {passenger[1][1]})")

        if action:
            action_names = {
                "n": "North ↑",
                "s": "South ↓",
                "e": "East →",
                "w": "West ←",
                "pick": "Pick up",
                "drop": "Drop off",
            }
            lines.append(f"Action: {action_names.get(action, action)}")

        # Draw background
        padding = 5
        line_height = 18
        max_width = 200
        bg_height = len(lines) * line_height + padding * 2 + 20

        bg_surface = pygame.Surface((max_width, bg_height), pygame.SRCALPHA)
        bg_surface.fill(self.bg_color)
        self.screen.blit(bg_surface, (x, y))

        # Draw title
        title = self.small_font.render("STATE", True, self.highlight_color)
        self.screen.blit(title, (x + padding, y + padding))

        # Draw lines
        for i, line in enumerate(lines):
            text = self.small_font.render(line, True, self.text_color)
            self.screen.blit(text, (x + padding, y + padding + 20 + i * line_height))

    def draw_statistics(
        self,
        step_count: int,
        total_reward: float,
        deliveries: int,
        x: int = 10,
        y: int = 280
    ) -> None:
        """Draw performance statistics.

        Args:
            step_count: Number of steps taken
            total_reward: Total accumulated reward
            deliveries: Number of successful deliveries
            x: X position
            y: Y position
        """
        avg_reward = total_reward / step_count if step_count > 0 else 0

        lines = [
            f"Steps: {step_count}",
            f"Deliveries: {deliveries}",
            f"Total Reward: {total_reward:.1f}",
            f"Avg Reward: {avg_reward:.2f}",
        ]

        # Draw background
        padding = 5
        line_height = 18
        max_width = 160
        bg_height = len(lines) * line_height + padding * 2 + 20

        bg_surface = pygame.Surface((max_width, bg_height), pygame.SRCALPHA)
        bg_surface.fill(self.bg_color)
        self.screen.blit(bg_surface, (x, y))

        # Draw title
        title = self.small_font.render("STATISTICS", True, self.highlight_color)
        self.screen.blit(title, (x + padding, y + padding))

        # Draw lines
        for i, line in enumerate(lines):
            text = self.small_font.render(line, True, self.text_color)
            self.screen.blit(text, (x + padding, y + padding + 20 + i * line_height))

    def draw_controls_hint(
        self,
        paused: bool,
        speed: float,
        x: Optional[int] = None,
        y: int = 10
    ) -> None:
        """Draw control hints in top-right corner.

        Args:
            paused: Whether simulation is paused
            speed: Current speed (delay in seconds)
            x: X position (default: right side)
            y: Y position
        """
        screen_width = self.screen.get_width()
        x = x if x is not None else screen_width - 160

        lines = [
            "SPACE: Pause",
            "↑/↓: Speed",
            "→: Step",
            "R: Reset",
            "H: Help",
            "Q: Quit",
            "",
            f"Speed: {speed:.2f}s",
            "PAUSED" if paused else "RUNNING",
        ]

        # Draw background
        padding = 5
        line_height = 16
        max_width = 150
        bg_height = len(lines) * line_height + padding * 2 + 20

        bg_surface = pygame.Surface((max_width, bg_height), pygame.SRCALPHA)
        bg_surface.fill(self.bg_color)
        self.screen.blit(bg_surface, (x, y))

        # Draw title
        title = self.small_font.render("CONTROLS", True, self.highlight_color)
        self.screen.blit(title, (x + padding, y + padding))

        # Draw lines
        for i, line in enumerate(lines):
            color = self.highlight_color if line in ("PAUSED", "RUNNING") else self.text_color
            text = self.small_font.render(line, True, color)
            self.screen.blit(text, (x + padding, y + padding + 20 + i * line_height))

    def draw_help_overlay(self, help_lines: List[str]) -> None:
        """Draw full-screen help overlay.

        Args:
            help_lines: List of help text lines
        """
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        # Draw help text centered
        line_height = 25
        start_y = (screen_height - len(help_lines) * line_height) // 2

        for i, line in enumerate(help_lines):
            color = self.highlight_color if line.startswith("===") else self.text_color
            text = self.font.render(line, True, color)
            text_rect = text.get_rect(center=(screen_width // 2, start_y + i * line_height))
            self.screen.blit(text, text_rect)
