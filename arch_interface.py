"""Interfaces all the different modules from the architecture."""
import matplotlib.pyplot as plt
import time
from multiprocessing import Process, Queue
import queue
from src.config import MAX_ITERS, START_TIME, SIMULATION
from vacuum import Vacuum
from camera import Camera
from qr_decoder import QRDecoder
from collide import Collide
from move_around import MoveAround
from localizer import Localizer
from bicycle import Bicycle
from pose_estimator import PosE
from goal_executive import GoalExec
from fwd_left import FwdLeft
from reverse_y import ReverseY
from terminator import Terminator


def plot_trajectory(tx, ty, linewidth=5):
    plt.plot((0, 3), (0.75, 0.75), 'k-', label='Cleaning bound')
    plt.plot((0, 3), (2.25, 2.25), 'k-')
    plt.plot((0.5, 0.5), (0.75, 2.25), 'k-')
    plt.plot((2.25, 2.25), (0.75, 2.25), 'k-')
    plt.plot(tx, ty, linewidth=linewidth, label='Car Trajectory')
    plt.legend()
    # plt.scatter(self.marker_x, self.marker_y, marker='x', c='red', s=50)
    plt.show()


def get_qrs(q, camera, qr_decoder):
    """Keeps putting newly detected QR codes into the queue."""
    while True:
        image = camera.output()
        qr_decoder.input(image)
        qrs = qr_decoder.output()
        q.put(qrs)


def interface():
    vacuum = Vacuum()
    q = Queue(maxsize=2)
    camera = Camera()
    qr_decoder = QRDecoder()
    collide = Collide()
    move_around = MoveAround()
    pose_est = PosE()
    localizer = Localizer()
    bike = Bicycle()
    fwdleft = FwdLeft()
    revy = ReverseY()
    goal_exec = GoalExec()
    terminator = Terminator()

    # Start the camera and qr_decoder on another process
    p = Process(target=get_qrs, args=(q, camera, qr_decoder))
    p.start()
    for _ in range(MAX_ITERS):
        try:
            qrs = q.get(block=False)
            # Distance from boundary
            bound_dist = min(qr[2] for qr in qrs)
        except (queue.Empty, TypeError):
            qrs = None
            bound_dist = None
        # Sucking in dust
        # Uncomment the line below to see the vacuum module in action
        # vacuum.output()
        # Get current pose
        current_pose = pose_est.output()
        # Check if final destination has been reached
        terminator.input(current_pose)
        if terminator.output():
            break
        # Pass current pose and QR codes to localizer
        localizer.input(qrs, current_pose)
        # Pass the QR codes to the collide module
        collide.input(bound_dist)
        # Pass pose and boundary distance to level 1 behaviours
        fwdleft.input(current_pose, bound_dist)
        revy.input(current_pose, bound_dist)
        # Get goal from the behaviours
        goal_pose = fwdleft.output()
        if goal_pose is None:
            goal_pose = revy.output()
        # Pass the current pose and goal pose to goal executive
        goal_exec.input(current_pose, goal_pose)
        # Get control inputs from move_around
        v, gamma = move_around.output()
        # Get control inputs from goal executive
        # Goal executive subsumes move_around
        if goal_exec:
            v, gamma = goal_exec.output()
        # Check for collision
        v_, gamma_ = collide.output()
        if v_ is not None:
            v, gamma = v_, gamma_
        # Pass the current pose and control inputs to the bicycle model
        bike.input(current_pose, v, gamma)
        # Get updated pose from the bicyle model
        new_bpose = bike.output()
        # Get updated pose from localizer
        new_lpose = localizer.output()
        # Pass the updated poses to the pose estimator
        pose_est.input(new_bpose, new_lpose)

    p.terminate()
    plot_trajectory(bike.trajectory_x, bike.trajectory_y)
    if not SIMULATION:
        max_steering_angle = max(90 - min(bike.turnangles),
                                 max(bike.turnangles) - 90)
        print(f'Max steering angle = {max_steering_angle}')
        with open('turnangles.txt', 'w') as tfile:
            tfile.writelines(map(lambda a: f'{a}\n', bike.turnangles))


if __name__ == '__main__':
    if not SIMULATION:
        time.sleep(START_TIME)
    interface()
