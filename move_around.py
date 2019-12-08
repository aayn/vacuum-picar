"""Moves the robot slightly in random directions."""
import numpy as np


class MoveAround(object):

    def input(self):
        "Nothing."

    def output(self):
        v = 0.02
        gamma = 0.5 * np.random.random_sample()
        return (v, gamma)
