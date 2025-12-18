ITERATIONS = 20
ACTIONS = ['n', 's', 'e', 'w', 'pick', 'drop']
DISCOUNT_FACTOR = 0.9
GRID_SIZE = 5  # change this to modify the grid size
GRID = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)] 
STATES = []
# init states
for taxi_loc in GRID:
    STATES.append((taxi_loc, ('none', None)))
    for passenger_loc in GRID:
        for dest_loc in GRID:
            STATES.append((taxi_loc, ('waiting', passenger_loc, dest_loc)))
        STATES.append((taxi_loc, ('in_taxi', passenger_loc)))

# state validity check
def within_grid(state):
    return 0 <= state[0] < GRID_SIZE and 0 <= state[1] < GRID_SIZE

# value calculation
def calc_value_action(state, values):
    max_value = float('-inf')
    reward = -1
    best_action = None
    for action in ACTIONS:
        if action == 'n':
            new_state = ( (state[0][0], state[0][1] + 1), state[1] )
        elif action == 's':
            new_state = ( (state[0][0], state[0][1] - 1), state[1] )
        elif action == 'e':
            new_state = ( (state[0][0] + 1, state[0][1]), state[1] )
        elif action == 'w':
            new_state = ( (state[0][0] - 1, state[0][1]), state[1] )
        elif action == 'pick':
            if state[1][0] == 'waiting' and state[0] == state[1][1]:
                reward = 0
                new_state = (state[0], ('in_taxi', state[1][2]))
            else:
                reward = -5
                new_state = state
        elif action == 'drop':
            if state[1][0] == 'in_taxi' and state[0] == state[1][1]:
                reward = 10
                new_state = (state[0], ('none', None))
            else:
                reward = -5
                new_state = state

        # check grid boundaries        
        if not within_grid(new_state[0]):
            new_state = state

        value = 0
        
        # handle arrival of new passengers
        if new_state[1][0] == 'none':
                arrival_value = 0
                for origin in GRID:
                    for dest in GRID:
                        if origin != dest:
                            arrival_value += values[(new_state[0], ('waiting', origin, dest))]
                arrival_value /= (len(GRID) * (len(GRID) - 1))
                value = 0.8 * (reward + DISCOUNT_FACTOR * values[new_state]) + 0.2 * (reward + DISCOUNT_FACTOR * arrival_value)
        else:
            value = reward + DISCOUNT_FACTOR * values[new_state]
        if value > max_value:
            max_value = value
            best_action = action

    return max_value, best_action
    

# initialize values
policy = {}
values = {}
for state in STATES:
    values[state] = 0

# value iteration
for _ in range(ITERATIONS):
    new_values = values.copy()
    for state in STATES:
        new_values[state], policy[state] = calc_value_action(state, values)
    values = new_values

print(values.values(), policy.values())

