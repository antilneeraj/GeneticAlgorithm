import pygame
import random


class Pipe:
    def __init__(self, x, pipe_sprite, pipe_gap=150, is_top=False, gap_center=300):
        self.original_image = pipe_sprite
        self.pipe_gap = pipe_gap
        self.is_top = is_top
        self.passed = False
        self.speed = 3
        self.gap_center = gap_center

        if is_top:
            # Flip the pipe for top pipe
            self.image = pygame.transform.flip(pipe_sprite, False, True)
            # Position top pipe
            self.rect = self.image.get_rect()
            self.rect.bottomleft = (x, gap_center - pipe_gap // 2)
        else:
            # Bottom pipe
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
        """Draw the pipe on screen"""
        screen.blit(self.image, self.rect)


class PipeManager:
    def __init__(self, pipe_sprite):
        self.pipe_sprite = pipe_sprite
        self.pipes = []
        self.spawn_timer = 0
        # Frames between pipe spawns (1.5 seconds at 60 FPS)
        self.spawn_delay = 90
        self.pipe_gap = 150  # Gap between top and bottom pipes

    def update(self):
        """Update all pipes and spawn new ones"""
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
        """Spawn a pair of pipes with random gap position"""
        x = 500  # Spawn off-screen to the right

        # Random gap center position (avoid too high or too low)
        min_gap_center = 150
        max_gap_center = 500
        gap_center = random.randint(min_gap_center, max_gap_center)

        # Create top and bottom pipes with same gap center
        top_pipe = Pipe(x, self.pipe_sprite, self.pipe_gap,
                        is_top=True, gap_center=gap_center)
        bottom_pipe = Pipe(x, self.pipe_sprite, self.pipe_gap,
                           is_top=False, gap_center=gap_center)

        self.pipes.extend([top_pipe, bottom_pipe])

    def get_pipes(self):
        """Get list of all pipes"""
        return self.pipes

    def check_score(self, bird):
        """Check if bird passed through pipes for scoring"""
        score_gained = 0
        for pipe in self.pipes:
            if (not pipe.passed and
                pipe.rect.right < bird.rect.left and
                    not pipe.is_top):  # Only count bottom pipes for scoring
                pipe.passed = True
                # Also mark the corresponding top pipe as passed
                for other_pipe in self.pipes:
                    if (other_pipe.is_top and
                        abs(other_pipe.rect.x - pipe.rect.x) < 10 and
                            not other_pipe.passed):
                        other_pipe.passed = True
                        break
                score_gained += 1
                bird.fitness += 100  # Bonus fitness for passing pipe
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
        """Draw all pipes"""
        for pipe in self.pipes:
            pipe.draw(screen)

    def clear(self):
        """Clear all pipes (for game reset)"""
        self.pipes.clear()
        self.spawn_timer = 0

    def get_statistics(self):
        """Get pipe statistics for debugging"""
        return {
            "total_pipes": len(self.pipes),
            "pipes_passed": sum(1 for pipe in self.pipes if pipe.passed and not pipe.is_top),
            "spawn_timer": self.spawn_timer
        }
