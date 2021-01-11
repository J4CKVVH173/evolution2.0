import math

import numpy as np


class NeuralNetwork:

    __slots__ = ("hide_weights", "out_weights")

    def __init__(self, hide_weights, out_weights):
        self.hide_weights = np.matrix(hide_weights)
        self.out_weights = np.matrix(out_weights)

    def compute(self, inputs: list) -> int:
        """На основании переданных ранее весов производится вычисление предполагаемого хода.

        Args:
            inputs (list): Входные значения окружающие клетку

        Returns:
            int: Индекс самого яркого выходного нейрона, он определяет действие
        """
        inputs_m = np.matrix(inputs)
        vectorized_sigmoid = np.vectorize(self._sigmoid)

        # вычисления нейронной сети
        hidden_inputs = np.dot(inputs_m, self.hide_weights)
        hidden_outputs = vectorized_sigmoid(hidden_inputs)
        out_input = np.dot(hidden_outputs, self.out_weights)
        result = vectorized_sigmoid(out_input)
        return np.argmax(result.getA()[0])

    @staticmethod
    def _sigmoid(x):
        return 1 / (1 + math.exp(-x))
