import pygame
import sys
import time
import random
import numpy as np
from src.utils.asset_loader import AssetLoader
from src.game.bird import Bird
from src.game.pipe import PipeManager
from src.game.renderer import Renderer
from src.utils.constants import *


class GameEngine:
    def __init__(self, mode="human"):
        pygame.init()
        pygame.mixer.init()

        self.paused = False
        self.theme = "DAY"

        # Set different random seeds for true randomness
        random.seed(time.time())
        np.random.seed(int(time.time() * 1000000) % 2**32)

        # Display setup
        # self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

        pygame.display.set_caption("Flappy Bird - Genetic Algorithm [DEBUG]")
        self.clock = pygame.time.Clock()

        # Screen dimensions
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        # Load assets
        print("Loading game assets...")
        self.asset_loader = AssetLoader()
        self.asset_loader.load_all_assets()
        print("Assets loaded successfully!")

        # Initialize renderer
        self.renderer = Renderer(self.screen, self.asset_loader)

        # Game mode and state
        self.mode = mode
        self.game_state = GAME_STATES["MENU"] if mode == "human" else GAME_STATES["PLAYING"]

        # Game objects
        self.birds = []
        self.pipe_manager = PipeManager(
            self.asset_loader.get_pipe_sprite("GREEN"))

        # Game variables
        self.score = 0
        self.high_score = self.load_high_score()
        self.frame_count = 0
        self.game_start_time = time.time()

        # AI training variables
        self.generation = 1
        self.population_size = POPULATION_SIZE
        self.generation_start_time = time.time()
        self.generation_frame_count = 0

        # Initialize genetic algorithm
        self.genetic_algorithm = None

        # DEBUG: Add comprehensive debugging
        self.debug_mode = False
        self.decision_log = []
        self.game_state_log = []
        self.collision_log = []

        # Performance tracking
        self.fps_counter = 0
        self.fps_timer = time.time()
        self.current_fps = 60

        # Initialize based on mode
        self.init_game_mode()

    def init_game_mode(self):
        """Initialize game based on selected mode"""
        if self.mode == "human":
            self.init_human_game()
        elif self.mode == "ai_training":
            self.init_ai_training()
        elif self.mode == "ai_play":
            self.init_ai_play()

    def init_human_game(self):
        """Initialize game for human player"""
        bird_sprites = self.asset_loader.get_bird_sprites("BLUE")
        self.birds = [Bird(100, 300, bird_sprites, "BLUE")]
        print("Human game mode initialized")

    def init_ai_training(self):
        """Initialize AI training with proper genetic algorithm integration"""
        from src.ai.genetic_algorithm import GeneticAlgorithm

        # Only initialize genetic algorithm once
        if self.genetic_algorithm is None:
            print(
                f"🧬 Initializing Genetic Algorithm with population size: {self.population_size}")
            self.genetic_algorithm = GeneticAlgorithm(
                population_size=self.population_size,
                generations=GENERATIONS,
                mutation_rate=MUTATION_RATE,
                crossover_rate=CROSSOVER_RATE,
                elite_count=ELITE_COUNT
            )
            print(f"✅ Genetic Algorithm initialized")

        # Create birds and assign neural network brains
        self.create_ai_birds_with_debugging()

    def create_ai_birds_with_debugging(self):
        """FIXED: Create AI birds with proper neural network diversity"""
        from src.ai.neural_network import NeuralNetwork

        bird_types = ["BLUE", "RED", "YELLOW"]
        self.birds = []

        print(f"🐦 Creating {self.population_size} AI birds...")

        # Create birds with spread positions
        for i in range(self.population_size):
            bird_type = bird_types[i % len(bird_types)]
            bird_sprites = self.asset_loader.get_bird_sprites(bird_type)

            # FIXED: Better position spread
            start_x = 80 + (i % 10) * 2  # Spread across screen width
            start_y = 200 + (i % 20) * 10  # Spread across different heights

            bird = Bird(start_x, start_y, bird_sprites, bird_type)
            self.birds.append(bird)

        # FIXED: Create diverse neural networks with different random seeds
        if not hasattr(self.genetic_algorithm, 'population') or not self.genetic_algorithm.population.individuals:
            print("🧠 Creating initial neural networks with diverse weights...")
            for i, bird in enumerate(self.birds):
                # Set different seed for each bird to ensure diversity
                seed = (int(time.time() * 1000000) + i * 1337) % (2**31 - 1)

                brain = NeuralNetwork(
                    NN_INPUT_NODES, NN_HIDDEN_NODES, NN_OUTPUT_NODES, seed=seed)
                bird.brain = brain

                # DEBUG: Log neural network weights for first few birds
                if i < 5:
                    weights = brain.get_weights_as_array()
                    print(
                        f"   Bird {i} brain: {len(weights)} params, sample weights: {weights[:5]}")
        else:
            # Use evolved brains from genetic algorithm
            self.genetic_algorithm.assign_brains_to_birds(self.birds)

            # DEBUG: Verify brain diversity
            if len(self.birds) >= 2:
                weights1 = self.birds[0].brain.get_weights_as_array()
                weights2 = self.birds[1].brain.get_weights_as_array()
                difference = np.mean(np.abs(weights1 - weights2))
                print(
                    f"🧬 Brain diversity check: avg difference = {difference:.4f}")
                if difference < 0.001:
                    print("⚠️  WARNING: Brains are too similar!")

        # DEBUG: Test neural network decisions with sample inputs
        self.test_neural_network_diversity()

        print(
            f"✅ Created {len(self.birds)} AI birds with diverse neural networks")

    def test_neural_network_diversity(self):
        """DEBUG: Test that neural networks make different decisions"""
        if len(self.birds) < 2:
            return

        print("🧪 Testing neural network diversity...")
        test_inputs = [
            [0.5, 0.0, 0.8, 0.5],   # Mid-height, no velocity, far pipe, center gap
            [0.2, -0.5, 0.6, 0.3],  # Low, falling, close pipe, low gap
            [0.8, 0.3, 0.4, 0.7],   # High, rising, very close pipe, high gap
        ]

        for i, test_input in enumerate(test_inputs):
            decisions = []
            for j in range(min(5, len(self.birds))):  # Test first 5 birds
                if self.birds[j].brain:
                    decision = self.birds[j].brain.predict(test_input)
                    decisions.append(decision)

            unique_decisions = len(set(decisions))
            print(
                f"   Test {i+1}: {unique_decisions}/{len(decisions)} unique decisions")
            if unique_decisions <= 1:
                print(f"   ⚠️  All birds made same decision: {decisions}")

    def init_ai_play(self):
        """Initialize game for watching trained AI play"""
        bird_sprites = self.asset_loader.get_bird_sprites("BLUE")
        bird = Bird(100, 300, bird_sprites, "BLUE")
        bird.brain = None
        self.birds = [bird]
        print("AI play mode initialized")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:   # Mouse wheel up
                    self.theme = "NIGHT"
                    print("Theme changed to NIGHT")
                elif event.button == 5:  # Mouse wheel down
                    self.theme = "DAY"
                    print("Theme changed to DAY")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:     # jump
                    if self.mode == "human":
                        self.handle_human_input()
                elif event.key == pygame.K_r:           # restart
                    self.restart_game()
                elif event.key == pygame.K_ESCAPE:  # quit
                    return False
                elif event.key == pygame.K_p:       # pause
                    self.paused = not self.paused
                    print(f"Paused: {self.paused}")
                elif event.key == pygame.K_d:  # Toggle debug mode
                    self.debug_mode = not self.debug_mode
                    print(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")

        return True

    def handle_human_input(self):
        """Handle human player input"""
        if self.game_state == GAME_STATES["MENU"]:
            self.game_state = GAME_STATES["PLAYING"]
            self.game_start_time = time.time()
        elif self.game_state == GAME_STATES["PLAYING"]:
            for bird in self.birds:
                if bird.alive:
                    bird.jump()
                    sound = self.asset_loader.get_sound("wing")
                    if sound:
                        sound.play()
        elif self.game_state == GAME_STATES["GAME_OVER"]:
            self.restart_game()

    def update_game(self):
        if self.paused:
            return

        if self.game_state not in [GAME_STATES["PLAYING"], GAME_STATES["TRAINING"]]:
            return

        self.frame_count += 1
        self.generation_frame_count += 1

        # Update birds with debugging
        self.update_birds_with_debugging()

        # Update pipes
        self.pipe_manager.update()

        # Check scoring
        self.check_scoring()

        # Check game over conditions
        self.check_game_over()

        # Update FPS counter
        self.update_fps_counter()

    def update_birds_with_debugging(self):
        """FIXED: Update all birds with comprehensive debugging"""
        alive_count = 0
        decision_summary = {"jump": 0, "no_jump": 0}

        for i, bird in enumerate(self.birds):
            if bird.alive:
                alive_count += 1
                jump = False

                if self.mode == "human":
                    # Human input handled in events
                    pass
                elif self.mode in ["ai_training", "ai_play"]:
                    # FIXED: AI decision making with detailed debugging
                    if bird.brain:
                        # Get current game state
                        pipes = self.pipe_manager.get_pipes()
                        game_state = bird.get_game_state(pipes)

                        # DEBUG: Log game state for first bird
                        if i == 0 and self.generation_frame_count % 10 == 0:
                            print(
                                f"Frame {self.generation_frame_count}: Bird state = {[f'{x:.3f}' for x in game_state]}")

                        # Make neural network decision
                        try:
                            output = bird.brain.forward_pass(game_state)
                            jump = output > 0.5

                            # DEBUG: Log decisions for analysis
                            if i < 3 and self.generation_frame_count % 15 == 0:
                                print(
                                    f"   Bird {i}: NN output={output:.3f}, jump={jump}")

                        except Exception as e:
                            print(f"⚠️ Neural network error for bird {i}: {e}")
                            jump = random.random() < 0.1  # Fallback

                        # Track decision statistics
                        if jump:
                            decision_summary["jump"] += 1
                        else:
                            decision_summary["no_jump"] += 1

                    else:
                        # Random behavior for birds without brains
                        jump = random.random() < 0.05

                # Update bird physics
                old_y = bird.rect.y
                bird.update(jump)

                # FIXED: More lenient collision detection
                ground_y = self.screen_height - 112
                collision = self.check_bird_collision_detailed(
                    bird, ground_y, i)

                if collision:
                    # DEBUG: Log collision details
                    if self.debug_mode and i < 3:
                        print(
                            f"   Bird {i} collision at frame {self.generation_frame_count}: y={bird.rect.y}, reason={collision}")

        # DEBUG: Print decision summary every 30 frames
        if self.generation_frame_count % 30 == 0 and alive_count > 0:
            total_decisions = sum(decision_summary.values())
            if total_decisions > 0:
                jump_pct = (decision_summary["jump"] / total_decisions) * 100
                print(
                    f"Frame {self.generation_frame_count}: {alive_count} alive, {jump_pct:.1f}% jumping")

    def check_bird_collision_detailed(self, bird, ground_y, bird_index):
        """FIXED: More detailed and lenient collision detection"""
        if not bird.alive:
            return False

        collision_reason = None

        # Check ground collision (with small buffer)
        if bird.rect.bottom >= ground_y - 5:  # 5 pixel buffer
            collision_reason = "ground"
            bird.alive = False

        # Check ceiling collision (with buffer)
        elif bird.rect.top <= 5:  # 5 pixel buffer from ceiling
            collision_reason = "ceiling"
            bird.alive = False

        # Check pipe collision with detailed detection
        else:
            pipes = self.pipe_manager.get_pipes()
            for pipe in pipes:
                if bird.rect.colliderect(pipe.rect):
                    # Use mask collision for pixel-perfect detection
                    try:
                        bird_mask = pygame.mask.from_surface(bird.image)
                        pipe_mask = pygame.mask.from_surface(pipe.image)
                        offset = (pipe.rect.x - bird.rect.x,
                                  pipe.rect.y - bird.rect.y)
                        if bird_mask.overlap(pipe_mask, offset):
                            collision_reason = f"pipe_{pipe.is_top}"
                            bird.alive = False
                            break
                    except:
                        # Fallback to rect collision
                        collision_reason = f"pipe_{pipe.is_top}_rect"
                        bird.alive = False
                        break

        # Handle collision for human mode
        if collision_reason and self.mode == "human":
            self.game_state = GAME_STATES["GAME_OVER"]
            sound = self.asset_loader.get_sound("hit")
            if sound:
                sound.play()
            self.save_high_score()

        return collision_reason

    def check_scoring(self):
        """Check and update scoring with debugging"""
        for bird in self.birds:
            if bird.alive:
                score_gained = self.pipe_manager.check_score(bird)
                if score_gained > 0:
                    bird.score += score_gained
                    self.score = max(self.score, bird.score)

                    print(f"🎯 Bird scored! New score: {bird.score}")

                    # Update high score
                    if self.score > self.high_score:
                        self.high_score = self.score

                    # Play sound
                    sound = self.asset_loader.get_sound("point")
                    if sound:
                        sound.play()

    def check_game_over(self):
        """Check game over conditions with debugging"""
        if self.mode == "ai_training":
            alive_birds = sum(1 for bird in self.birds if bird.alive)
            generation_time = time.time() - self.generation_start_time

            # FIXED: More reasonable timeout and ending conditions
            should_end = (
                alive_birds == 0 or  # All birds dead
                generation_time > 60 or  # 60 second timeout
                self.generation_frame_count > 3600  # 60 seconds at 60fps
            )

            if should_end:
                if generation_time > 60:
                    print(f"⏰ Generation timeout after {generation_time:.1f}s")
                elif self.generation_frame_count > 3600:
                    print(
                        f"⏰ Generation frame limit reached: {self.generation_frame_count}")

                self.end_generation()

        elif self.mode in ["human", "ai_play"]:
            if not any(bird.alive for bird in self.birds):
                self.game_state = GAME_STATES["GAME_OVER"]

    def end_generation(self):
        """FIXED: Handle end of generation with proper fitness calculation"""
        if not self.genetic_algorithm:
            print("❌ No genetic algorithm initialized!")
            return

        generation_time = time.time() - self.generation_start_time

        print(f"\n🧬 Generation {self.generation} Analysis:")
        print(f"   ⏱️  Duration: {generation_time:.1f}s")
        print(f"   🏃‍♂️ Frames survived: {self.generation_frame_count}")

        # FIXED: Calculate fitness based on actual performance
        fitness_scores = []
        individual_stats = []

        for i, bird in enumerate(self.birds):
            # Calculate fitness based on actual survival time and score
            survival_time = self.generation_frame_count if bird.alive else bird.fitness / \
                FITNESS_BONUS_DISTANCE

            # FIXED: Proper fitness calculation
            fitness = (
                survival_time * FITNESS_BONUS_DISTANCE +  # Distance traveled
                bird.score * FITNESS_BONUS_PIPE +         # Pipes passed
                (50 if bird.alive else 0)                 # Survival bonus
            )

            bird.fitness = fitness
            fitness_scores.append(fitness)

            individual_stats.append({
                "id": i,
                "fitness": fitness,
                "score": bird.score,
                "survival": survival_time,
                "alive": bird.alive
            })

        # Update population fitness scores
        self.genetic_algorithm.population.fitness_scores = fitness_scores

        # Display detailed statistics
        alive_birds = sum(1 for bird in self.birds if bird.alive)
        max_fitness = max(fitness_scores) if fitness_scores else 0
        avg_fitness = sum(fitness_scores) / \
            len(fitness_scores) if fitness_scores else 0
        best_score = max(
            bird.score for bird in self.birds) if self.birds else 0
        max_survival = max(
            bird.fitness / FITNESS_BONUS_DISTANCE for bird in self.birds) if self.birds else 0

        print(f"   📊 Alive at end: {alive_birds}/{len(self.birds)}")
        print(f"   🏆 Best fitness: {max_fitness:.1f}")
        print(f"   📈 Average fitness: {avg_fitness:.1f}")
        print(f"   🎯 Best score: {best_score}")
        print(f"   ⚡ Max survival: {max_survival:.1f} frames")

        # Show top performers
        top_performers = sorted(
            individual_stats, key=lambda x: x["fitness"], reverse=True)[:3]
        print(f"   🏅 Top performers:")
        for i, perf in enumerate(top_performers):
            print(
                f"      {i+1}. Bird {perf['id']}: fitness={perf['fitness']:.1f}, score={perf['score']}, survival={perf['survival']:.1f}")

        # Evolve to next generation
        print(f"   🧬 Evolving to generation {self.generation + 1}...")
        gen_stats = self.genetic_algorithm.evolve_generation()

        # Save best individual periodically
        if self.generation % 10 == 0:
            best_fitness = self.genetic_algorithm.save_best_individual()
            print(f"   💾 Saved best bird (fitness: {best_fitness:.2f})")

        # Save statistics
        if self.generation % 5 == 0:
            self.genetic_algorithm.save_generation_stats()
            print(f"   📊 Saved generation statistics")

        # Prepare for next generation
        self.generation += 1
        self.generation_start_time = time.time()
        self.generation_frame_count = 0
        self.score = 0

        # Clear pipes and create new birds
        self.pipe_manager.clear()
        self.create_ai_birds_with_debugging()

        print(f"   ✅ Generation {self.generation} ready!\n")

    def update_fps_counter(self):
        self.fps_counter += 1
        if time.time() - self.fps_timer >= 1.0:
            self.current_fps = self.fps_counter
            self.fps_counter = 0
            self.fps_timer = time.time()

    def render_game(self):
        self.renderer.clear_screen()

        self.renderer.draw_fps(self.current_fps)
        self.renderer.draw_background(self.theme)
        self.renderer.draw_pipes(self.pipe_manager)
        self.renderer.draw_birds(self.birds)

        ground_y = self.renderer.draw_ground()

        # Draw UI based on game state
        self.render_ui()

        #! DEBUG: Draw additional debug info
        if self.debug_mode:
            self.draw_debug_info()

        # Update display
        pygame.display.flip()

    def draw_debug_info(self):
        """Draw debug information on screen"""
        font = self.asset_loader.get_font("small")
        if font:
            alive_count = sum(1 for bird in self.birds if bird.alive)
            debug_text = f"DEBUG: Frame {self.generation_frame_count}, Alive: {alive_count}"
            text_surface = font.render(debug_text, True, (255, 255, 0))
            self.screen.blit(text_surface, (self.screen_width - 240, self.screen_height - 80))

    def render_ui(self):
        """Render user interface"""
        if self.game_state == GAME_STATES["MENU"]:
            self.renderer.draw_start_message()
        elif self.game_state == GAME_STATES["PLAYING"] or self.game_state == GAME_STATES["TRAINING"]:
            # Draw score
            self.renderer.draw_score(self.score)

            # Draw mode-specific information
            if self.mode == "human":
                self.draw_human_ui()
            elif self.mode == "ai_training":
                self.draw_ai_training_ui()
            elif self.mode == "ai_play":
                self.draw_ai_play_ui()

        elif self.game_state == GAME_STATES["GAME_OVER"]:
            self.renderer.draw_game_over()
            self.renderer.draw_score(self.score)

            # Draw high score
            font = self.asset_loader.get_font("medium")
            if font:
                text = font.render(
                    f"High Score: {self.high_score}", True, (255, 255, 255))
                rect = text.get_rect(center=(self.screen_width//2, 300))
                self.screen.blit(text, rect)

    def draw_human_ui(self):
        """Draw UI for human player mode"""
        stats = {
            "High Score": self.high_score,
            "Time": f"{time.time() - self.game_start_time:.1f}s",
            "FPS": self.current_fps
        }
        self.renderer.draw_statistics(stats, 10, 10, "Game Stats")

    def draw_ai_training_ui(self):
        if not self.genetic_algorithm:
            return

        alive_birds = sum(1 for bird in self.birds if bird.alive)
        scores = [bird.score for bird in self.birds]
        best_score = max(scores) if scores else 0

        # Get current fitness scores
        if self.birds:
            current_fitness = [bird.fitness for bird in self.birds]
            best_fitness = max(current_fitness) if current_fitness else 0
            avg_fitness = sum(current_fitness) / \
                len(current_fitness) if current_fitness else 0
        else:
            best_fitness = 0
            avg_fitness = 0

        # Draw AI training stats top-left with smaller font/block
        self.renderer.draw_ai_info(
            self.generation,
            alive_birds,
            best_score,
            best_fitness,
            avg_fitness,
            len(self.birds),
            x=self.screen_width - 180,
            y=15,
            font_size='small'
        )

        # Draw training progress bar at bottom-left
        progress = self.generation / GENERATIONS
        self.renderer.draw_progress_bar(
            progress, 15, self.screen_height - 38, 250, 18, label="Training Progress")

        # Draw FPS at bottom-left, just above progress bar
        self.renderer.draw_fps(self.current_fps, 15, self.screen_height - 80)

    def draw_ai_play_ui(self):
        """Draw UI for AI play mode"""
        if self.birds:
            bird = self.birds[0]
            stats = {
                "Score": bird.score,
                "Fitness": bird.fitness,
                "Status": "Alive" if bird.alive else "Dead"
            }
            self.renderer.draw_statistics(stats, 10, 10, "AI Performance")

    def restart_game(self):
        self.game_state = GAME_STATES["PLAYING"]
        self.score = 0
        self.frame_count = 0
        self.generation_frame_count = 0
        self.game_start_time = time.time()
        self.pipe_manager.clear()

        # Reinitialize birds based on mode
        self.init_game_mode()

    def load_high_score(self):
        """Load high score from file"""
        try:
            with open("data/high_score.txt", "r") as f:
                return int(f.read().strip())
        except:
            return 0

    def save_high_score(self):
        """Save high score to file"""
        try:
            import os
            os.makedirs("data", exist_ok=True)
            with open("data/high_score.txt", "w") as f:
                f.write(str(self.high_score))
        except Exception as e:
            print(f"Could not save high score: {e}")

    def run(self):
        """Main game loop"""
        print(f"🚀 Starting Flappy Bird DEBUG MODE in {self.mode} mode")
        print("Press 'D' to toggle debug info during gameplay")
        running = True

        while running:
            # Handle events
            running = self.handle_events()

            if not running:
                break

            # Update game
            self.update_game()

            # Render
            self.render_game()

            # Control framerate
            self.clock.tick(FPS)

        # Cleanup
        self.save_high_score()
        print("Game ended. Thanks for playing!")
        pygame.quit()
        sys.exit()
