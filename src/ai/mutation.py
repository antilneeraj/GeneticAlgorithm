import numpy as np
import random


class Mutation:
    @staticmethod
    def gaussian_mutation(individual, mutation_rate=0.1, mutation_strength=0.2):
        """
        Gaussian mutation: Add random noise to weights and biases

        Args:
            individual: Neural network to mutate
            mutation_rate: Probability of mutating each parameter
            mutation_strength: Standard deviation of Gaussian noise

        Returns:
            Mutated neural network
        """
        mutated_individual = individual.copy()
        params = mutated_individual.get_weights_as_array()

        for i in range(len(params)):
            if random.random() < mutation_rate:
                # Add Gaussian noise
                params[i] += np.random.normal(0, mutation_strength)

        mutated_individual.set_weights_from_array(params)
        return mutated_individual

    @staticmethod
    def uniform_mutation(individual, mutation_rate=0.1, mutation_range=0.5):
        """
        Uniform mutation: Replace parameters with random values in range

        Args:
            individual: Neural network to mutate
            mutation_rate: Probability of mutating each parameter
            mutation_range: Range for uniform random values [-range, +range]

        Returns:
            Mutated neural network
        """
        mutated_individual = individual.copy()
        params = mutated_individual.get_weights_as_array()

        for i in range(len(params)):
            if random.random() < mutation_rate:
                # Replace with uniform random value
                params[i] = random.uniform(-mutation_range, mutation_range)

        mutated_individual.set_weights_from_array(params)
        return mutated_individual

    @staticmethod
    def adaptive_mutation(individual, generation, max_generations,
                          initial_rate=0.3, final_rate=0.05, mutation_strength=0.2):
        """
        Adaptive mutation: Mutation rate decreases over generations

        Args:
            individual: Neural network to mutate
            generation: Current generation number
            max_generations: Total number of generations
            initial_rate: Starting mutation rate
            final_rate: Ending mutation rate
            mutation_strength: Strength of mutations

        Returns:
            Mutated neural network
        """
        # Calculate adaptive mutation rate
        progress = generation / max_generations
        mutation_rate = initial_rate * (1 - progress) + final_rate * progress

        return Mutation.gaussian_mutation(individual, mutation_rate, mutation_strength)
