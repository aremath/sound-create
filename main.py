
import classes

if __name__ == "__main__":
    sl = classes.SoundListener("ayylmao", (0, 0))
    so = classes.SoundObject("wut", (10, 0), "48.wav", 2)
    sl.hear_sound(so)
    sl.write_sound()
