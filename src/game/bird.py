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

        self.flap_speed = 5
        self.frames_survived = 0

    def update(self, jump=False):
        if not self.alive:
            return

        self.frames_survived += 1

        # Handle jump
        if jump:
            self.velocity = self.jump_strength
            self.flap_animation_counter = 0

        # Apply gravity
        self.velocity += self.gravity
        if self.velocity > self.max_velocity:
            self.velocity = self.max_velocity

        self.rect.y += int(self.velocity)
        self.rotation = min(25, max(-90, -(self.velocity * 3)))
        self.update_animation()

        # Continuous fitness reward for staying alive
        # Small reward prevents them from just maximizing score without surviving
        self.fitness += 0.1

    def update_animation(self):
        if not self.sprites:
            return
        self.flap_animation_counter += 1
        if self.flap_animation_counter >= self.flap_speed:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.flap_animation_counter = 0

        original_image = self.sprites[self.current_sprite]
        self.image = pygame.transform.rotate(original_image, self.rotation)
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)

    def jump(self):
        if self.alive:
            self.velocity = self.jump_strength

    def check_collision(self, pipes, ground_y, screen_height):
        """Lenient collision detection for faster training"""
        if not self.alive:
            return False

        # Ground/Ceiling Collision
        if self.rect.bottom >= ground_y - 5:
            self.alive = False
            return True
        if self.rect.top <= 0:
            self.alive = False
            return True

        # Pipe Collision (with buffer)
        # Shrink bird hitbox by 4 pixels on all sides to be forgiving
        hitbox = self.rect.inflate(-8, -8)

        for pipe in pipes:
            # Shrink pipe hitbox slightly too
            pipe_hitbox = pipe.rect.inflate(-4, -4)

            if hitbox.colliderect(pipe_hitbox):
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
        diff_y = 0.5

        # Find the next relevant pipe
        next_pipe = None
        min_dist = float('inf')

        for pipe in pipes:
            # Look for bottom pipes only (simplifies logic)
            if not pipe.is_top:
                # Find pipe that is to the right of the bird (with small buffer for "inside" pipe)
                # Using rect.right > bird.rect.left - 10 allows bird to 'see' pipe while passing through
                if pipe.rect.right > self.rect.left - 20:
                    dist = pipe.rect.left - self.rect.right
                    if dist < min_dist:
                        min_dist = dist
                        next_pipe = pipe

        if next_pipe:
            # Horizontal Distance (Normalized 0-1)
            # 0 = touching pipe, 1 = far edge of screen
            raw_dist_x = next_pipe.rect.left - self.rect.right
            dist_x = max(0.0, min(1.0, raw_dist_x / SCREEN_WIDTH))

            # Vertical Difference to Gap (Normalized 0-1)
            # Find the center of the gap associated with this pipe
            # If pipe object has gap_center, use it. Otherwise calculate.
            gap_center = getattr(next_pipe, 'gap_center',
                                 next_pipe.rect.top - 75)

            # Difference between bird and gap
            # 0.5 = Bird is exactly at gap center
            # < 0.5 = Bird is ABOVE gap (needs to drop)
            # > 0.5 = Bird is BELOW gap (needs to jump)
            raw_diff_y = self.rect.centery - gap_center

            # Normalize diff to range roughly [-300, 300] mapped to [0, 1]
            diff_y = 0.5 + (raw_diff_y / SCREEN_HEIGHT)
            diff_y = max(0.0, min(1.0, diff_y))

        # Bird Y Position (Normalized 0-1)
        # 0 = Top, 1 = Bottom
        bird_y = self.rect.centery / SCREEN_HEIGHT
        bird_y = max(0.0, min(1.0, bird_y))

        # Bird Velocity (Normalized 0-1)
        # Map range [-10, 10] to [0, 1]
        vel = (self.velocity + 10) / 20
        vel = max(0.0, min(1.0, vel))

        return [bird_y, vel, dist_x, diff_y]

    def reset(self, x, y):
        self.rect.center = (x, y)
        self.velocity = 0
        self.rotation = 0
        self.alive = True
        self.score = 0
        self.fitness = 0
        self.current_sprite = 0
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
