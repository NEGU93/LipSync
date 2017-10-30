from cepstrum import real_cepstrum
import matplotlib.pyplot as plt
import data


def compute_real_cepstrum(signal):
    ceps = real_cepstrum(signal)

    fig = plt.figure()
    ax0 = fig.add_subplot(211)
    ax0.plot(t, signal)
    ax0.set_xlabel('time in seconds')
    ax0.set_xlim(0.0, 0.05)
    ax1 = fig.add_subplot(212)
    ax1.plot(t, ceps)
    ax1.set_xlabel('quefrency in seconds')
    ax1.set_xlim(0.005, 0.015)
    ax1.set_ylim(-5., +10.)
    plt.show()