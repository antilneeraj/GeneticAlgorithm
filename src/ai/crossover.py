import numpy as np
import random


class Crossover:
    @staticmethod
    def single_point_crossover(parent1, parent2):
        """Single-point crossover: Split at one random point"""
        # Get parent parameters as arrays
        params1 = parent1.get_weights_as_array()
        params2 = parent2.get_weights_as_array()

        # Random crossover point
        crossover_point = random.randint(1, len(params1) - 1)

        # Create offspring
        child1_params = np.concatenate([params1[:crossover_point],
                                        params2[crossover_point:]])
        child2_params = np.concatenate([params2[:crossover_point],
                                        params1[crossover_point:]])

        # Create child networks
        child1 = parent1.copy()
        child2 = parent2.copy()
        child1.set_weights_from_array(child1_params)
        child2.set_weights_from_array(child2_params)

        return child1, child2

    @staticmethod
    def uniform_crossover(parent1, parent2, crossover_rate=0.5):
        """Uniform crossover: Each gene independently chosen from either parent"""
        params1 = parent1.get_weights_as_array()
        params2 = parent2.get_weights_as_array()

        # Create offspring parameters
        child1_params = np.zeros_like(params1)
        child2_params = np.zeros_like(params2)

        for i in range(len(params1)):
            if random.random() < crossover_rate:
                child1_params[i] = params1[i]
                child2_params[i] = params2[i]
            else:
                child1_params[i] = params2[i]
                child2_params[i] = params1[i]

        # Create child networks
        child1 = parent1.copy()
        child2 = parent2.copy()
        child1.set_weights_from_array(child1_params)
        child2.set_weights_from_array(child2_params)

        return child1, child2

    @staticmethod
    def arithmetic_crossover(parent1, parent2, alpha=0.5):
        """Arithmetic crossover: Weighted average of parent parameters"""
        params1 = parent1.get_weights_as_array()
        params2 = parent2.get_weights_as_array()

        # Create offspring as weighted averages
        child1_params = alpha * params1 + (1 - alpha) * params2
        child2_params = alpha * params2 + (1 - alpha) * params1

        # Create child networks
        child1 = parent1.copy()
        child2 = parent2.copy()
        child1.set_weights_from_array(child1_params)
        child2.set_weights_from_array(child2_params)

        return child1, child2
