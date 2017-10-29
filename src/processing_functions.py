import numpy as np
from scipy import signal
from scipy.fftpack import fft, fftshift
import matplotlib.pyplot as plt
import math
import wave
import sounddevice as sd
import sys
import struct
import cmath
from audiolazy import lazy_lpc
from scipy.signal import lfilter, lfilter_zi


def shorttime_energy(sig, window, step_size):
    energy = 0
    for it in range(0, int(math.ceil(sig.size / step_size))):
        frame_signal = sig[it*step_size:min(it*step_size + window.size, sig.size - 1)]
        if window.size != frame_signal.size:
            window = window[0:frame_signal.size] #no falta un -1?
        frame_energy = np.sum(np.square(np.multiply(frame_signal, window)))
        energy += frame_energy

    return energy


def short_time_energy(signal, window, step_size):
    energy_time = np.zeros(signal.size)
    energy_frames = []

    for it in range(0, int(math.ceil(signal.size / step_size))):
        frame_signal = signal[it*step_size:min(it*step_size + window.size, signal.size)]
        # import pdb; pdb.set_trace()
        if window.size != frame_signal.size:
            window = window[0:frame_signal.size]
        if (frame_signal.size == 0) or (frame_signal.size == 0):
            return energy_time, energy_frames

        frame_energy = np.sum(np.square(np.multiply(frame_signal, window)))
        energy_time[it * step_size: min(it * step_size + window.size, signal.size)] = frame_energy
        energy_frames.append(frame_energy)
    return energy_time, energy_frames


def formants_calculator(signal, window, step_size, lpc_order, fs):
    poles = np.zeros((lpc_order, signal.size))
    formants = []

    for it in range(0, int(math.ceil(signal.size / step_size))):
        frame_signal = signal[it*step_size:min(it*step_size + window.size, signal.size)]
        # import pdb; pdb.set_trace()
        if it == 325:
            print(1)
        elif it == 423:
            print(2)

        if window.size != frame_signal.size:
            window = window[0:frame_signal.size]
        if (frame_signal.size == 0) or (frame_signal.size == 0):
            return formants

        frame_signal_windowed = np.multiply(frame_signal, window)
        if frame_signal_windowed.size <= lpc_order:
            return formants

        preemph = np.asarray([1, 0.63])
        x_frame_filtered = lfilter(np.asarray([1]), preemph, frame_signal_windowed)
        h = lazy_lpc.lpc.autocor(x_frame_filtered, lpc_order)
        roots = np.roots(h.numerator)

        r = [i for i in roots if i.imag >= 0]
        angz = np.angle(r)
        angf = np.multiply(angz, (fs / (2*math.pi)))

        frqs = np.sort(angf)
        indeces = np.argsort(angf)
        bw = -1/2 * (fs/(2 * math.pi)) * np.log(np.abs(np.asarray([r[it] for it in indeces])))

        frame_formants = []
        n = 1
        for k in range(0, frqs.size):
            if (frqs[k] > 90) and (bw[k] < 400):
                frame_formants.append(frqs[k])

        formants.append(frame_formants)
        # plt.plot(np.linspace(0, 1e4, int(1e4))*fs / 1e4, np.abs(np.fft.fft(frame_signal, int(1e4))) / max(abs(np.fft.fft(frame_signal, int(1e4)))))
        # spect = np.array(np.divide(1, np.abs((np.fft.fft(h.numerator, int(1e4))))))
        # plt.plot(np.linspace(0, 1e4, int(1e4))*fs / 1e4, spect / max(spect))
        # plt.show()

    return formants
