# Basic CNN to classify SVHN dataset using Keras
import os
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
from keras.layers import MaxPooling2D, Dropout, BatchNormalization
from keras.layers.advanced_activations import LeakyReLU
from keras import backend as K
from scipy.io import loadmat
from datetime import datetime
from urllib.request import urlretrieve


def get_data():
    train_url = 'http://ufldl.stanford.edu/housenumbers/train_32x32.mat'
    test_url = 'http://ufldl.stanford.edu/housenumbers/test_32x32.mat'
    train_file = 'dataset/train_32x32.mat'
    test_file = 'dataset/test_32x32.mat'
    if not os.path.exists('dataset'):
        os.makedirs('dataset')
    print('Downloading SVHN dataset...')
    urlretrieve(train_url, train_file)
    urlretrieve(test_url, test_file)
    print('Download complete.')
    train, test = loadmat(train_file), loadmat(test_file)
    return train, test


num_classes = 10
img_rows, img_cols = 32, 32
num_colors = 3

train, test = get_data()
x_train = train['X']
y_train = train['y'].flatten() - 1
del train

x_test = test['X']
y_test = test['y'].flatten() - 1
del test

if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[3], num_colors, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[3], num_colors, img_rows, img_cols)
    input_shape = (num_colors, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[3], img_rows, img_cols, num_colors)
    x_test = x_test.reshape(x_test.shape[3], img_rows, img_cols, num_colors)
    input_shape = (img_rows, img_cols, num_colors)

y_train = y_train.astype('int32')
y_test = y_test.astype('int32')

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
normalizer = x_train.max().astype('float32')
x_train /= normalizer
x_test /= normalizer
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)
print('y_train shape:', y_train.shape)
print(y_train.shape[0], 'train samples')
print(y_test.shape[0], 'test samples')

print(x_train[0])
print(y_train[1])

# hyper-params
batch_size = 128
epochs = 500
filter_size = (3, 3)
alpha = 0.2
pool_size = (2, 2)
dropout = 0.5
lr = 0.001
padding = 'same'

model = Sequential()

model.add(Conv2D(32, filter_size,
          padding=padding,
          input_shape=input_shape,
          activation=None,
          use_bias=False))
model.add(LeakyReLU(alpha=alpha))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=pool_size))
model.add(Dropout(dropout))

model.add(Conv2D(64, filter_size,
          padding=padding,
          activation=None,
          use_bias=False))
model.add(LeakyReLU(alpha=alpha))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=pool_size))
model.add(Dropout(dropout))

model.add(Conv2D(128, filter_size,
          padding=padding,
          activation=None,
          use_bias=False))
model.add(LeakyReLU(alpha=alpha))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=pool_size))
model.add(Dropout(dropout))

model.add(Flatten())
model.add(Dense(500, activation=None, use_bias=False))
model.add(BatchNormalization())
model.add(LeakyReLU(alpha=alpha))
model.add(Dropout(dropout))
model.add(Dense(num_classes, activation='softmax'))

start = datetime.now()
model.compile(optimizer=keras.optimizers.RMSprop(lr=lr),
              loss=keras.losses.categorical_crossentropy,
              metrics=['accuracy'])
model.fit(x_train, y_train,
          epochs=epochs,
          batch_size=batch_size,
          verbose=2,
          shuffle=True,
          validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=1)
end = datetime.now()
print('Test loss:', score[0])
print('Test accuracy:', score[1])
print('Elapsed time:', end - start)

if not os.path.exists('output'):
    os.makedirs('output')
model_file = 'output/model.json'
weights_file = 'output/model.h5'
with open(model_file, 'w') as f:
    f.write(model.to_json())
model.save_weights(weights_file)
