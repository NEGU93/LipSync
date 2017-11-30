from scipy import signal
import math
import wave
import data
import struct
from processing_functions import short_time_energy
from processing_functions import formants_calculator
from phonemes import *


def most_common(lst):
    return max(set(lst), key=lst.count)


def vocal_phonemes():
    # filename = '../sounds/vocales.wav'
    datos = data.LipSyncData.get_instance()
    # sound_frames, fs = wav_to_floats(filename)
    # sound_frames = np.asarray(sound_frames)
    L = round(20e-3*datos.fs)
    window = signal.hann(L)
    step_size = round(L/2)
    lpc_order = 16
    formants_freq = formants_calculator(datos.audio, window, step_size, lpc_order, datos.fs)
    formants = list(formants_freq)
    energy_time, energy_frames = short_time_energy(datos.audio, window, step_size)

    sound_frames_formants = [0] * len(datos.audio)
    for it in range(0, len(formants)):
        if energy_frames[it] < (max(energy_frames)*.1):
            formants[it] = 'silent'
            formants_freq[it] = 0
            sound_frames_formants[min(it*step_size, len(datos.audio)):min((it+1)*step_size, len(datos.audio))] = [data.Phonemes.rest] * \
                (min((it+1)*step_size, len(datos.audio)) - min(it*step_size, len(datos.audio)))
        else:
            formants[it] = best_phoneme(np.array([formants[it][0], formants[it][1]])).phoneme_name
            if formants[it] == '/a/':
                a = data.Phonemes.AI
            elif formants[it] == '/e/':
                a = data.Phonemes.E
            elif formants[it] == '/i/':
                a = data.Phonemes.AI
            elif formants[it] == '/o/':
                a = data.Phonemes.O
            elif formants[it] == '/u/':
                a = data.Phonemes.U
            else:
                a = data.Phonemes.etc
            sound_frames_formants[min(it*step_size, len(datos.audio)):min((it+1)*step_size, len(datos.audio))] = [a] * \
                (min((it+1)*step_size, len(datos.audio)) - min(it*step_size, len(datos.audio)))


    # formantss = formants_freq[300:-1]

    average_size = int(round(100e-3*datos.fs)) #length of a phoneme
    sound_frames_average = [0] * len(datos.audio)
    for it in range(0, int(math.ceil(len(sound_frames_formants) / average_size))):
        formant_average = sound_frames_formants[it * average_size:min((it+1) * average_size, len(sound_frames_formants))]
        average = most_common(formant_average)
        sound_frames_average[it * average_size:min((it + 1) * average_size, len(sound_frames_formants))] = \
            [average] * (min((it + 1) * average_size, len(sound_frames_formants)) - it * average_size)

    for it in range(0, len(sound_frames_average)):
        if it == 0:
            prev = sound_frames_average[it]
        else:
            if prev != sound_frames_average[it] and prev != sound_frames_average[min(it+1, len(sound_frames_average))] \
                    and prev != sound_frames_average[min(it+2, len(sound_frames_average))]:
            # if prev != sound_frames_formants[it]:
                prev = sound_frames_average[it]
                datos.append_dat(it, sound_frames_average[it])
