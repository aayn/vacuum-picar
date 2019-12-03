"""Module responsible for moving to a goal pose."""
import numpy as np
import src.utils as u
from src.config import GOAL_TOLERANCE, K_RHO, K_ALPHA, K_BETA, MAX_SPEED


class GoalExec(object):
    def __init__(self):
        self.current_pose = None
        self.goal_pose = None
    
    def input(self, current_pose, goal_pose):
        self.current_pose = current_pose
        if goal_pose is not None:
            self.goal_pose = goal_pose
    
    def __bool__(self):
        return True

    def near_goal(self):
        xc, yc, _ = self.current_pose
        xg, yg, _ = self.goal_pose
        if u.euclidean_dist([xc, yc], [xg, yg]) < GOAL_TOLERANCE:
            return True
        return False

    def calc_polars(self):
        if self.current_pose is None:
            raise ValueError('GoalExec: Current pose is not set.')
        if self.goal_pose is None:
            raise ValueError('GoalExec: Goal pose is not set.')
        delta_x = self.goal_pose[0] - self.current_pose[0]
        delta_y = self.goal_pose[1] - self.current_pose[1]
        rho = np.sqrt(delta_x ** 2 + delta_y ** 2)
        # Adjust the values to be in [-pi, pi]
        alpha = np.mod(np.arctan2(delta_y, delta_x) - self.current_pose[2] +
                       np.pi, 2 * np.pi) - np.pi
        beta = np.mod(-self.current_pose[2] - alpha + 
                      self.goal_pose[2] + np.pi, 2 * np.pi) - np.pi

        return rho, alpha, beta
    
    def output(self):
        rho, alpha, beta = self.calc_polars()
        v = min(K_RHO * rho, MAX_SPEED)
        gamma = K_ALPHA * alpha + K_BETA * beta
        gamma = np.mod(gamma + np.pi, 2*np.pi) - np.pi
        # print(np.rad2deg(self.gamma))
        if alpha <= (-np.pi/2) or alpha > (np.pi / 2):
            v = -v
        return v, gamma
