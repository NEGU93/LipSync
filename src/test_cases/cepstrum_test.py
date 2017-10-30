import numpy as np
import matplotlib.pyplot as plt
from cepstrum import complex_cepstrum, inverse_complex_cepstrum
from numpy import ceil
import pvutils as pv
import scipy.signal
import data


def is_silence(signal):
    e, _ = pv.short_time_energy(signal, scipy.signal.get_window("boxcar", 201))
    sil = pv.superior_to(e, max(e) * 0.0001)
    return sum(sil)

data = data.LipSyncData.get_instance()

data.open_wav('../sounds/vocales.wav')
samples = int(data.fs*data.audio_time)
t = np.arange(samples + 1) / data.fs

signal = data.audio
step_size = int(0.1 * data.fs)
# ceps, _ = complex_cepstrum(signal, step_size)

fig = plt.figure()
ax0 = fig.add_subplot(211)
ax0.plot(t, signal)
ax0.set_xlabel('time[s]')
ax0.set_title('Input')

# ceps = np.zeros(signal.shape)
for it in range(0, int(ceil(signal.size / step_size))):
    frame_signal = signal[it * step_size:min(it * step_size + step_size, signal.size)]
    if is_silence(frame_signal) != 0:
        ceps, n = complex_cepstrum(frame_signal)
        trng = t[it * step_size:min(it * step_size + step_size, signal.size)]
        place = np.argmax(ceps[:int(len(ceps)/2)])
        print('F0 = ' + str(place) + ' Hz')
        # plt.figure()
        # plt.plot(ceps)
        # plt.show()
        frame_signal = inverse_complex_cepstrum(ceps, n)
        signal[it * step_size:min(it * step_size + step_size, signal.size)] = frame_signal

# import pdb; pdb.set_trace()

ax1 = fig.add_subplot(212)

ax1.plot(t, signal, label='signal')
e, _ = pv.short_time_energy(signal, scipy.signal.get_window("boxcar", 201))
sil = pv.superior_to(e, max(e) * 0.08)
ax1.plot(t, e / e.max(), 'm', label='energy')
ax1.plot(t, sil, 'r', label='Silence')
ax1.set_xlabel('time[s]')
ax1.set_title('Output')
plt.show()