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

[![](https://mermaid.ink/img/pako:eNqNlP9q2zAQx19FqBQSUKCWHEM92BgLTB5jGWSUbvMYmq0korZkbHkQSt9iz7Vn2sVKjK-02_SXP987fXWnH76nhSs1TemuVc2efFrllsDo-h9ByGzT--_v1UG3X3M6EBmIzAT5oPvW2W6e029h2nFkEST-_vWZeEfeqgbH-BC7PcY-mkbjoIDgja5cYfxhjGhbho9HhUlTltqOlQU8l5aMpZEF2Zhd7UxJXhfe_FTeOIuWldFsJqP5fKJwUDhSBCgCKTEoMVKWoCyRkoCSnJXnGln3frrFAc-NRKdG_qOPNfTxrq-bV88seHlJ3jhrdXGc2QUti8hi8RK2ACPHKDDGGJcYk-maGcf-HPtz7M-xP8f-_Cl_gf0F9hfYX2B_gf3FE_4yNLU--UuOUWCMMS4xJgjHM9n4Q2XsLnBRqa5b6S0xw0PbmqpKL66vkqtoyzrfujudXgghXjzK3ofLf0q__muuC_frH9aTSXCyLOMM9mcoahqREZOcScFkzOSSQYuhkmnOOjotSRmtdVsrU8Lf5v6YklO_1zX8BFL4LFV7l9PcPkCe6r3bHGxBU9_2mtHW9bs9Tbeq6oD6plRer4yC91OPaqPsF-fO_PAHDctN9g?type=png)](https://mermaid.live/edit#pako:eNqNlP9q2zAQx19FqBQSUKCWHEM92BgLTB5jGWSUbvMYmq0korZkbHkQSt9iz7Vn2sVKjK-02_SXP987fXWnH76nhSs1TemuVc2efFrllsDo-h9ByGzT--_v1UG3X3M6EBmIzAT5oPvW2W6e029h2nFkEST-_vWZeEfeqgbH-BC7PcY-mkbjoIDgja5cYfxhjGhbho9HhUlTltqOlQU8l5aMpZEF2Zhd7UxJXhfe_FTeOIuWldFsJqP5fKJwUDhSBCgCKTEoMVKWoCyRkoCSnJXnGln3frrFAc-NRKdG_qOPNfTxrq-bV88seHlJ3jhrdXGc2QUti8hi8RK2ACPHKDDGGJcYk-maGcf-HPtz7M-xP8f-_Cl_gf0F9hfYX2B_gf3FE_4yNLU--UuOUWCMMS4xJgjHM9n4Q2XsLnBRqa5b6S0xw0PbmqpKL66vkqtoyzrfujudXgghXjzK3ofLf0q__muuC_frH9aTSXCyLOMM9mcoahqREZOcScFkzOSSQYuhkmnOOjotSRmtdVsrU8Lf5v6YklO_1zX8BFL4LFV7l9PcPkCe6r3bHGxBU9_2mtHW9bs9Tbeq6oD6plRer4yC91OPaqPsF-fO_PAHDctN9g)

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
