# coding=utf-8
from __future__ import print_function

import os
import pickle as pk

import keras
import numpy as np
from keras import backend as K
from keras.datasets import mnist
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Activation, Dense, Dropout, Flatten
from keras.models import Sequential
from keras.utils import np_utils
from PIL import Image

K.set_image_dim_ordering('th')


def img2matrix(img_name):
    ''' convert image to matrix '''
    img = Image.open(img_name)  # read image
    # width, height = img.size
    img = img.convert('L')  # convert to grey-scale graph
    data = img.getdata()
    # convert image to ndarray and normalization
    data = np.matrix(data, dtype='float') / 255.0
    # new_data = np.reshape(data, (height, width))  # create height*width matrix
    # return new_data
    return data


def get_all_img(file_dir):
    ''' get all images in folder '''
    imgs = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            imgs.append(root + '\\' + file)
    return imgs


def preprocessing():
    ''' data preprocessing '''
    all_img = get_all_img('traindata')  # get image file
    face_label = np.empty(60, dtype=int)  # create labels
    face_data = np.empty((60, 64*64))
    for i in range(60):
        face_label[i] = i / 10
        face_data[i] = img2matrix(all_img[i])  # get image data

    # pickling file
    f = open('train_faces.pkl', 'wb')
    pk.dump((face_data, face_label), f)
    f.close()


def reshape_img():
    imgs = get_all_img('traindata')
    for img_name in imgs:
        img = Image.open(img_name)
        img.resize((64, 64), Image.ANTIALIAS).save(img_name)


class ClassificationModel:
    def __init__(self, batch_size=10, nb_classes=6, nb_epoch=16, nb_filters=32, nb_pool=2, nb_conv=3):
        self.batch_size = batch_size
        self.nb_classes = nb_classes  # total number of classes
        self.nb_epoch = nb_epoch

        self.nb_filters = nb_filters  # number of convolutional filter
        self.nb_pool = nb_pool  # size of pooling area for max pooling
        self.nb_conv = nb_conv  # convolution kernal size

    def get_data(self):
        fname = 'train_faces.pkl'
        (X_train, Y_train, X_valid, Y_valid, X_test, Y_test) = split_data(fname)
        X_train = X_train.reshape(X_train.shape[0], 1, 64, 64)
        X_test = X_test.reshape(X_test.shape[0], 1, 64, 64)
        X_valid = X_test.reshape(X_valid.shape[0], 1, 64, 64)
        Y_train = np_utils.to_categorical(Y_train, self.nb_classes)
        Y_test = np_utils.to_categorical(Y_test, self.nb_classes)
        Y_valid = np_utils.to_categorical(Y_valid, self.nb_classes)
        print('X_train shape:', X_train.shape)
        print(X_train.shape[0], 'train samples')
        print(X_test.shape[0], 'test samples')
        data = {
            'X_train': X_train,
            'Y_train': Y_train,
            'X_valid': X_valid,
            'Y_valid': Y_valid,
            'X_test': X_test,
            'Y_test': Y_test
        }
        return data
    
    def generate_model(self):
        data = self.get_data()
        X_train = data.get('X_train')
        Y_train = data.get('Y_train')
        X_valid = data.get('X_valid')
        Y_valid = data.get('Y_valid')
        model = Sequential()
        model.add(Conv2D(self.nb_filters, self.nb_conv, self.nb_conv,
                        border_mode='valid',
                        # use rectifier linear units: max(0.0, x)
                        activation='relu',
                        input_shape=(1, 64, 64)))
        # second convolution layer with 6 filters of size 3*3
        model.add(Conv2D(self.nb_filters, self.nb_conv, self.nb_conv))
        model.add(Activation('relu'))
        # max pooling layer, pool size is 2*2
        model.add(MaxPooling2D(pool_size=(self.nb_pool, self.nb_pool)))
        # drop out of max-pooling layer, drop out rate is 0.25
        model.add(Dropout(0.25))
        # flatten inputs from 2d to 1d
        model.add(Flatten())
        # add fully connected layer with 128 hidden units
        model.add(Dense(128))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        # output layer with softmax
        model.add(Dense(self.nb_classes))
        model.add(Activation('softmax'))
        # use cross-entropy cost and adadelta to optimize paras
        # model.compile(loss='categorical_crossentropy', optimizer='adadelta')
        model.compile(loss=keras.losses.categorical_crossentropy,
                    optimizer=keras.optimizers.Adadelta(),
                    metrics=['accuracy'])
        # train model with bath_size=10, epoch=12
        # set verbose=1 to show train info
        model.fit(X_train, Y_train,
                batch_size=self.batch_size,
                epochs=self.nb_epoch,
                verbose=1,
                validation_data=(X_valid, Y_valid))
        return model
    
    def cal_score(self):
        model = self.generate_model()
        data = self.get_data()
        X_test = data.get('X_test')
        Y_test = data.get('Y_test')
        score = model.evaluate(X_test, Y_test, verbose=0)
        print('Test score:', score[0])
        print('Test accuracy:', score[1])
    
    def predict(self):
        model = self.generate_model()
        X_test = self.get_data().get('X_test')
        predictions = model.predict(X_test)
        # round predictions
        rounded = [np.around(x) for x in predictions]
        print(rounded)


def split_data(fname):
    ''' split data into train, valid and test 
        train: 48
        valid: 6
        test: 6
    '''
    f = open(fname, 'rb')
    face_data, face_label = pk.load(f)
    X_train = np.empty((48, 64*64))
    Y_train = np.empty(48, dtype=int)
    X_valid = np.empty((6, 64*64))
    Y_valid = np.empty(6, dtype=int)
    X_test = np.empty((6, 64*64))
    Y_test = np.empty(6, dtype=int)
    for i in range(6):
        X_train[i*8:(i+1)*8, :] = face_data[i*10:i*10+8, :]
        Y_train[i*8:(i+1)*8] = face_label[i*10:i*10+8]
        X_valid[i] = face_data[i*10+8, :]
        Y_valid[i] = face_label[i*10+8]
        X_test[i] = face_data[i*10+9, :]
        Y_test[i] = face_label[i*10+9]
    return (X_train, Y_train, X_valid, Y_valid, X_test, Y_test)


if __name__ == '__main__':
    # reshape_img()
    classify = ClassificationModel()
    classify.predict()