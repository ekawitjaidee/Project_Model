from keras.models import load_model,Sequential
from keras.layers import Input, Dense, LSTM
from keras.utils import to_categorical
from keras.callbacks import Callback, ModelCheckpoint


import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

from sklearn.metrics import confusion_matrix,accuracy_score

def signal_to_catagorical(data):
  data.loc[data['Signal'] == 'wait ot hold', 'Signal'] = 'wait or hold'
  data.loc[data['Signal'] == 'buy', 'Signal'] = 0
  data.loc[data['Signal'] == 'sell', 'Signal'] = 1 
  data.loc[data['Signal'] == 'wait or hold', 'Signal'] = 2 
  return data

def add_shift_day(data,day):
  r_list = []
  for i in range(day,len(data)):#Number mean day to shift
    r_list.append(data[i-day : i])
  return np.array(r_list)

datalist = [f for f in glob.glob("Dataset/*.csv")]
print('have stock = ',len(datalist))

#test
test_list = []
for test_name in range(75,76):
    df = pd.read_csv(datalist[test_name])
    test = df[['MACD-SL_n','DMI_n','Close_n','Signal','Close','Date']]
    # test = add_shift_day(test,30)
    test_list.append(test)

model = load_model('Model/Lstm_delta_macd_dmi/lstm_model5.h5')
# model = load_model('Model/Lstm_delta_macd_dmi/my_model_delta_6.h5')
for i in range(len(test_list)):
    p_test = test_list[i]
    p_test = signal_to_catagorical(p_test)
    x_test = p_test[['MACD-SL_n','DMI_n','Close_n']].values
    x_test = add_shift_day(x_test,30)
    y_test = p_test['Signal'].values
    y_test = y_test.tolist()
    del y_test[0:30]
    y_test = np.array(y_test)
    y_pred = model.predict(x_test)
    y_pred = np.argmax(y_pred,axis = -1)
    p_test = p_test.iloc[30:]

    cm = confusion_matrix(y_test, y_pred)
    ac = accuracy_score(y_test,y_pred)
    print("Confusion Matrix")
    print(cm)
    print("Accuracy")
    print(ac)


    p_test['pred'] = y_pred
    p_test['pred_b'] = np.where(p_test['pred'] == 0,p_test['Close'],np.nan)
    p_test['pred_s'] = np.where(p_test['pred'] == 1,p_test['Close'],np.nan)
    
    p_test = p_test.set_index(p_test['Date'])
    p_test.index = pd.to_datetime(p_test.index,format='%d/%m/%Y')
    plt.figure(figsize=(18,8))
    # plt.grid()
    plt.title('Predict Buy and Sold Signal')
    plt.plot(p_test['Close'][-300:])
    plt.plot(p_test['pred_b'][-300:],color='yellow')
    plt.plot(p_test['pred_s'][-300:],color='red')
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.show()
    print(p_test)