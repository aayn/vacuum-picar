"""Localization module responsible improving position estimates of the robot."""
import numpy as np
import numpy.linalg as LA
from scipy.optimize import minimize
from src import utils as u
from src.config import WHEEL_BASE, QR_POS, LOC_ERR_TOLERANCE


class Localizer(object):
    def __init__(self):
        self.qrs = None

    def input(self, qrs, pose):
        self.qrs = qrs
        self.pose = pose

    def best_fit(self, qr1_p, qr2_p):
        """Returns position of the car the best fit the observed QR positions."""
        x1, y1 = qr1_p
        x2, y2 = qr2_p

        rho1, rho2 = self.qrs[0][2], self.qrs[1][2]

        # Choose x, y such that they minimize the triangulation/trilateration
        # error.
        f = lambda p: ((p[0] - x1)**2 + (p[1] - y1)**2 - rho1**2 +
                       (p[0] - x2)**2 + (p[1] - y2)**2 - rho2**2)**2
        res = minimize(f, [1, 0], method='L-BFGS-B', tol=1e-12)
        x, y = res.x
        error = LA.norm([x - self.pose[0], y - self.pose[1]])
        return (x, y), error

    def localize(self):
        if self.qrs is None or len(self.qrs) == 1:
            return None
        self.qrs = sorted(self.qrs, key=lambda q: q[2])
        name1, name2 = self.qrs[0][0], self.qrs[1][0]

        for qr1_p in QR_POS[name1]:
            for qr2_p in QR_POS[name2]:
                (x, y), error = self.best_fit(qr1_p, qr2_p)

            if error < lowest_error:
                lowest_error = error
                best_x, best_y = x, y

        if lowest_error > LOC_ERR_TOLERANCE:
            return None
        # print(f'Lowest error = {lowest_error}')
        return (best_x, best_y, self.pose[2])

    def simple_localize(self):
        if self.qrs is None or len(self.qrs) == 1:
            return None
        self.qrs = sorted(self.qrs, key=lambda q: q[2])
        name1, name2 = self.qrs[0][0], self.qrs[1][0]
        qr1_p = QR_POS[name1][0]
        qr2_p = QR_POS[name2][0]
        (x, y), error = self.best_fit(qr1_p, qr2_p)

        if error > LOC_ERR_TOLERANCE:
            return None
        return (x, y, self.pose[2])

    def output(self):
        return self.simple_localize()
