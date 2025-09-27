import numpy as np
import json
import time
from src.utils.constants import *


class NeuralNetwork:
    def __init__(self, input_nodes=4, hidden_nodes=[6, 4], output_nodes=1, seed=None):
        """
        Initialize neural network with specified architecture

        Args:
            input_nodes: Number of input neurons (bird state: y, velocity, pipe_x, pipe_y)
            hidden_nodes: List of hidden layer sizes [6, 4] 
            output_nodes: Number of output neurons (1 for jump decision)
            seed: Random seed for initialization (None for automatic)
        """
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Network architecture
        self.layer_sizes = [input_nodes] + hidden_nodes + [output_nodes]
        self.num_layers = len(self.layer_sizes)

        # FIXED: Set unique random seed if not provided
        if seed is not None:
            # Ensure seed is in valid range for numpy
            seed = int(seed) % (2**31 - 1)
            np.random.seed(seed)
        else:
            # Create unique seed based on current time and random component
            unique_seed = (int(time.time() * 1000000) +
                           np.random.randint(0, 100000)) % (2**31 - 1)
            np.random.seed(unique_seed)

        # Initialize weights and biases
        self.weights = []
        self.biases = []
        self.initialize_network()

        # Activation functions
        self.activation_functions = {
            'sigmoid': self.sigmoid,
            'tanh': self.tanh,
            'relu': self.relu,
            'leaky_relu': self.leaky_relu
        }

    def initialize_network(self):
        """FIXED: Initialize weights and biases with proper diversity"""
        for i in range(self.num_layers - 1):
            # Xavier/Glorot initialization for better convergence
            fan_in = self.layer_sizes[i]
            fan_out = self.layer_sizes[i + 1]
            limit = np.sqrt(6.0 / (fan_in + fan_out))

            # Weights: shape (current_layer_size, next_layer_size)
            # FIXED: Add extra randomization to ensure diversity
            weight_matrix = np.random.uniform(-limit, limit,
                                              (self.layer_sizes[i], self.layer_sizes[i + 1]))

            # Add small random perturbation to ensure no two networks are identical
            perturbation = np.random.normal(0, 0.01, weight_matrix.shape)
            weight_matrix += perturbation

            self.weights.append(weight_matrix)

            # Biases: shape (next_layer_size,)
            bias_vector = np.random.uniform(-0.5,
                                            0.5, (self.layer_sizes[i + 1],))

            # Add perturbation to biases too
            bias_perturbation = np.random.normal(0, 0.01, bias_vector.shape)
            bias_vector += bias_perturbation

            self.biases.append(bias_vector)

    def sigmoid(self, x):
        """Sigmoid activation function"""
        # Prevent overflow
        x = np.clip(x, -500, 500)
        return 1.0 / (1.0 + np.exp(-x))

    def tanh(self, x):
        """Hyperbolic tangent activation function"""
        x = np.clip(x, -500, 500)
        return np.tanh(x)

    def relu(self, x):
        """ReLU activation function"""
        return np.maximum(0, x)

    def leaky_relu(self, x, alpha=0.01):
        """Leaky ReLU activation function"""
        return np.where(x > 0, x, alpha * x)

    def forward_pass(self, inputs):
        """
        Perform forward pass through the network

        Args:
            inputs: List/array of input values [bird_y, velocity, pipe_distance, gap_y]

        Returns:
            output: Network output value (0-1 for jump decision)
        """
        if len(inputs) != self.input_nodes:
            raise ValueError(
                f"Expected {self.input_nodes} inputs, got {len(inputs)}")

        # Convert to numpy array and ensure proper shape
        activation = np.array(inputs, dtype=np.float32)

        # Forward propagation through all layers
        for i in range(self.num_layers - 1):
            # Linear transformation: z = w^T * a + b
            z = np.dot(activation, self.weights[i]) + self.biases[i]

            # Apply activation function
            if i < self.num_layers - 2:  # Hidden layers
                activation = self.tanh(z)  # Use tanh for hidden layers
            else:  # Output layer
                # Use sigmoid for output (0-1 probability)
                activation = self.sigmoid(z)

        # Return single output value
        return activation[0] if len(activation) == 1 else activation

    def predict(self, inputs):
        """
        Make a prediction (used by birds during gameplay)

        Args:
            inputs: Game state inputs

        Returns:
            bool: True if bird should jump, False otherwise
        """
        output = self.forward_pass(inputs)
        return output > 0.5  # Jump if output > 0.5

    def get_weights_as_array(self):
        """
        Get all weights and biases as a single flattened array
        Used by genetic algorithm for crossover and mutation

        Returns:
            numpy array: All network parameters flattened
        """
        params = []
        for i in range(len(self.weights)):
            params.extend(self.weights[i].flatten())
            params.extend(self.biases[i].flatten())
        return np.array(params)

    def set_weights_from_array(self, params_array):
        """
        Set network weights and biases from flattened array
        Used by genetic algorithm to create offspring

        Args:
            params_array: Flattened array of all network parameters
        """
        if len(params_array) != self.get_total_params():
            raise ValueError(
                f"Expected {self.get_total_params()} parameters, got {len(params_array)}")

        idx = 0
        for i in range(len(self.weights)):
            # Reshape weights
            weight_size = self.weights[i].size
            self.weights[i] = params_array[idx:idx +
                                           weight_size].reshape(self.weights[i].shape)
            idx += weight_size

            # Reshape biases
            bias_size = self.biases[i].size
            self.biases[i] = params_array[idx:idx +
                                          bias_size].reshape(self.biases[i].shape)
            idx += bias_size

    def get_total_params(self):
        """Get total number of parameters in the network"""
        total = 0
        for i in range(len(self.weights)):
            total += self.weights[i].size + self.biases[i].size
        return total

    def copy(self):
        """Create a deep copy of the neural network"""
        new_network = NeuralNetwork(
            self.input_nodes, self.hidden_nodes, self.output_nodes)
        new_network.set_weights_from_array(self.get_weights_as_array())
        return new_network

    def save_to_file(self, filename):
        """Save network to JSON file"""
        network_data = {
            'architecture': {
                'input_nodes': self.input_nodes,
                'hidden_nodes': self.hidden_nodes,
                'output_nodes': self.output_nodes
            },
            'weights': [w.tolist() for w in self.weights],
            'biases': [b.tolist() for b in self.biases]
        }

        with open(filename, 'w') as f:
            json.dump(network_data, f, indent=2)

    def load_from_file(self, filename):
        """Load network from JSON file"""
        with open(filename, 'r') as f:
            network_data = json.load(f)

        # Restore architecture
        arch = network_data['architecture']
        self.__init__(arch['input_nodes'],
                      arch['hidden_nodes'], arch['output_nodes'])

        # Restore weights and biases
        self.weights = [np.array(w) for w in network_data['weights']]
        self.biases = [np.array(b) for b in network_data['biases']]

    def get_network_info(self):
        """Get network architecture information"""
        return {
            'layers': self.layer_sizes,
            'total_params': self.get_total_params(),
            'connections': [(self.layer_sizes[i], self.layer_sizes[i+1]) for i in range(len(self.layer_sizes)-1)]
        }

    def get_diversity_signature(self):
        """Get a signature for checking network diversity"""
        weights = self.get_weights_as_array()
        return {
            'weight_sum': np.sum(weights),
            'weight_mean': np.mean(weights),
            'weight_std': np.std(weights),
            'weight_sample': weights[:min(10, len(weights))].tolist()
        }

    def __str__(self):
        return f"NeuralNetwork({self.layer_sizes}) - {self.get_total_params()} parameters"
