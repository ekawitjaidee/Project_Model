import matplotlib.pyplot as plt
import glob
import matplotlib.pyplot as plt
import pandas as pd
import glob
from Indicator import Indicator

from sklearn.cluster import KMeans
datalist = [f for f in glob.glob("Dataset/*.csv")]
print('have stock = ',len(datalist))
indicator = Indicator()
for i in range(5):
    df = pd.read_csv(datalist[i])
    df['MACD-SL'] = df['MACD'] - df['SIGNAL LINE']
    df['DMI-SIGNAL'] = df['plusDI'] - df['minusDI']
    df = indicator.ATR(df)
    # plt.scatter(df['MACD-SL'],df['DMI-SIGNAL'])
    df.loc[df['Signal'] == 'buy', 'Signal'] = 0
    df.loc[df['Signal'] == 'sell', 'Signal'] = 1 
    df.loc[df['Signal'] == 'wait or hold', 'Signal'] = 2 
    plt.scatter(df['MACD-SL'],df['ATR'],c=df['Signal'].values)
    plt.show()
