from statistics import median

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

def Flatten(x, y, slope):
    FlatY = []
    
    for i in range(len(x)):
        point= y[i] - slope * x[i] 
        FlatY.append(point)
        
    return FlatY

def Inflate(x, y, slope):
    CleanedY = []
    
    for i in range(len(x)):
        point= y[i] + slope * x[i] 
        CleanedY.append(point)
        
    return CleanedY
    
def Cleaner(x, y, slope):
    FlatY = Flatten(x, y, slope)
    CleanSet = OutlierRemoval(x, FlatY)
    CleanX = CleanSet[0]
    FlatCleanY = CleanSet[1]
    CleanY = Inflate(CleanX, FlatCleanY, slope)
    return CleanX, CleanY