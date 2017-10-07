
import classes
import random_audio
import math


if __name__ == "__main__":
    sl1 = classes.SoundListener("sl1", (0, 0, 0), (1, 0, 0), polar_pattern_=lambda x: math.cos(x))
    sl2 = classes.SoundListener("sl2", (10, 0, 4), (0, 1, 0))
    listeners = [sl1, sl2]
    random_audio.random_data(listeners, "..", 10, (0, 10), [(0, 10), (0, 10), (0, 10)])
    for l in listeners:
        l.write_sound()
