# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a **Flappy Bird AI** project that uses genetic algorithms and neural networks to evolve AI players that learn to play Flappy Bird without any training data. Birds start with random behavior and evolve over generations to achieve expert-level gameplay.

**Key Technologies:**
- Neural Networks (custom implementation with 4→6→4→1 architecture)
- Genetic Algorithm evolution with elitism, crossover, and mutation
- Pygame for game simulation and visualization
- Real-time performance monitoring and statistics

## Common Commands

### Running the Game/AI
```powershell
# Watch AI learn to play (main training mode)
python main.py --mode ai_training --population 50

# Play the game manually
python main.py --mode human

# Watch trained AI play
python main.py --mode ai_play

# Run with different parameters
python main.py --mode ai_training --population 100 --generations 200 --fps 120
```

### Development & Testing
```powershell
# Run AI diagnostics and debugging
python diagnostic_ai_debug.py

# Validate neural network implementation
python validateNN.py

# Validate AI constants and parameters
python validate_ai_constants.py

# Run tests
python -m pytest tests/

# Run tests with coverage
python -m pytest --cov=src tests/
```

### Code Quality & Formatting
```powershell
# Format code
python -m black src/
python -m isort src/

# Check linting
python -m flake8 src/

# Install development dependencies
pip install -r requirements-dev.txt
```

### Environment Setup
```powershell
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Architecture Overview

### Core Components

**1. Genetic Algorithm Pipeline**
- `src/ai/genetic_algorithm.py` - Main evolution orchestrator
- `src/ai/population.py` - Population management and statistics
- `src/ai/selection.py` - Parent selection methods (tournament, roulette, rank)
- `src/ai/crossover.py` - Breeding strategies (single-point, uniform, arithmetic)
- `src/ai/mutation.py` - Genetic mutation (Gaussian, adaptive, boundary)
- `src/ai/fitness.py` - Fitness evaluation with survival + performance bonuses

**2. Neural Network Brain**
- `src/ai/neural_network.py` - Custom NN implementation
- Architecture: 4 inputs → [6, 4] hidden → 1 output
- Inputs: bird_y_position, velocity, pipe_distance, gap_center_distance
- Output: jump_decision (sigmoid activation > 0.5 = jump)

**3. Game Engine**
- `src/game/game_engine.py` - Main game loop and AI training coordinator
- `src/game/bird.py` - Bird physics, collision detection, AI brain integration
- `src/game/pipe.py` - Pipe generation and collision boundaries
- `src/game/renderer.py` - Graphics rendering and performance visualization

**4. Configuration & Constants**
- `src/utils/constants.py` - All tunable parameters for GA, NN, and game physics
- `config/` - Modular configuration files for different aspects

### Training Flow

1. **Population Initialization**: 50 birds with random neural network weights
2. **Simulation**: All birds play simultaneously until they die or timeout
3. **Fitness Evaluation**: Score based on survival time + pipes passed + consistency bonuses
4. **Selection**: Tournament selection picks parents weighted by fitness
5. **Reproduction**: Crossover + mutation creates next generation
6. **Elitism**: Top 5 performers are preserved unchanged
7. **Repeat**: Process continues for 100+ generations until convergence

### Key Parameters (src/utils/constants.py)

**Genetic Algorithm:**
- `POPULATION_SIZE = 50` - Birds per generation
- `MUTATION_RATE = 0.1` - 10% mutation probability
- `CROSSOVER_RATE = 0.8` - 80% crossover probability  
- `ELITE_COUNT = 5` - Top performers preserved

**Neural Network:**
- `NN_INPUT_NODES = 4` - Game state inputs
- `NN_HIDDEN_NODES = [6, 4]` - Hidden layer architecture
- `NN_OUTPUT_NODES = 1` - Jump decision output

**Fitness Calculation:**
- `FITNESS_BONUS_PIPE = 100` - Points per pipe passed
- `FITNESS_BONUS_DISTANCE = 1` - Points per frame survived
- `FITNESS_PENALTY_DEATH = -50` - Death penalty

### Debug & Diagnostics

The codebase includes comprehensive debugging tools:

- **Neural Network Diversity Testing**: Ensures networks have different weights/behaviors
- **Game State Validation**: Verifies input data quality and ranges
- **Collision Detection Analysis**: Tests for overly aggressive collision boundaries
- **Performance Monitoring**: Tracks FPS, memory usage, and training metrics
- **Real-time Visualization**: Shows fitness graphs, generation statistics

### Troubleshooting Common Issues

**Birds not learning/identical behavior:**
```powershell
python diagnostic_ai_debug.py  # Check NN diversity
```

**Poor AI performance:**
- Increase `MUTATION_RATE` (try 0.15) for more exploration
- Increase `POPULATION_SIZE` (try 100) for better genetic diversity
- Adjust collision detection buffers in `src/game/bird.py`

**Slow training:**
- Reduce `POPULATION_SIZE` to 20-30 for faster iterations
- Increase `--fps` parameter for faster simulation
- Set `MAX_VISIBLE_BIRDS = 5` to reduce rendering load

### File Organization Notes

- Main entry point: `main.py` with argument parsing
- Dual architecture exists: newer modular `src/` structure + legacy `agents/`, `managers/`, `components/` folders
- Focus on `src/` directory for current implementation
- Configuration split between `src/utils/constants.py` and `config/` files
- Data persistence in `data/` directory for high scores and model saves