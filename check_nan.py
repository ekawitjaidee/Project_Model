import pandas as pd
import glob


def Check_nan(fname):
    data = pd.read_csv(fname)

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


def Check_nan_eachfile(fname,s):
    df = pd.read_csv(fname)
    for index, row in df.iterrows():
        if row['Signal'] != 'buy' and row['Signal'] != 'sell' and row['Signal'] != 'wait or hold':
            print(index ,fname)
            s.append(fname)

        
datalist = [f for f in glob.glob("Dataset/*.csv")]
s = []
for stname in datalist:
    try:
        Check_nan_eachfile(stname,s)
        print('pass',stname)
    except:
        print('Fail',stname)
print('---------------------done-----------------')
print(s)