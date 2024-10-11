# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 15:36:39 2024

@author: johnl
"""
from statistics import mean, sqrt, stdev

def ConfidenceInt(y,z):
    ave = mean(y)
    n = len(y)
    n = sqrt(n)
    st = stdev(y)
    CI = z*(st/n)
    
    CI_pos = ave + CI
    CI_neg = ave - CI
    
    return CI, CI_neg, CI_pos, ave

lst = [(50.43185921670085-50)/50,
       (50.29202642885923-50)/50,
       (25.30842711519204-25)/25,
       (5.049612486852339-5)/5,
       (5.081914628656187-5)/5,
       (1.0036771846754022-1)]
conf = []
for i in ConfidenceInt(lst, 1.96):
    conf.append(100*i)
print(conf)
print(lst)