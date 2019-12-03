"""Localization module responsible improving position estimates of the robot."""
import numpy as np
import numpy.linalg as LA
from scipy.optimize import minimize
from src import utils as u
from src.config import WHEEL_BASE, QR_POS


class Localizer(object):
    def __init__(self):
        self.qrs = None
    
    def input(self, qrs, pose):
        self.qrs = qrs
        self.pose = pose
    
    def estimate_qr_position(self, distance, angle):
        # TODO: Recheck
        """Estimate the position of the QR code.
        
        rect: QR code bounding rectangle.
        pose: pose of PiCar.
        """
        # Adding WHEEL_BASE to shift from camera to car coordinates
        rho = distance + WHEEL_BASE
        theta_ = np.mod(self.pose[2] + angle, 2 * np.pi)
        
        dx = rho * np.cos(theta_)
        dy = rho * np.sin(theta_)
        qx = self.pose[0] + dx
        qy = self.pose[1] + dy
        
        return (qx, qy)

    def localize(self):
        if self.qrs is None or len(self.qrs) == 1:
            return None
        
        name1, name2 = self.qrs[0][0], self.qrs[1][0]

        for qr1 in QR_POS[name1]:
            for qr2 in QR_POS[name2]:
                x1, y1 = qr1
                x2, y2 = qr2

            rho1, rho2 = self.qrs[0][2], self.qrs[1][2]

            f = lambda p: ((p[0] - x1)**2 + (p[1] - y1)**2 - rho1**2
                        + (p[0] - x2)**2 + (p[1] - y2)**2 - rho2**2)**2
            res = minimize(f, [1, 0], method='L-BFGS-B', tol=1e-12)
            x, y = res.x
            error = LA.norm([x - self.pose[0], y - self.pose[1]])
            if error < lowest_error:
                lowest_error = error
                best_x, best_y = x, y
        # print(f'Lowest error = {lowest_error}')
        return (best_x, best_y, self.pose[2])
    
    def output(self):
        return self.localize()