import numpy as np

from keras.models import load_model
from keras.callbacks import ModelCheckpoint

checkpoint = [ModelCheckpoint(filepath='model_{epoch:02d}_{val_loss:.2f}.hdf5')]


def load_and_train(epoch=1):
    features_train = np.load('../../data/features_train_reshaped.npy')
    features_test = np.load('../../data/features_test_reshaped.npy')
    label_test = np.load('../../data/label_test_reshaped.npy')
    label_train = np.load('../../data/label_train_reshaped.npy')

    model = load_model('../../data/saved_rnn/model_00_1.30.hdf5')
    model.summary()

    model.fit(features_train, label_train, batch_size=100, epochs=1, callbacks=checkpoint,
              validation_data=(features_test, label_test))


if __name__ == '__main__':
    load_and_train()

    import pdb; pdb.set_trace()