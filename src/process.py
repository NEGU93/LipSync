import numpy as np
from scipy import signal
from scipy.fftpack import fft, fftshift
import matplotlib.pyplot as plt
import math
import wave
import sys
import struct
from processing_functions import short_time_energy
from processing_functions import formants_calculator
from audiolazy import lazy_lpc
from phonemes import *


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
L = round(20e-3*fs)
window = signal.hann(L)
step_size = round(L/2)
lpc_order = 12
formants_freq = formants_calculator(sound_frames, window, step_size, lpc_order, fs)
formants = list(formants_freq)
energy_time, energy_frames = short_time_energy(sound_frames, window, step_size)

sound_frames_formants = [0] * len(sound_frames)
for it in range(0, len(formants)):
    if energy_frames[it] < (max(energy_frames)*.1):
        formants[it] = 'silent'
        formants_freq[it] = 0
        sound_frames_formants[min(it*step_size, len(sound_frames)):min((it+1)*step_size, len(sound_frames))] = [1] * \
            (min((it+1)*step_size, len(sound_frames)) - min(it*step_size, len(sound_frames)))
    else:
        formants[it] = best_phoneme(np.array([formants[it][0], formants[it][1]])).phoneme_name
        if formants[it] == '/a/':
            a = 2
        elif formants[it] == '/e/':
            a = 3
        elif formants[it] == '/i/':
            a = 4
        elif formants[it] == '/o/':
            a = 5
        elif formants[it] == '/u/':
            a = 6
        else:
            a = 7
        sound_frames_formants[min(it*step_size, len(sound_frames)):min((it+1)*step_size, len(sound_frames))] = [a] * \
            (min((it+1)*step_size, len(sound_frames)) - min(it*step_size, len(sound_frames)))


formantss = formants_freq[300:-1]
# print(st_energy.size)
# print(sound_frames.size)

# sd.play(sound_frames, fs)
plt.plot(sound_frames)
plt.plot(sound_frames_formants)
# sound_frames_a = [i for i in formants if i == '/a/']
# for i in range(0, len(sound_frames)):
#     sound_frames_a[min(i*step_size, len(sound_frames))] =
# sound_frames_a = np.array([0] * len(sound_frames))
# for it in range(0, len(sound_frames)):
#     if sound_frames_formants[it] == '/a/':
#         sound_frames_a[it] = sound_frames[it]
# plt.plot(sound_frames_a)
# sound_frames_a = [i for i in sound_frames_formants if i == '/a/']
# plt.plot(sound_frames_a)
# plt.plot(st_energy)
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