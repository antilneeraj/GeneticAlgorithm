import pygame
import random
from config.settings import WINDOW, PIPE_LIST, GROUND_Y
from agents.neural_net import NeuralNet

class Agent:
    def __init__(self):
        self.x, self.y = 50, 200
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.velocity = 0
        self.alive = True
        self.lifespan = 0
        self.fitness = 0
        self.vision = [0.5, 1, 0.5]
        self.decision = None
        self.num_inputs = 3
        self.brain = NeuralNet(self.num_inputs)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def collides_with_ground(self, ground_rect):
        return self.rect.colliderect(ground_rect)

    def collides_with_pipe(self):
        for pipe in PIPE_LIST:
            # Check collision with both top and bottom of the pipe
            if self.rect.colliderect(pipe.top_rect) or self.rect.colliderect(pipe.bottom_rect):
                return True
        return False

    def update(self, ground_rect):
        if not (self.collides_with_ground(ground_rect) or self.collides_with_pipe()):
            self.velocity += 0.25
            self.velocity = min(self.velocity, 5)
            self.rect.y += self.velocity
            self.lifespan += 1
        else:
            self.alive = False
            self.velocity = 0

    def flap(self):
        if self.rect.y > 30:
            self.velocity = -5

    def look(self):
        if PIPE_LIST:
            pipe = self.closest_pipe()
            # Normalize distances (assume max distance ~500 for normalization)
            self.vision[0] = max(0, self.rect.centery - pipe.top_rect.bottom) / 500
            self.vision[1] = max(0, pipe.x - self.rect.centerx) / 500
            self.vision[2] = max(0, pipe.bottom_rect.top - self.rect.centery) / 500
            # (Optional) draw vision lines
            pygame.draw.line(WINDOW, self.color, self.rect.center, (self.rect.centerx, pipe.top_rect.bottom))
            pygame.draw.line(WINDOW, self.color, self.rect.center, (pipe.x, self.rect.centery))
            pygame.draw.line(WINDOW, self.color, self.rect.center, (self.rect.centerx, pipe.bottom_rect.top))
    
    def closest_pipe(self):
        for pipe in PIPE_LIST:
            if not pipe.passed:
                return pipe
        return PIPE_LIST[0] if PIPE_LIST else None

    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.73:
            self.flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone_agent = Agent()
        clone_agent.brain = self.brain.clone()
        return clone_agent
