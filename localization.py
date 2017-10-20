from constants import *
import numpy as np
from sympy.solvers import solve
from sympy import Symbol
from scipy.signal import correlate

# takes multiple audio feeds (for the same sound) of the form
# (position, numpyarray)
# and calculates the approximate position of the sound
def localize(mics):
    for index1, mic1 in enumerate(mics):
        for index2, mic2 in enumerate(mics):
            if index1 != index2:
                # find the most likely distance difference (highest cross-correlation peak)
                position1, audio1 = mic1
                position2, audio2 = mic2
                corr_distance = find_distance(position1, audio1, position2, audio2)

def find_distance(position1, audio1, position2, audio2):
    """Returns the difference in the distances based on mic positions and the audios they heard"""
    correlation = scipy.signal.correlate(audio1, audio2)
    max_time = np.argmax(correlation) / sampling_rate
    return max_time * speed_of_sound

# compute the loss function for our gradient descent.
# hyperbola is a 3-tuple of (constant distance difference, tuple of foci positions)
# we want a loss function that will minimize the distance between the two hyperboloids
# given a point in 3-space, one measure of how far away it is from a hyperboloid is the amount by
# which its distance to the two foci differs from the specified distance. We'll square this because
# we want negative values to have a positive loss.
# Now we add this function for both hyperboloids, such that the loss is minimized at points that lie
# on both hyperboloids
def hyperboloid_loss(pos, hyper1, hyper2):
    """compute the loss function for gradient descent"""
    d1, foci1 = hyper1
    d2, foci2 = hyper2
    # distance to each focus
    dist_f1 = [np.linalg.norm(pos - f) for f in foci1]
    dist_f2 = [np.linalg.norm(pos - f) for f in foci2]
    loss_h1 = (dist_f1[0] - dist_f1[1] - d1)**2
    loss_h2 = (dist_f2[0] - dist_f2[1] - d2)**2
    return loss_h1 + loss_h2

def estimate_gradient(pos, loss_fn, steps):
    """estimate the gradient of loss_fn. The step sizes are defined by the array df
       which is an array of vectors that represents the step size in each dimension"""
    base = loss_fn(pos)
    # estimate partials w.r.t each dimension
    partials = []
    for vec in steps:
        behind = loss_fn(pos - vec)
        ahead = loss_fn(pos + vec)
        partial = (behind + ahead) / 2*np.linalg.norm(vec)
        partials.append(partial)
    return partials

def gdescend(initial_position, loss_fn, dx):
    """descend the gradient defined by the loss function.
       dx is the step size (in all dimensions)"""
    pass

