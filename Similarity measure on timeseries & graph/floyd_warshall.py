import os
import sys
import argparse
import numpy as np
import scipy.io
#from shortest_path_kernel import floyd_warshall
#from shortest_path_kernel import spkernel

mat = scipy.io.loadmat('../data/MUTAG.mat')
label = np.reshape(mat['lmutag'], (len(mat['lmutag'], )))
adj = np.reshape(mat['MUTAG']['am'], (len(label), ))

def floyd_warshall(A):
    S = np.asarray(A, dtype='float')
    S[S<1]=np.inf
    S= S - np.diag(np.diag(S))

    for k in range(0,len(A)):
        for i in range(0,len(A)):
            for j in range(0,len(A)):
                if S[i,j]>S[i,k]+S[k,j]:
                    S[i,j]=S[i,k]+S[k,j]
    return(S)


floyd_warshall(test)