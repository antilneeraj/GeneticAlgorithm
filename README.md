# 🐦 Flappy Bird AI Evolution 🧬

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![PyGame](https://img.shields.io/badge/PyGame-2.1.3-green)](https://www.pygame.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Watch artificial intelligence master Flappy Bird through genetic evolution!** This project demonstrates how genetic algorithms combined with neural networks can create self-learning game agents that progressively improve their performance across generations.

![Demo GIF](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbHk4eGQ2M2t4dWZ1N3h3cHZ1aTk4eW9kbW0xZ3J6bmZ5bTJ2b3JvYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3ohzdUbYJu1bkNm8ZW/giphy.gif)

## 🚀 Features

- 🧠 **Neural Network AI** with 3-layer architecture (input, hidden, output)
- 🧬 **Genetic Algorithm** implementation with:
  - Tournament selection
  - Uniform crossover
  - Gaussian mutation
  - Elitism preservation
- 🎮 **Pygame Visualization** showing best performer in each generation
- ⚙️ **Configurable Parameters** for evolution and gameplay
- 📊 **Real-time Statistics** tracking fitness scores and generation progress
- 💥 **Collision Detection** with precise physics simulation

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/antilneeraj/GeneticAlgorithm.git
cd GeneticAlgorithm
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🕹️ Usage

```bash
python main.py
```
Watch the AI learn through generations:
- The best bird in each generation is displayed
- Fitness score increases with survival time
- Genetic diversity is maintained through mutation
- Performance improves automatically!

## 🧪 How It Works
Genetic Algorithm Flow
- Selection: Top performers chosen through tournament selection
- Crossover: Neural network weights combined from parents
- Mutation: Random weight modifications for diversity
- Elitism: Best performers carried to next generation

```mermaid
graph TD
    subgraph Input Layer[Input Layer - 3 Neurons]
        I1[ΔY to Gap]
        I2[ΔX to Pipe]
        I3[Velocity]
    end
    
    subgraph Hidden Layer[Hidden Layer - 6 Neurons]
        H1((H1)) -->|Sigmoid|
        H2((H2)) -->|Sigmoid|
        H3((H3)) -->|Sigmoid|
        H4((H4)) -->|Sigmoid|
        H5((H5)) -->|Sigmoid|
        H6((H6)) -->|Sigmoid|
    end
    
    subgraph Output Layer[Output Layer - 1 Neuron]
        O1((Jump?)) -->|Sigmoid|
    end
    
    %% Connections with weights
    I1 -->|w₁₁| H1
    I1 -->|w₁₂| H2
    I1 -->|w₁₃| H3
    I1 -->|w₁₄| H4
    I1 -->|w₁₅| H5
    I1 -->|w₁₆| H6
    
    I2 -->|w₂₁| H1
    I2 -->|w₂₂| H2
    I2 -->|w₂₃| H3
    I2 -->|w₂₄| H4
    I2 -->|w₂₅| H5
    I2 -->|w₂₆| H6
    
    I3 -->|w₃₁| H1
    I3 -->|w₃₂| H2
    I3 -->|w₃₃| H3
    I3 -->|w₃₄| H4
    I3 -->|w₃₅| H5
    I3 -->|w₃₆| H6
    
    H1 -->|wₕ₁| O1
    H2 -->|wₕ₂| O1
    H3 -->|wₕ₃| O1
    H4 -->|wₕ₄| O1
    H5 -->|wₕ₅| O1
    H6 -->|wₕ₆| O1
    
    %% Styling
    classDef input fill:#9f9,stroke:#333;
    classDef hidden fill:#99f,stroke:#333;
    classDef output fill:#f99,stroke:#333;
    
    class I1,I2,I3 input
    class H1,H2,H3,H4,H5,H6 hidden
    class O1 output
    
    style Input_Layer fill:#dfd,stroke:#8f8
    style Hidden_Layer fill:#ddf,stroke:#88f
    style Output_Layer fill:#fdd,stroke:#f88
```

**Key Features:**
1. **Color-coded layers**: 
   - Green = Input layer
   - Blue = Hidden layer
   - Red = Output layer
2. **Mathematical Notation**:
   - ΔY = Vertical distance to pipe gap
   - ΔX = Horizontal distance to pipe
   - w = Connection weights
3. **Activation Functions**: Sigmoid (σ) shown for each neuron
4. **Full Connectivity**: All possible connections between layers
5. **Weight Notation**: Matrix-style weight indices (w₁₁, w₁₂, etc.)

## Neural Network Architecture

- Inputs:
  - Horizontal distance to next pipe
  - Vertical distance to pipe gap
  - Current velocity

- Hidden Layer: 6 neurons with sigmoid activation
- Output: Jump probability

## ⚙️ Customization
Modify `utils/config.py` to tweak parameters:
```python
CONFIG = {
    'SCREEN_WIDTH': 400,          # Window width
    'SCREEN_HEIGHT': 600,         # Window height
    'POPULATION_SIZE': 50,        # Number of birds per generation
    'MUTATION_RATE': 0.1,         # Chance of weight mutation
    'ELITISM': 0.2,               # Percentage of top performers to keep
    'PIPE_GAP': 160,              # Space between pipe pairs
    'GRAVITY': 0.5,               # Downward acceleration
    'JUMP_FORCE': -12             # Upward thrust strength
}
```

## 📺 Demo
<To add a gif to show Generation Progress>
Example of AI learning progress over generations

## 🤝 Contributing
We welcome contributions! Here's how:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.

🙏 Acknowledgments
- Inspired by classic Flappy Bird game
- Pygame community for excellent documentation
- NumPy for efficient matrix operations
