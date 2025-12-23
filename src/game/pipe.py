import pygame
import random
from src.utils.constants import *


class Pipe:
    def __init__(self, x, pipe_sprite, pipe_gap=150, is_top=False, gap_center=300):
        self.original_image = pipe_sprite
        self.pipe_gap = pipe_gap
        self.is_top = is_top
        # self.passed = False  <-- REMOVED: State should not be on shared object
        self.speed = PIPE_SPEED
        self.gap_center = gap_center

        if is_top:
            self.image = pygame.transform.flip(pipe_sprite, False, True)
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.bottom = gap_center - pipe_gap // 2
            # Prevent top pipe from detaching if gap is too low
            if self.rect.bottom < 0:
                self.rect.bottom = 0
        else:
            self.image = pipe_sprite.copy()
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, gap_center + pipe_gap // 2)

    def update(self):
        """Update pipe position"""
        self.rect.x -= self.speed

    def is_off_screen(self):
        """Check if pipe is completely off screen"""
        return self.rect.right < 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class PipeManager:
    def __init__(self, pipe_sprite):
        self.pipe_sprite = pipe_sprite
        self.pipes = []
        self.spawn_timer = 0
        self.spawn_delay = 90
        self.pipe_gap = PIPE_GAP

    def update(self):
        # Update existing pipes
        for pipe in self.pipes[:]:
            pipe.update()
            if pipe.is_off_screen():
                self.pipes.remove(pipe)

        # Spawn new pipes
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_pipes()
            self.spawn_timer = 0

    def spawn_pipes(self):
        x = SCREEN_WIDTH + 10

        min_gap_center = 150
        max_gap_center = SCREEN_HEIGHT - 150  # Keep gap within playable area
        gap_center = random.randint(min_gap_center, max_gap_center)

        top_pipe = Pipe(x, self.pipe_sprite, self.pipe_gap,
                        is_top=True, gap_center=gap_center)
        bottom_pipe = Pipe(x, self.pipe_sprite, self.pipe_gap,
                           is_top=False, gap_center=gap_center)

        self.pipes.extend([top_pipe, bottom_pipe])

    def get_pipes(self):
        return self.pipes

    def check_score(self, bird):
        """
        Check if bird passed through pipes.
        Uses bird.passed_pipes list to track state per-bird.
        """
        score_gained = 0

        # Ensure bird has the tracking list (handled in Bird class usually, but safe check here)
        if not hasattr(bird, 'passed_pipes'):
            bird.passed_pipes = []

        for pipe in self.pipes:
            # We only score based on the bottom pipe to avoid double counting
            if pipe.is_top:
                continue

            # Check if pipe is behind bird
            if pipe.rect.right < bird.rect.left:
                # Check if we haven't counted this pipe yet for this specific bird
                if pipe not in bird.passed_pipes:
                    bird.passed_pipes.append(pipe)
                    score_gained += 1
                    # Immediate fitness reward for passing
                    bird.fitness += FITNESS_BONUS_PIPE

        # Cleanup: Remove pipes from bird's memory that are no longer in game
        # This prevents memory leaks in long runs
        if len(bird.passed_pipes) > 5:
            bird.passed_pipes = [
                p for p in bird.passed_pipes if p in self.pipes]

        return score_gained

    def get_next_pipes(self, bird_x):
        """Get the next pair of pipes for AI decision making"""
        next_pipes = []
        for pipe in self.pipes:
            if pipe.rect.right > bird_x:
                next_pipes.append(pipe)
                if len(next_pipes) >= 2:  # Get top and bottom of next pipe
                    break
        return next_pipes

    def draw(self, screen):
        for pipe in self.pipes:
            pipe.draw(screen)

    def clear(self):
        self.pipes.clear()
        self.spawn_timer = 0

    def get_statistics(self):
        """Get pipe statistics for debugging"""
        return {
            "total_pipes": len(self.pipes),
            "pipes_passed": sum(1 for pipe in self.pipes if pipe.passed and not pipe.is_top),
            "spawn_timer": self.spawn_timer
        }
