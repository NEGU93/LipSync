from scipy import signal
import data
import numpy as np
from scipy.interpolate import interp1d
import numpy as np
import math


def duration_change(duration_factor):
    datos = data.LipSyncData.get_instance()

    L = round(50e-3 * datos.fs)
    window = signal.hamming(L, sym=True)

    duration_factor = duration_factor / 100

    if duration_factor == 0:
        duration_factor = 1

    if duration_factor < 0:
        duration_factor = -1 / duration_factor

    step_size = round(L * duration_factor)

    signal_ = np.asarray(datos.audio)

    stretched_data = np.array([])

    for i in range(0, int(math.ceil(signal_.size / step_size))):
        frame_signal = signal_[i * step_size:min(i * step_size + window.size, signal_.size)]
        window = np.resize(window, frame_signal.shape)
        if frame_signal.size == 0:
            break

        stretched_data = np.append(stretched_data, frame_signal)

    datos.audio = stretched_data
