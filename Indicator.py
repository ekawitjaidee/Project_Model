import pandas as pd
import numpy as np

#Technical-analysis
from ta.trend import ADXIndicator
from ta.trend import AroonIndicator
from ta.trend import CCIIndicator

from ta.momentum import StochRSIIndicator
from ta.momentum import AwesomeOscillatorIndicator

from ta.volume import OnBalanceVolumeIndicator


'''
สร้างอินดิเคเตอร์
trend แนวโน้มราคา
Momentum แรงเหวี่ยงของราคา
Votatility ความผันผวนของราคา


'''

class Indicator():

  def MACD(self,df):#trend
    df_MACD = df.copy()
    df_MACD['EWMA-5'] = df_MACD['Close'].ewm(span=5).mean()
    df_MACD['EWMA-12'] = df_MACD['Close'].ewm(span=12).mean()
    df_MACD['EWMA-26'] = df_MACD['Close'].ewm(span=26).mean()
    df['MACD'] = df_MACD['EWMA-12'] - df_MACD['EWMA-26']
    df['SIGNAL LINE'] = df['MACD'].ewm(span=9).mean() 

    # df['MACD'] = np.where((df_MACD['MACD']>df_MACD['SIGNAL LINE'])&(df_MACD['MACD'].shift()<df_MACD['SIGNAL LINE'].shift()),'buy',
    #                           (np.where((df_MACD['MACD'] < df_MACD['SIGNAL LINE'])  & (df_MACD['MACD'].shift()>df_MACD['SIGNAL LINE'].shift()),'sell','wait or hold')))

    return df

  def DMI(self,df):#trend
    df_DMI = df.copy()
    adxi = ADXIndicator(df['High'],df['Low'],df['Close'],14,False)
    df['+DI'] = adxi.adx_pos()
    df['-DI'] = adxi.adx_neg()
    df['adx'] = adxi.adx()

    # df['DMI'] = np.where((df_DMI['+DI']>df_DMI['-DI'])&(df_DMI['+DI'].shift()<df_DMI['-DI'].shift()),'buy',
    #                           (np.where((df_DMI['+DI'] < df_DMI['-DI'])  & (df_DMI['+DI'].shift()>df_DMI['-DI'].shift()),'sell','wait or hold')))
    
    return df
  
  def STOCHRSI(self,df):#momentum
    df_STRSI = df.copy()
    strsi = StochRSIIndicator(df['Close'],n=14,d1=3,d2=3)
    df['storsi'] = strsi.stochrsi()
    df['%K'] = strsi.stochrsi_k()
    df['%D'] = df['%K'].ewm(span=3).mean()

    # df['STOCHRSI']  = np.where((df_STRSI['%K']>df_STRSI['%D'])&(df_STRSI['%K'].shift()<df_STRSI['%D'].shift())&(df_STRSI['%K']<20),'buy',
    #                             (np.where((df_STRSI['%K'] < df_STRSI['%D']) & (df_STRSI['%K'].shift()>df_STRSI['%D'].shift()) & (df_STRSI['%K']>80),'sell','wait or hold')))

    return df

  def AROON(self,df):#trend
    df_AROON = df.copy()
    aroon = AroonIndicator(df['Close'])
    df['aroon_up'] = aroon.aroon_up()
    df['aroon_down'] = aroon.aroon_down()

    return df

  def ATR(self,df):#Volatility
    df_ATR = df.copy()
    df_ATR['H(t) - L(t)'] = df['High'] - df['Low']
    df_ATR['H(t) - C(Y)'] = df['High'] - df['Close'].shift(1)
    df_ATR['L(t) - C(Y)'] = df['Low'] - df['Close'].shift(1)
    selected_columns = df_ATR[['H(t) - L(t)','H(t) - C(Y)','L(t) - C(Y)']]
    df['ATR'] = selected_columns.max(axis = 1)

    return df
  
  def CCI(self,df):#trend
    df_CCI = df.copy()
    cci = CCIIndicator(df['High'],df['Low'],df['Close'])
    df['CCI'] = cci.cci()
    return df

  def OBV(self,df):
    df_OBV = df.copy()
    obv = OnBalanceVolumeIndicator(df['Close'],df['Volume'])
    df['OBV'] = obv.on_balance_volume()
    return df

  def AO(self,df):
    df_AO = df.copy()
    AO = AwesomeOscillatorIndicator(df['High'],df['Low'])
    df['AO'] = AO.ao()
    return df