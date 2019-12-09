"""Module responsible for a very simple, forward-left motion."""
import numpy as np
from src.config import FL_X, FL_BD, FL_INT, FL_G_ANGLE, BEH_TOLERANCE


class FwdLeft(object):
    """Class for forward-left behaviour."""
    def __init__(self):
        self.pose = None
        self.bound_dist = None

    def input(self, pose, bound_dist=None):
        self.pose = pose
        self.bound_dist = bound_dist

    def output(self):
        if self.bound_dist is None:
            if self.pose[0] <= FL_X + BEH_TOLERANCE:
                return (2.25, self.pose[1] + FL_INT, FL_G_ANGLE)
        else:
            if (self.bound_dist >= FL_BD
                    or self.pose[0] <= FL_X + BEH_TOLERANCE):
                return (2.25, self.pose[1] + FL_INT, FL_G_ANGLE)
        return None
