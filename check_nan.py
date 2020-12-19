import pandas as pd

data = pd.read_csv('test1.csv')

data.loc[data['Signal'] == 'wait ot hold', 'Signal'] = 'wait or hold'
data.loc[data['Signal'] == 'buy', 'Signal'] = 0
data.loc[data['Signal'] == 'sell', 'Signal'] = 1 
data.loc[data['Signal'] == 'wait or hold', 'Signal'] = 2 

count = 0

for index, row in data.iterrows():
    if row['Signal'] != 0 and row['Signal'] != 1 and row['Signal'] != 2:
        count+=1
        print(index,row['Signal'])
print(count)