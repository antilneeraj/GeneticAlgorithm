import random
from typing import List
from agents.agent import Agent
from agents.neural_net import NeuralNet  # Assuming NeuralNet is defined in agents.neural_net

class SpeciesGroup:
    """
    Represents a species in the genetic algorithm. Agents in the same species
    share similar neural network characteristics. The species maintains a
    benchmark brain and fitness for comparison, tracks its champion, and
    controls the breeding process.
    """

    def __init__(self, agent: Agent) -> None:
        """
        Initializes a new species group with an initial agent.
        
        :param agent: The initial agent that forms this species.
        """
        self.agents: List[Agent] = [agent]
        self.benchmark_fitness: float = agent.fitness
        self.benchmark_brain: NeuralNet = agent.brain.clone()
        self.champion: Agent = agent.clone()
        self.staleness: int = 0
        self.threshold: float = 1.2
        self.average_fitness: float = 0.0

    def is_similar(self, brain: NeuralNet) -> bool:
        """
        Determines if the provided brain is similar enough to the species' benchmark brain.
        
        :param brain: The neural network to compare.
        :return: True if the total weight difference is less than the threshold.
        """
        diff = self._weight_difference(self.benchmark_brain, brain)
        return diff < self.threshold

    def _weight_difference(self, brain1: NeuralNet, brain2: NeuralNet) -> float:
        """
        Computes the total absolute difference in synapse weights between two neural networks.
        
        :param brain1: The first neural network.
        :param brain2: The second neural network.
        :return: The sum of absolute differences between corresponding synapse weights.
        :raises ValueError: If the two brains have a different number of synapses.
        """
        if len(brain1.synapses) != len(brain2.synapses):
            raise ValueError("Brains have a different number of synapses.")
        return sum(abs(syn1.weight - syn2.weight)
                   for syn1, syn2 in zip(brain1.synapses, brain2.synapses))

    def add(self, agent: Agent) -> None:
        """
        Adds an agent to the species.
        
        :param agent: The agent to add.
        """
        self.agents.append(agent)

    def sort_agents(self) -> None:
        """
        Sorts agents in descending order of fitness. Updates the species champion
        and resets staleness if a new benchmark fitness is found.
        """
        self.agents.sort(key=lambda a: a.fitness, reverse=True)
        if self.agents and self.agents[0].fitness > self.benchmark_fitness:
            self.benchmark_fitness = self.agents[0].fitness
            self.champion = self.agents[0].clone()
            self.staleness = 0
        else:
            self.staleness += 1

    def calculate_average_fitness(self) -> None:
        """
        Calculates the average fitness of the agents in the species.
        """
        if self.agents:
            self.average_fitness = float(sum(agent.fitness for agent in self.agents)) / len(self.agents)
        else:
            self.average_fitness = 0.0

    def get_champion(self) -> Agent:
        """
        Retrieves the champion (highest performing agent) of the species.
        
        :return: The champion agent.
        """
        return self.champion

    def breed(self) -> Agent:
        """
        Produces a new agent via breeding. If the species contains only one agent,
        a clone of the champion is returned. Otherwise, a random parent (excluding
        the champion) is selected, cloned, and its brain mutated.
        
        :return: A new agent resulting from the breeding process.
        """
        if len(self.agents) < 2:
            return self.champion.clone()
        parent = random.choice(self.agents[1:])  # Exclude the champion for variety.
        child = parent.clone()
        child.brain.mutate()
        return child
