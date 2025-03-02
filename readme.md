# **Flappy Bird AI - Neural Network-Based Evolutionary Agent**

## 📌 Introduction
This project implements an AI agent to play a Flappy Bird-like game using **Neural Networks and Evolutionary Algorithms**. The agents learn to navigate through pipes by evolving over generations, improving their performance with **genetic algorithms**.  

## 🎯 Objectives
- Develop an AI agent that learns to play Flappy Bird using **Neural Networks**.  
- Implement **evolutionary learning** for continuous improvement.  
- Simulate a **genetic algorithm** for natural selection among agents.  
- Experiment with **mutation** for better performance.  

## 🌟 Highlights
- **AI-powered gameplay**: No human intervention needed.  
- **Neural Network-based decision-making** for flapping.  
- **Genetic Algorithm for Evolution**: Best agents survive and reproduce.  
- **Vision-based AI**: Agents "see" pipes and decide actions.  

## 🔧 Recent Updates / Changes
- **Randomized Initial Y**: Each bird starts at a random vertical position to avoid converging at the same point.  
- **Top Collision**: Birds now die if they collide with the top boundary, preventing them from “sticking” there.  
- **Reduced Flap Strength**: The flap velocity was lowered from -7 to -6 to give more precise control.  
- **Increased Pipe Gap (Optional)**: Pipe openings can be widened to make early learning easier.  
- **Lower Mutation Rate**: Reduced from 80% to 20% for more stable evolution.  
- **Improved Fitness**: Birds gain extra points for each pipe they pass, in addition to lifespan-based scoring.  

## 🔬 Methodology
1. **Initialize Population**  
   Random agents with different neural network weights.  
2. **Vision Processing**  
   Agents detect pipes, ground, and boundaries.  
3. **Decision Making**  
   The neural network predicts whether to flap or not.  
4. **Fitness Calculation**  
   Longer survival + passing pipes → higher fitness.  
5. **Natural Selection**  
   The best-performing agents reproduce for the next generation.  
6. **Mutation & Evolution**  
   New agents inherit traits with slight mutations to explore new strategies.  

## 🛠️ Software and Libraries Used
- **Python** (Main language)  
- **Pygame** (For game rendering)  
- **NumPy** (For potential matrix operations)  
- **Random** (For mutations and randomness in evolution)  

## 🚀 Usage
### 1️⃣ **Setup the Environment**
Make sure you have Python installed, then install dependencies:
```bash
pip install pygame numpy
```
### 2️⃣ **Run the Game**
Execute the main application:
```bash
python app.py
```
### 3️⃣ **Observe the AI**
Watch how the agents evolve and improve over time. You’ll see statistics like:
- Generation Count
- Number of Agents Alive
- Average Fitness
- Number of Pipes Passed

### 🔮 **Future Scope**
- Implement Deep Reinforcement Learning for more advanced training.
- Introduce multi-layered (hidden-layer) Neural Networks for richer decision-making.
- Add GUI-based visualization of each agent’s network and fitness progress.
- Extend to more complex environments for broader generalization.