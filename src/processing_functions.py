import numpy as np
from scipy import signal
from scipy.fftpack import fft, fftshift
import matplotlib.pyplot as plt
import math
import wave
import sounddevice as sd
import sys
import struct


def shorttime_energy(sig, window, step_size):
    energy = 0
    for it in range(0, math.ceil(sig.size / step_size)):
        frame_signal = sig[it*step_size:min(it*step_size + window.size, sig.size - 1)]
        if window.size != frame_signal.size:
            window = window[0:frame_signal.size] #no falta un -1?
        frame_energy = np.sum(np.square(np.multiply(frame_signal, window)))
        energy += frame_energy

    return energy


def short_time_energy(signal, window, step_size):
    energy_time = np.zeros(signal.size)

    for it in range(0, int(math.ceil(signal.size / step_size))):
        frame_signal = signal[it*step_size:min(it*step_size + window.size, signal.size)]
        # import pdb; pdb.set_trace()
        if window.size != frame_signal.size:
            window = window[0:frame_signal.size]
        if (frame_signal.size == 0) or (frame_signal.size == 0):
            return energy_time

        frame_energy = np.sum(np.square(np.multiply(frame_signal, window)))
        energy_time[it * step_size: min(it * step_size + window.size, signal.size)] = frame_energy
    return energy_time


# energy_time = zeros(1, length(signal));
#
# for it = 0:ceil(length(signal) / step_size)
# frame_signal = signal(it * step_size + 1:min(it * step_size + length(window), length(signal)));
# if length(window) ~= length(frame_signal)
# window = window(1:length(frame_signal));
# end
# if isempty(frame_signal) | | isempty(window)
#     return
# end
# frame_energy = sum((frame_signal. * window). ^ 2);
# energy_time(it * step_size + 1: min(it * step_size + length(window), length(signal))) = frame_energy;
#
# end