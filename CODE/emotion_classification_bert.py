# -*- coding: utf-8 -*-
"""Emotion classification_BERT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IBqpvMzQoL5C-Gz9OhflbkGPRVasG-3J
"""

import os
import zipfile

from google.colab import drive
drive.mount('/content/gdrive')



df='/content/data.zip'

df

df1=zipfile.ZipFile(df,'r')

df1.extractall('/content/data')

df1.close()

os.listdir('/content/data/data/')

!pip install ktrain

import pandas as pd
import numpy as np

import ktrain
from ktrain import text

data_train = pd.read_csv('/content/data/data/data_train.csv', encoding='utf-8')
data_test = pd.read_csv('/content/data/data/data_test.csv', encoding='utf-8')

X_train = data_train.Text.tolist()
X_test = data_test.Text.tolist()

y_train = data_train.Emotion.tolist()
y_test = data_test.Emotion.tolist()

data = data_train.append(data_test, ignore_index=True)

class_names = ['joy', 'sadness', 'fear', 'anger', 'neutral']

print('size of training set: %s' % (len(data_train['Text'])))
print('size of validation set: %s' % (len(data_test['Text'])))
print(data.Emotion.value_counts())

data.head(10)

encoding = {
    'joy': 0,
    'sadness': 1,
    'fear': 2,
    'anger': 3,
    'neutral': 4
}

# Integer values for each class
y_train = [encoding[x] for x in y_train]
y_test = [encoding[x] for x in y_test]

(x_train,  y_train), (x_test, y_test), preproc = text.texts_from_array(x_train=X_train, y_train=y_train,
                                                                       x_test=X_test, y_test=y_test,
                                                                       class_names=class_names,
                                                                       preprocess_mode='bert',
                                                                       maxlen=350, 
                                                                       max_features=35000)

model = text.text_classifier('bert', train_data=(x_train, y_train), preproc=preproc)

learner = ktrain.get_learner(model, train_data=(x_train, y_train), 
                             val_data=(x_test, y_test),
                             batch_size=6)

learner.fit_onecycle(2e-5, 3)

learner.validate(val_data=(x_test, y_test), class_names=class_names)

predictor = ktrain.get_predictor(learner.model, preproc)
predictor.get_classes()

import time 

message = "Hello ?"

start_time = time.time() 
prediction = predictor.predict(message)

print('predicted: {} ({:.2f})'.format(prediction, (time.time() - start_time)))

predictor.save("models/bert_model")

import matplotlib.pyplot as plt

plt.plot(learner.history.history['accuracy'],'r')
plt.plot(learner.history.history['val_accuracy'],'b')
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.savefig(r"\bert_acc.png")
plt.show()

plt.plot(learner.history.history['loss'],'r')
plt.plot(learner.history.history['val_loss'],'b')
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.savefig(r"\bert_loss.png")
plt.show()

