# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Taxi MDP (Markov Decision Process) implementation that solves the classic taxi problem using value iteration. The project simulates a taxi navigating a grid world to pick up and drop off passengers.

**Current Version**: 1.1 (Enhanced with bug fixes, tests, and documentation)

## Quick Start Commands

```bash
# Setup
pip install -r requirements.txt        # Install dependencies
pip install -r requirements-dev.txt    # Install dev dependencies (testing)

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Run MDP solver (computes optimal policy with convergence)
python main.py

# Run visualization (requires pygame)
python visualization.py

# Run tests
pytest tests/ -v                       # All tests
pytest tests/ --cov=. --cov-report=html  # With coverage report
```

## Dependencies

### Production
- Python 3.7+
- pygame>=2.5.0 (for visualization)
- PyYAML>=6.0 (for future config support)

### Development
- pytest>=7.0.0
- pytest-cov>=4.0.0
- black>=23.0.0
- mypy>=1.0.0
- flake8>=6.0.0

## Architecture

**main.py** - MDP solver using value iteration
- **State space**: `(taxi_location, passenger_status)` where passenger_status is:
  - `('none', None)` - no passenger
  - `('waiting', origin, destination)` - passenger waiting at origin
  - `('in_taxi', destination)` - passenger picked up, heading to destination
- **Actions**: `n`, `s`, `e`, `w` (movement), `pick`, `drop`
- **Reward structure**:
  - -1 per step (movement cost)
  - -5 for invalid pick/drop
  - 0 for successful pickup
  - +10 for successful delivery
- **Convergence checking**: Automatically stops when max value change < 1e-3
- **Progress logging**: Shows iteration progress every 5 iterations
- Exports `policy` dict, `values` dict, and grid constants for visualization

**visualization.py** - Pygame-based simulation
- Imports computed `policy` from main.py with safe lookup (no crashes on missing states)
- **Visual legend**:
  - Blue square = taxi
  - Green circle = waiting passenger
  - Red square = destination
  - Yellow circle = passenger in taxi
- Runs simulation loop applying policy actions with 0.4s delay
- Probabilistic passenger arrivals (20% chance when taxi is empty)

**tests/** - Comprehensive test suite
- `test_transitions.py` - Tests for movement, boundary collisions, pickup/dropoff logic
- `test_policy.py` - Tests for policy completeness, lookup safety, quality
- `test_mdp_solver.py` - Tests for value iteration, convergence, rewards
- **Coverage**: 48 tests with >95% coverage

## Key Constants

### main.py
- `GRID_SIZE` = 5 - Grid dimensions (5x5 grid)
- `ITERATIONS` = 100 - Max iterations (increased from 20 for reliable convergence)
- `DISCOUNT_FACTOR` = 0.9 - Future reward discounting (γ)
- `CONVERGENCE_THRESHOLD` = 1e-3 - Early stopping threshold

### visualization.py
- `CELL_SIZE` = 100 - Grid cell size in pixels
- Simulation speed: 0.4s delay per step (line 133)

## Recent Bug Fixes (v1.1)

1. **✅ Fixed policy lookup crash** (visualization.py:91, 127)
   - Changed `policy[state]` to `policy.get(state, 'n')` for safe lookup with default

2. **✅ Fixed duplicate GRID generation** (visualization.py:10)
   - Removed duplicate list comprehension, using import from main.py

3. **✅ Added convergence detection** (main.py:79-99)
   - Early stopping when max_delta < CONVERGENCE_THRESHOLD
   - Progress logging every 5 iterations
   - Converges around iteration 40 for 5x5 grid

4. **✅ Increased max iterations**
   - Changed from 20 to 100 to ensure convergence for larger grids

## Development Guidelines

### Running Tests
```bash
pytest tests/ -v                    # Verbose output
pytest tests/test_policy.py -v     # Specific file
pytest tests/ --cov=. --cov-report=html  # Coverage report
```

### Code Quality
```bash
black main.py visualization.py tests/  # Format code
flake8 main.py visualization.py        # Lint
mypy main.py                           # Type check
```

### State Space Size
For grid size `n`:
- States with 'none': n²
- States with 'waiting': n² × n² × n² = n⁶
- States with 'in_taxi': n² × n² = n⁴
- **Total**: n² + n⁶ + n⁴

For 5x5 grid: **16,275 states**

## Future Enhancements (Planned)

See README.md for the full roadmap, including:
- Modular package structure (mdp_taxi/)
- Configuration file support (YAML)
- Policy export to JSON
- Interactive visualization controls (pause, speed, step-through)
- CLI scripts for solver and visualization
- Type hints throughout codebase
- HUD overlay with statistics and legend
- Additional MDP algorithms

## Common Issues

### Issue: "ModuleNotFoundError: No module named 'pygame'"
**Solution**: Install pygame: `pip install pygame` or use pre-built wheel

### Issue: "Convergence takes too long"
**Solution**: Increase `CONVERGENCE_THRESHOLD` or decrease `GRID_SIZE`

### Issue: "Tests fail with pygame import error"
**Note**: One test is skipped if pygame isn't installed (expected behavior)
