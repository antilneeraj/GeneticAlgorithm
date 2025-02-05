import random
from agents.neuron import Neuron
from agents.synapse import Synapse
import math

class NeuralNet:
    def __init__(self, num_inputs, clone=False):
        self.num_inputs = num_inputs
        self.neurons = []  # All neurons in the network
        self.synapses = []  # All connections
        self.layers = 2  # Fixed: input (layer 0) and output (layer 1)
        
        if not clone:
            # Create input neurons
            for i in range(num_inputs):
                n = Neuron(i)
                n.layer = 0
                self.neurons.append(n)
            # Create bias neuron (id = num_inputs)
            bias = Neuron(num_inputs)
            bias.layer = 0
            self.neurons.append(bias)
            # Create output neuron (id = num_inputs+1)
            out = Neuron(num_inputs + 1)
            out.layer = 1
            self.neurons.append(out)
            
            # Connect each input and bias neuron to the output neuron
            for i in range(num_inputs + 1):
                weight = random.uniform(-1, 1)
                self.synapses.append(Synapse(self.neurons[i], out, weight))
        
        self._build_net()
    
    def _build_net(self):
        # Reset connections for each neuron and add outgoing synapses
        for neuron in self.neurons:
            neuron.outgoing = []
        for syn in self.synapses:
            syn.from_neuron.outgoing.append(syn)
        # Create ordered list of neurons by layer
        self.net_order = [n for layer in range(self.layers) for n in self.neurons if n.layer == layer]

    def feed_forward(self, inputs):
        # Set input neurons’ output
        for i in range(self.num_inputs):
            self.neurons[i].output = inputs[i]
        # Bias neuron output always 1
        self.neurons[self.num_inputs].output = 1
        
        # Activate neurons layer by layer
        for neuron in self.net_order:
            neuron.activate()
        # Get output from the output neuron
        out_val = self.neurons[-1].output
        # Reset internal state for next evaluation
        for n in self.neurons:
            n.input_sum = 0
        return out_val

    def clone(self):
        clone_net = NeuralNet(self.num_inputs, clone=True)
        # Clone neurons (shallow copy of layer and id is sufficient)
        clone_net.neurons = [n.clone() for n in self.neurons]
        # Clone synapses using matching neurons in the clone
        clone_net.synapses = []
        for syn in self.synapses:
            from_clone = clone_net.get_neuron(syn.from_neuron.id)
            to_clone = clone_net.get_neuron(syn.to_neuron.id)
            clone_net.synapses.append(syn.clone(from_clone, to_clone))
        clone_net.layers = self.layers
        clone_net._build_net()
        return clone_net

    def get_neuron(self, nid):
        for n in self.neurons:
            if n.id == nid:
                return n

    def mutate(self):
        # 80% chance to mutate each synapse’s weight
        if random.random() < 0.8:
            for syn in self.synapses:
                syn.mutate_weight()
