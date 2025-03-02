import pygame
import random
from config.settings import WINDOW, PIPE_LIST, GROUND_Y
from agents.neural_net import NeuralNet

class Agent:
    def __init__(self):
        self.x, self.y = 50, 200
        self.radius = 10 
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
        pygame.draw.circle(surface, self.color, (self.x, int(self.y)), self.radius)
    
    def collides_with_ground(self, ground_rect):
        return self.y + self.radius >= ground_rect.top

    def collides_with_pipe(self):
        for pipe in PIPE_LIST:
            if pipe.top_rect.collidepoint(self.x, self.y) or pipe.bottom_rect.collidepoint(self.x, self.y):
                return True
        return False

    def update(self, ground_rect):
        if not (self.collides_with_ground(ground_rect) or self.collides_with_pipe()):
            self.velocity += 0.5
            self.velocity = min(self.velocity, 7)
            self.y += self.velocity
            self.lifespan += 1
        else:
            self.alive = False
            self.velocity = 0

    def flap(self):
        if self.y > 30:
            self.velocity = -7

    def look(self):
        if PIPE_LIST:
            pipe = self.closest_pipe()
            # Normalize distances (assume max distance ~500 for normalization)
            self.vision[0] = max(0, self.y - pipe.top_rect.bottom) / 500
            self.vision[1] = max(0, pipe.x - self.x) / 500
            self.vision[2] = max(0, pipe.bottom_rect.top - self.y) / 500

            # Visualizing navigation lines with color coding:
            # Red if the horizontal distance is small, yellow for medium, green for safe.
            line_color = (255, 0, 0) if self.vision[1] < 0.3 else (255, 255, 0) if self.vision[1] < 0.6 else (0, 255, 0)
            
            # Draw three lines from the agent's center to key points on the pipe
            pygame.draw.line(WINDOW, line_color, (self.x, self.y), (self.x, pipe.top_rect.bottom), 2)
            pygame.draw.line(WINDOW, line_color, (self.x, self.y), (pipe.x, self.y), 2)
            pygame.draw.line(WINDOW, line_color, (self.x, self.y), (self.x, pipe.bottom_rect.top), 2)
    
    def closest_pipe(self):
        for pipe in PIPE_LIST:
            if not pipe.passed:
                return pipe
        return PIPE_LIST[0] if PIPE_LIST else None

    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.5:
            self.flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone_agent = Agent()
        clone_agent.brain = self.brain.clone()
        return clone_agent
