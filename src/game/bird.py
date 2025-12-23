import pygame
from src.utils.constants import *


class Bird:
    def __init__(self, x, y, bird_sprites, bird_type="BLUE"):
        self.sprites = bird_sprites
        self.bird_type = bird_type
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite] if self.sprites else pygame.Surface(
            (34, 24))
        self.rect = self.image.get_rect(center=(x, y))
        self.original_rect = self.rect.copy()

        # Physics
        self.velocity = 0
        self.gravity = GRAVITY
        self.jump_strength = JUMP_STRENGTH
        self.max_velocity = 10
        self.rotation = 0
        self.flap_animation_counter = 0

        # Status
        self.alive = True
        self.score = 0
        self.fitness = 0
        self.brain = None

        # Track passed pipes for scoring (Fix for AI training)
        self.passed_pipes = []

        self.frames_survived = 0

    def update(self, jump=False):
        if not self.alive:
            return

        self.frames_survived += 1

        if jump:
            self.velocity = self.jump_strength
            self.flap_animation_counter = 0

        self.velocity += self.gravity
        if self.velocity > self.max_velocity:
            self.velocity = self.max_velocity

        self.rect.y += int(self.velocity)

        # Rotation
        self.rotation = min(25, max(-90, -(self.velocity * 3)))
        self.update_animation()

        # Fitness accumulation: Reward survival slightly every frame
        if self.alive:
            self.fitness += FITNESS_BONUS_DISTANCE

    def update_animation(self):
        if not self.sprites:
            return
        self.flap_animation_counter += 1
        if self.flap_animation_counter >= 5:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.flap_animation_counter = 0
            self.image = pygame.transform.rotate(
                self.sprites[self.current_sprite], self.rotation)
            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)

    def jump(self):
        if self.alive:
            self.velocity = self.jump_strength

    def check_collision(self, pipes, ground_y, screen_height):
        """FIXED: More lenient collision detection with proper buffers"""
        if not self.alive:
            return False

        # FIXED: Check ground collision with bigger buffer (was 3, now 6)
        if self.rect.bottom >= ground_y - 6:  # 6 pixel buffer
            self.alive = False
            return True

        # FIXED: Check ceiling collision with buffer
        if self.rect.top <= 5:  # 5 pixel buffer from top
            self.alive = False
            return True

        # FIXED: More lenient pipe collision detection
        for pipe in pipes:
            # Create smaller collision rect for more forgiving collision (was -4, now -6)
            # 6px smaller on all sides
            bird_collision_rect = self.rect.inflate(-6, -6)

            if bird_collision_rect.colliderect(pipe.rect):
                # Use mask collision for pixel-perfect detection
                try:
                    bird_mask = pygame.mask.from_surface(self.image)
                    pipe_mask = pygame.mask.from_surface(pipe.image)
                    offset = (pipe.rect.x - bird_collision_rect.x,
                              pipe.rect.y - bird_collision_rect.y)
                    if bird_mask.overlap(pipe_mask, offset):
                        self.alive = False
                        return True
                except:
                    # Fallback to rect collision if mask fails
                    self.alive = False
                    return True

        return False

    def get_game_state(self, pipes):
        """
        Optimized inputs for the Neural Network.
        Returns: [bird_y, velocity, distance_to_pipe_x, distance_to_gap_y]
        """
        # Default values (if no pipes)
        dist_x = 1.0
        dist_y = 0.5

        # Find closest pipe that is NOT passed yet
        next_pipe = None
        for pipe in pipes:
            # We look for the bottom pipe of the pair
            if not pipe.is_top:
                # If pipe right edge is ahead of bird left edge (plus buffer)
                if pipe.rect.right > self.rect.left:
                    next_pipe = pipe
                    break

        if next_pipe:
            # Normalize X distance: 0 = at pipe, 1 = far away
            raw_dist_x = next_pipe.rect.left - self.rect.right
            dist_x = max(0, min(1, raw_dist_x / SCREEN_WIDTH))

            # Normalize Y distance (Delta Y): 0.5 = level with gap, >0.5 below gap, <0.5 above gap
            # Gap center is stored in the pipe object (thanks to our pipe.py update)
            # If gap_center is not on pipe, calculate it from rect
            gap_center = getattr(next_pipe, 'gap_center',
                                 next_pipe.rect.top - 75)

            raw_diff_y = (gap_center - self.rect.centery)
            # Map diff from [-height, height] to [0, 1]
            dist_y = 0.5 + (raw_diff_y / SCREEN_HEIGHT)
            dist_y = max(0.0, min(1.0, dist_y))

        # Inputs
        # 1. Bird Y (0=top, 1=bottom)
        input_y = self.rect.centery / SCREEN_HEIGHT

        # 2. Bird Velocity (normalized)
        input_vel = (self.velocity + 10) / 20  # Map -10..10 to 0..1
        input_vel = max(0.0, min(1.0, input_vel))

        return [input_y, input_vel, dist_x, dist_y]

    def reset(self, x, y):
        self.rect.center = (x, y)
        self.velocity = 0
        self.rotation = 0
        self.alive = True
        self.score = 0
        self.fitness = 0
        self.passed_pipes = []
        self.frames_survived = 0

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.rect)

    def get_mask(self):
        """Get collision mask for the bird"""
        return pygame.mask.from_surface(self.image)

    def get_fitness_info(self):
        return {
            "frames_survived": self.frames_survived,
            "score": self.score,
            "base_fitness": self.fitness,
            "alive": self.alive,
            "position": (self.rect.x, self.rect.y),
            "velocity": self.velocity
        }

    def __str__(self):
        return f"Bird({self.bird_type}, Score: {self.score}, Fitness: {self.fitness:.1f}, Alive: {self.alive}, Frames: {self.frames_survived})"
