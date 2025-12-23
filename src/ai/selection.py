import random

class Selection:
    @staticmethod
    def tournament_selection(population, fitness_scores, tournament_size=3):
        # Select random individuals for tournament
        tournament_indices = random.sample(range(len(population)), 
                                         min(tournament_size, len(population)))
        
        # Find the best individual in tournament
        best_idx = max(tournament_indices, key=lambda i: fitness_scores[i])
        return population[best_idx]
    
    @staticmethod
    def roulette_wheel_selection(population, fitness_scores):
        # Handle negative fitness values by shifting
        min_fitness = min(fitness_scores)
        if min_fitness < 0:
            adjusted_fitness = [f - min_fitness + 1 for f in fitness_scores]
        else:
            adjusted_fitness = fitness_scores
            
        total_fitness = sum(adjusted_fitness)
        if total_fitness == 0:
            return random.choice(population)
            
        # Calculate selection probabilities
        probabilities = [f / total_fitness for f in adjusted_fitness]
        
        # Spin the wheel
        r = random.random()
        cumulative_prob = 0
        for i, prob in enumerate(probabilities):
            cumulative_prob += prob
            if r <= cumulative_prob:
                return population[i]
                
        return population[-1]  # Fallback
    
    @staticmethod  
    def rank_selection(population, fitness_scores):
        # Create rank-based weights
        sorted_indices = sorted(range(len(fitness_scores)), 
                              key=lambda i: fitness_scores[i])
        ranks = [0] * len(population)
        for rank, idx in enumerate(sorted_indices):
            ranks[idx] = rank + 1
            
        return Selection.roulette_wheel_selection(population, ranks)
    
    @staticmethod
    def elite_selection(population, fitness_scores, elite_count):
        elite_indices = sorted(range(len(fitness_scores)), 
                             key=lambda i: fitness_scores[i], 
                             reverse=True)[:elite_count]
        return [population[i] for i in elite_indices]