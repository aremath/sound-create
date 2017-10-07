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
