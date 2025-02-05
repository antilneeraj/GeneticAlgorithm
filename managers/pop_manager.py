import random
import math
from agents.agent import Agent
from config import settings
from managers.species_manager import SpeciesGroup


class PopulationManager:
    def __init__(self, size):
        self.size = size
        self.agents = [Agent() for _ in range(size)]
        self.generation = 1
        self.species_groups = []

    def update_live_agents(self):
        # Remove dead or None agents
        self.agents = [
            agent for agent in self.agents if agent is not None and agent.alive]

        if not self.agents:  # If all agents are dead
            print("All agents died! Generating a new population...")
            self._next_generation()

        for agent in self.agents:
            if agent.alive:
                agent.look()
                agent.think()
                agent.update(settings.GROUND.rect)
                agent.draw(settings.WINDOW)

    def extinct(self):
        return all(not agent.alive for agent in self.agents)

    def natural_selection(self):
        self._speciate()
        self._calculate_fitness()
        self._remove_extinct_species()
        self._remove_stale_species()
        self._sort_species()
        self._next_generation()
        self.generation += 1

    def _speciate(self):
        for group in self.species_groups:
            group.agents = []
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

    def _calculate_fitness(self):
        for agent in self.agents:
            agent.calculate_fitness()
        for group in self.species_groups:
            group.calculate_average_fitness()

    def _remove_extinct_species(self):
        self.species_groups = [
            g for g in self.species_groups if len(g.agents) > 0]

    def _remove_stale_species(self):
        survivors = []
        for group in self.species_groups:
            if group.staleness < 8 or len(self.species_groups) <= 1:
                survivors.append(group)
        self.species_groups = survivors

    def _sort_species(self):
        for group in self.species_groups:
            group.sort_agents()
        self.species_groups.sort(
            key=lambda g: g.benchmark_fitness, reverse=True)

    def _next_generation(self):
        children = []
        for group in self.species_groups:
            children.append(group.get_champion().clone())
        children_per_group = math.floor(
            (self.size - len(self.species_groups)) / len(self.species_groups))
        for group in self.species_groups:
            for _ in range(children_per_group):
                children.append(group.breed())
        while len(children) < self.size:
            children.append(self.species_groups[0].breed())
        self.agents = children
