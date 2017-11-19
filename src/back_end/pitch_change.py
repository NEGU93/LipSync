from scipy import signal
import data
import numpy as np


def pitch_change(freq_shift):
    datos = data.LipSyncData.get_instance()
    L = round(20e-3*datos.fs)
    window = signal.hann(L)
    step_size = round(L/2)
    fr = 20
    sz = datos.fs // fr  # Read and process 1/fr second at a time.
    # A larger number for fr means less reverb.
    c = len(datos.audio) // sz # count of the whole file
    shift = freq_shift // fr  # shifting 100 Hz
    audio_mod = []
    for it in range(c):
        da = np.fromstring(datos.audio_int[min(sz*it, datos.audio_int.size):min(sz*(it+1), datos.audio_int.size)], dtype = np.int16)
        left, right = da[0::2], da[1::2]  # left and right channel
        lf, rf = np.fft.rfft(left), np.fft.rfft(right)
        lf, rf = np.roll(lf, shift), np.roll(rf, shift)
        if shift < 0:
            lf[shift:0], rf[shift:0] = 0, 0
        else:
            lf[0:shift], rf[0:shift] = 0, 0
        nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
        ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
        audio_mod.extend(ns)

    data.audio = audio_mod
