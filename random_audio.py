import random
import classes
import os
import sys

class PositionDistribution:

    def __init__(self, distribution):
        """distribution is a list of lists of intervals. Each element describes a rectangular prism."""
        self.distribution = distribution

    def choose_position(self):
        """choose a position uniformly out of the entire set of rectangles"""
        # weight each prism by volume
        weighted_prisms = [(prism, find_volume(prism)) for prism in self.distribution]
        # choose one uniformly
        choice = weighted_choice(weighted_prisms)
        # choose a position within that prism uniformly
        position = [random.uniform(*interval) for interval in choice]
        return tuple(position)

def find_volume(intervals):
    """find the volume of a 3-dimensional rectangular prism"""
    assert len(intervals) == 3
    breadth = intervals[0][1] - intervals[0][0]
    width = intervals[1][1] - intervals[1][0]
    height = intervals[2][1] - intervals[2][0]
    return abs(breadth * width * height)

def weighted_choice(choices):
    """returns an item chosen at random from choices; expects choices to be a list of tuples of (choice, weight)"""
    total_weight = sum([weight for choice, weight in choices])
    # choose a number to pick a choice
    r = random.uniform(0, total_weight)
    accumulate = 0
    for choice, weight in choices:
        accumulate += weight
        if accumulate > r:
            return choice
    assert False, "weighted choice somehow broken"
        
def random_sounds(sound_files, distribution, nsounds, start_times):
    sobjects = []
    for i in range(nsounds):
        sound_file = random.choice(sound_files)
        start_time = random.uniform(*start_times)
        pos = distribution.choose_position()
        assert len(pos) == 3, "Position should have 3 dimensions"
        so = classes.SoundObject(str(i), pos, sound_file, start_time)
        sobjects.append(so)
    return sobjects

def random_data(mic_array, path_to_sounds, nsounds, start_times, position_limits):
    """given a path to a directory, make some random sounds and listen to them"""
    # use sound files at the top level with .wav extension
    sound_files = os.listdir(path_to_sounds)
    sound_files = filter(lambda x: x.split(".")[-1] == "wav", sound_files)
    # give the direct path to the file (rather than just the name)
    sound_files = map(lambda x: path_to_sounds + "/" + x, sound_files)
    sounds = random_sounds(sound_files, position_limits, nsounds, start_times)
    classes.hear_all(sounds, mic_array)

def random_data_crowd(mic_array, normal_sounds, normal_dist, nnormal, crowd_sounds, crowd_dist, ncrowd, start_times):
    normal_sobjects = random_sounds(normal_sounds, normal_dist, nnormal, start_times)
    crowd_sobjects = random_sounds(crowd_sounds, crowd_dist, ncrowd, start_times)
    classes.hear_all(normal_sobjects, mic_array)
    classes.hear_all(crowd_sobjects, mic_array)
