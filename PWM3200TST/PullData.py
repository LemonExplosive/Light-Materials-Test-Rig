import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import scipy
from SlopeCleaner import Cleaner
#cc = 1.082
#cc is a constant that converts the distance that the TOF sensor returns into mm
cc = 1.0994297902935737#84.95 - 63.75
#cc = 1.0999483892512594#84.95 - 63.74
#cc = 1.0989111913358882#84.95 - 63.76
#cc = 1.1004669882089444#84.96 - 63.74
#cc = 1.0983925923782023
file = 'PullTest5.csv'
desired_slope = 30
data = pd.read_csv(file, delimiter=",")
data_list = [list(row) for row in data.values]


time = []
Force = []
Distance = []
Pulses = []

for row in data_list:
    time.append(row[2]/60000)

    Force.append(row[0])
    
    Distance.append(row[1]*cc)



pulses_per_mm = 400/8

polyDirty = np.polyfit(time, Distance, 1)
print(polyDirty)
Cleaned = Cleaner(time, Distance, polyDirty[0])

CleanTime = Cleaned[0]
CleanDist = Cleaned[1]

poly = np.polyfit(CleanTime, CleanDist, 1)
trendpoly = np.poly1d(poly)
compare = trendpoly([time[0],time[-1]])
DesTrend = np.poly1d([-desired_slope,poly[1]])

#scipy
scipoly = scipy.stats.linregress(CleanTime, CleanDist)
critical_t = scipy.stats.t.ppf(q=1-0.025,df=(len(time)-2))
CI = critical_t*scipoly[4]
#######

font_type = 'Arial'
mpl.rcParams['figure.dpi'] = 500
scaler = 5
sx = 4*scaler
sy = 2*scaler
fig, ax = plt.subplots(figsize=(sx, sy))
plt.grid(True)
plt.grid(c='grey')
plt.grid(linewidth=0.4)



ax.scatter(time, Distance, linestyle='', marker='.', label='Distance With Outliers', linewidths=0.5, color='darkblue')
ax.scatter(CleanTime, CleanDist, linestyle='', marker='.', label='Distance With Outliers Removed', linewidths=0.5, color='red')
ax.plot(time, trendpoly(time), linestyle='-', linewidth=5.0, label=f'Measured Trend: {-1*round(poly[0],2)} mm/min', color='black')
ax.plot(time, DesTrend(time), linestyle='--', linewidth=5.0, label=f'Desired Trend: {desired_slope} mm/min', color='yellowgreen')
#ax.plot(time, Pulses, linestyle='--', marker='o', label='Pulses')
#ax.plot(time, Force, linestyle='--', marker='o', label='Force(N)')

plt.ylabel('Distance(mm)',fontsize=25,font=font_type)
plt.xlabel('Time(min)',fontsize=25,font=font_type)
string = f'Error Compensation Value: {cc}\nSlope: {scipoly[0]} mm/min\nR Value: {scipoly[2]}\nCI(95%): {CI} mm/min\nNumber of Samples: {len(time)}\n\nInterval\n   Positive: {scipoly[0]+CI} mm/min\n   Negative: {scipoly[0]-CI} mm/min'
plt.figtext(0.12, -0.18, string, ha='left', fontsize=20, font=font_type)
ax.legend(loc='best', prop={'size': 20})
plt.suptitle('Calibration Graph(PWM)',fontsize=30,font=font_type)
plt.show()