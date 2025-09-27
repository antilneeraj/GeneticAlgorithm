from src.ai.neural_network import NeuralNetwork
import numpy as np
import time

# Create 3 different networks
networks = []
for i in range(3):
    seed = (int(time.time() * 1000000) + i * 1000) % (2**31 - 1)
    nn = NeuralNetwork(4, [6, 4], 1, seed=seed)
    networks.append(nn)

# Test with same input - should get different outputs
test_input = [0.5, 0.0, 0.8, 0.5]
for i, nn in enumerate(networks):
    output = nn.forward_pass(test_input)
    print(f"Network {i+1}: {output:.4f}")  # Should be different!
