import numpy as np

def normalize(vector):
    """returns a unit vector in the same direction as vector"""
    if np.linalg.norm(vector) == 0:
        return vector
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """returns the angle between v1 and v2 in radians"""
    v1_unit = normalize(v1)
    v2_unit = normalize(v2)
    return np.arccos(np.dot(v1_unit, v2_unit))

