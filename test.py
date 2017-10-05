
import classes
import math

if __name__ == "__main__":
    sl1 = classes.SoundListener("sl1", (0, 0, 0), (1, 0, 0), polar_pattern_=lambda x: math.cos(x))
    sl2 = classes.SoundListener("sl2", (10, 0, 4), (0, 1, 0))
    listeners = [sl1, sl2]
    so1 = classes.SoundObject("sound1", (10, 0, 4), "../48.wav", 2, 1)
    so2 = classes.SoundObject("sound2", (5, 5, 5), "../46.wav", 2, 1)
    sounds = [so1, so2]
    classes.hear_all(sounds, listeners)
    for l in listeners:
        l.write_sound()
