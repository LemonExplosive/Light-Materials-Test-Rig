import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
from statistics import mean, stdev, sqrt

Gram_To_N = 0.00980665
bitToNewton = 9.831159958591358e-06

def ConfidenceInt(y,z):
    ave = mean(y)
    n = len(y)
    n = sqrt(n)
    st = stdev(y)
    CI = z*(st/n)
    return CI, ave



def dataExtract(filedir):
    print(filedir)
    data = pd.read_csv(filedir, delimiter=",")
    data_list = [list(row) for row in data.values]
    extracted = []
    for point in data_list:
        extracted.append(point[0])
    return extracted



def flatten(data):
    lowValues = []
    for i in range(1000):
        lowValues.append(data[i])
    
    highValues = []
    for i in range(1000,2000):
        highValues.append(data[i])
        
    Difference = []
    for i in range(1000):
        dif = highValues[i] - lowValues[i]
        newton = dif * bitToNewton
        Difference.append(newton)
    
    conf = ConfidenceInt(Difference, 1.96)
    
    return conf



def foldercomb(folders):
    
    data_sets = []
    for folder in folders:
        dir_list = os.listdir(folder)
        for file in dir_list:
            data_sets.append(dataExtract(f'{folder}\\{file}'))
        
    return data_sets



def dataExtractAndCompile(folders, CI=1.96):
    data = foldercomb(folders)
    conf = []
    averages = []
    for i in data:
        packet = flatten(i)
        conf.append(packet[0])
        averages.append(packet[1])
    return conf, averages
    


def errorPercent(data1, data2):
    error = []
    for i in range(len(data1)):
        errorval = abs(data1[i] - data2[i])
        
        errorval = 100 * (errorval / data2[i])
       
        error.append(errorval)
    conf = ConfidenceInt(error, 1.96)
    return conf, error


decades = ['Decade1','Decade2','Decade3']
Masses = [10,20,40,70,100,201,401,702,1003,1704,1905]

Forces = []
for i in Masses:
    Forces.append(i*Gram_To_N)
    
MassX = [1,2,3,4,5,6,7,8,9,10,11]
Mass_Error = 1
Force_Error = Mass_Error * Gram_To_N

data_sets = dataExtractAndCompile(decades)

err = errorPercent(data_sets[1], Forces)
print(err)







font_type = 'Arial'
mpl.rcParams['figure.dpi'] = 1000
scaler = 2
sx = 4*scaler
sy = 2*scaler
fig, ax = plt.subplots(figsize=(sx, sy))
plt.grid(True)
plt.grid(c='grey')
plt.grid(linewidth=0.4)
font = 10
titlefont = 15


ax.errorbar(MassX, Forces, linestyle='', marker='^', yerr=Force_Error, label='Applied Force', color='red')

ax.errorbar(MassX, data_sets[1], linestyle='', marker='.', yerr=data_sets[0], label='Measured Force')


plt.ylabel('Force(N)',fontsize=font,font=font_type)
plt.xlabel('Trial',fontsize=font,font=font_type)

ax.legend(loc='best', prop={'size': 10})
plt.suptitle('Calibration Graph',fontsize=titlefont,font=font_type)
plt.show()
