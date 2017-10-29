
import classes
import random_audio
import localization
import math


if __name__ == "__main__":
    sl1 = classes.SoundListener("sl1", (0, 0, 5), (1, 0, 0))
    sl2 = classes.SoundListener("sl2", (0, 5, 0), (0, 1, 0))
    sl3 = classes.SoundListener("sl3", (5, 0, 0), (0, 1, 0))
    listeners = [sl1, sl2, sl3]
    so = classes.SoundObject("a", (6, 3, 7), "../46.wav", 1)
    classes.hear_all([so], listeners)
    d12 = localization.find_distance(sl1.pos, sl1.sounds["a"], sl2.pos, sl2.sounds["a"])
    d23 = localization.find_distance(sl2.pos, sl2.sounds["a"], sl3.pos, sl3.sounds["a"])
    d13 = localization.find_distance(sl1.pos, sl1.sounds["a"], sl3.pos, sl3.sounds["a"])
    h12 = (d12, (sl1.pos, sl2.pos))
    h23 = (d23, (sl2.pos, sl3.pos))
    h13 = (d13, (sl1.pos, sl3.pos))
    hloss = lambda p: localization.hyperboloid_loss(p, [h12, h23, h13])
    localization.plot_loss(hloss, 10, 10, 7, 0.1)
    data, pos, loss = localization.gdescend((7, 4, 2), hloss, 0.1, 1, 0.00001)
    print pos, loss
    localization.plot_data(data)

