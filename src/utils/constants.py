import os

# =============================================================================
# ASSET PATHS
# =============================================================================
ASSETS_DIR = "assets"
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

# =============================================================================
# DISPLAY SETTINGS
# =============================================================================
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
FPS = 60

# =============================================================================
# GAME PHYSICS
# =============================================================================
GRAVITY = 0.5
JUMP_STRENGTH = -9
BIRD_SIZE = 34

# =============================================================================
# PIPE SETTINGS
# =============================================================================
PIPE_WIDTH = 80
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds between pipes
PIPE_SPEED = 3

# =============================================================================
# GROUND SETTINGS
# =============================================================================
GROUND_HEIGHT = 112  # Based on base.png height
GROUND_SPEED = 3

# =============================================================================
# COLORS (RGB)
# =============================================================================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# =============================================================================
# BIRD TYPES (matching your assets)
# =============================================================================
BIRD_TYPES = {
    "BLUE": "bluebird",
    "RED": "redbird",
    "YELLOW": "yellowbird"
}

# =============================================================================
# PIPE TYPES (matching your assets)
# =============================================================================
PIPE_TYPES = {
    "GREEN": "pipe-green.png",
    "RED": "pipe-red.png"
}

# =============================================================================
# BACKGROUND TYPES (matching your assets)
# =============================================================================
BACKGROUND_TYPES = {
    "DAY": "background-day.png",
    "NIGHT": "background-night.png"
}

# =============================================================================
# GAME STATES
# =============================================================================
GAME_STATES = {
    "MENU": 0,
    "PLAYING": 1,
    "GAME_OVER": 2,
    "TRAINING": 3,
    "PAUSED": 4
}

# =============================================================================
# AUDIO SETTINGS
# =============================================================================
SOUND_VOLUME = 0.5
MUSIC_VOLUME = 0.3

# =============================================================================
# GENETIC ALGORITHM PARAMETERS
# =============================================================================

# Population Settings
POPULATION_SIZE = 150          # INCREASED: More birds = higher chance of good mutation
GENERATIONS = 1000
ELITE_COUNT = 10               # Keep top 10 to ensure best traits persist

# Evolution Rates
MUTATION_RATE = 0.2            # Increased to 20% to prevent stagnation
CROSSOVER_RATE = 0.7

# Selection Parameters
TOURNAMENT_SIZE = 3           # Size of tournament selection groups
SELECTION_PRESSURE = 1.5      # Pressure for rank-based selection

# Mutation Parameters
MUTATION_STRENGTH = 0.2       # Standard deviation for Gaussian mutation
MUTATION_RANGE = 0.5          # Range for uniform mutation
ADAPTIVE_MUTATION = True      # Enable adaptive mutation rates

# =============================================================================
# NEURAL NETWORK ARCHITECTURE
# =============================================================================

# Network Structure
# Bird inputs: [y_pos, velocity, pipe_dist, gap_y]
NN_INPUT_NODES = 4
NN_HIDDEN_NODES = [6, 4]      # Hidden layers: [layer1_size, layer2_size]
NN_OUTPUT_NODES = 1           # Output: jump decision (0-1)

# Activation Functions
HIDDEN_ACTIVATION = "tanh"    # Hidden layer activation
OUTPUT_ACTIVATION = "sigmoid"  # Output layer activation

# Weight Initialization
WEIGHT_INIT_RANGE = 0.5       # Range for random weight initialization
BIAS_INIT_RANGE = 0.5         # Range for random bias initialization

# =============================================================================
# FITNESS CALCULATION PARAMETERS
# =============================================================================

# Base Fitness Components
FITNESS_BONUS_PIPE = 200      # Higher reward for passing pipe
FITNESS_BONUS_DISTANCE = 0.1    # Lower reward for just surviving (discourages floating at top)
FITNESS_PENALTY_DEATH = -10

# Advanced Fitness Bonuses
FITNESS_BONUS_CONSISTENCY = 50   # Bonus for consistent performance
FITNESS_BONUS_EFFICIENCY = 25    # Bonus for smooth/efficient flight
FITNESS_BONUS_HIGH_SCORE = 200   # Extra bonus for scores > 10

# Fitness Modifiers
FITNESS_GENERATION_MULTIPLIER = 0.1  # Increase fitness slightly each generation
# Weight for diversity-based fitness adjustment
FITNESS_DIVERSITY_WEIGHT = 0.1

# =============================================================================
# TRAINING PARAMETERS
# =============================================================================

# Time Limits
MAX_GAME_TIME = 30000         # Maximum milliseconds per bird per generation
MAX_IDLE_TIME = 5000          # Maximum time without progress before ending
GENERATION_TIMEOUT = 120      # Maximum seconds per generation

# Training Control
AUTO_SAVE_INTERVAL = 10       # Save best bird every N generations
STATS_SAVE_INTERVAL = 5       # Save statistics every N generations
CONVERGENCE_THRESHOLD = 0.01  # Fitness improvement threshold for convergence

