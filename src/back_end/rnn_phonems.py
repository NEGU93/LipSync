import parser_timit as pt
import scipy.io.wavfile as wav
import data
from train_RNN import reshape_data
import numpy as np
from python_speech_features import mfcc, base
from keras.models import load_model


def rnn_phonemes():
    window_size = 0.02  # length of window in seconds
    step_size = 0.01  # step of succesive windows in seconds
    numcep = 13  # number of cepstrum to return (paper uses 40, default is 13)
    nfft = 512  # FFT size

    data_rnn = data.LipSyncData.get_instance()
    # x = data_rnn.audio
    # fs = data_rnn.fs

    (fs, x) = wav.read('../../data/TIMIT/TRAIN/DR1/FCJF0/SA1RIFF.WAV')

    mfcc_feat = mfcc(x, fs, winlen=window_size, winstep=step_size, numcep=numcep, nfft=nfft, appendEnergy=True)
    mfcc_delta = base.delta(mfcc_feat, 2)
    mfcc_delta_delta = base.delta(mfcc_delta, 2)
    all_data = np.hstack([mfcc_feat, mfcc_delta, mfcc_delta_delta])
    center_of_win = (np.arange(len(all_data)) + 1) * fs * 0.01  # returns position of the center of the window

    timesteps = 4

    data_reshaped = reshape_data(all_data, timesteps)

    model = load_model('../../data/saved_rnn/model.hdf5')

    classes = model.predict(data_reshaped, batch_size=100)

    result_phonemes = []
    first = True
    for i, win_class in enumerate(classes):
        if first:
            result_phonemes.append((int(i * step_size * fs), data.Phonemes(win_class.argmax() + 1)))
            first = False
        elif data.Phonemes(win_class.argmax()+1) is not result_phonemes[len(result_phonemes)-1][1]:
            result_phonemes.append((int(i*step_size*fs), data.Phonemes(win_class.argmax()+1)))

    # i = 1
    # while i < len(result_phonemes)-1:
    #     if (result_phonemes[i+1][0] - result_phonemes[i-1][0]) < 8*step_size*fs:
    #         if result_phonemes[i+1][1] == result_phonemes[i-1][1]:
    #             del result_phonemes[i]
    #         del result_phonemes[i]
    #     else:
    #         i = i + 1

    print(result_phonemes)
    import pdb; pdb.set_trace()


if __name__ == '__main__':
    rnn_phonemes()