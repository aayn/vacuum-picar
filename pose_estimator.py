"""Keeps track of the robot's current pose and updates to it."""
import numpy as np
from src.config import START_POSE, LOC_WEIGHT


class PosE(object):
    def __init__(self):
        self.x, self.y, self.theta = START_POSE
        self.b_estimate, self.l_estimate = None, None

    def input(self, b_estimate, l_estimate=None):
        """Collect and store position estimates from various sources.
        
        Args:
            b_estimate: Estimates from bicycle model.
            l_estimate: Estimates from localization.
        """
        self.b_estimate, self.l_estimate = b_estimate, l_estimate

    def to_list(self):
        return [self.x, self.y, self.theta]

    def update_pose(self):
        if self.l_estimate is not None:
            print('Localization Correction.')
            b_estimate = (1 - LOC_WEIGHT) * np.array(self.b_estimate)
            l_estimate = LOC_WEIGHT * np.array(self.l_estimate)
            estimate = b_estimate + l_estimate
        else:
            estimate = self.b_estimate
        if estimate is not None:
            self.x, self.y, self.theta = estimate

    def output(self):
        self.update_pose()
        return self.to_list()
