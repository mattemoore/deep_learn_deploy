# Basic CNN to classify SVHN dataset using Keras
import os
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
from keras.layers import MaxPooling2D, Dropout
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
    with open(train_file, 'w'):
        pass
    with open(test_file, 'w'):
        pass
    print('Downloading SVHN dataset...')
    urlretrieve(train_url, train_file)
    urlretrieve(test_url, test_file)
    print('Download complete.')
    train, test = loadmat(train_file), loadmat(test_file)
    return train, test


batch_size = 128
epochs = 5
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

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Conv2D(32, (3, 3),
          padding='valid',
          input_shape=input_shape,
          activation='relu'))
model.add(Conv2D(32, (3, 3),
          activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

start = datetime.now()
model.compile(optimizer=keras.optimizers.Adadelta(),
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
