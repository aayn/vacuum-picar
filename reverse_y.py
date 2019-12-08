"""Module responsible for a very simple, reverse motion."""
import numpy as np
from src.config import R_X, R_BD, BEH_TOLERANCE


class ReverseY(object):

    def __init__(self):
        self.pose = None
        self.bound_dist = None

    def input(self, pose, bound_dist=None):
        self.pose = pose
        self.bound_dist = bound_dist

    def output(self):
        if self.bound_dist is None:
            if self.pose[0] >= R_X - BEH_TOLERANCE:
                return (0.5, self.pose[1], 0)
        else:
            if (self.bound_dist <= R_BD or self.pose[0] >= R_X - BEH_TOLERANCE):
                return (0.5, self.pose[1], 0)
        return None
