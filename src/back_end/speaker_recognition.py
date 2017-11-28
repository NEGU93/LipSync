from python_speech_features import mfcc
from python_speech_features import logfbank
from python_speech_features import base
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np
from sklearn import mixture
import itertools
from scipy import linalg
import matplotlib as mpl


def mfcc_wav(file):
    (rate, sig) = wav.read(file)
    mfcc_feat = mfcc(sig, rate, nfft=512, appendEnergy=True)
    # fbank_feat = logfbank(sig,rate,nfft=512)
    return mfcc_feat


def signal_is_speaker(signal_file, speaker_model, world_model):
    mfcc_feat = mfcc_wav(signal_file)
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
    cv_types = ['spherical']  # , 'tied', 'diag', 'full']
    for cv_type in cv_types:
        for n_components in n_components_range:
            # Fit a Gaussian mixture with EM
            gmm = mixture.GaussianMixture(n_components=n_components,
                                          covariance_type=cv_type)
            gmm.fit(mfcc_feat)
            bic.append(gmm.bic(mfcc_feat))
            if bic[-1] < lowest_bic:
                lowest_bic = bic[-1]
                best_gmm = gmm
    return best_gmm


def speaker_recognition():
    men_model = create_model('../sounds/men.wav')
    women_model = create_model('../sounds/women.wav')
    print(signal_is_speaker('../sounds/test_women.wav', women_model, men_model))
    print(signal_is_speaker('../sounds/test_men.wav', women_model, men_model))
