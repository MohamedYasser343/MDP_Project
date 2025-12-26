"""Tests for the new modular package structure."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestConstants:
    """Test constants module."""

    def test_constants_import(self):
        """Test that constants can be imported."""
        from mdp_taxi.core.constants import (
            GRID_SIZE,
            GRID,
            ACTIONS,
            DISCOUNT_FACTOR,
            MAX_ITERATIONS,
            CONVERGENCE_THRESHOLD,
        )

        assert GRID_SIZE == 5
        assert len(GRID) == 25
        assert len(ACTIONS) == 6
        assert DISCOUNT_FACTOR == 0.9
        assert MAX_ITERATIONS == 100
        assert CONVERGENCE_THRESHOLD == 1e-3

    def test_reward_constants(self):
        """Test reward constants."""
        from mdp_taxi.core.constants import (
            REWARD_STEP,
            REWARD_INVALID_ACTION,
            REWARD_SUCCESSFUL_PICKUP,
            REWARD_SUCCESSFUL_DELIVERY,
        )

        assert REWARD_STEP == -1
        assert REWARD_INVALID_ACTION == -5
        assert REWARD_SUCCESSFUL_PICKUP == 0
        assert REWARD_SUCCESSFUL_DELIVERY == 10

    def test_color_constants(self):
        """Test color constants."""
        from mdp_taxi.core.constants import (
            COLOR_WHITE,
            COLOR_BLACK,
            COLOR_BLUE,
            COLOR_GREEN,
            COLOR_RED,
            COLOR_YELLOW,
        )

        assert COLOR_WHITE == (255, 255, 255)
        assert COLOR_BLACK == (0, 0, 0)
        assert COLOR_BLUE == (0, 0, 255)


class TestStates:
    """Test states module."""

    def test_generate_states(self):
        """Test state generation."""
        from mdp_taxi.core.states import generate_states

        states = generate_states()
        assert len(states) == 16275  # For 5x5 grid

    def test_within_grid(self):
        """Test within_grid function."""
        from mdp_taxi.core.states import within_grid

        assert within_grid((0, 0))
        assert within_grid((2, 2))
        assert within_grid((4, 4))
        assert not within_grid((-1, 0))
        assert not within_grid((5, 0))
        assert not within_grid((0, 5))


class TestMDPSolver:
    """Test MDP solver class."""

    def test_solver_creation(self):
        """Test solver instantiation."""
        from mdp_taxi.core.mdp_solver import ValueIterationSolver

        solver = ValueIterationSolver()
        assert solver.discount_factor == 0.9
        assert solver.convergence_threshold == 1e-3
        assert len(solver.states) == 16275

    def test_solver_custom_params(self):
        """Test solver with custom parameters."""
        from mdp_taxi.core.mdp_solver import ValueIterationSolver

        solver = ValueIterationSolver(
            discount_factor=0.95,
            convergence_threshold=1e-4,
        )
        assert solver.discount_factor == 0.95
        assert solver.convergence_threshold == 1e-4

    def test_solver_solve(self):
        """Test solver execution."""
        from mdp_taxi.core.mdp_solver import ValueIterationSolver

        solver = ValueIterationSolver()
        values, policy, metadata = solver.solve(max_iterations=50)

        assert isinstance(values, dict)
        assert isinstance(policy, dict)
        assert isinstance(metadata, dict)
        assert "iterations" in metadata
        assert "converged" in metadata
        assert "final_delta" in metadata

    def test_solver_returns_valid_policy(self):
        """Test that solver returns valid actions."""
        from mdp_taxi.core.mdp_solver import ValueIterationSolver
        from mdp_taxi.core.constants import ACTIONS

        solver = ValueIterationSolver()
        _, policy, _ = solver.solve(max_iterations=50)

        for state, action in policy.items():
            assert action in ACTIONS


class TestPolicy:
    """Test Policy class."""

    def test_policy_creation(self):
        """Test Policy instantiation."""
        from mdp_taxi.core.policy import Policy

        policy_dict = {((0, 0), ("none", None)): "n"}
        policy = Policy(policy_dict)

        assert len(policy) == 1
        assert ((0, 0), ("none", None)) in policy

    def test_policy_get_action(self):
        """Test safe action retrieval."""
        from mdp_taxi.core.policy import Policy

        policy_dict = {((0, 0), ("none", None)): "n"}
        policy = Policy(policy_dict)

        # Existing state
        assert policy.get_action(((0, 0), ("none", None))) == "n"

        # Missing state - should return default
        assert policy.get_action(((5, 5), ("none", None))) == "n"

        # Missing state with custom default
        assert policy.get_action(((5, 5), ("none", None)), "e") == "e"

    def test_policy_statistics(self):
        """Test policy statistics."""
        from mdp_taxi.core.policy import Policy

        policy_dict = {
            ((0, 0), ("none", None)): "n",
            ((1, 1), ("none", None)): "n",
            ((2, 2), ("none", None)): "e",
        }
        policy = Policy(policy_dict)

        stats = policy.get_statistics()
        assert stats["total_states"] == 3
        assert stats["action_distribution"]["n"] == 2
        assert stats["action_distribution"]["e"] == 1

    def test_policy_validate(self):
        """Test policy validation."""
        from mdp_taxi.core.policy import Policy

        # Valid policy
        policy_dict = {((0, 0), ("none", None)): "n"}
        policy = Policy(policy_dict)
        assert policy.validate()

        # Empty policy
        empty_policy = Policy({})
        assert not empty_policy.validate()


class TestIOUtils:
    """Test I/O utilities."""

    def test_get_default_config_path(self):
        """Test default config path retrieval."""
        from mdp_taxi.utils.io_utils import get_default_config_path

        path = get_default_config_path()
        assert path.exists()
        assert path.name == "default_config.yaml"

    def test_load_config(self):
        """Test configuration loading."""
        pytest.importorskip("yaml", reason="PyYAML not installed")
        from mdp_taxi.utils.io_utils import load_config

        config = load_config()

        assert "mdp" in config
        assert "rewards" in config
        assert "visualization" in config
        assert config["mdp"]["grid_size"] == 5

    def test_get_config_value(self):
        """Test nested config value retrieval."""
        from mdp_taxi.utils.io_utils import get_config_value

        config = {"mdp": {"grid_size": 5, "nested": {"value": 10}}}

        assert get_config_value(config, "mdp.grid_size") == 5
        assert get_config_value(config, "mdp.nested.value") == 10
        assert get_config_value(config, "mdp.missing", 42) == 42

    def test_merge_configs(self):
        """Test configuration merging."""
        from mdp_taxi.utils.io_utils import merge_configs

        base = {"a": 1, "b": {"c": 2}}
        override = {"b": {"c": 3, "d": 4}}

        merged = merge_configs(base, override)
        assert merged["a"] == 1
        assert merged["b"]["c"] == 3
        assert merged["b"]["d"] == 4


class TestLogging:
    """Test logging utilities."""

    def test_setup_logging(self):
        """Test logging setup."""
        from mdp_taxi.utils.logging_config import setup_logging
        import logging

        logger = setup_logging(level="DEBUG")
        assert logger.level == logging.DEBUG

    def test_get_logger(self):
        """Test logger retrieval."""
        from mdp_taxi.utils.logging_config import get_logger

        logger = get_logger("test")
        assert logger.name == "mdp_taxi.test"

        logger2 = get_logger("mdp_taxi.test2")
        assert logger2.name == "mdp_taxi.test2"


class TestVisualizationModules:
    """Test visualization module imports (without pygame)."""

    def test_renderer_import(self):
        """Test renderer module import."""
        # This should not fail even without pygame
        from mdp_taxi.visualization import renderer

        assert hasattr(renderer, "TaxiRenderer")
        assert hasattr(renderer, "PYGAME_AVAILABLE")

    def test_controls_import(self):
        """Test controls module import."""
        from mdp_taxi.visualization import controls

        assert hasattr(controls, "SimulationController")

    def test_display_import(self):
        """Test display module import."""
        from mdp_taxi.visualization import display

        assert hasattr(display, "HUDDisplay")
