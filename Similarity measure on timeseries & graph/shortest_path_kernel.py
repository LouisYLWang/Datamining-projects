import numpy as np
from collections import Counter

def spkernel(S1, S2):
    count=0
    for i in range(len(S1)):
        for j in range(len(S1)):
            for k in range(len(S2)):
                if np.triu(S1)[i,j]!=0:
                    count+=Counter(np.triu(S2)[k])[np.triu(S1)[i,j]]
    return(count)
