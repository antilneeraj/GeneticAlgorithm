import random
import numpy as np
from game.models.bird import Bird

class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate=0.1, elitism=0.2):
        try:
            self.population_size = population_size
            self.mutation_rate = mutation_rate
            self.elitism = elitism
            self.generation = 0
            
            if not (0 <= elitism <= 1):
                raise ValueError("Elitism must be between 0 and 1")
        except Exception as e:
            print(f"GA initialization error: {str(e)}")
            raise

    def evolve(self, population):
        try:
            population.sort(key=lambda x: x.fitness, reverse=True)
            elite_size = int(self.elitism * self.population_size)
            elites = population[:elite_size]
            
            offspring = []
            while len(offspring) < self.population_size - elite_size:
                parent1 = self._select_parent(population)
                parent2 = self._select_parent(population)
                child_weights = self._crossover(parent1, parent2)
                self._mutate(child_weights)
                offspring.append(Bird(genome=child_weights))
            
            self.generation += 1
            return elites + offspring
        except Exception as e:
            print(f"Evolution error: {str(e)}")
            return population

    def _select_parent(self, population):
        try:
            tournament = random.sample(population, min(5, len(population)))
            return max(tournament, key=lambda x: x.fitness)
        except Exception as e:
            print(f"Parent selection error: {str(e)}")
            return random.choice(population)

    def _crossover(self, parent1, parent2):
        try:
            child_weights = []
            for w1, w2 in zip(parent1.genome, parent2.genome):
                mask = np.random.rand(*w1.shape) < 0.5
                child_w = np.where(mask, w1, w2)
                child_weights.append(child_w)
            return child_weights
        except Exception as e:
            print(f"Crossover error: {str(e)}")
            return parent1.genome

    def _mutate(self, child_weights):
        try:
            for i in range(len(child_weights)):
                if random.random() < self.mutation_rate:
                    mutation = np.random.normal(scale=0.1, size=child_weights[i].shape)
                    child_weights[i] += mutation
            return child_weights
        except Exception as e:
            print(f"Mutation error: {str(e)}")
            return child_weights