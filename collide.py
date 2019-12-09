"""Simple collision-detection module."""
from src.config import IMMINENT_COLLISION


class Collide(object):
    def __init__(self):
        self.bound_dist = None

    def input(self, bound_dist):
        self.bound_dist = bound_dist

    def output(self):
        # Distance to the closest object
        if self.bound_dist is not None:
            if self.bound_dist < IMMINENT_COLLISION:
                return (0, 0)  # Halt
        return None, None