# Performance Settings
MAX_VISIBLE_BIRDS = 10        # Limit birds shown for performance
SPEED_MULTIPLIER = 1.0        # Game speed during training (1.0 = normal)
HEADLESS_TRAINING = False     # Run without graphics for faster training

# =============================================================================
# DATA PATHS
# =============================================================================

# Directories
DATA_DIR = "data"
MODELS_DIR = os.path.join(DATA_DIR, "models")
STATS_DIR = os.path.join(DATA_DIR, "statistics")
LOGS_DIR = "logs"

# File Names
BEST_BIRD_FILE = os.path.join(MODELS_DIR, "best_bird.json")
GENERATION_STATS_FILE = os.path.join(STATS_DIR, "generation_stats.csv")
EVOLUTION_STATS_FILE = os.path.join(STATS_DIR, "evolution_stats.json")
TRAINING_LOG_FILE = os.path.join(LOGS_DIR, "training.log")

# Backup Files
BACKUP_INTERVAL = 20          # Backup every N generations
BACKUP_COUNT = 5              # Keep last N backups

# =============================================================================
# ALGORITHM CONFIGURATION
# =============================================================================

# Selection Methods
SELECTION_METHODS = {
    "tournament": "Tournament Selection",
    "roulette": "Roulette Wheel Selection",
    "rank": "Rank-Based Selection",
    "elite": "Elite Selection"
}

# Crossover Methods
CROSSOVER_METHODS = {
    "single_point": "Single-Point Crossover",
    "two_point": "Two-Point Crossover",
    "uniform": "Uniform Crossover",
    "arithmetic": "Arithmetic Crossover"
}

# Mutation Methods
MUTATION_METHODS = {
    "gaussian": "Gaussian Mutation",
    "uniform": "Uniform Mutation",
    "creep": "Creep Mutation",
    "boundary": "Boundary Mutation",
    "adaptive": "Adaptive Mutation"
}

# Default Algorithm Configuration
DEFAULT_SELECTION = "tournament"
DEFAULT_CROSSOVER = "single_point"
DEFAULT_MUTATION = "gaussian"

# =============================================================================
# DEBUGGING & VISUALIZATION
# =============================================================================

# Debug Settings
DEBUG_MODE = False            # Enable debug output
VERBOSE_LOGGING = False       # Detailed logging
SHOW_NEURAL_NETWORK = False   # Visualize neural networks
SHOW_GAME_STATE = False       # Show bird input states

# Statistics Display
SHOW_GENERATION_STATS = True  # Display generation statistics
SHOW_FITNESS_GRAPH = True     # Show real-time fitness graph
SHOW_DIVERSITY_GRAPH = True   # Show genetic diversity graph
UPDATE_FREQUENCY = 60         # Update display every N frames

# Performance Monitoring
MONITOR_PERFORMANCE = True    # Track performance metrics
MEMORY_MONITORING = False     # Monitor memory usage
FPS_MONITORING = True         # Monitor frame rate

# =============================================================================
# VERSION INFORMATION
# =============================================================================
VERSION = "1.0.0"
AUTHOR = "Neeraj Antil"
DESCRIPTION = "Flappy Bird with Genetic Algorithm AI"
BUILD_DATE = "2025-09-23"

# =============================================================================
# VALIDATION HELPERS
# =============================================================================


def validate_constants():
    """Validate that all constants are properly set"""
    assert POPULATION_SIZE > 0, "Population size must be positive"
    assert GENERATIONS > 0, "Generations must be positive"
    assert 0 <= MUTATION_RATE <= 1, "Mutation rate must be between 0 and 1"
    assert 0 <= CROSSOVER_RATE <= 1, "Crossover rate must be between 0 and 1"
    assert ELITE_COUNT < POPULATION_SIZE, "Elite count must be less than population size"
    assert len(NN_HIDDEN_NODES) > 0, "Must have at least one hidden layer"
    assert NN_INPUT_NODES > 0, "Must have input nodes"
    assert NN_OUTPUT_NODES > 0, "Must have output nodes"


def print_config_summary():
    """Print a summary of the current configuration"""
    print("GENETIC ALGORITHM CONFIGURATION")
    print("="*50)
    print(f"Population Size: {POPULATION_SIZE}")
    print(f"Generations: {GENERATIONS}")
    print(f"Elite Count: {ELITE_COUNT}")
    print(f"Mutation Rate: {MUTATION_RATE}")
    print(f"Crossover Rate: {CROSSOVER_RATE}")
    print(
        f"Neural Network: {NN_INPUT_NODES} → {NN_HIDDEN_NODES} → {NN_OUTPUT_NODES}")
    print(f"Fitness - Pipe Bonus: {FITNESS_BONUS_PIPE}")
    print(f"Fitness - Distance Bonus: {FITNESS_BONUS_DISTANCE}")
    print(f"Fitness - Death Penalty: {FITNESS_PENALTY_DEATH}")


if __name__ == "__main__":
    # Run validation and print config when file is executed directly
    validate_constants()
    print_config_summary()
