import numpy as np
from scipy import signal
from scipy.fftpack import fft, fftshift
import matplotlib.pyplot as plt
import math
import wave
import sounddevice as sd
import sys
import struct
from processing_functions import short_time_energy


def wav_to_floats(wave_file):
    w = wave.open(wave_file)
    fs = w.getframerate()
    astr = w.readframes(w.getnframes())
    # convert binary chunks to short
    a = struct.unpack("%ih" % (w.getnframes()* w.getnchannels()), astr)
    a = [float(val) / pow(2, 15) for val in a]
    return a, fs


filename = '../sounds/vocales.wav'
sound_frames, fs = wav_to_floats(filename)
sound_frames = np.asarray(sound_frames)
window = signal.hann(100)
step_size = 50
st_energy = short_time_energy(sound_frames, window, step_size)
print(st_energy.size)
print(sound_frames.size)

# sd.play(sound_frames, fs)
plt.plot(sound_frames)
plt.plot(st_energy)
# print(st_energy)
plt.show()

# print(np.zeros((2, 5)))
#
# x = np.linspace(-np.pi, np.pi, 200)
# sig = np.sin(x)
# window = signal.hann(100)
# ww = np.linspace(-np.pi, np.pi, 10)
# print(ww[ww.size-1])
# print(shorttime_energy(sig, window, 50))