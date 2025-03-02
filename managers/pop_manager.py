import random
import logging
from typing import List
from agents.agent import Agent
from config import settings
from managers.species_manager import SpeciesGroup

# Configure logging for debugging purposes.
logging.basicConfig(level=logging.INFO)

class PopulationManager:
    """
    Manages a population of agents (birds) and handles their evolution
    using a genetic algorithm. Agents are grouped into species based on
    the similarity of their neural networks (brains), and each generation
    produces a new set of agents using breeding and mutation.
    """
    def __init__(self, size: int):
        self.size: int = size
        self.agents: List[Agent] = [Agent() for _ in range(size)]
        self.generation: int = 1
        self.species_groups: List[SpeciesGroup] = []
        self.breeding_count: int = 0  # Counter for breeding events
        # Store the average fitness of the last completed generation.
        self.last_generation_avg_fitness: float = 0.0

    def update_live_agents(self) -> None:
        """
        Updates the state of each live agent by:
          - Removing dead or None agents.
          - Processing vision (look), decision making (think),
            and movement (update).
        If no agents remain alive, a new generation is triggered.
        """
        self.agents = [agent for agent in self.agents if agent is not None and agent.alive]
        if not self.agents:
            logging.info("All agents died! Generating a new population...")
            self.natural_selection()
            return

        for agent in self.agents:
            agent.look()
            agent.think()
            agent.update(settings.GROUND.rect)

    def extinct(self) -> bool:
        """
        Checks if the entire population is extinct.
        """
        return all(not agent.alive for agent in self.agents)

    def natural_selection(self) -> None:
        """
        Runs the complete cycle of natural selection:
          - Speciation: Grouping agents into species.
          - Fitness evaluation: Calculating individual and species fitness.
          - Removing extinct and stale species.
          - Sorting species for breeding priority.
          - Creating a new generation.
        After running, increments the generation counter.
        """
        self._speciate()
        self._calculate_fitness()
        # Compute and store the overall average fitness for this generation
        if self.agents:
            self.last_generation_avg_fitness = sum(agent.fitness for agent in self.agents) / len(self.agents)
        else:
            self.last_generation_avg_fitness = 0.0

        self._remove_extinct_species()
        self._remove_stale_species()
        self._sort_species()
        self._next_generation()
        self.generation += 1
        logging.info(f"Advanced to generation {self.generation} with avg fitness: {self.last_generation_avg_fitness:.2f}")

    def _speciate(self) -> None:
        """
        Groups agents into species based on the similarity of their brains.
        Clears out previous group assignments and reassigns agents to either
        an existing species or creates a new one.
        """
        # Clear agents in each existing species.
        for group in self.species_groups:
            group.agents = []
        # Assign each agent to an existing species or a new species.
        for agent in self.agents:
            added = False
            for group in self.species_groups:
                if group.is_similar(agent.brain):
                    group.add(agent)
                    added = True
                    break
            if not added:
                new_group = SpeciesGroup(agent)
                self.species_groups.append(new_group)

    def _calculate_fitness(self) -> None:
        """
        Calculates fitness for each agent and computes the average fitness
        for each species group.
        """
        for agent in self.agents:
            agent.calculate_fitness()
        for group in self.species_groups:
            group.calculate_average_fitness()

    def _remove_extinct_species(self) -> None:
        """
        Removes any species groups that no longer have any agents.
        """
        self.species_groups = [group for group in self.species_groups if group.agents]

    def _remove_stale_species(self) -> None:
        """
        Eliminates species that have not shown improvement (i.e. are stale)
        unless they are the only remaining species.
        """
        survivors = []
        for group in self.species_groups:
            if group.staleness < 8 or len(self.species_groups) <= 1:
                survivors.append(group)
        self.species_groups = survivors

    def _sort_species(self) -> None:
        """
        Sorts the agents in each species group and orders species groups by
        their benchmark fitness in descending order.
        """
        for group in self.species_groups:
            group.sort_agents()
        self.species_groups.sort(key=lambda g: g.benchmark_fitness, reverse=True)

    def _next_generation(self) -> None:
        """
        Produces the next generation of agents:
          - Each species passes its champion to the next generation.
          - Additional offspring are produced proportional to the species'
            share of the total agent population.
          - If too many offspring are generated, they are trimmed; if too few,
            the best champion is cloned until the desired population size is met.
        """
        children: List[Agent] = []
        self.breeding_count = 0  # Reset breeding counter
        total_agents = sum(len(group.agents) for group in self.species_groups)

        if total_agents == 0:
            logging.warning("No agents in any species. Resetting with a fresh population.")
            children = [Agent() for _ in range(self.size)]
        else:
            for group in self.species_groups:
                champion = group.get_champion()
                if champion is not None:
                    # Always carry the champion over.
                    children.append(champion.clone())
                else:
                    continue  # Skip group if no champion is found.
                # Determine number of children for this group.
                num_children = max(1, int(round((len(group.agents) / total_agents) * self.size)) - 1)
                for _ in range(num_children):
                    child = group.breed()
                    if child is not None:
                        children.append(child)
                        self.breeding_count += 1

            # Trim excess children if necessary.
            if len(children) > self.size:
                children = children[:self.size]
            # If there are not enough children, fill with clones of the best champion.
            while len(children) < self.size:
                if self.species_groups:
                    children.append(self.species_groups[0].get_champion().clone())
                else:
                    children.append(Agent())

        self.agents = children
