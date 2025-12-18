import pygame
import time
import random
from main import policy, GRID, GRID_SIZE

pygame.init()

CELL_SIZE = 100

GRID = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]

WIDTH = HEIGHT = CELL_SIZE * GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Taxi MDP")

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)

clock = pygame.time.Clock()

def within_grid(loc):
    return 0 <= loc[0] < GRID_SIZE and 0 <= loc[1] < GRID_SIZE

state = ((0,0), ('none', None))

def draw(state):
    screen.fill(WHITE)

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(
                x * CELL_SIZE,
                (GRID_SIZE - 1 - y) * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, BLACK, rect, 2)

    taxi_loc, passenger = state
    tx, ty = taxi_loc

    taxi_x = tx * CELL_SIZE + CELL_SIZE * 0.25
    taxi_y = (GRID_SIZE - 1 - ty) * CELL_SIZE + CELL_SIZE * 0.25
    taxi_size = CELL_SIZE * 0.5

    taxi_rect = pygame.Rect(taxi_x, taxi_y, taxi_size, taxi_size)
    pygame.draw.rect(screen, BLUE, taxi_rect)
    if passenger[0] == 'waiting':
        dest_x = passenger[2][0] * CELL_SIZE + CELL_SIZE * 0.25
        dest_y = (GRID_SIZE - 1 - passenger[2][1]) * CELL_SIZE + CELL_SIZE * 0.25
        dest_rect = pygame.Rect(dest_x, dest_y, taxi_size, taxi_size)
        pygame.draw.rect(screen, RED, dest_rect)
    if passenger[0] == 'in_taxi':
        dest_x = passenger[1][0] * CELL_SIZE + CELL_SIZE * 0.25
        dest_y = (GRID_SIZE - 1 - passenger[1][1]) * CELL_SIZE + CELL_SIZE * 0.25
        dest_rect = pygame.Rect(dest_x, dest_y, taxi_size, taxi_size)
        pygame.draw.rect(screen, RED, dest_rect)

    if passenger[0] == 'waiting':
        px, py = passenger[1]
        pygame.draw.circle(
            screen,
            GREEN,
            (
                px * CELL_SIZE + CELL_SIZE // 2,
                (GRID_SIZE - 1 - py) * CELL_SIZE + CELL_SIZE // 2
            ),
            CELL_SIZE // 8
        )

    elif passenger[0] == 'in_taxi':
        pygame.draw.circle(
            screen,
            YELLOW,
            (
                int(taxi_x + taxi_size / 2),
                int(taxi_y + taxi_size / 2)
            ),
            CELL_SIZE // 8
        )

    pygame.display.flip()


def step(state):
    taxi_loc, passenger = state
    action = policy.get(state, None)
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


origin, destination = random.sample(GRID, 2)
state = ((0,0), ('waiting', origin, destination))
draw(state)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    state = step(state)
    draw(state)
    print(state, policy[state])

    if state[1][0] == 'none' and random.random() < 0.2:
        origin, destination = random.sample(GRID, 2)
        state = (state[0], ('waiting', origin, destination))
    time.sleep(0.4)
    clock.tick(60)

pygame.quit()
