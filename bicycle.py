"""Kinematic model for the robot that deals with the motors and servos."""
import numpy as np
from src.config import TIMESTEP, V_CALIB, G_CALIB, SIMULATION
from src import picar
from src import utils as u


class Bicycle(object):
    def __init__(self):
        self.pose = None
        self.v = 0
        self.gamma = 0
        self.trajectory_x = []
        self.trajectory_y = []
        self.turnangles = []

    def input(self, pose, v, gamma):
        self.pose = pose
        self.v = v
        self.gamma = gamma

    def update_step(self):
        self.trajectory_x.append(self.pose[0])
        self.trajectory_y.append(self.pose[1])

        if not SIMULATION:
            if self.v >= 0:
                picar.run_action('forward')
            else:
                picar.run_action('backward')
            picar_v = u.real_to_picar_v(np.fabs(self.v))
            picar.run_speed(picar_v)

            w = self.gamma * G_CALIB
            if self.v >= 0:
                turnangle = 90 - int(np.round(np.rad2deg(w)))
            else:
                turnangle = 90 + int(np.round(np.rad2deg(w)))
            picar.run_action(f'fwturn:{turnangle}')
            self.turnangles.append(turnangle)

        self.pose[2] = self.pose[2] + TIMESTEP * self.gamma
        self.pose[0] += TIMESTEP * V_CALIB * self.v * np.cos(self.pose[2])
        self.pose[1] += TIMESTEP * V_CALIB * self.v * np.sin(self.pose[2])

    def output(self):
        self.update_step()
        return self.pose
