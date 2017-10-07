import random
import classes
import os
import sys

def random_sounds(sound_files, n, start_times, positions):
    """make some random sounds in the specified ranges from the file list"""
    sound_objects = []
    for i in range(n):
        sound_file = random.choice(sound_files)
        start_time = random.uniform(start_times[0], start_times[1])
        pos  = []
        # get a random value for every dimension of position specified
        for position_range in positions:
            pos.append(random.uniform(position_range[0], position_range[1]))
        assert len(positions) == 3, "Position should have three dimensions"
        so = classes.SoundObject(str(i), tuple(pos), sound_file, start_time)
        sound_objects.append(so)
    return sound_objects

# given a path to a directory, make some random sounds and listen to them
def random_data(mic_array, path_to_sounds, nsounds, start_times, position_limits):
    # use sound files at the top level with .wav extension
    sound_files = os.listdir(path_to_sounds)
    sound_files = filter(lambda x: x.split(".")[-1] == "wav", sound_files)
    # give the direct path to the file (rather than just the name)
    sound_files = map(lambda x: path_to_sounds + "/" + x, sound_files)
    sounds = random_sounds(sound_files, nsounds, start_times, position_limits)
    classes.hear_all(sounds, mic_array)

