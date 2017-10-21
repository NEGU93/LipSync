import numpy as np
from scipy import signal
from scipy.fftpack import fft, fftshift
import matplotlib.pyplot as plt
import math
import wave
import sounddevice as sd
import sys

def shorttime_energy(sig, window, step_size):
    energy = 0
    for it in range(0, math.ceil(sig.size / step_size)):
        frame_signal = sig[it*step_size:min(it*step_size + window.size, sig.size - 1)]
        if window.size != frame_signal.size:
            window = window[0:frame_signal.size] #no falta un -1?
        frame_energy = np.sum(np.square(np.multiply(frame_signal, window)))
        energy += frame_energy

    return energy

filename = '../sounds/vocales.wav'
wave.open(filename, mode=None)
x = np.linspace(-np.pi, np.pi, 200)
sig = np.sin(x)
window = signal.hann(100)
print(shorttime_energy(sig, window, 50))