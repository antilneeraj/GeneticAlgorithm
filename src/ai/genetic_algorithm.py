import random
import time
import os
import json
from src.ai.neural_network import NeuralNetwork
from src.ai.population import Population
from src.ai.selection import Selection
from src.ai.crossover import Crossover
from src.ai.mutation import Mutation
from src.ai.fitness import Fitness
from src.utils.constants import *


class GeneticAlgorithm:
    def __init__(self, population_size=POPULATION_SIZE,
                 generations=GENERATIONS,
                 mutation_rate=MUTATION_RATE,
                 crossover_rate=CROSSOVER_RATE,
                 elite_count=ELITE_COUNT):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_count = elite_count

        # Initialize population
        self.population = Population(population_size)

        # Evolution statistics
        self.generation_stats = []
        self.best_fitness_history = []
        self.average_fitness_history = []
        self.diversity_history = []

        # Algorithm parameters
        self.selection_method = "tournament"
        self.crossover_method = "single_point"
        self.mutation_method = "gaussian"

        # Adaptive parameters
        self.adaptive_mutation = True
        self.diversity_threshold = 0.1

    def assign_brains_to_birds(self, birds):
        """Assign neural network brains to birds"""
        # Ensure population is large enough (handle edge cases)
        while len(self.population.individuals) < len(birds):
            self.population.individuals.append(
                NeuralNetwork(NN_INPUT_NODES, NN_HIDDEN_NODES, NN_OUTPUT_NODES)
            )
            
        for i, bird in enumerate(birds):
            if i < len(self.population.individuals):
                bird.brain = self.population.individuals[i]

    def calculate_fitness_scores(self, birds, game_time_ms):
        """Calculate fitness for all birds after simulation"""
        fitness_scores = []

        for bird in birds:
            fitness = Fitness.calculate_fitness(bird, game_time_ms,
                                                self.population.generation + 1)
            fitness_scores.append(fitness)

        # Update population fitness scores
        self.population.fitness_scores = fitness_scores[:len(
            self.population.individuals)]
        return fitness_scores

    def select_parents(self, count=2):
        """Select parents for reproduction"""
        parents = []

        for _ in range(count):
            if self.selection_method == "tournament":
                parent = Selection.tournament_selection(
                    self.population.individuals,
                    self.population.fitness_scores,
                    tournament_size=3
                )
            elif self.selection_method == "roulette":
                parent = Selection.roulette_wheel_selection(
                    self.population.individuals,
                    self.population.fitness_scores
                )
            elif self.selection_method == "rank":
                parent = Selection.rank_selection(
                    self.population.individuals,
                    self.population.fitness_scores
                )
            else:
                parent = random.choice(self.population.individuals)

            parents.append(parent)

        return parents

    def create_offspring(self, parent1, parent2):
        """Create offspring through crossover and mutation"""
        offspring = []

        # Crossover
        if random.random() < self.crossover_rate:
            if self.crossover_method == "single_point":
                child1, child2 = Crossover.single_point_crossover(
                    parent1, parent2)
            elif self.crossover_method == "two_point":
                child1, child2 = Crossover.two_point_crossover(
                    parent1, parent2)
            elif self.crossover_method == "uniform":
                child1, child2 = Crossover.uniform_crossover(parent1, parent2)
            elif self.crossover_method == "arithmetic":
                child1, child2 = Crossover.arithmetic_crossover(
                    parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()
        else:
            child1, child2 = parent1.copy(), parent2.copy()

        offspring.extend([child1, child2])

        # Mutation
        for i, child in enumerate(offspring):
            if self.mutation_method == "gaussian":
                offspring[i] = Mutation.gaussian_mutation(
                    child, self.mutation_rate)
            elif self.mutation_method == "uniform":
                offspring[i] = Mutation.uniform_mutation(
                    child, self.mutation_rate)
            elif self.mutation_method == "creep":
                offspring[i] = Mutation.creep_mutation(
                    child, self.mutation_rate)
            elif self.mutation_method == "boundary":
                offspring[i] = Mutation.boundary_mutation(
                    child, self.mutation_rate)
            elif self.mutation_method == "adaptive":
                offspring[i] = Mutation.adaptive_mutation(
                    child, self.population.generation, self.generations
                )

        return offspring

    def evolve_generation(self):
        """Evolve population to next generation"""
        start_time = time.time()

        # Get current statistics
        current_stats = self.population.get_fitness_statistics()
        diversity = self.population.get_diversity_measure()

        # Store statistics
        self.best_fitness_history.append(current_stats['max'])
        self.average_fitness_history.append(current_stats['avg'])
        self.diversity_history.append(diversity)

        # Create next generation
        new_population = []

        # Elitism - keep best individuals
        self.population.sort_by_fitness(descending=True)
        elites = self.population.individuals[:self.elite_count]
        
        new_population = [elite.copy() for elite in elites]

        # Reproduction (Selection + Crossover)
        # We leave space for random immigrants (10% of population)
        immigrant_count = int(self.population_size * 0.1)
        repro_count = self.population_size - len(new_population) - immigrant_count

        while len(new_population) < (self.population_size - immigrant_count):
            parent1 = Selection.tournament_selection(self.population.individuals, self.population.fitness_scores)
            parent2 = Selection.tournament_selection(self.population.individuals, self.population.fitness_scores)
            
            offspring = Crossover.uniform_crossover(parent1, parent2)
            
            # Add mutated offspring
            for child in offspring:
                if len(new_population) < (self.population_size - immigrant_count):
                    child = Mutation.gaussian_mutation(child, self.mutation_rate)
                    new_population.append(child)
        
        # Random Immigrants (Fresh Genes)
        # Inject completely random individuals to maintain diversity
        for _ in range(immigrant_count):
            new_population.append(NeuralNetwork(NN_INPUT_NODES, NN_HIDDEN_NODES, NN_OUTPUT_NODES))

        # Fill any remaining gaps
        while len(new_population) < self.population_size:
            new_population.append(NeuralNetwork(NN_INPUT_NODES, NN_HIDDEN_NODES, NN_OUTPUT_NODES))

        self.population.replace_population(new_population)

        # Adaptive parameter adjustment
        if self.adaptive_mutation and diversity < self.diversity_threshold:
            self.mutation_rate = min(0.5, self.mutation_rate * 1.1)
        elif self.adaptive_mutation and diversity > self.diversity_threshold * 3:
            self.mutation_rate = max(0.01, self.mutation_rate * 0.9)

        generation_time = time.time() - start_time

        # Compile generation statistics
        gen_stats = {
            'generation': self.population.generation - 1,
            'best_fitness': current_stats['max'],
            'average_fitness': current_stats['avg'],
            'worst_fitness': current_stats['min'],
            'fitness_std': current_stats['std'],
            'diversity': diversity,
            'mutation_rate': self.mutation_rate,
            'evolution_time': generation_time,
            'elite_count': self.elite_count
        }

        self.generation_stats.append(gen_stats)
        return gen_stats

    def save_generation_stats(self, filename="data/statistics/evolution_stats.json"):
        """Save evolution statistics to file"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        stats_data = {
            'algorithm_parameters': {
                'population_size': self.population_size,
                'generations': self.generations,
                'mutation_rate': MUTATION_RATE,
                'crossover_rate': self.crossover_rate,
                'elite_count': self.elite_count,
                'selection_method': self.selection_method,
                'crossover_method': self.crossover_method,
                'mutation_method': self.mutation_method
            },
            'generation_statistics': self.generation_stats,
            'fitness_history': {
                'best': self.best_fitness_history,
                'average': self.average_fitness_history,
                'diversity': self.diversity_history
            }
        }

        with open(filename, 'w') as f:
            json.dump(stats_data, f, indent=2)

    def save_best_individual(self, filename="data/models/best_bird.json"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        return self.population.save_best(filename)

    def get_evolution_summary(self):
        """Get summary of evolution process"""
        if not self.generation_stats:
            return {}

        best_gen = max(self.generation_stats, key=lambda x: x['best_fitness'])

        return {
            'total_generations': len(self.generation_stats),
            'best_fitness_achieved': best_gen['best_fitness'],
            'best_generation': best_gen['generation'],
            'final_average_fitness': self.generation_stats[-1]['average_fitness'],
            'improvement': self.generation_stats[-1]['best_fitness'] - self.generation_stats[0]['best_fitness']
        }

    def __str__(self):
        return (f"GeneticAlgorithm(pop={self.population_size}, "
                f"gen={self.population.generation}/{self.generations}, "
                f"mutation={self.mutation_rate:.3f})")
