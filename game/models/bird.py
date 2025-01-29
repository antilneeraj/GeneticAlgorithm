import numpy as np
from game.ai.neural import NeuralNetwork

class Bird:
    def __init__(self, genome=None):
        try:
            self.x = 50
            self.y = 300
            self.velocity = 0
            self.size = 20
            self.fitness = 0
            self.brain = NeuralNetwork()
            
            if genome is not None:
                if len(genome) != 2:
                    raise ValueError("Invalid genome structure")
                self.brain.weights = genome
        except Exception as e:
            print(f"Error initializing Bird: {str(e)}")
            raise

    def jump(self, gravity):
        try:
            self.velocity = gravity
        except AttributeError as e:
            print(f"Jump failed: {str(e)}")

    def update(self):
        try:
            self.velocity += 0.5  # Gravity
            self.y += self.velocity
        except TypeError as e:
            print(f"Update failed: {str(e)}")

    def think(self, pipes, screen_height):
        try:
            closest = None
            for pipe in pipes:
                if pipe.x + pipe.width > self.x:
                    closest = pipe
                    break

            if closest:
                inputs = [
                    (self.y - closest.y) / screen_height,
                    (closest.x - self.x) / screen_height,
                    self.velocity / 10
                ]
                output = self.brain.predict(inputs)
                if output[0] > 0.5:
                    self.jump(-12)
        except Exception as e:
            print(f"Thinking error: {str(e)}")

    @property
    def genome(self):
        return self.brain.weights