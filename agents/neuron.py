import math

class Neuron:
    def __init__(self, nid):
        self.id = nid
        self.layer = 0
        self.input_sum = 0
        self.output = 0
        self.outgoing = []  # Synapses from this neuron

    def activate(self):
        if self.layer != 0:  # input layer passes value directly
            self.output = self._sigmoid(self.input_sum)
        for syn in self.outgoing:
            syn.to_neuron.input_sum += syn.weight * self.output

    def _sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def clone(self):
        n = Neuron(self.id)
        n.layer = self.layer
        return n
