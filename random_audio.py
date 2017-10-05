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
        assert len(position) == 3, "Position should have three dimensions"
        so = classes.SoundObject(str(i), tuple(position), soundfile, start_time)
        sound_objects.append(so)
    return sound_objects

# given a path to a directory, make some random sounds and listen to them,
# then write them out
"""
if __name__ == "__main__":
    dirname = sys.argv[1]
    # use sound files at the top level with .wav extension
    _, _, sound_files = os.listdir(".")
    sound_files = filter(lambda x: x.split(".")[-1] == "wav", sound_files)
    sounds = random_sounds(sound_files, 10, (0, 10), [(0, 10), (0, 10), (0, 10)])
    #TODO: random microphone array? fixed array?
"""
