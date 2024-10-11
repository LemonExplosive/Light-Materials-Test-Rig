from OutlierRemoval import OutlierRemoval
import pandas as pd
from statistics import mean, stdev, sqrt
Gram_To_N = 0.00980665
loadgram = 1003
file = 'PullTest8.csv'

data = pd.read_csv(file, delimiter=",")
data_list = [list(row) for row in data.values]

Force = []

for row in data_list:
    Force.append(int(row[0]))
    
rest = []    

for i in range(1000):
    rest.append(Force[i])

load = []

for i in range(1000,2000):
    load.append(Force[i])

def ConfidenceInt(y,z):
    ave = mean(y)
    n = len(y)
    n = sqrt(n)
    st = stdev(y)
    CI = z*(st/n)
    
    CI_pos = ave + CI
    CI_neg = ave - CI
    
    return CI, CI_neg, CI_pos, ave

restClean = OutlierRemoval(rest)
loadClean = OutlierRemoval(load)

restStats = ConfidenceInt(restClean, 1.96)
loadStats = ConfidenceInt(loadClean, 1.96)



print(f'rest\nCI:{restStats[0]}\nAverage:{restStats[-1]}\n')
print(f'load\nCI:{loadStats[0]}\nAverage:{loadStats[-1]}\n')
compare = loadStats[-1] - restStats[-1]
bitToNewton = loadgram * Gram_To_N / compare
print(f'RawDataToNewton: {bitToNewton}\n')
#print(bitToNewton*compare)

# for generating average absolute error
Error = []
for i in restClean:
    abserror = abs(restStats[-1] - i) * bitToNewton
    Error.append(abserror)
    
# ErrorStats = ConfidenceInt(Error, 1.96)
# print(ErrorStats)

LoadError = []
for i in loadClean:
    abserror = abs(loadStats[-1] - i) * bitToNewton
    LoadError.append(abserror)
    Error.append(abserror)
    
LoadError = ConfidenceInt(LoadError, 1.96)
ErrorStats = ConfidenceInt(Error, 1.96)

print(f'ASTM Minimum Weight: {400 * ErrorStats[-1]} N\nAverage Error: {ErrorStats[-1]} N')
print(f'\nASTM Minimum Weight: {400 * ErrorStats[-1] / Gram_To_N} g\nAverage Error: {ErrorStats[-1] / Gram_To_N} g')