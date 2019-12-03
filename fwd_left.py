"""Module responsible for a very simple, forward-left motion."""
import numpy as np
from src.config import FL_X, BEH_TOLERANCE


class FwdLeft(object):
    def __init__(self):
        self.pose = None
    
    def input(self, pose):
        self.pose = pose
    
    def output(self):
        if np.fabs(self.pose[0] - FL_X) < BEH_TOLERANCE:
            return (2.5, self.pose[1] + 0.25, np.pi/10)
        return None