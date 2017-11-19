import numpy as np
import os
import scipy.io.wavfile as wav
from python_speech_features import mfcc, base

timit_phonemes = [
    'aa', 'ae', 'ah', 'ao', 'aw', 'ax', 'ax-h', 'axr', 'ay', 'b', 'bcl', 'ch', 'd', 'dcl', 'dh',
    'dx', 'eh', 'el', 'em', 'en', 'eng', 'epi', 'er', 'ey', 'f', 'g', 'gcl', 'h#', 'hh', 'hv', 'ih',
    'ix', 'iy', 'jh', 'k', 'kcl', 'l', 'm', 'n', 'ng', 'nx', 'ow', 'oy', 'p', 'pau', 'pcl', 'q', 'r',
    's', 'sh', 't', 'tcl', 'th', 'uh', 'uw', 'ux', 'v', 'w', 'y', 'z', 'zh']

phoneme_dict = {v: k for k, v in enumerate(timit_phonemes)}


def mfcc_wav(file):
    """ Funcion de Carlos Selmo, no lo usamos igual"""
    (rate,sig) = wav.read(file)
    mfcc_feat = mfcc(sig,rate,nfft=512,appendEnergy=True)
    #fbank_feat = logfbank(sig,rate,nfft=512)
    return mfcc_feat


def read_timit_phn(f):
    """ Reads TIMIT phn file.
        Structure of the file goes like: [start_sample end_sample phoneme]
        Return a tuple of 3 lists. Element i of the list corresponds to each phoneme """
    f = open(f, 'r')
    start_sample = []
    end_sample = []
    phn = []
    for line in f:
        word_split = str(line).split()
        assert len(word_split) == 3
        start_sample.append(int(word_split[0]))
        end_sample.append(int(word_split[1]))
        phn.append(phoneme_dict[word_split[2]])
    return start_sample, end_sample, phn


def create_annotations(center_of_win, start_sample, end_sample, phn):
    annotations = np.zeros(len(center_of_win))
    index = 0
    for i in range(len(annotations)):
        print(center_of_win[i], start_sample[index], end_sample[index], i)
        while index < len(end_sample):
            if start_sample[index] <= center_of_win[i] <= end_sample[index]:
                annotations[i] = phn[index]
                break
            else:
                index += 1
    return annotations


def get_data_of(path):
    window_size = 0.02  # length of window in seconds
    step_size = 0.01  # step of succesive windows in seconds
    numcep = 13  # number of cepstrum to return (paper uses 40, default is 13)
    nfft = 512  # FFT size

    (fs, x) = wav.read(path + 'RIFF.wav')

    mfcc_feat = mfcc(x, fs, winlen=window_size, winstep=step_size, numcep=numcep, nfft=nfft, appendEnergy=True)
    mfcc_delta = base.delta(mfcc_feat, 2)
    mfcc_delta_delta = base.delta(mfcc_delta, 2)
    all_data = np.hstack([mfcc_feat, mfcc_delta, mfcc_delta_delta])

    center_of_win = (np.arange(len(all_data)) + 1) * fs * step_size  # returns position of the center of the window

    start_sample, end_smple, phn = read_timit_phn(path + '.PHN')

    annotations = create_annotations(center_of_win, start_sample, end_smple, phn)

    return annotations


def parse_training_data():
    print('Processing train data... this could take a while')
    base_train_dir = '../data/TIMIT/TRAIN'
    DRS = [DR for DR in os.listdir(base_train_dir)]  # if os.path.isfile(f)]
    for DR in DRS:
        folders = [folder for folder in os.listdir(base_train_dir + '/' + DR)]
        for folder in folders:
            files = [f for f in os.listdir(base_train_dir + '/' + DR + '/' + folder)]
            for f in files:
                if f.endswith(".wav"):
                    base_name = f[:len(f)-8]
                    if not base_name.endswith('RIFF'):
                        print('Found file: ' + base_train_dir+'/'+DR+'/'+folder+'/'+base_name)
    print('Parsing successful')


if __name__ == '__main__':
    window_size = 0.02      # length of window in seconds
    step_size = 0.01        # step of succesive windows in seconds
    numcep = 13             # number of cepstrum to return (paper uses 40, default is 13)
    nfft = 512              # FFT size

    (fs, x) = wav.read('../data/TIMIT/TRAIN/DR1/FCJF0/SA1RIFF.WAV')
    mfcc_feat = mfcc(x, fs, winlen=window_size, winstep=step_size, numcep=numcep, nfft=nfft, appendEnergy=True)
    mfcc_delta = base.delta(mfcc_feat, 2)
    mfcc_delta_delta = base.delta(mfcc_delta, 2)
    all_data = np.hstack([mfcc_feat, mfcc_delta, mfcc_delta_delta])
    center_of_win = (np.arange(len(all_data)) + 1) * fs * 0.01       # returns position of the center of the window
    print(all_data.shape)
    start_sample, end_smple, phn = read_timit_phn(f='../data/TIMIT/TRAIN/DR1/FCJF0/SA1.PHN')
    for i in range(1, len(end_smple)):
        assert start_sample[i] == end_smple[i-1]

    annotations = create_annotations(center_of_win, start_sample, end_smple, phn)

    parse_training_data()

    import pdb; pdb.set_trace()
