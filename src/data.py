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
        self.fs = 44100
        self.start_time = 0.0
        self.audio_time = 0.0
        self.dat = [(0, Phonemes.rest)]

    def open_wav(self, path):
        sound_frames, fs = self.wav_to_floats(path)
        self.audio = np.asarray(sound_frames)
        self.audio_time = len(self.audio) / fs

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
        return a, self.fs

    def play_audio(self):
        sd.play(self.audio, self.fs)
        self.start_time = sd.get_stream().time

    def stop_audio(self):
        sd.stop()

    def get_status(self):
        return sd.get_status()

    def get_stream(self):
        return sd.get_stream()

    def get_current_time(self):
        temp_time = sd.get_stream().time
        if (self.start_time + self.audio_time) < temp_time:
            return 0.0
        return temp_time - self.start_time

    def get_current_index(self):
        return int(self.get_current_time() * self.fs)

    def example_dat(self):
        self.dat = [
            (0, Phonemes.rest),
            (10, Phonemes.AI),
            (8000, Phonemes.E),
            (16000, Phonemes.etc),
            (24000, Phonemes.MBP)
        ]
