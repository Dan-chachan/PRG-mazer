import pygame

# ---------------------- COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (74, 255, 54)
RED = (255, 33, 31)
BLUE = (59, 71, 255)
AQUA = (49, 225, 232)
PINK = (232, 42, 204)
ORANGE = (255, 85, 14)
YELLOW = (232, 194, 55)
DEEP_PURPLE = (35, 24, 46)
GREYISH_PURPLE = (61, 45, 64)


BACK_COL = DEEP_PURPLE
WALL_COL = GREYISH_PURPLE
EXIT_COL = GREEN
ENTRY_COL = RED

PLAYER_COL = PINK
# ---------------------- COLORS

content = {
    "FREE": " ",
    "BASE": "B",
    "WALL": "X",
    "PLAYER": "P",
    "ENTRY": "I",
    "EXIT": "O"
}

MAZE_SIZE = 9

# -------------------------------- WINDOW
GRID_SIZE = 50

WINDOW_WIDTH = GRID_SIZE*MAZE_SIZE
WINDOW_HEIGHT = WINDOW_WIDTH
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
# -------------------------------- WINDOW

SQUARES_WID = WINDOW_WIDTH / GRID_SIZE
SQUARES_HEI = WINDOW_HEIGHT / GRID_SIZE


# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()