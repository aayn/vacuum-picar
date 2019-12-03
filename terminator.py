"""Module responsible for terminating the motion."""
from src import utils as u
from src.config import GOAL_TOLERANCE, END_GOAL


class Terminator(object):
    def __init__(self):
        self.pose = None
    
    def input(self, pose):
        self.pose = pose
    
    def output(self):
        goal_dist = u.euclidean_dist(END_GOAL, [self.pose[0], self.pose[1]])
        if goal_dist < GOAL_TOLERANCE:
            return True
        return False