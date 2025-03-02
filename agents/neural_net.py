import random
from typing import List
from agents.neuron import Neuron
from agents.synapse import Synapse

class NeuralNet:
    """
    A simple feed-forward neural network with a fixed two-layer structure:
    input (with bias) and output. This network supports cloning and mutation,
    making it well-suited for use in genetic algorithms.
    """

    def __init__(self, num_inputs: int, clone: bool = False) -> None:
        """
        Initializes a neural network.
        
        :param num_inputs: The number of input neurons.
        :param clone: If True, creates an empty network for cloning purposes.
                      Otherwise, builds a network with input, bias, and output neurons.
        """
        self.num_inputs: int = num_inputs
        self.neurons: List[Neuron] = []   # All neurons in the network.
        self.synapses: List[Synapse] = []   # All connections between neurons.
        self.layers: int = 2              # Fixed: layer 0 for input (and bias) and layer 1 for output.

        if not clone:
            # Create input neurons (IDs: 0 to num_inputs - 1).
            for i in range(num_inputs):
                neuron = Neuron(i)
                neuron.layer = 0
                self.neurons.append(neuron)
            # Create bias neuron (ID: num_inputs).
            bias = Neuron(num_inputs)
            bias.layer = 0
            self.neurons.append(bias)
            # Create output neuron (ID: num_inputs + 1).
            output = Neuron(num_inputs + 1)
            output.layer = 1
            self.neurons.append(output)

            # Connect each input and bias neuron to the output neuron with random weights.
            for i in range(num_inputs + 1):
                weight = random.uniform(-1, 1)
                self.synapses.append(Synapse(self.neurons[i], output, weight))
        
        self._build_net()

    def _build_net(self) -> None:
        """
        Resets the outgoing synapses for each neuron and orders the neurons
        layer by layer for proper feed-forward processing.
        """
        # Reset outgoing connections.
        for neuron in self.neurons:
            neuron.outgoing = []
        # Add each synapse to its originating neuron's outgoing list.
        for syn in self.synapses:
            syn.from_neuron.outgoing.append(syn)
        # Create an ordered list of neurons sorted by their layer.
        self.net_order: List[Neuron] = [
            neuron for layer in range(self.layers) for neuron in self.neurons if neuron.layer == layer
        ]

    def feed_forward(self, inputs: List[float]) -> float:
        """
        Feeds input values through the network and returns the output value.
        
        :param inputs: A list of input values matching the number of input neurons.
        :return: The output value from the output neuron.
        :raises ValueError: If the length of inputs does not match num_inputs.
        """
        if len(inputs) != self.num_inputs:
            raise ValueError(f"Expected {self.num_inputs} inputs, got {len(inputs)}.")

        # Set the output of input neurons.
        for i in range(self.num_inputs):
            self.neurons[i].output = inputs[i]
        # The bias neuron's output is always 1.
        self.neurons[self.num_inputs].output = 1

        # Activate neurons in order.
        for neuron in self.net_order:
            neuron.activate()
        # Retrieve the output from the output neuron (assumed to be the last in the list).
        output_value = self.neurons[-1].output

        # Reset the internal input sum for each neuron for the next evaluation.
        for neuron in self.neurons:
            neuron.input_sum = 0

        return output_value

    def clone(self) -> "NeuralNet":
        """
        Creates a deep copy of this neural network, including cloned neurons and synapses.
        
        :return: A new NeuralNet instance with the same structure and weights.
        """
        clone_net = NeuralNet(self.num_inputs, clone=True)
        # Clone neurons.
        clone_net.neurons = [neuron.clone() for neuron in self.neurons]
        # Clone synapses using the corresponding cloned neurons.
        clone_net.synapses = []
        for syn in self.synapses:
            from_clone = clone_net.get_neuron(syn.from_neuron.id)
            to_clone = clone_net.get_neuron(syn.to_neuron.id)
            clone_net.synapses.append(syn.clone(from_clone, to_clone))
        clone_net.layers = self.layers
        clone_net._build_net()
        return clone_net

    def get_neuron(self, nid: int) -> Neuron:
        """
        Retrieves a neuron from the network by its unique identifier.
        
        :param nid: The identifier of the neuron.
        :return: The Neuron object with the given id.
        :raises ValueError: If no neuron with the given id is found.
        """
        for neuron in self.neurons:
            if neuron.id == nid:
                return neuron
        raise ValueError(f"Neuron with id {nid} not found.")

    def mutate(self) -> None:
        """
        Mutates the network by giving each synapse an 80% chance to mutate its weight.
        """
        for syn in self.synapses:
            if random.random() < 0.8:
                syn.mutate_weight()
