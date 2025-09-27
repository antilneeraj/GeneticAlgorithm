from tkinter import font
import pygame
import math


class Renderer:
    def __init__(self, screen, asset_loader):
        self.screen = screen
        self.assets = asset_loader
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Background scrolling
        self.bg_x = 0
        self.ground_x = 0

        # UI colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)
        self.gray = (128, 128, 128)

        self.frame_count = 0

    def draw_background(self, bg_type="DAY"):
        background = self.assets.get_background(bg_type)
        if background:
            # Scale background to screen if needed
            bg_width = background.get_width()
            if bg_width < self.screen_width:
                background = pygame.transform.scale(
                    background, (self.screen_width, self.screen_height))

            # Draw two backgrounds for seamless scrolling
            self.screen.blit(background, (self.bg_x, 0))
            self.screen.blit(background, (self.bg_x + self.screen_width, 0))

            # Scroll background slowly
            self.bg_x -= 1
            if self.bg_x <= -self.screen_width:
                self.bg_x = 0

    def draw_ground(self):
        ground = self.assets.images.get("base")
        if ground:
            ground_y = self.screen_height - ground.get_height()

            ground_width = ground.get_width()
            num_grounds = (self.screen_width // ground_width) + 2

            for i in range(num_grounds):
                x_pos = (i * ground_width) + self.ground_x
                self.screen.blit(ground, (x_pos, ground_y))

            # Scroll ground
            self.ground_x -= 3
            if self.ground_x <= -ground_width:
                self.ground_x = 0

            return ground_y
        else:
            ground_y = self.screen_height - 50
            pygame.draw.rect(self.screen, self.green,
                             (0, ground_y, self.screen_width, 50))
            return ground_y

    def draw_birds(self, birds):
        colors = [self.red, self.blue, self.yellow,
                  self.green, (255, 0, 255), (0, 255, 255)]

        for i, bird in enumerate(birds):
            if bird.alive:
                bird.draw(self.screen)

                # Draw a small colored circle to identify different AI birds
                if len(birds) > 1:  # Only for AI training mode
                    color = colors[i % len(colors)]
                    pygame.draw.circle(self.screen, color,
                                       (bird.rect.centerx, bird.rect.centery), 3)

    def draw_pipes(self, pipe_manager):
        pipe_manager.draw(self.screen)

    def draw_score(self, score, center_x=None):
        score_str = str(score)
        numbers = self.assets.images.get("numbers", {})

        if not numbers or len(numbers) == 0:
            font = self.assets.get_font("large")
            if font:
                text = font.render(str(score), True, self.white)
                text_rect = text.get_rect(
                    center=(center_x or self.screen_width//2, 50))

                shadow = font.render(str(score), True, self.black)
                shadow_rect = shadow.get_rect(
                    center=(text_rect.centerx + 2, text_rect.centery + 2))
                self.screen.blit(shadow, shadow_rect)
                self.screen.blit(text, text_rect)
            return

        # Calculate total width of score
        total_width = sum(numbers[int(digit)].get_width()
                          for digit in score_str if digit.isdigit())
        start_x = (center_x or self.screen_width//2) - total_width//2

        # Draw each digit
        current_x = start_x
        for digit in score_str:
            if digit.isdigit():
                digit_sprite = numbers[int(digit)]
                self.screen.blit(digit_sprite, (current_x, 50))
                current_x += digit_sprite.get_width()

    def draw_game_over(self):
        gameover_img = self.assets.images.get("gameover")
        if gameover_img:
            go_rect = gameover_img.get_rect(center=(self.screen_width//2, 200))
            self.screen.blit(gameover_img, go_rect)
        else:
            # Fallback text
            font = self.assets.get_font("large")
            if font:
                text = font.render("GAME OVER", True, self.red)
                text_rect = text.get_rect(center=(self.screen_width//2, 200))
                self.screen.blit(text, text_rect)

    def draw_start_message(self):
        message_img = self.assets.images.get("message")
        if message_img:
            msg_rect = message_img.get_rect(center=(self.screen_width//2, 250))
            self.screen.blit(message_img, msg_rect)
        else:
            # Fallback text
            font = self.assets.get_font("medium")
            if font:
                text1 = font.render("Press SPACE to start", True, self.white)
                text2 = font.render("Press R to restart", True, self.white)

                rect1 = text1.get_rect(center=(self.screen_width//2, 250))
                rect2 = text2.get_rect(center=(self.screen_width//2, 280))

                self.screen.blit(text1, rect1)
                self.screen.blit(text2, rect2)

    def draw_statistics(self, stats, x=10, y=10, title="Statistics", font_size='small'):
        """Draw real-time statistics with nice formatting"""
        font = self.assets.get_font(font_size)
        font_medium = self.assets.get_font("medium")

        if not font:
            return

        line_height = 18 if font_size == 'small' else 22
        padding = 8

        # Calculate box dimensions
        max_text_width = 0
        lines = [title] + [
            f"{key}: {value:.2f}" if isinstance(value, float)
            else f"{key}: {value}"
            for key, value in stats.items()
        ]

        for line in lines:
            text_surface = font.render(line, True, self.white)
            max_text_width = max(max_text_width, text_surface.get_width())

        box_width = max_text_width + padding * 2
        box_height = len(lines) * line_height + padding * 2

        # Create semi-transparent background
        stats_surface = pygame.Surface((box_width, box_height))
        stats_surface.set_alpha(200)
        stats_surface.fill(self.black)

        # Add border
        pygame.draw.rect(stats_surface, self.white, (0, 0, box_width, box_height), 2)

        self.screen.blit(stats_surface, (x, y))

        # Draw title with different font/color
        if font_medium:
            title_surface = font_medium.render(title, True, self.yellow)
        else:
            title_surface = font.render(title, True, self.yellow)
        self.screen.blit(title_surface, (x + padding, y + padding))

        # Draw statistics text
        current_y = y + padding + line_height + 3
        for key, value in stats.items():
            if isinstance(value, float):
                text = f"{key}: {value:.2f}"
            elif isinstance(value, int):
                text = f"{key}: {value:,}"
            else:
                text = f"{key}: {value}"

            text_surface = font.render(text, True, self.white)
            self.screen.blit(text_surface, (x + padding, current_y))
            current_y += line_height

    def draw_ai_info(self, generation, alive, best_score, best_fitness, avg_fitness,
                 population, x=15, y=80, font_size='small'):
        ai_stats = {
            "Gen": generation,
            "Alive": f"{alive}/{population}",
            "Best Score": best_score,
            "Best Fitness": int(best_fitness),
            "Avg Fitness": int(avg_fitness),
            "Survival Rate": f"{(alive/population)*100:.0f}%" if population > 0 else "0%"
        }
        self.draw_statistics(ai_stats, x, y, "AI Training", font_size=font_size)

    def draw_progress_bar(self, progress, x, y, width=200, height=20, label="Progress"):
        """Draw training progress bar with label"""
        # Draw label
        font = self.assets.get_font("small")
        if font and label:
            text = font.render(label, True, self.black)
            self.screen.blit(text, (x, y - 25))

        # Background
        pygame.draw.rect(self.screen, self.gray, (x, y, width, height))
        pygame.draw.rect(self.screen, self.black, (x, y, width, height), 2)

        # Progress fill
        fill_width = int(width * min(progress, 1.0))
        if fill_width > 0:
            color = self.green if progress < 0.8 else self.yellow if progress < 1.0 else self.blue
            pygame.draw.rect(self.screen, color, (x + 1, y +
                             1, fill_width - 2, height - 2))

        # Progress text
        if font:
            progress_text = f"{progress*100:.1f}%"
            text = font.render(progress_text, True, self.black)
            text_rect = text.get_rect(center=(x + width//2, y + height//2))
            self.screen.blit(text, text_rect)

    def draw_fps(self, fps, x=10, y=None):
        y = y or self.screen_height - 80
        font = self.assets.get_font("small")
        if font:
            fps_text = f"FPS: {int(fps)}"
            text = font.render(fps_text, True, self.blue if fps >= 30 else self.red)
            self.screen.blit(text, (x, y))


    def draw_instructions(self):
        font = self.assets.get_font("small")
        if font:
            instructions = [
                "SPACE: Jump (Human mode)",
                "R: Restart game",
                "ESC: Quit",
                "",
                "Watch AI birds learn!",
            ]

            y_start = self.screen_height - len(instructions) * 20 - 10
            for i, instruction in enumerate(instructions):
                if instruction:  # Skip empty lines
                    text = font.render(instruction, True, self.white)
                    self.screen.blit(
                        text, (self.screen_width - 200, y_start + i * 20))

    def clear_screen(self, color=None):
        self.screen.fill(color or self.black)
