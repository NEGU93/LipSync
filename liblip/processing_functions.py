import numpy as np
import math
import scipy.io.wavfile as wf
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


def read_wav(s):
    fs, x = wf.read(s)
    x = np.array(x, dtype=float)
    t = np.arange(len(x)) * (1.0 / fs)
    return x, t


def shift(l, n):
    return np.append(np.zeros(n), l[:len(l)-n])


def _sgn(x):
    """ return 1 if positive and -1 if negative (array like return) """
    y = np.zeros_like(x)
    y[np.where(x >= 0)] = 1.0
    y[np.where(x < 0)] = -1.0
    return y


def short_time_energy(signal, window, step_size=1):
    """ Short time energy """
    """ time response is the same size of the signal.
        frame response is the size considering the step size
        Normally frame is the response you look for, but time is cool to plot with the signal """
    energy_time = np.zeros(signal.size)
    energy_frames = np.zeros(int(math.ceil(signal.size / step_size)))
    for i in range(0, int(math.ceil(signal.size / step_size))):
        frame_signal = signal[i*step_size:min(i*step_size + window.size, signal.size)]
        window = np.resize(window, frame_signal.shape)
        if frame_signal.size == 0:
            return energy_time, energy_frames

        frame_energy = np.sum(np.multiply(np.square(frame_signal), window))
        energy_time[int(i * step_size + len(window)/2): int(min(i * step_size + window.size, signal.size) + len(window)/2)] = frame_energy
        energy_frames[i] = frame_energy
    return energy_time, energy_frames


def short_time_zero_cross_rate(signal, window, step_size=1):
    """ Short time zero crossing rate """
    """ time response is the same size of the input.
        frame response is the size considering the step size
        Normally frame is the response you look for, but time is cool to plot with the signal """
    zcr_time = np.zeros(signal.size)
    zcr_frames = np.zeros(int(math.ceil(signal.size / step_size)))
    for i in range(0, int(math.ceil(signal.size / step_size))):
        frame_signal = signal[int(i*step_size):int(min(i*step_size + window.size, signal.size))]
        frame_zeros = 0
        sign = _sgn(frame_signal)
        for j in range(1, len(sign)):
            frame_zeros = frame_zeros + abs(sign[j] - sign[j-1])
        zcr_frames[i] = frame_zeros
        zcr_time[int(i * step_size + len(window)/2): int(min(i * step_size + window.size, signal.size) + len(window)/2)] = frame_zeros
    return zcr_time, zcr_frames


def superior_to(e, threshold=1):
    """ Gives 1 if i element of e is higher than threshold and 0 elsewhere """
    return [int(x > threshold) for x in e]


def short_time_autocorrelation(signal, window, step_size=1):
    """ Gives a matrix where each column i gives the autocorrelation of the i window """
    window_len_backup = int(2 * len(window) - 1)
    autocorr = np.zeros((window_len_backup, int(np.ceil(len(signal)/step_size))))
    for i in range(0, int(np.ceil(len(signal)/step_size))):
        frame_signal = signal[int(i*step_size):int(min(i*step_size + len(window), len(signal)))]
        window = np.resize(window, frame_signal.shape)
        a = np.multiply(window, frame_signal)
        frame_autocorr = np.correlate(a, a, 'full')
        frame_autocorr = np.resize(frame_autocorr, window_len_backup)
        # import pdb; pdb.set_trace()
        autocorr[:, i] = frame_autocorr
    return autocorr


def short_time_amdf(signal, window, step_size, cte):
    """ Same as autocorrelation but faster (less precise also) """
    amdf = np.zeros((2*len(window)-1, int(np.ceil(len(signal)/step_size))))
    for i in range(0, int(np.ceil(len(signal)/step_size))):
        frame1 = signal[int(i*step_size):int(min(i*step_size + len(window), len(signal)))]
        frame2 = signal[int(min(i * step_size + cte, len(signal))):int(min(i * step_size + len(window) + 2* cte, len(signal)))]
        frame3 = np.zeros(len(frame2))
        # import pdb; pdb.set_trace()
        frame3[(len(frame2) - len(frame1)):] = frame1
        # frame1 = np.resize(frame1, frame2.shape)
        frame_amdf = np.zeros(cte)

        for j in range(0, cte):
            for k in range(0, len(frame2)):
                frame_amdf[j] = frame_amdf[j] + abs(min(frame3[k], len(frame3))) - frame2[min(k - j + cte, len(frame2))]

        amdf[:, i] = frame_amdf


def ola(signal, step_size, analysis_win, process_func, synthesis_win, fs):
    """ Applies Overlap-and-Add algorithm to the process_func passed as argument """
    """ signal: is the imput signal such as an audio
        step_size is the step at which the algorithm takes frames
        analysisis and synthesis are the windows for the input frames and the output frames 
        fs: is the sample frequency of the input argument signal"""
    out_signal = np.zeros(len(signal))

    for i in range(0, int(np.ceil(len(signal)/step_size))):
        frame_signal = signal[int(i*step_size):min(i*step_size + len(analysis_win), len(signal))]
        analysis_win = np.resize(analysis_win, frame_signal.shape)
        synthesis_win = np.resize(synthesis_win, frame_signal.shape)

        frame_spectrum = np.fft.fft(np.multiply(frame_signal, analysis_win))
        processed_frame_spectrum = process_func(i, fs, frame_spectrum)
        processed_frame = np.fft.ifft(np.multiply(processed_frame_spectrum, synthesis_win))
        out_signal[int(i*step_size):min(i*step_size + len(analysis_win), len(signal))] = out_signal[int(i*step_size):min(i*step_size + len(analysis_win), len(signal))] + processed_frame

    return out_signal


def formants_calculator(signal, window, step_size, lpc_order, fs):
    poles = np.zeros((lpc_order, signal.size))
    formants = []

    for it in range(0, int(math.ceil(signal.size / step_size))):
        frame_signal = signal[it*step_size:min(it*step_size + window.size, signal.size)]
        # import pdb; pdb.set_trace()

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
