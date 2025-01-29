import pygame
import sys
from collections import deque
from pygame.locals import *
from .models.bird import Bird
from .models.pipe import Pipe
from .ai.genetic import GeneticAlgorithm

class Game:
    def __init__(self, config):
        try:
            pygame.init()
            self.config = config
            self.screen = pygame.display.set_mode(
                (config['SCREEN_WIDTH'], config['SCREEN_HEIGHT']))
            pygame.display.set_caption("Flappy Bird AI")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 36)
            
            self.ga = GeneticAlgorithm(
                config['POPULATION_SIZE'],
                config['MUTATION_RATE'],
                config['ELITISM']
            )
            self.reset()
        except Exception as e:
            print(f"Game initialization failed: {str(e)}")
            pygame.quit()
            sys.exit(1)

    def reset(self):
        try:
            self.population = [Bird() for _ in range(self.config['POPULATION_SIZE'])]
            self.pipes = deque()
            self.spawn_pipe()
        except Exception as e:
            print(f"Reset failed: {str(e)}")
            self.population = []

    def spawn_pipe(self):
        try:
            self.pipes.append(Pipe(
                self.config['SCREEN_WIDTH'] + 200,
                self.config['SCREEN_WIDTH'],
                self.config['SCREEN_HEIGHT']
            ))
        except Exception as e:
            print(f"Pipe spawn failed: {str(e)}")

    def handle_events(self):
        try:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
        except Exception as e:
            print(f"Event handling error: {str(e)}")

    def check_collisions(self, bird):
        try:
            # Screen boundaries
            if bird.y < 0 or bird.y + bird.size > self.config['SCREEN_HEIGHT']:
                return True
                
            # Pipe collisions
            for pipe in self.pipes:
                if (bird.x < pipe.x + pipe.width and
                    bird.x + bird.size > pipe.x and
                    (bird.y < pipe.y or bird.y + bird.size > pipe.y + pipe.gap)):
                    return True
            return False
        except Exception as e:
            print(f"Collision check error: {str(e)}")
            return True

    def update_game_state(self, alive_birds):
        try:
            # Update pipes
            for pipe in self.pipes:
                pipe.update()
            
            if self.pipes[0].offscreen():
                self.pipes.popleft()
                self.spawn_pipe()

            # Update birds
            for bird in alive_birds:
                bird.think(self.pipes, self.config['SCREEN_HEIGHT'])
                bird.update()
                bird.fitness += 0.1
                
                if self.check_collisions(bird):
                    alive_birds.remove(bird)
        except Exception as e:
            print(f"Game state update error: {str(e)}")

    def draw(self, bird):
        try:
            self.screen.fill((78, 192, 202))
            
            # Draw pipes
            for pipe in self.pipes:
                pygame.draw.rect(self.screen, (94, 201, 72), 
                               (pipe.x, 0, pipe.width, pipe.y))
                pygame.draw.rect(self.screen, (94, 201, 72),
                               (pipe.x, pipe.y + pipe.gap, pipe.width, 
                                self.config['SCREEN_HEIGHT']))
            
            # Draw bird
            pygame.draw.circle(self.screen, (255, 204, 0), 
                             (int(bird.x), int(bird.y)), bird.size)
            
            # UI Elements
            gen_text = self.font.render(f"Gen: {self.ga.generation}", True, (255, 255, 255))
            fit_text = self.font.render(f"Fit: {bird.fitness:.1f}", True, (255, 255, 255))
            alive_text = self.font.render(f"Alive: {len(self.population)}", True, (255, 255, 255))
            
            self.screen.blit(gen_text, (10, 10))
            self.screen.blit(fit_text, (10, 40))
            self.screen.blit(alive_text, (10, 70))
            
            pygame.display.update()
        except Exception as e:
            print(f"Drawing error: {str(e)}")

    def run_generation(self):
        try:
            alive_birds = list(self.population)
            
            while len(alive_birds) > 0:
                self.handle_events()
                self.update_game_state(alive_birds)
                
                if alive_birds:
                    best_bird = max(alive_birds, key=lambda x: x.fitness)
                    self.draw(best_bird)
                    self.clock.tick(30)
                else:
                    break

            self.population = self.ga.evolve(self.population)
            self.pipes = deque()
            self.spawn_pipe()
        except Exception as e:
            print(f"Generation run failed: {str(e)}")
            self.reset()

    def run(self):
        try:
            while True:
                self.run_generation()
        except KeyboardInterrupt:
            pygame.quit()
            sys.exit()
        except Exception as e:
            print(f"Fatal game error: {str(e)}")
            pygame.quit()
            sys.exit(1)