import wave
import struct
import numpy as np


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

    def open_wav(self, path):
        sound_frames, fs = self.wav_to_floats(path)
        self.audio = np.asarray(sound_frames)

    def get_audio(self):
        return self.audio

    def wav_to_floats(self, path):
        w = wave.open(path)
        fs = w.getframerate()
        astr = w.readframes(w.getnframes())
        # convert binary chunks to short
        a = struct.unpack("%ih" % (w.getnframes() * w.getnchannels()), astr)
        a = [float(val) / pow(2, 15) for val in a]
        return a, fs