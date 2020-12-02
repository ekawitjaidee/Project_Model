from keras.models import Sequential
from keras.layers import Input, Dense
from keras.utils import to_categorical
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
from keras.models import load_model


class Model():
  def __init__(self,input_node):
    self.input_node = input_node
    self.initial_model()

  def initial_model(self):
    model = Sequential()
    model.add(Dense(10, input_dim=5, activation='tanh'))
    model.add(Dense(10, activation='tanh'))
    model.add(Dense(3, activation='softmax'))

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['acc'])
    self.model = model

  def summary(self):
    self.model.summary()

  def savemodel(self,modelname):
    self.model.save(modelname)

  def loadmodel(self,modelname):
    self.model = load_model(modelname)

  def trainmodel(self,x_train,y_train,ep,batch):
    self.model.fit(x_train, y_train, epoch=ep, batch_size = batch)

  def pred(self,x_test,y_test):
    self.predict = self.model.predict(x_test)
    self.predict = np.argmax(self.predict,axis = -1)
    print("Confusion_Matrix")
    print(confusion_matrix(y_test, self.predict))

  def get_input(self,data):
    self.inputset = data[['MACD','SIGNAL LINE','+DI','-DI',
                'adx','storsi','%K','%D',
                'aroon_up','aroon_down','ATR','CCI',
                'OBV','AO']]
    self.inputset  = self.inputset.to_numpy()
    return self.inputset
