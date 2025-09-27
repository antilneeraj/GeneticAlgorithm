from src.utils.constants import *


class Fitness:
    @staticmethod
    def calculate_fitness(bird, game_time_ms, generation=1):
        """
        Calculate fitness score for a bird

        Args:
            bird: Bird object with game performance data
            game_time_ms: Time bird survived in milliseconds
            generation: Current generation (for adaptive scoring)

        Returns:
            float: Fitness score
        """
        # Base components of fitness
        survival_bonus = game_time_ms * FITNESS_BONUS_DISTANCE
        pipe_bonus = bird.score * FITNESS_BONUS_PIPE
        distance_bonus = bird.fitness  # Accumulated during gameplay

        # Penalty for early death
        death_penalty = 0 if bird.alive else abs(FITNESS_PENALTY_DEATH)

        # Progressive difficulty bonus (reward consistency over time)
        consistency_bonus = 0
        if bird.score > 0:
            # Exponential reward for high scores
            consistency_bonus = (bird.score ** 1.5) * 50

        # Adaptive fitness based on generation
        # Slight increase over generations
        generation_multiplier = 1.0 + (generation * 0.1)

        total_fitness = (
            survival_bonus +
            pipe_bonus +
            distance_bonus +
            consistency_bonus -
            death_penalty
        ) * generation_multiplier

        return max(0, total_fitness)  # Ensure non-negative fitness

    @staticmethod
    def normalize_fitness(fitness_scores):
        """
        Normalize fitness scores to 0-1 range

        Args:
            fitness_scores: List of fitness values

        Returns:
            List of normalized fitness values
        """
        if not fitness_scores or len(fitness_scores) <= 1:
            return fitness_scores

        min_fitness = min(fitness_scores)
        max_fitness = max(fitness_scores)

        if max_fitness == min_fitness:
            return [0.5] * len(fitness_scores)

        range_fitness = max_fitness - min_fitness
        normalized = [(f - min_fitness) /
                      range_fitness for f in fitness_scores]

        return normalized
