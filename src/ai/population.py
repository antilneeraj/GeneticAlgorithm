import random
from src.ai.neural_network import NeuralNetwork
from src.utils.constants import *


class Population:
    def __init__(self, size, network_architecture=None):
        """
        Initialize population of neural networks

        Args:
            size: Population size
            network_architecture: Dict with input_nodes, hidden_nodes, output_nodes
        """
        self.size = size
        self.individuals = []
        self.fitness_scores = []
        self.generation = 0

        # Default architecture for Flappy Bird
        if network_architecture is None:
            network_architecture = {
                'input_nodes': NN_INPUT_NODES,
                'hidden_nodes': NN_HIDDEN_NODES,
                'output_nodes': NN_OUTPUT_NODES
            }

        self.architecture = network_architecture
        self.initialize_population()

    def initialize_population(self):
        """Create initial random population"""
        self.individuals = []
        for _ in range(self.size):
            network = NeuralNetwork(
                input_nodes=self.architecture['input_nodes'],
                hidden_nodes=self.architecture['hidden_nodes'],
                output_nodes=self.architecture['output_nodes']
            )
            self.individuals.append(network)

        self.fitness_scores = [0.0] * self.size

    def get_best_individual(self):
        """Get the best performing individual"""
        if not self.fitness_scores:
            return None

        best_idx = max(range(len(self.fitness_scores)),
                       key=lambda i: self.fitness_scores[i])
        return self.individuals[best_idx], self.fitness_scores[best_idx]

    def get_average_fitness(self):
        """Get average fitness of population"""
        return sum(self.fitness_scores) / len(self.fitness_scores) if self.fitness_scores else 0

    def get_fitness_statistics(self):
        """Get comprehensive fitness statistics"""
        if not self.fitness_scores:
            return {'min': 0, 'max': 0, 'avg': 0, 'std': 0}

        import numpy as np
        scores = np.array(self.fitness_scores)
        return {
            'min': float(np.min(scores)),
            'max': float(np.max(scores)),
            'avg': float(np.mean(scores)),
            'std': float(np.std(scores)),
            'median': float(np.median(scores))
        }

    def replace_population(self, new_individuals):
        """Replace current population with new individuals"""
        if len(new_individuals) != self.size:
            raise ValueError(
                f"New population size {len(new_individuals)} != expected size {self.size}")

        self.individuals = new_individuals
        self.fitness_scores = [0.0] * self.size
        self.generation += 1

    def sort_by_fitness(self, descending=True):
        """Sort population by fitness"""
        sorted_data = sorted(zip(self.individuals, self.fitness_scores),
                             key=lambda x: x[1], reverse=descending)
        self.individuals, self.fitness_scores = zip(*sorted_data)
        self.individuals = list(self.individuals)
        self.fitness_scores = list(self.fitness_scores)

    def save_best(self, filename):
        """Save best individual to file"""
        best_individual, best_fitness = self.get_best_individual()
        if best_individual:
            best_individual.save_to_file(filename)
            return best_fitness
        return 0

    def get_diversity_measure(self):
        """Calculate genetic diversity of population"""
        if len(self.individuals) < 2:
            return 0

        # Calculate average pairwise distance between individuals
        total_distance = 0
        comparisons = 0

        for i in range(min(10, len(self.individuals))):  # Sample for performance
            for j in range(i + 1, min(10, len(self.individuals))):
                params1 = self.individuals[i].get_weights_as_array()
                params2 = self.individuals[j].get_weights_as_array()
                distance = sum(abs(p1 - p2)
                               for p1, p2 in zip(params1, params2))
                total_distance += distance
                comparisons += 1

        return total_distance / comparisons if comparisons > 0 else 0

    def __len__(self):
        return len(self.individuals)

    def __str__(self):
        stats = self.get_fitness_statistics()
        return (f"Population(size={self.size}, gen={self.generation}, "
                f"fitness: avg={stats['avg']:.2f}, max={stats['max']:.2f})")
