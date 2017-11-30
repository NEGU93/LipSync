from scipy import signal
import data
import numpy as np


def pitch_change(freq_shift):
    datos = data.LipSyncData.get_instance()
    L = round(20e-3*datos.fs)
    window = signal.hann(L)
    step_size = round(L/2)
    samples = 20
    size = datos.fs // samples

    c = len(datos.audio) // size
    shift = freq_shift // samples
    audio_mod = []
    for it in range(c):
        da = np.fromstring(datos.audio_int[min(size*it, datos.audio_int.size):min(size*(it+1), datos.audio_int.size)], dtype = np.int16)
        left, right = da[0::2], da[1::2]
        left_signal, right_signal = np.fft.rfft(left), np.fft.rfft(right)
        left_signal, right_signal = np.roll(left_signal, shift), np.roll(right_signal, shift)
        if shift < 0:
            left_signal[shift:0], right_signal[shift:0] = 0, 0
        else:
            left_signal[0:shift], right_signal[0:shift] = 0, 0
        left_signal_shifted, right_signal_shifted = np.fft.irfft(left_signal), np.fft.irfft(right_signal)
        ns = np.column_stack((left_signal_shifted, right_signal_shifted)).ravel().astype(np.int16)
        audio_mod.extend(ns)

    data.audio = audio_mod
