"""Core constants for the Taxi MDP environment."""

# Grid configuration
GRID_SIZE = 5
GRID = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]

# Actions
ACTIONS = ['n', 's', 'e', 'w', 'pick', 'drop']

# MDP parameters
DISCOUNT_FACTOR = 0.9
MAX_ITERATIONS = 100
CONVERGENCE_THRESHOLD = 1e-3  # Early stopping threshold

# Rewards
REWARD_STEP = -1
REWARD_INVALID_ACTION = -5
REWARD_SUCCESSFUL_PICKUP = 0
REWARD_SUCCESSFUL_DELIVERY = 10

# Passenger arrival probability (when taxi is empty)
PASSENGER_ARRIVAL_PROB = 0.2

# Visualization constants
CELL_SIZE = 100
FPS = 60
DEFAULT_STEP_DELAY = 0.4  # seconds between simulation steps

# Colors (RGB)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)
