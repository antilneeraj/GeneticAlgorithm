import random

class Synapse:
    def __init__(self, from_neuron, to_neuron, weight):
        self.from_neuron = from_neuron
        self.to_neuron = to_neuron
        self.weight = weight

    def mutate_weight(self):
        if random.random() < 0.1:
            self.weight = random.uniform(-1, 1)
        else:
            self.weight += random.gauss(0, 1) / 10
            self.weight = max(-1, min(1, self.weight))
 
    def clone(self, from_clone, to_clone):
        return Synapse(from_clone, to_clone, self.weight)
