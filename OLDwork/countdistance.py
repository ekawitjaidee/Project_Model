import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np

from sklearn.cluster import KMeans

datalist = [f for f in glob.glob("Dataset/*.csv")]
print('have stock = ',len(datalist))

for h in range(6):
  df = pd.read_csv(datalist[h])
  df['MACD-SL'] = df['MACD'] - df['SIGNAL LINE']
  df['DMI-SIGNAL'] = df['plusDI'] - df['minusDI']
  count = 0
  k  = []
  flag = True

  for i ,row in df.iterrows():
      if row['MACD-SL'] > 0 and flag == True:
          count = 0 
          flag = False
      elif row['MACD-SL']<0 and flag == False:
          flag = True
          count = 0
      k.append(count)
      count+=1
  df['count'] = k
  df.to_csv('scattershow/'+str(h)+'.csv',index = False)