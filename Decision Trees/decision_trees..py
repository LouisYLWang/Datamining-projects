import numpy as np
from sklearn.datasets import load_iris
from collections import *

iris = load_iris()
X = iris.data
y = iris.target
featureNames = iris.feature_names
yNames = iris.target_names

def do_split(data, y, a_idx, theta):
    """
    split the data according to a_idx (feature) and theta (threshold).
    """

    y_a = y[X[:,a_idx]<theta]
    y_b = y[X[:,a_idx]>=theta]
    
    return([y_a,y_b])
    pass

#do_split(X, y, a_idx, theta)


def compute_info_content(y):
    """
    commpute information content info(D).
    """

    p = np.array(list(Counter(y).values()))/len(y)
    return(-sum(p*np.log2(p)))
    pass


def compute_info_a(data, y, a_idx, theta):
    """
    compute conditional information content Info_A(D).
    """

    split = do_split(data, y, a_idx, theta)

    return(sum([len(i)/len(y)*compute_info_content(i) for i in split]))
    pass



def compute_info_gain(data, y, a_idx, theta):
    """
    compute information gain(A) = Info(D) - Info_A(D)
    """

    return(compute_info_content(y)-compute_info_a(data, y, a_idx, theta))
    pass


if __name__ == '__main__':


    print('''\nExercise 2.b\n------------------\n
    Split ( sepal length (cm) < 5.5 ):%f\n
    Split ( sepal width (cm) < 3.0 ):%f\n
    Split ( petal length (cm) < 2.0 ):%f\n
    Split ( petal width (cm) < 1.0 ):%f\n
    '''%(compute_info_gain(X, y, 0, 5.5),
         compute_info_gain(X, y, 1, 3.0),
         compute_info_gain(X, y, 2, 2.0),
         compute_info_gain(X, y, 3, 1.0)))

    print('\nExercise 2.c\n------------------')





