import numpy as np
from parser_timit import timit_phonemes
from data import Phonemes

import tensorflow as tf
from tensorflow.python.client import device_lib

from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.optimizers import SGD, Adam
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau

checkpoint = ModelCheckpoint(filepath='../data/saved_rnn/model_{epoch:02d}_{val_loss:.2f}.hdf5')
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.001)


def phn_reduce(label):
    nout = np.zeros(len(Phonemes))
    item_index = np.where(label == 1.)[0][0]        # get the index of the place where I have a 1.
    phn = timit_phonemes[item_index]
    # case rest
    if ('epi' == phn) or ('h#' == phn):
        nout[9] = 1
    # Case AI
    elif ('a' in phn) or ('i' in phn):
        nout[0] = 1
    # Case E
    elif 'e' in phn:
        nout[1] = 1
    # Case U
    elif 'u' in phn:
        nout[2] = 1
    # Case O
    elif 'o' in phn:
        nout[3] = 1
    # Case FV
    elif ('f' in phn) or ('v' in phn):
        nout[5] = 1
    # Case MBP
    elif ('m' in phn) or ('b' in phn) or ('p' in phn):
        nout[6] = 1
    # Case L
    elif 'l' in phn:
        nout[7] = 1
    # Case WQ
    elif ('w' in phn) or ('q' in phn):
        nout[8] = 1
    # Case etc
    else:
        nout[4] = 1
    return nout


def reshape_data(features, timesteps):
    [N, M] = np.shape(features)
    out = np.zeros([N-timesteps,timesteps,M])
    for i in range(N-timesteps):
        for j in range(timesteps):
            out[i, j, :] = features[i+j, :]
    return out


def reduce_phn_data(labels):
    out = np.zeros([len(labels), len(Phonemes)])
    for i, l in enumerate(labels):
        out[i] = phn_reduce(l)
    return out


if __name__ == '__main__':
    # Prepare data
    print('Loading data')
    # Uncomment following block of code to parse to reduced set
    """ 
    label_training = np.load('../data/labels_training.npy')
    label_train_reduced = reduce_phn_data(label_training)
    np.save('../data/label_train_reduced.npy', label_train_reduced)

    label_test = np.load('../data/labels_test.npy')
    label_test_reduced = reduce_phn_data(label_test)
    np.save('../data/label_test_reduced.npy', label_test_reduced)"""
    features_train = np.load('../data/features_train_reshaped.npy')
    features_test = np.load('../data/features_test_reshaped.npy')
    label_test = np.load('../data/label_test_reshaped.npy')
    label_train = np.load('../data/label_train_reshaped.npy')

    timesteps = 4
    # features_train = reshape_data(features_train, timesteps)
    # features_test = reshape_data(features_test, timesteps)
    # label_train_reduced = label_train_reduced[0:len(label_train_reduced) - timesteps]
    # label_test_reduced = label_test_reduced[0:len(label_test_reduced) - timesteps]
    #
    # np.save('../data/features_train_reshaped.npy', features_train)
    # np.save('../data/features_test_reshaped.npy', features_test)
    # np.save('../data/label_test_reshaped.npy', label_test_reduced)
    # np.save('../data/label_train_reshaped.npy', label_train_reduced)

    # Net constant
    print('Creating Net')
    data_dim = features_test.shape[2]
    out_dim = label_test.shape[1]
    hidden_levels = 1
    lstm_cells = 250
    sgd = SGD(lr=0.0001, momentum=0.9, nesterov=False)  # Use stochastic gradient descent
    adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)

    # Initializing model
    # print(device_lib.list_local_devices())    # Check GPU use
    model = Sequential()
    model.add(LSTM(lstm_cells, return_sequences=True, input_shape=(timesteps, data_dim)))
    model.add(LSTM(lstm_cells, return_sequences=True))
    model.add(LSTM(lstm_cells))
    model.add(Dense(out_dim, activation='softmax'))
    # model.summary()
    model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])   # TODO: use CTC loss function

    # Train
    print('Training Net')
    model.fit(features_train, label_train, batch_size=100, epochs=1, callbacks=[checkpoint, reduce_lr],
              validation_data=(features_test, label_test))

    model.save('../data/saved_rnn/model_adam.hdf5')

    import pdb; pdb.set_trace()
