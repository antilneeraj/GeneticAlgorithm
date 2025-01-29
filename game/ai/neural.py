import numpy as np

class NeuralNetwork:
    def __init__(self):
        try:
            self.input_size = 3
            self.hidden_size = 6
            self.output_size = 1
            self.weights = [
                np.random.randn(self.input_size, self.hidden_size),
                np.random.randn(self.hidden_size, self.output_size)
            ]
        except Exception as e:
            print(f"Neural network initialization failed: {str(e)}")
            raise

    def predict(self, inputs):
        try:
            if len(inputs) != self.input_size:
                raise ValueError("Invalid input dimensions")
            
            hidden = np.dot(inputs, self.weights[0])
            hidden = self.sigmoid(hidden)
            output = np.dot(hidden, self.weights[1])
            return self.sigmoid(output)
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return np.array([0])

    def sigmoid(self, x):
        try:
            return 1 / (1 + np.exp(-x))
        except Exception as e:
            print(f"Sigmoid error: {str(e)}")
            return x