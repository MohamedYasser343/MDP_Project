"""Simulation control handling (pause, speed, step-through)."""
from typing import Optional
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

from ..core.constants import DEFAULT_STEP_DELAY


class SimulationController:
    """Manages user input and simulation control.

    Attributes:
        paused: Whether simulation is paused
        speed: Delay between steps in seconds
        step_mode: Whether to advance one step (when paused)
        quit_requested: Whether user requested to quit
        reset_requested: Whether user requested to reset
        show_help: Whether to show help overlay
    """

    def __init__(self, initial_speed: float = DEFAULT_STEP_DELAY):
        """Initialize simulation controller.

        Args:
            initial_speed: Initial delay between steps in seconds
        """
        self.paused = False
        self.speed = initial_speed
        self.step_mode = False
        self.quit_requested = False
        self.reset_requested = False
        self.show_help = False

        # Speed limits
        self.min_speed = 0.05  # Fastest (50ms)
        self.max_speed = 2.0   # Slowest (2s)
        self.speed_step = 0.05  # Speed change increment

    def handle_events(self) -> None:
        """Process pygame events and update control state.

        Call this once per frame to handle user input.
        """
        if not PYGAME_AVAILABLE:
            return

        self.step_mode = False  # Reset step mode each frame
        self.reset_requested = False  # Reset request each frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True
            elif event.type == pygame.KEYDOWN:
                self._handle_keypress(event.key)

    def _handle_keypress(self, key: int) -> None:
        """Handle keyboard input.

        Args:
            key: Pygame key code

        Controls:
            SPACE: Pause/Resume
            UP: Increase speed (decrease delay)
            DOWN: Decrease speed (increase delay)
            RIGHT: Step forward one action (when paused)
            R: Reset simulation
            H: Toggle help overlay
            Q/ESC: Quit
        """
        if key == pygame.K_SPACE:
            self.paused = not self.paused
        elif key == pygame.K_UP:
            self.speed = max(self.min_speed, self.speed - self.speed_step)
        elif key == pygame.K_DOWN:
            self.speed = min(self.max_speed, self.speed + self.speed_step)
        elif key == pygame.K_RIGHT and self.paused:
            self.step_mode = True
        elif key == pygame.K_r:
            self.reset_requested = True
        elif key == pygame.K_h:
            self.show_help = not self.show_help
        elif key in (pygame.K_q, pygame.K_ESCAPE):
            self.quit_requested = True

    def should_advance(self) -> bool:
        """Check if simulation should advance to next step.

        Returns:
            True if simulation should advance, False otherwise
        """
        if self.quit_requested:
            return False
        if self.paused:
            return self.step_mode
        return True

    def get_status_text(self) -> str:
        """Get current status as text.

        Returns:
            String describing current control state
        """
        status = []
        if self.paused:
            status.append("PAUSED")
        status.append(f"Speed: {self.speed:.2f}s")
        return " | ".join(status)

    def get_help_text(self) -> list:
        """Get help text for controls.

        Returns:
            List of help text lines
        """
        return [
            "=== CONTROLS ===",
            "SPACE: Pause/Resume",
            "UP/DOWN: Adjust speed",
            "RIGHT: Step (when paused)",
            "R: Reset simulation",
            "H: Toggle this help",
            "Q/ESC: Quit",
            "",
            f"Current speed: {self.speed:.2f}s",
            f"Status: {'PAUSED' if self.paused else 'RUNNING'}",
        ]
