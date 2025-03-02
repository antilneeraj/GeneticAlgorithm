import pygame
from components.graphics_components import Ground

WIN_WIDTH = 550
WIN_HEIGHT = 720
GROUND_Y = 500  # Ground level y-coordinate
FPS = 60

WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
GROUND = Ground(WIN_WIDTH, GROUND_Y)
PIPE_LIST = []  # Global list of pipes

# Global counter for number of pipes passed (poles covered)
PIPE_COVERED = 0
