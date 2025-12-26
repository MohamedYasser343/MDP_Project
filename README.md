# Taxi MDP - Markov Decision Process Solver

A Python implementation of the classic Taxi problem using value iteration to compute the optimal policy. This project demonstrates reinforcement learning concepts with an interactive visualization.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [MDP Formulation](#mdp-formulation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)

## Overview

The Taxi MDP problem is a classic reinforcement learning benchmark where a taxi must navigate a grid world to pick up and drop off passengers at various locations. The agent must learn an optimal policy to maximize rewards while minimizing costs.

### Features

- **Value Iteration Solver**: Computes optimal policy using dynamic programming
- **Convergence Detection**: Automatically stops when the policy has converged
- **Interactive Visualization**: Pygame-based visual simulation of the computed policy
- **Configurable Parameters**: Easy-to-modify grid size, rewards, and hyperparameters
- **Comprehensive Testing**: Unit tests for correctness validation

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone or download this repository:
```bash
cd MDP_Project
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

For development (includes testing and linting tools):
```bash
pip install -r requirements-dev.txt
```

## Quick Start

### 1. Compute the Optimal Policy

Run the MDP solver to compute the optimal taxi policy:

```bash
python main.py
```

**Output:**
```
Iteration 0: max_delta=10.000000
Iteration 5: max_delta=5.904900
...
Iteration 40: max_delta=0.000679
Converged at iteration 40 (delta=6.79e-04)
Value iteration complete. Final policy computed.
```

### 2. Visualize the Policy

Run the interactive visualization:

```bash
python visualization.py
```

**Controls:**
- Close the window or press the X button to quit

**Visual Legend:**
- **Blue square**: Taxi
- **Green circle**: Passenger waiting at pickup location
- **Yellow circle**: Passenger inside the taxi
- **Red square**: Destination location

## MDP Formulation

### State Space

Each state is represented as a tuple `(taxi_location, passenger_status)`:

- **taxi_location**: `(x, y)` coordinates on the grid
- **passenger_status**: One of:
  - `('none', None)` - No passenger present
  - `('waiting', origin, destination)` - Passenger waiting at origin
  - `('in_taxi', destination)` - Passenger picked up, heading to destination

For a 5x5 grid, there are **16,275 total states**:
- 25 states with no passenger
- 15,625 states with waiting passengers (25 × 25 × 25)
- 625 states with passenger in taxi (25 × 25)

### Action Space

Six possible actions:
- `'n'` - Move North (+y direction)
- `'s'` - Move South (-y direction)
- `'e'` - Move East (+x direction)
- `'w'` - Move West (-x direction)
- `'pick'` - Pick up passenger (only valid when at passenger's origin)
- `'drop'` - Drop off passenger (only valid when at passenger's destination)

### Reward Structure

- **-1**: Step cost (each movement action)
- **0**: Successful pickup
- **+10**: Successful delivery
- **-5**: Invalid pickup or dropoff attempt

### Transition Dynamics

- **Deterministic movements**: Actions always succeed unless hitting grid boundaries
- **Boundary collisions**: Taxi stays in place if attempting to move outside the grid
- **Passenger arrivals**: 20% probability of new passenger arriving when taxi is empty

### Discount Factor

γ = 0.9 (balances immediate vs. future rewards)

## Project Structure

```
MDP_Project/
├── main.py                 # MDP solver with value iteration
├── visualization.py        # Pygame-based visualization
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── .gitignore             # Git ignore patterns
├── README.md              # This file
├── CLAUDE.md              # Guide for Claude Code
└── tests/                 # Unit tests (to be added)
    ├── conftest.py
    ├── test_transitions.py
    ├── test_policy.py
    └── test_mdp_solver.py
```

## Configuration

### Modifying Parameters

Edit constants in `main.py`:

```python
GRID_SIZE = 5               # Grid dimensions (5x5 default)
ITERATIONS = 100            # Max iterations for value iteration
DISCOUNT_FACTOR = 0.9       # Discount factor (γ)
CONVERGENCE_THRESHOLD = 1e-3  # Early stopping threshold
```

### Reward Tuning

In the `calc_value_action()` function:

```python
reward = -1    # Step cost
reward = 0     # Successful pickup
reward = 10    # Successful delivery
reward = -5    # Invalid action penalty
```

### Visualization Settings

Edit constants in `visualization.py`:

```python
CELL_SIZE = 100  # Size of each grid cell in pixels
```

Adjust simulation speed at line 133:
```python
time.sleep(0.4)  # Delay between steps (seconds)
```

## Development

### Setting Up Development Environment

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run code formatting:
```bash
black main.py visualization.py
```

3. Run linting:
```bash
flake8 main.py visualization.py
```

4. Run type checking:
```bash
mypy main.py visualization.py
```

### Recent Improvements

**Version 1.1 (Current)**
- ✅ Added convergence detection with early stopping
- ✅ Fixed policy lookup crash in visualization
- ✅ Removed duplicate GRID generation
- ✅ Increased max iterations to 100 for reliable convergence
- ✅ Added progress logging during value iteration

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_transitions.py -v
```

### Test Coverage

The test suite covers:
- State transitions for all actions
- Boundary collision handling
- Pickup/dropoff logic
- Policy completeness
- Value iteration convergence
- Reward calculations

## Algorithm Details

### Value Iteration

The solver uses the Bellman equation to iteratively improve value estimates:

```
V(s) = max_a [R(s,a) + γ * Σ P(s'|s,a) * V(s')]
```

Where:
- `V(s)` = value of state s
- `R(s,a)` = immediate reward for action a in state s
- `γ` = discount factor (0.9)
- `P(s'|s,a)` = transition probability from s to s' given action a

### Convergence Criterion

The algorithm stops when the maximum value change across all states falls below the threshold:

```
max_s |V_new(s) - V_old(s)| < ε
```

Where ε = 0.001 (CONVERGENCE_THRESHOLD)

## Troubleshooting

### Issue: ValueError during visualization

**Cause**: Policy dictionary may be incomplete for some states.

**Solution**: This is now fixed with safe dict lookup using `.get(state, 'n')` which defaults to moving north if state is missing.

### Issue: Convergence takes too long

**Cause**: Grid size or threshold may be too aggressive.

**Solution**: Increase `CONVERGENCE_THRESHOLD` or decrease `GRID_SIZE` for faster iteration.

### Issue: Pygame window not responding

**Cause**: The main loop runs continuously.

**Solution**: Close the window using the X button or Ctrl+C in the terminal.

## Contributing

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linters
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use `black` for code formatting
- Add docstrings to all functions
- Include type hints where possible
- Write tests for new functionality

## License

This project is available for educational purposes.

## Acknowledgments

- Inspired by the classic Taxi domain from reinforcement learning literature
- Built as a demonstration of dynamic programming and MDP solving techniques

## Future Enhancements

Planned improvements:
- [ ] Modular package structure with `mdp_taxi/` directory
- [ ] Configuration file support (YAML/JSON)
- [ ] Policy export to JSON
- [ ] Interactive visualization controls (pause, speed adjustment)
- [ ] Performance optimizations for larger grids
- [ ] Type hints throughout codebase
- [ ] Comprehensive logging system
- [ ] CLI scripts for solver and visualization
- [ ] HUD overlay with statistics
- [ ] Additional MDP algorithms (Q-learning, Policy Iteration)

---

For questions or issues, please refer to CLAUDE.md for development guidance.
