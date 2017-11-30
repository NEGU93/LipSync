from python_speech_features import mfcc
from python_speech_features import logfbank
from python_speech_features import base
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np
from sklearn import mixture
import data
import math
import itertools
from scipy import linalg
import matplotlib.pyplot as plt
import pickle


def mfcc_wav(file):
    (rate, signal) = wav.read(file)
    # signal = (signal[:, 0] + signal[:, 1]) / 2
    mfcc_feat = mfcc(signal, rate, nfft=512, appendEnergy=True)
    return mfcc_feat


def mfcc_signal(signal, fs):
    mfcc_feat = mfcc(signal, fs, nfft=512, appendEnergy=True)
    return mfcc_feat

# def signal_is_speaker(signal_file, speaker_model, world_model):
#     mfcc_feat = mfcc_wav(signal_file)
#     score_world = world_model.score(mfcc_feat)
#     score_speaker = speaker_model.score(mfcc_feat)
#     if score_speaker > score_world:
#         return True
#     else:
#         return False


def signal_is_speaker(signal, fs, speaker_model, world_model):
    mfcc_feat = mfcc_signal(signal, fs)
    score_world = world_model.score(mfcc_feat)
    score_speaker = speaker_model.score(mfcc_feat)
    if score_speaker > score_world:
        return True
    else:
        return False


def create_model(signal_file):
    mfcc_feat = mfcc_wav(signal_file)

    lowest_bic = np.infty
    bic = []
    n_components_range = range(1, 45)
    cv_types = ['spherical']
    for cv_type in cv_types:
        for n_components in n_components_range:
            gmm = mixture.GaussianMixture(n_components=n_components,
                                          covariance_type=cv_type)
            gmm.fit(mfcc_feat)
            bic.append(gmm.bic(mfcc_feat))
            if bic[-1] < lowest_bic:
                lowest_bic = bic[-1]
                best_gmm = gmm
    return best_gmm


# def speaker_recognition_men_woman():
#     men_model = create_model('../sounds/men.wav')
#     women_model = create_model('../sounds/women.wav')
#     print(signal_is_speaker('../sounds/test_women.wav', women_model, men_model))
#     print(signal_is_speaker('../sounds/test_men.wav', women_model, men_model))


def speaker_recognition_frame(signal, client1_model, client2_model, world_model, step_size, fs):
    # result = np.zeros(signal.size)
    result = np.array([])
    for i in range(0, int(math.ceil(signal.size / step_size))):
        frame_signal = signal[i*step_size:min(i*step_size + step_size, signal.size)]
        if frame_signal.size == 0:
            return result

        mfcc_feat = mfcc_signal(frame_signal, fs)
        score_client1 = client1_model.score(mfcc_feat)
        score_client2 = client2_model.score(mfcc_feat)
        score_world = world_model.score(mfcc_feat)

        max_score = max(score_client1, score_client2, score_world)

        if max_score == score_client1:
            frame_result = 1
        elif max_score == score_client2:
            frame_result = 2
        else:
            frame_result = 0

        # plt.plot(frame_signal)
        # plt.show()
        print(frame_result)

        frame_result_array = np.ones(frame_signal.size) * frame_result
        result = np.append(result, frame_result_array)

    return result


def speaker_recognition(client1_model, client2_model, world_model):

    datos = data.LipSyncData.get_instance()
    fs, signal = wav.read(datos.filename)
    # signal = (signal[:, 0] + signal[:, 1]) / 2

    step_size = round(700e-3 * fs)
    # step_size = signal.size

    data.speaker_recognized = speaker_recognition_frame(signal, client1_model, client2_model, world_model, step_size, fs)

    plt.plot(np.linspace(0.0, 1.0, num=datos.audio.size), datos.audio)
    plt.plot(np.linspace(0.0, 1.0, num=data.speaker_recognized.size), data.speaker_recognized)
    plt.show()
    plt.show()


def build_model():
    client2bis = create_model('../sounds/speakers/homero-old.wav')

    f = open('client2bis_model.pckl', 'wb')
    pickle.dump(client2bis, f)
    f.close()

# model1 = create_model('../sounds/speakers/burns.wav')
# model2 = create_model('../sounds/speakers/homero-old.wav')
# modelworld = create_model('../sounds/speakers/mundo.wav')
#     result = speaker_recognition_frame(signal, model1, model2, modelworld, step_size, fs)
#     print(signal_is_speaker(signal, fs, model1, world_model))
#     print(signal_is_speaker(signal, fs, model2, world_model))