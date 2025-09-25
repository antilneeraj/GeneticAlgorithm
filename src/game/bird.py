import pygame
import math
from src.utils.constants import *

class Bird:
    def __init__(self, x, y, bird_sprites, bird_type="BLUE"):
        """Initialize bird with AI capabilities"""
        self.sprites = bird_sprites  # List of bird animation frames
        self.bird_type = bird_type
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite] if self.sprites else pygame.Surface((34, 24))
        self.rect = self.image.get_rect(center=(x, y))
        self.original_rect = self.rect.copy()
        
        # Physics
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -8
        self.max_velocity = 10
        self.rotation = 0
        self.flap_animation_counter = 0
        
        # Status
        self.alive = True
        self.score = 0
        self.fitness = 0
        
        # AI Brain (will be set by genetic algorithm)
        self.brain = None
        
        # Animation
        self.flap_speed = 5  # Frames between animation changes
        
        # FIXED: Add frame tracking for proper fitness calculation
        self.frames_survived = 0
        
    def update(self, jump=False):
        """Update bird physics and animation"""
        if not self.alive:
            return
            
        # FIXED: Track frames for fitness
        self.frames_survived += 1
        
        # Handle jump
        if jump:
            self.velocity = self.jump_strength
            self.flap_animation_counter = 0
            
        # Apply gravity
        self.velocity += self.gravity
        if self.velocity > self.max_velocity:
            self.velocity = self.max_velocity
            
        # Update position
        self.rect.y += int(self.velocity)
        
        # Update rotation based on velocity
        self.rotation = min(25, max(-90, -(self.velocity * 3)))
        
        # Update animation
        self.update_animation()
        
        # FIXED: Update fitness based on survival time (frames * distance bonus)
        if self.alive:
            self.fitness = self.frames_survived * FITNESS_BONUS_DISTANCE
        
    def update_animation(self):
        """Update bird flapping animation"""
        if not self.sprites:
            return
            
        self.flap_animation_counter += 1
        if self.flap_animation_counter >= self.flap_speed:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.flap_animation_counter = 0
            
        # Get rotated sprite
        original_image = self.sprites[self.current_sprite]
        self.image = pygame.transform.rotate(original_image, self.rotation)
        
        # Keep center position when rotating
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)
        
    def jump(self):
        """Make the bird jump"""
        if self.alive:
            self.velocity = self.jump_strength
            
    def check_collision(self, pipes, ground_y, screen_height):
        """FIXED: More lenient collision detection with proper buffers"""
        if not self.alive:
            return False
            
        # FIXED: Check ground collision with bigger buffer (was 3, now 8)
        if self.rect.bottom >= ground_y - 8:  # 8 pixel buffer
            self.alive = False
            return True
            
        # FIXED: Check ceiling collision with buffer
        if self.rect.top <= 5:  # 5 pixel buffer from top
            self.alive = False
            return True
            
        # FIXED: More lenient pipe collision detection
        for pipe in pipes:
            # Create smaller collision rect for more forgiving collision (was -4, now -6)
            bird_collision_rect = self.rect.inflate(-6, -6)  # 6px smaller on all sides
            
            if bird_collision_rect.colliderect(pipe.rect):
                # Use mask collision for pixel-perfect detection
                try:
                    bird_mask = pygame.mask.from_surface(self.image)
                    pipe_mask = pygame.mask.from_surface(pipe.image)
                    offset = (pipe.rect.x - bird_collision_rect.x, pipe.rect.y - bird_collision_rect.y)
                    if bird_mask.overlap(pipe_mask, offset):
                        self.alive = False
                        return True
                except:
                    # Fallback to rect collision if mask fails
                    self.alive = False
                    return True
                    
        return False
        
    def get_game_state(self, pipes):
        """CRITICAL FIX: Get properly changing game state for neural network input"""
        try:
            # DEBUG: Add this line temporarily to see what's happening
            #* print(f"DEBUG: get_game_state called with {len(pipes)} pipes, bird at y={self.rect.centery}")
            
            # FIXED: Always return dynamic values based on current bird state
            
            # 1. Bird Y position (changes as bird moves up/down)
            bird_y_norm = max(0.0, min(1.0, self.rect.centery / SCREEN_HEIGHT))
            
            # 2. Bird velocity (changes as bird falls/jumps)
            velocity_norm = max(0.0, min(1.0, (self.velocity + self.max_velocity) / (2 * self.max_velocity)))
            
            # 3. & 4. Pipe-related values
            pipe_distance_norm = 1.0  # Default: no pipe nearby
            gap_distance_norm = 0.5   # Default: gap at screen center
            
            if pipes:
                # Find the next pipe pair that the bird hasn't passed yet
                next_pipes = []
                
                # Look for pipes ahead of the bird
                for pipe in pipes:
                    if hasattr(pipe, 'rect') and pipe.rect.centerx > self.rect.centerx:
                        next_pipes.append(pipe)
                
                if next_pipes:
                    # Get the closest pipe
                    closest_pipe = min(next_pipes, key=lambda p: p.rect.centerx)
                    
                    # 3. Horizontal distance to next pipe
                    pipe_distance = closest_pipe.rect.centerx - self.rect.centerx
                    pipe_distance_norm = max(0.0, min(1.0, pipe_distance / SCREEN_WIDTH))
                    
                    # 4. Find gap center for this pipe set
                    pipes_at_x = [p for p in pipes if abs(p.rect.centerx - closest_pipe.rect.centerx) < 50]
                    
                    if len(pipes_at_x) >= 2:
                        # Sort by y position to get top and bottom
                        pipes_at_x.sort(key=lambda p: p.rect.y)
                        
                        # Calculate gap center between top and bottom pipes
                        if hasattr(pipes_at_x[0], 'is_top'):
                            # Use is_top attribute if available
                            top_pipes = [p for p in pipes_at_x if getattr(p, 'is_top', False)]
                            bottom_pipes = [p for p in pipes_at_x if not getattr(p, 'is_top', True)]
                            
                            if top_pipes and bottom_pipes:
                                gap_center = (top_pipes[0].rect.bottom + bottom_pipes[0].rect.top) / 2
                            else:
                                # Fallback: assume first pipe is top, second is bottom
                                gap_center = (pipes_at_x[0].rect.bottom + pipes_at_x[1].rect.top) / 2
                        else:
                            # Fallback: assume first pipe is top, second is bottom  
                            gap_center = (pipes_at_x[0].rect.bottom + pipes_at_x[1].rect.top) / 2
                            
                        # Normalize gap position relative to bird
                        gap_distance = gap_center - self.rect.centery
                        gap_distance_norm = max(0.0, min(1.0, (gap_distance + SCREEN_HEIGHT/2) / SCREEN_HEIGHT))
            
            # Return dynamic state that changes every frame
            state = [
                bird_y_norm,        # Bird Y position [0-1] - CHANGES as bird moves
                velocity_norm,      # Velocity [0-1] - CHANGES as bird accelerates/jumps
                pipe_distance_norm, # Pipe distance [0-1] - CHANGES as pipes approach
                gap_distance_norm   # Gap distance [0-1] - CHANGES based on pipe positions
            ]
            
            # DEBUG: Uncomment this to see if values are changing
            # if hasattr(self, 'debug_counter'):
            #     self.debug_counter += 1
            # else:
            #     self.debug_counter = 1
            # if self.debug_counter % 30 == 0:  # Print every 30 frames
            #     print(f"Bird state: y={bird_y_norm:.3f}, vel={velocity_norm:.3f}, pipe={pipe_distance_norm:.3f}, gap={gap_distance_norm:.3f}")
            
            return state
            
        except Exception as e:
            print(f"Error in get_game_state: {e}")
            # Return safe defaults that still vary based on bird position
            bird_y_norm = max(0.0, min(1.0, self.rect.centery / SCREEN_HEIGHT))
            velocity_norm = max(0.0, min(1.0, (self.velocity + self.max_velocity) / (2 * self.max_velocity)))
            return [bird_y_norm, velocity_norm, 1.0, 0.5]
        
    def reset(self, x, y):
        """Reset bird to starting position"""
        self.rect.center = (x, y)
        self.velocity = 0
        self.rotation = 0
        self.alive = True
        self.score = 0
        self.fitness = 0
        self.current_sprite = 0
        self.flap_animation_counter = 0
        self.frames_survived = 0  # FIXED: Reset frame counter
        
    def draw(self, screen):
        """Draw the bird on screen"""
        if self.alive:
            screen.blit(self.image, self.rect)
            
    def get_mask(self):
        """Get collision mask for the bird"""
        return pygame.mask.from_surface(self.image)
    
    def get_fitness_info(self):
        """Get detailed fitness information for debugging"""
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