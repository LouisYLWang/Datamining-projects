from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import os


def computeAccuracy(Y, Yhat):
    """
    compute the accuracy of a prediction Yhat wrt. the true class labels Y
    
    :param Y: true class labels
    :type Y: list
    
    :param Yhat: predicted class labels
    :type Yhat: list
    
    :return: accuracy value
    :rtype: float
    """
    L = len(Y)

    # true/false pos/neg.
    tp_count = 0
    fp_count = 0
    tn_count = 0
    fn_count = 0

    # define positive and negative classes.
    pos = 1
    neg = 0
    for i in range(0, L):
        if Y[i] == pos:
            # positive class.
            if Yhat[i] == pos:
                tp_count += 1
            else:
                fn_count += 1
        else:
            # negative class.
            if Yhat[i] == neg:
                tn_count += 1
            else:
                fp_count += 1

    # compute the accurary.
    accuracy = (tp_count + tn_count) / float(
        tp_count + fp_count + tn_count + fn_count)

    # output to screen.
    print('TP: {0:d}'.format(tp_count))
    print('FP: {0:d}'.format(fp_count))
    print('TN: {0:d}'.format(tn_count))
    print('FN: {0:d}'.format(fn_count))
    print('accuracy: {0:.3f}'.format(accuracy))

    pass

if __name__ in "__main__":
    fileTrain = "diabetesTrain.csv"
    fileTest = "diabetesTest.csv"
    df = pd.read_csv(fileTrain)
    x_train = df.iloc[:, 0:7].as_matrix()
    y_train = df.iloc[:, 7].as_matrix()
    model = LogisticRegression()
    train = model.fit(x_train,y_train)
    df = pd.read_csv(fileTest)
    x_test = df.iloc[:, 0:7].as_matrix()
    y_test = df.iloc[:, 7].as_matrix()
    predicted = model.predict(x_test)
    result = computeAccuracy(y_test, predicted) 
    print('\nExercise 1.b\n------------------%s' %result)

    print('\nExercise 1.c\n------------------')
    print('For the diabetes dataset I would choose ...')

    print('\nExercise 1.d\n------------------')
    print('For another dataset, I would choose ...')



