import os
import numpy as np
# Compute all-pair distances using cdist()
from scipy.spatial import distance
# Count number of elements with each label among k-nearest neighbors
import collections

class KNNClassifier:
    '''
    A class object that implements the methods of a k-Nearest Neighbor classifier
    The class assumes there are only two labels, namely POS and NEG

    Attributes of the class
    -----------------------
    k : Number of neighbors
    X : A matrix containing the data points (train set)
    y : A vector with the labels
    dist : Distance metric used. Possible values are: 'euclidean', 'hamming', 'minkowski', and others
           For a full list of possible metrics have a look at:
           http://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html
    '''
    def __init__(self):
        '''
        Default constructor.
        '''
        self.verbose = False
        self.k = 0
        self.X = np.empty([2, 2])
        self.y = np.empty(2)
        self.metric = ""

    def __init__(self, X, y, metric):
        '''
        Constructor when X and Y are given.

        Parameters
        ----------
        X : Matrix with data points
        Y : Vector with class labels
        metric : Name of the distance metric to use
        '''
        # Default values
        self.verbose = False
        self.k = 1

        # Parameters
        self.X = X
        self.y = y
        self.metric = metric

    def debug(self, switch):
        '''
        Method to set the debug mode.

        Parameters
        ----------
        switch : String with value 'on' or 'off'
        '''
        self.verbose = True if switch == "on" else False

    def set_k(self, k):
        '''
        Method to set the value of k.

        Parameters
        ----------
        k : Number of nearest neighbors
        '''
        self.k = k

    def _compute_distances(self, X, x):
        '''
        Private function to compute distances. Invokes distance function from SciPy.
        Each row of X is a data point in the training set.
        x is one data point in the test set.
        Compute the distance between x and all rows in X

        Parameters
        ----------
        x : a vector (data point)
        '''
        return distance.cdist(X, x, self.metric)

    def predict(self, x):
        '''
        Method to predict the label of one data point.
		
        Parameters
        ----------
        x : Vector from the test data.
        Insert code here!!!!
        '''
        dist = list()
        for i in range(0,len(self.X)):
            dist.append(self._compute_distances(self.X[i],x))
            x_copy = dist.copy() 
            dist.sort()
            knn_val = dist[0:self.k+1]
            knn_lab = [self.y[x_copy.index(i)] for i in knn_val]
        return Counter(knn_lab[0]).most_common(1)[0][0]
        pass
