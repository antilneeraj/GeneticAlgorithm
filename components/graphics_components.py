import pygame
import random

class Ground:
    def __init__(self, win_width, ground_y):
        self.rect = pygame.Rect(0, ground_y, win_width, 20)
        self.color = (139, 69, 19)  # Brown ground

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Pipe:
    width = 50  # Increased width for better visuals
    opening = 150  # Increased opening for better playability

    def __init__(self, win_width, ground_y):
        self.x = win_width
        self.bottom_height = random.randint(100, 300)
        self.top_height = ground_y - self.bottom_height - self.opening
        self.passed = False
        self.off_screen_flag = False
        self.color = (34, 139, 34)  # Green pipes

    def draw(self, surface, ground_y):
        top_rect = pygame.Rect(self.x, 0, Pipe.width, self.top_height)
        bottom_rect = pygame.Rect(self.x, ground_y - self.bottom_height, Pipe.width, self.bottom_height)
        
        # Adding gradient effect
        pygame.draw.rect(surface, self.color, top_rect)
        pygame.draw.rect(surface, self.color, bottom_rect)
        pygame.draw.rect(surface, (0, 100, 0), top_rect, 3)  # Dark outline
        pygame.draw.rect(surface, (0, 100, 0), bottom_rect, 3)  # Dark outline
        
        # Store these for collision detection if needed
        self.top_rect = top_rect
        self.bottom_rect = bottom_rect

    def update(self):
        self.x -= 2  # Slightly smoother movement
        if self.x + Pipe.width <= 50:
            self.passed = True
        if self.x <= -Pipe.width:
            self.off_screen_flag = True