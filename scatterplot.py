import glob
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from Indicator import Indicator
from mpl_toolkits.mplot3d import Axes3D
from ta.trend import ADXIndicator

from sklearn.cluster import KMeans

def norm(df,col_name):# this will get columnname + _n
    #Normalize data each colunm in to range -1 to 1
    df[col_name+'_n'] = 2*(df[col_name]-df[col_name].min())/(df[col_name].max()-df[col_name].min())-1    
    return df

def MACD(df,n1,n2,n3):#trend 

    df_MACD = df.copy()
    df_MACD['EWMA-12'] = df_MACD['Close'].ewm(span=n1).mean()
    df_MACD['EWMA-26'] = df_MACD['Close'].ewm(span=n2).mean()
    df['MACD'] = df_MACD['EWMA-12'] - df_MACD['EWMA-26']
    df['SIGNAL LINE'] = df['MACD'].ewm(span=n3).mean() 

    return df

def DMI(df,n1):#trend
    df_DMI = df.copy()
    adxi = ADXIndicator(df['High'],df['Low'],df['Close'],n1,False)
    df['plusDI'] = adxi.adx_pos()
    df['minusDI'] = adxi.adx_neg()
    df['adx'] = adxi.adx()
    return df

def check_trend(df):
    df.loc[(df['Close'] > df['MA']) &
    ((df['Close'] > df['Close'].shift(1)) | (df['MA'] > df['MA'].shift(1))) &
    ((df['Close'] > df['Close'].shift(2)) | (df['MA'] > df['MA'].shift(2))) &
    ((df['Close'] > df['Close'].shift(3)) | (df['MA'] > df['MA'].shift(3))) &
    ((df['Close'] > df['Close'].shift(4)) | (df['MA'] > df['MA'].shift(4))) &
    ((df['Close'] > df['Close'].shift(5)) | (df['MA'] > df['MA'].shift(5))) , 'Trend'] = 'Up'

    df.loc[(df['Close'] < df['MA']) &
    ((df['Close'] < df['Close'].shift(1)) | (df['MA'] < df['MA'].shift(1))) &
    ((df['Close'] < df['Close'].shift(2)) | (df['MA'] < df['MA'].shift(2))) &
    ((df['Close'] < df['Close'].shift(3)) | (df['MA'] < df['MA'].shift(3))) &
    ((df['Close'] < df['Close'].shift(4)) | (df['MA'] < df['MA'].shift(4))) &
    ((df['Close'] < df['Close'].shift(5)) | (df['MA'] < df['MA'].shift(5))) , 'Trend'] = 'Down'
    
    df.loc[df['Trend'].isnull(), 'Ntrend'] = df['Trend'].shift(1)
    df.loc[df['Trend'].isnull() & df['Trend'].shift(1).isnull(),'Ntrend'] = df['Trend'].shift(2)
    df.loc[df['Trend'].isnull() & df['Trend'].shift(1).isnull() & df['Trend'].shift(2).isnull(),'Ntrend'] = df['Trend'].shift(3)
    df.loc[df['Trend'].isnull() & df['Trend'].shift(1).isnull() & df['Trend'].shift(2).isnull() & 
    df['Trend'].shift(3).isnull(),'Ntrend'] = df['Trend'].shift(4)
    df.loc[df['Trend'].isnull() & df['Trend'].shift(1).isnull() & df['Trend'].shift(2).isnull() & 
    df['Trend'].shift(3).isnull() & df['Trend'].shift(4).isnull(),'Ntrend'] = df['Trend'].shift(5)
    df.loc[df['Trend'].isnull() & df['Trend'].shift(1).isnull() & df['Trend'].shift(2).isnull() & 
    df['Trend'].shift(3).isnull() & df['Trend'].shift(4).isnull() & df['Trend'].shift(5).isnull(),'Ntrend'] = df['Trend'].shift(6)
    
    df['S1'] = df['Close'].shift(-1)
    df['S2'] = df['Close'].shift(-2)
    df.loc[df['S1'].isnull(),'S1'] = 0
    df.loc[df['S2'].isnull(),'S2'] = 0

   
    #Trading Signal (0,1)
    df.loc[(df['Trend'] == 'Up') | (df['Ntrend'] == 'Up'), 'Trading Signal'] = ((abs(df['Close'] - df[['Close','S1','S2']].min(axis = 1)) / 
    abs(df[['Close','S1','S2']].max(axis = 1) - df[['Close','S1','S2']].min(axis = 1)))*0.5) + 0.5
    df.loc[(df['Trend'] == 'Down') | (df['Ntrend'] == 'Down'), 'Trading Signal'] = ((abs(df['Close'] - df[['Close','S1','S2']].min(axis = 1)) / 
    abs(df[['Close','S1','S2']].max(axis = 1) - df[['Close','S1','S2']].min(axis = 1)))*0.5)
   
    df.loc[df['Trend'].isnull(),'Trend'] =df['Ntrend']
    
    df = df.drop(['Ntrend','S1','S2'],axis=1)
        
    return df

datalist = [f for f in glob.glob("Dataset2/*.csv")]
print('have stock = ',len(datalist))
indicator = Indicator()
for i in range(30,35):
    df = pd.read_csv(datalist[i])
    df = MACD(df,24,36,24)#default 12,26,9
    df = DMI(df,60)#default 14
    df = indicator.MA(df,15)
    df = check_trend(df)
    df['MACD-SL'] = df['MACD'] - df['SIGNAL LINE']
    df['DMI'] = df['plusDI'] - df['minusDI']
    # df = norm(df,'Close')
    # df = indicator.ATR(df)

    df.loc[df['Signal'] == 'buy', 'Signal'] = 0
    df.loc[df['Signal'] == 'sell', 'Signal'] = 1 
    df.loc[df['Signal'] == 'wait or hold', 'Signal'] = 2 

    df.loc[df['Trend'] == 'Down', 'Trend'] = 0
    df.loc[df['Trend'] == 'Up', 'Trend'] = 1 
    
    df['up'] = np.where(df['Trend']==1,df['Close'],np.nan)
    df['down'] = np.where(df['Trend']==0,df['Close'],np.nan)

    # plt.scatter(df['MACD-SL'],df['DMI'],c=df['Signal'].values)
    # plt.plot(df['Close'])
    plt.plot(df['plusDI'])
    plt.plot(df['minusDI'])
    # fig = plt.figure()
    # ax = Axes3D(fig)
    # ax.scatter(df['MACD-SL'],df['DMI'],df['Close'],c=df['Trend'].values)
    plt.show()
