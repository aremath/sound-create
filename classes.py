import numpy as np
import scipy.io.wavfile as wavfile

# speed of sound in air in m/s
speed_of_sound = 340.29
# Number of samples per second in hz
sampling_rate = 44100

#note: start time in seconds, not in samples
class SoundObject:
    def __init__(self, name_, pos_, sound_file_, start_time_):
        self.name = name_
        self.pos = pos_
        print "load"
        srate, self.sound = wavfile.read(sound_file_) # read the sound_file_
        #TODO: wat do if bitrate is different?
        assert srate == sampling_rate, srate
        self.start_time = start_time_

class SoundListener:
    def __init__(self, name_, pos_, gain_function_=lambda x: x):
        self.name = name_
        self.pos = pos_
        self.gain_function = gain_function_ # a function of frequency
        #TODO: direction_function and facing?
        #TODO: noise function?
        # holds the listener's absolute sound
        self.sound = np.zeros((0, 2)) # numpy array
        # holds each sound the listener heard separately
        self.sounds = []

    def hear_sound(self, sound_object):
        # add what this listener hears of the sound object to its sound
        
        # TODO: apply a distance factor to the amplitude
        # take the FFT
        # apply the gain function + direction function (?)
        # take the IFFT
        
        # apply time-of-flight delay
        distance = ((self.pos[0] - sound_object.pos[0])**2 + (self.pos[1] - sound_object.pos[1])**2)**0.5
        real_time = sound_object.start_time + (distance/speed_of_sound)
        sample_time = int(sampling_rate * real_time)
        pad = np.zeros((sample_time, 2))
        real_sound = np.append(pad, sound_object.sound, axis=0)
        print sound_object.sound.shape
        print real_sound.shape
        
        # add the new sound into the set of sounds heard by this listener
        # TODO: with delay?
        self.sounds.append(real_sound)
        # add the new sound to the actual sound heard by the listener
        # first, make the two sounds the same length
        zeros_to_add = self.sound.shape[0] - real_sound.shape[0]
        if zeros_to_add < 0:
            self.sound = np.append(self.sound, np.zeros((-zeros_to_add, 2)), axis=0)
        elif zeros_to_add > 0:
            real_sound = np.append(real_sound, np.zeros((zeros_to_add, 2)), axis=0)
        assert real_sound.size == self.sound.size

        self.sound += real_sound

    def write_sound(self):
        # convert the sounds this listener heard to sound files
        #TODO: be able to reference the indivudual sound objects rather than just by index (use name?)
        print "write"
        for index, sound in enumerate(self.sounds):
            wavfile.write(self.name + "_" + str(index) + ".wav", sampling_rate, sound)
        wavfile.write(self.name + "_composite.wav", sampling_rate, self.sound)

