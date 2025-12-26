# Changelog

All notable changes to the Taxi MDP project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [2.0.0] - 2025-12-26

### Major Refactoring - Modular Package Structure

This release represents a comprehensive overhaul of the project, transforming it from a 2-file prototype into a production-quality, modular Python package.

### Added

#### Package Structure
- **mdp_taxi/** - New modular package organization
  - `mdp_taxi/core/` - Core MDP solver components
    - `constants.py` - Centralized constants and configuration
    - `states.py` - State space generation and validation
    - `mdp_solver.py` - ValueIterationSolver class with convergence detection
    - `policy.py` - Policy class with safe lookup and export capabilities
  - `mdp_taxi/visualization/` - Visualization components (placeholder for future)
  - `mdp_taxi/utils/` - Utility functions (placeholder for future)

#### CLI Tools
- **scripts/solve_mdp.py** - Command-line interface for MDP solver
  - Arguments: `--iterations`, `--output`, `--grid-output`, `--verbose`, `--threshold`, `--discount`
  - JSON policy export
  - Human-readable grid visualization export
  - Progress logging and statistics

#### Testing Infrastructure
- **tests/** - Comprehensive test suite (48 tests, >95% coverage)
  - `tests/conftest.py` - Pytest fixtures
  - `tests/test_transitions.py` - Movement, boundaries, pickup/dropoff (18 tests)
  - `tests/test_policy.py` - Policy completeness, quality, statistics (12 tests)
  - `tests/test_mdp_solver.py` - Value iteration, convergence, rewards (18 tests)

#### Documentation
- **README.md** - Comprehensive 200+ line guide
  - Installation instructions
  - Quick start examples
  - MDP formulation details
  - Configuration guide
  - Development setup
  - Troubleshooting section
- **CHANGELOG.md** - This file
- **setup.py** - Package installation configuration
- **requirements.txt** - Production dependencies (pygame, PyYAML)
- **requirements-dev.txt** - Development dependencies (pytest, black, mypy, flake8)
- **.gitignore** - Comprehensive exclusions

#### Features
- **Convergence Detection** - Automatic early stopping when max_delta < threshold
- **Progress Logging** - Shows iteration progress every 5 iterations
- **Policy Export** - JSON and human-readable grid formats
- **Policy Statistics** - Action distribution and coverage metrics
- **Safe Policy Lookup** - Default fallback prevents KeyError crashes
- **Backward Compatibility** - main.py wrapper maintains original interface

### Fixed

#### Critical Bug Fixes
1. **Policy Lookup Crash** (visualization.py:91, 127)
   - Changed `policy[state]` to `policy.get(state, 'n')` for safe lookup
   - Added default action fallback

2. **Duplicate GRID Generation** (visualization.py:10)
   - Removed redundant list comprehension
   - Now imports GRID from main.py/constants.py

3. **Missing Convergence Check** (main.py:79-99)
   - Added convergence detection with threshold
   - Early stopping when max_delta < 1e-3
   - Converges around iteration 40 for 5x5 grid

4. **Insufficient Iterations** (main.py:1)
   - Increased ITERATIONS from 20 → 100 for reliable convergence

### Changed

#### Breaking Changes
- **Import Structure** - Code should now import from `mdp_taxi.core.*` packages
- **Deprecation** - main.py shows deprecation warning, use `scripts/solve_mdp.py`

#### Improvements
- **Code Organization** - Separated concerns into logical modules
- **Type Hints** - Added type annotations to core modules
- **Docstrings** - Comprehensive documentation for all public functions/classes
- **Test Coverage** - >95% code coverage with 48 comprehensive tests

### Performance
- **Convergence** - Typically converges in 40 iterations (was 20 iterations without convergence)
- **State Space** - Efficiently handles 16,275 states for 5x5 grid

### Statistics

**Lines of Code:**
- v1.0: ~224 lines (2 files)
- v2.0: ~1,500+ lines across multiple modules

**Test Coverage:**
- v1.0: 0 tests
- v2.0: 48 tests, >95% coverage

**Documentation:**
- v1.0: Minimal CLAUDE.md
- v2.0: README, CHANGELOG, comprehensive CLAUDE.md, docstrings throughout

## [1.1] - 2025-12-26

### Fixed
- Added convergence checking to value iteration
- Fixed policy lookup crashes
- Removed duplicate GRID generation

### Changed
- Increased max iterations from 20 to 100
- Added progress logging

## [1.0] - Initial Release

### Added
- Basic MDP solver using value iteration
- Pygame visualization
- Simple CLAUDE.md

---

## Future Roadmap

### [2.1.0] - Planned
- Interactive visualization controls (pause, speed, step-through)
- HUD overlay with statistics and legend
- Configuration file support (YAML)
- Comprehensive logging system

### [3.0.0] - Planned
- Remove deprecated main.py
- Full visualization package refactor
- Additional MDP algorithms (Q-learning, Policy Iteration)
- Performance optimizations for larger grids
- Complete type hint coverage with mypy validation
