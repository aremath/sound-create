import numpy as np
import scipy.io.wavfile as wavfile
import vectors

# speed of sound in air in m/s
speed_of_sound = 340.29
# Number of samples per second in hz
sampling_rate = 44100

#note: start time in seconds, not in samples

# TODO: global volume control
# TODO: moving sound sources! - How?
class SoundObject:
    def __init__(self, name_, pos_, sound_file_, start_time_, loudness_=1):
        self.name = name_
        self.pos = np.array(pos_)
        srate, self.sound = wavfile.read(sound_file_) # read the sound_file_
        dinfo = np.iinfo(self.sound.dtype)
        # convert to float32
        self.sound = self.sound.astype(np.float32) / dinfo.max 
        #TODO: what to do if bitrate is different?
        # average the channels to get mono audio
        self.sound *= loudness_
        self.sound = np.mean(self.sound, axis=1)
        assert srate == sampling_rate, srate
        self.start_time = start_time_

class SoundListener:
    def __init__(self, name_, pos_, direction_, gain_function_=lambda x: 1, polar_pattern_=lambda x: 1):
        self.name = name_
        self.pos = np.array(pos_)
        self.direction = np.array(direction_)
        self.gain_function = gain_function_ # a function of frequency
        self.polar_pattern = polar_pattern_ # a function of angle
        #TODO: noise function?
        # holds the listener's absolute sound
        self.sound = np.zeros((0, 1), dtype=np.float32) # using float32 for all sounds
        # holds each sound the listener heard separately
        self.sounds = {}

    def hear_sound(self, sound_object):
        """add what this listener hears of the sound object to its sound"""

        sound_dtype = sound_object.sound.dtype
        distance = np.linalg.norm(self.pos - sound_object.pos)
        angle = vectors.angle_between(self.direction, sound_object.pos - self.pos)

        # apply a distance factor to the amplitude
        real_sound = sound_object.sound / (1 + distance**2)

        # apply the polar pattern
        real_sound = real_sound * self.polar_pattern(angle)

        #TODO:
        # take the FFT
        # apply the gain function
        # take the IFFT
        
        # apply time-of-flight delay
        real_time = sound_object.start_time + (distance/speed_of_sound)
        sample_time = int(sampling_rate * real_time)
        pad = np.zeros((sample_time), dtype=sound_dtype)
        real_sound = np.append(pad, real_sound, axis=0)

        # add the new sound into the set of sounds heard by this listener
        self.sounds[sound_object.name] = real_sound
        #print sound_object.sound.shape
        #print real_sound.shape

        # add the new sound to the actual sound heard by the listener
        # first, make the two sounds the same length
        zeros_to_add = self.sound.shape[0] - real_sound.shape[0]
        if zeros_to_add < 0:
            self.sound = np.append(self.sound, np.zeros(-zeros_to_add, dtype=sound_dtype))
        elif zeros_to_add > 0:
            real_sound = np.append(real_sound, np.zeros(zeros_to_add, dtype=sound_dtype))
        assert real_sound.size == self.sound.size

        self.sound += real_sound

    def write_sound(self):
        """convert the sounds this listener heard to sound files"""
        for name, sound in self.sounds.items():
            wavfile.write(self.name + "_" + name + ".wav", sampling_rate, sound)
        wavfile.write(self.name + "_composite.wav", sampling_rate, self.sound)

def hear_all(sobjects, slisteners):
    """every listener in slistners hears every sound in sobjects"""
    for slistener in slisteners:
        for sobject in sobjects:
            slistener.hear_sound(sobject)

