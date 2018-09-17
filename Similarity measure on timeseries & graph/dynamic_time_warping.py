import numpy as np
def DTW(t1, t2):
    W=np.array([abs(np.array(t1)-np.array(t2)[i])  for i in range(len(t2))])
    C=np.zeros([len(t2)+1,len(t1)+1])
    C[0,0]=0
    C[0,1:]=np.inf
    C[1:,0]=np.inf
    for i in range(1,len(t2)+1):
        for j in range(1,len(t1)+1):
            C[i,j]=W[i-1,j-1]+min(C[i-1,j-1],C[i,j-1],C[i-1,j])
    return C[len(t2),len(t1)]


