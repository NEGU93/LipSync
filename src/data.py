from pitch_change import *
import wave
import struct
import numpy as np
import sounddevice as sd
from enum import Enum


class Phonemes(Enum):
    AI = 1
    E = 2
    U = 3
    O = 4
    etc = 5
    FV = 6
    MBP = 7
    L = 8
    WQ = 9
    rest = 10


class LipSyncData:
    __instance = None

    @staticmethod
    def get_instance():
        if LipSyncData.__instance is None:
            LipSyncData()
        return LipSyncData.__instance

    def __init__(self):
        if LipSyncData.__instance is not None:
            raise Exception("This Class is a singleton!")
        else:
            LipSyncData.__instance = self
        self.audio = []
        self.audio_right = []
        self.audio_left = []
        self.audio_int = []
        self.audio_int_right = []
        self.audio_int_left = []
        self.fs = 8000
        self.start_time = 0.0
        self.audio_time = 0.0
        self.dat = [(0, Phonemes.rest)]
        self.playing = False

    def open_wav(self, path):
        sound_frames, fs = self.wav_to_floats(path)
        self.wav_to_ints(path)
        self.audio = np.asarray(sound_frames)
        self.audio_time = len(self.audio) / fs
        pitch_change()

    def get_audio(self):
        return self.audio

    def get_audio_fs(self):
        return self.audio, self.fs

    def wav_to_floats(self, path):
        w = wave.open(path)
        self.fs = w.getframerate()
        astr = w.readframes(w.getnframes())
        # convert binary chunks to short
        a = struct.unpack("%ih" % (w.getnframes() * w.getnchannels()), astr)
        a = [float(val) / pow(2, 15) for val in a]
        if w.getnchannels() == 1:  # mono
            return a, self.fs
        else:  # stereo
            self.audio_right = np.asarray(a[0::2])
            self.audio_left = np.asarray(a[1::2])
            return a, self.fs

    def wav_to_ints(self, path):
        w = wave.open(path, 'r')
        self.fs = w.getframerate()
        da = np.fromstring(w.readframes(w.getnframes()), dtype=np.int16)
        if w.getnchannels() == 1:  # mono
            self.audio_int = da
        else:  # stereo
            self.audio_int_right, self.audio_int_left = da[0::2], da[1::2]  # left and right channel

    def play_audio(self):
        self.playing = True
        sd.play(self.audio, self.fs)
        self.start_time = sd.get_stream().time

    def stop_audio(self):
        self.playing = False
        sd.stop()

    def get_status(self):
        return sd.get_status()

    def get_stream(self):
        return sd.get_stream()

    def get_current_time(self):
        if self.playing:
            temp_time = sd.get_stream().time
            if (self.start_time + self.audio_time) < temp_time:
                return 0.0
            return temp_time - self.start_time
        else:
            return 0.0

    def get_current_index(self):
        return int(self.get_current_time() * self.fs)

    def append_dat(self, index, phoneme):
        self.dat.append((index, phoneme))

    def export_dat(self, path):
        file = open(path, "w")

        file.write('MohoSwitch1\n')
        for i in range(0, len(self.dat)):
            file.write(str(self.dat[i][0]) + ' ' + self.dat[i][1].name + '\n')

        file.close()

    def example_dat(self):
        self.dat = [
            (0, Phonemes.rest),
            (100, Phonemes.AI),
            (8000, Phonemes.E),
            (16000, Phonemes.etc),
            (24000, Phonemes.MBP)
        ]
