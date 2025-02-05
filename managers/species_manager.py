import random


class SpeciesGroup:
    def __init__(self, agent):
        self.agents = [agent]
        self.benchmark_fitness = agent.fitness
        self.benchmark_brain = agent.brain.clone()
        self.champion = agent.clone()
        self.staleness = 0
        self.threshold = 1.2

    def is_similar(self, brain):
        diff = self._weight_difference(self.benchmark_brain, brain)
        return diff < self.threshold

    def _weight_difference(self, brain1, brain2):
        total_diff = 0
        for i in range(len(brain1.synapses)):
            total_diff += abs(brain1.synapses[i].weight -
                              brain2.synapses[i].weight)
        return total_diff

    def add(self, agent):
        self.agents.append(agent)

    def sort_agents(self):
        self.agents.sort(key=lambda a: a.fitness, reverse=True)
        if self.agents[0].fitness > self.benchmark_fitness:
            self.benchmark_fitness = self.agents[0].fitness
            self.champion = self.agents[0].clone()
            self.staleness = 0
        else:
            self.staleness += 1

    def calculate_average_fitness(self):
        if self.agents:
            self.average_fitness = sum(
                a.fitness for a in self.agents) / len(self.agents)
        else:
            self.average_fitness = 0

    def get_champion(self):
        return self.champion

    def breed(self):
        if len(self.agents) < 2:
            print("Warning: Not enough agents to breed!")
            return None  # Handle cases where breeding isn't possible

        parent = random.choice(self.agents[1:])  # Select from remaining agents
        child = parent.clone()  # Clone the chosen parent
        return child
