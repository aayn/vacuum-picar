"""Module responsible for a very simple, reverse motion."""
import numpy as np
from src.config import R_X, BEH_TOLERANCE


class ReverseY(object):
    def __init__(self):
        self.pose = None
    
    def input(self, pose):
        self.pose = pose
    
    def output(self):
        if np.fabs(self.pose[0] - R_X) < BEH_TOLERANCE:
            return (0.5, self.pose[1], 0)
        return None