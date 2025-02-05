import pygame
import random

class Ground:
    def __init__(self, win_width, ground_y):
        self.rect = pygame.Rect(0, ground_y, win_width, 5)
    
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)

class Pipe:
    width = 15
    opening = 100

    def __init__(self, win_width, ground_y):
        self.x = win_width
        self.bottom_height = random.randint(10, 300)
        self.top_height = ground_y - self.bottom_height - self.opening
        self.passed = False
        self.off_screen_flag = False
    
    def draw(self, surface, ground_y):
        top_rect = pygame.Rect(self.x, 0, Pipe.width, self.top_height)
        bottom_rect = pygame.Rect(self.x, ground_y - self.bottom_height, Pipe.width, self.bottom_height)
        pygame.draw.rect(surface, (255, 255, 255), top_rect)
        pygame.draw.rect(surface, (255, 255, 255), bottom_rect)
        # Store these for collision detection if needed
        self.top_rect = top_rect
        self.bottom_rect = bottom_rect

    def update(self):
        self.x -= 1
        if self.x + Pipe.width <= 50:
            self.passed = True
        if self.x <= -Pipe.width:
            self.off_screen_flag = True
