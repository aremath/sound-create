from constants import *
import numpy as np
# don't require an X-server
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import correlate
import itertools
import math

# takes multiple audio feeds (for the same sound) of the form
# (position, numpyarray)
# and calculates the approximate position of the sound
def localize(mics):
    hyperboloids = []
    for index1, mic1 in enumerate(mics):
        for index2, mic2 in enumerate(mics):
            if index1 != index2:
                # find the most likely distance difference (highest cross-correlation peak)
                position1, audio1 = mic1
                position2, audio2 = mic2
                corr_distance = find_distance(position1, audio1, position2, audio2)
                # put the corresponding hyperbola into the list
                hyperboloids.append((corr_distance, (position1, position2)))
    # find all mic pairs
    all_pairs = itertools.combinations(hyperboloids, 2)
    intersects = []
    for h1, h2 in all_pairs:
        hloss = lambda p: hyperboloid_loss(p, h1, h2)
        #TODO: random initial position
        intersects.append(gdescend((0,0,0), hloss, 0.01, 0.1, 0.01))
    return intersects

#TODO: break this ^ up into functions

def find_distance(position1, audio1, position2, audio2):
    """Returns the difference in the distances based on mic positions and the audios they heard"""
    correlation = correlate(audio1, audio2)
    max_time = (np.argmax(correlation) - (audio2.size)) / float(sampling_rate)
    return max_time * speed_of_sound

# compute the loss function for our gradient descent.
# hyperbola is a 3-tuple of (constant distance difference, tuple of foci positions)
# we want a loss function that will minimize the distance between the two hyperboloids
# given a point in 3-space, one measure of how far away it is from a hyperboloid is the amount by
# which its distance to the two foci differs from the specified distance. We'll square this because
# we want negative values to have a positive loss.
# Now we add this function for both hyperboloids, such that the loss is minimized at points that lie
# on both hyperboloids
def hyperboloid_loss(pos, hyperboloids):
    """compute the loss function based on sum of squared distances to hyperbolas"""
    losses = []
    for dist, foci in hyperboloids:
        foci_dist = [np.linalg.norm(pos - f) for f in foci]
        loss = (foci_dist[0] - foci_dist[1] - dist)**2
        losses.append(loss)
    return sum(losses)

def estimate_gradient(pos, loss_fn, steps):
    """estimate the gradient of loss_fn. The step sizes are defined by the array df
       which is an array of vectors that represents the step size in each dimension"""
    base = loss_fn(pos)
    # estimate partials w.r.t each dimension
    partials = []
    for vec in steps:
        behind = loss_fn(pos - vec)
        ahead = loss_fn(pos + vec)
        partial = (ahead - behind) / 2*np.linalg.norm(vec)
        partials.append(partial)
    return np.array(partials)

def gdescend(initial_position, loss_fn, dx, learning_rate, threshold, maxsteps=100000, nsteps=1000):
    """descend the gradient defined by the loss function.
       dx is the step size (in all dimensions)"""
    pos = initial_position
    steps = np.zeros((3, 3))
    np.fill_diagonal(steps, dx)
    loss = loss_fn(pos)
    counter = 0
    data = []
    while loss > threshold:
        grad = estimate_gradient(pos, loss_fn, steps)
        pos -= learning_rate * grad
        loss = loss_fn(pos)
        counter += 1
        if counter % nsteps == 0:
            data.append((loss, pos))
            print loss
            print pos
        if counter > maxsteps:
            break
    return data, pos, loss


def plot_loss(loss_fn, range_x, range_y, z, dx):
    lf = np.zeros((int(range_x / dx), int(range_y / dx)))
    for index, _ in np.ndenumerate(lf):
        pos = np.array([index[0]*dx, index[1]*dx, z])
        lf[index] = math.log(loss_fn(pos))
    #fig = plt.figure()
    #axes = fig.add_subplot()
    #axes.set_xlabel("xlabel")
    #axes.set_ylabel("ylabel")
    plt.imshow(lf, cmap='hot', interpolation='nearest')
    plt.gca().invert_yaxis()
    plt.savefig("temploss.png")
    plt.clf()

#TODO: this doesn't do what I was hoping :(
def plot_data(data):
    x = []
    y = []
    for _, pos in data:
        x.append(pos[0])
        y.append(pos[1])
    plt.scatter(x, y)
    plt.savefig("temppos.png")


