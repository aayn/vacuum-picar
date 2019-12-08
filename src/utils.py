import numpy as np
import numpy.linalg as LA
from scipy.interpolate import interp1d


def mapl(f, *seq):
    return list(map(f, *seq))


widths = [58, 61, 67, 76, 90, 104, 111, 152, 192, 253]
distances = [1.90, 1.815, 1.64, 1.45, 1.25, 1.07, 0.99, 0.73, 0.58, 0.445]
distances_inv = mapl(lambda x: 1 / x, distances)

fd2w_ = interp1d(distances_inv, widths, fill_value='extrapolate')
fd2w = lambda x: fd2w_(1 / x)

fw2d_ = interp1d(widths, distances_inv, fill_value='extrapolate')
fw2d = lambda w: 1 / fw2d_(w)

actual_angle = [-15, 0, 15]
predicted_angle = [-7.3, 23.4, 47.2]
correct_alpha = interp1d(predicted_angle,
                         actual_angle,
                         fill_value='extrapolate')


def get_correct_alpha(x):
    return correct_alpha(x)


def get_alpha(polygon):
    qr_centroid = np.mean(np.array(polygon), axis=0)
    dist_from_center = qr_centroid[0] - 320
    alpha = np.deg2rad(-dist_from_center * 60 / 320)
    alpha = np.mod(alpha + np.pi, 2 * np.pi) - np.pi
    alpha = np.deg2rad(get_correct_alpha(np.rad2deg(alpha)))
    alpha = np.mod(alpha + np.pi, 2 * np.pi) - np.pi
    return alpha


def picar_to_real_v(v_picar):
    # TODO: Calculate for my carpet
    return 0.0065 * v_picar - 0.078


def real_to_picar_v(v_real):
    # TODO: Calculate for my carpet
    return int(np.round((v_real + 0.078) / 0.0065))


def euclidean_dist(x1, x2):
    return LA.norm(np.array(x1) - np.array(x2))
