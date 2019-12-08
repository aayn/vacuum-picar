# Host and port of the PiCar remote-control server
HOST = '192.168.7.48'
PORT = '8000'
# Maximum number of iterations to run the robot for
MAX_ITERS = 5000
# Whether to run a simulation or the physical robot
SIMULATION = True
# Note: All distances/speed are in meters or meters/s
# Starting pose in world coordinates
START_POSE = (0.5, 0.5, 0)
# Length of PiCar's wheel base
WHEEL_BASE = 0.141
# Acceptable distance to goal
GOAL_TOLERANCE = 0.05
# Positions of the QR codes
QR_POS = {
    'Landmark 1': [(3, 1), (0, 1), (0.5, 3)],
    'Landmark 2': [(3, 1.5), (1.5, 3), (0, 0.5)],
    'Landmark 3': [(3, 2.5), (0, 2), (2, 0)],
    'GOAL': [(3, 0.5), (0, 1.5), (1, 0)]
}
# How much weight to give to localization correction
LOC_WEIGHT = 0.5
# Tolerance beyond which localization updates are rejected
LOC_ERR_TOLERANCE = 0.25
# Duration for which the input is applied
TIMESTEP = 0.1
# Calibration multiplier for velocity
V_CALIB = 1.0
# Calibration multiplier for steering angle
G_CALIB = 0.9
# K-values for moving to a pose controller
K_RHO = 1
K_ALPHA = 7
K_BETA = -3
# Limits on how fast/slow the PiCar can move
# MAX_SPEED = 0.35  # corresponds to 66 PiCar speed
MAX_SPEED = 0.20  # corresponds to 66 PiCar speed
MIN_SPEED = 0.00
# Vertical line at which the forward-left motion is triggered
FL_X = 0.5
# Distance from the boundary at which the forward-left motion is triggered
FL_BD = 2.5
# Vertical line at which the reverse-y motion is triggered
R_X = 2.5
# Distance from the boundary at which the reverse motion is triggered
R_BD = 0.5
# Tolerance for behaviour trigger
BEH_TOLERANCE = 0.001
# Distance for collide module to kick in
IMMINENT_COLLISION = 0.05
# Final destination
END_GOAL = (0.5, 2.5)