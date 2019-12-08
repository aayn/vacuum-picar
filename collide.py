"""Simple collision-detection module."""
from src.config import IMMINENT_COLLISION


class Collide(object):

    def __init__(self):
        self.qrs = None

    def input(self, qrs):
        self.qrs = qrs

    def output(self):
        # Distance to the closest object
        if self.qrs is not None:
            closest = min(qr[2] for qr in self.qrs)
            if closest < IMMINENT_COLLISION:
                return (0, 0)  # Halt
        return None, None
