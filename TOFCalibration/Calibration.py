import pandas as pd
from statistics import mean, median, stdev, sqrt

def Split(lst):
    lst = sorted(lst)
    length = len(lst)
    chunk = length / 2
    
    first_half = []
    last_half = []
    
    for i in range(length):
        if i >= chunk:
            last_half.append(lst[i])
        else:
            first_half.append(lst[i])
    
    return first_half, last_half

def OutlierRemoval(x, y, Z=1.5):
    Q = Split(y)
    Q1 = Q[0]
    Q3 = Q[1]
    
    median_Q1 = median(Q1)
    median_Q3 = median(Q3)
    C = median_Q3 - median_Q1
    Low = median_Q1 - Z*C
    High = median_Q3 + Z*C
    
    new_y = []
    new_x = []
    
    for i in range(len(y)):
        Y = y[i]
        X = x[i]
        
        if Y <= Low or Y >= High:
            pass
        else:
            new_x.append(X)
            new_y.append(Y)
    
    return new_x, new_y

def ConfidenceInt(y,z):
    ave = mean(y)
    n = len(y)
    n = sqrt(n)
    st = stdev(y)
    CI = z*(st/n)
    
    CI_pos = ave + CI
    CI_neg = ave - CI
    
    return CI, CI_neg, CI_pos, ave

file = 'MountedCalLong.csv'
file2 = 'MountedCalShort.csv'

data = pd.read_csv(file, delimiter=",")
data_list = [list(row) for row in data.values]

data2 = pd.read_csv(file2, delimiter=",")
data2_list = [list(row) for row in data2.values]

time = []
Distance_Sample = []

for row in data_list:
    time.append(row[1])
    Distance_Sample.append(row[0])

time2 = []
Distance_Sample2 = []

for row in data2_list:
    time2.append(row[1])
    Distance_Sample2.append(row[0])
 
    
 

change = 84.95 - 63.75

filt = OutlierRemoval(time, Distance_Sample)

time_filt = filt[0]
Distance_Sample_filt = filt[1]
  
CI = ConfidenceInt(Distance_Sample_filt, 1.96)



filt2 = OutlierRemoval(time2, Distance_Sample2)

time_filt2 = filt2[0]
Distance_Sample_filt2 = filt2[1]

CI2 = ConfidenceInt(Distance_Sample_filt2, 1.96)

dist = CI[-1] - CI2[-1]
print(f'TOF reported change in distance: {dist} +/-{CI[0]} CI 95%\nChange in distance measured from calipers: {change} +/-~0.02mm')
print(f'\nTOF to mm multiplier: {change/dist}')