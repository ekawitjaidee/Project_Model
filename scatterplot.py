import matplotlib.pyplot as plt
import glob

datalist = [f for f in glob.glob("Dataset/*.csv")]
print('have stock = ',len(datalist))

for i in range(5):
    