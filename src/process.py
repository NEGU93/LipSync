import numpy as np
from scipy import signal
from scipy.fftpack import fft, fftshift
import matplotlib.pyplot as plt
import math
import wave
import sounddevice as sd
import sys
import struct
from processing_functions import shorttime_energy


def wav_to_floats(wave_file):
    w = wave.open(wave_file)
    astr = w.readframes(w.getnframes())
    # convert binary chunks to short
    a = struct.unpack("%ih" % (w.getnframes()* w.getnchannels()), astr)
    a = [float(val) / pow(2, 15) for val in a]
    return a


filename = '../sounds/vocales.wav'
wave_read = wave.open(filename, mode=None)
fs = wave_read.getframerate()
n = wave_read.getnframes()
frames = wav_to_floats(filename)

print(frames[1])
sd.play(frames, fs)
plt.plot(frames)
plt.show()

x = np.linspace(-np.pi, np.pi, 200)
sig = np.sin(x)
window = signal.hann(100)
print(shorttime_energy(sig, window, 50))