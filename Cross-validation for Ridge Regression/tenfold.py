from sklearn.linear_model import Ridge
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold

filedir = r"C:\Users\ym559sz\Desktop\pddzml\ML\task1a_lm1d1z"
sample = filedir +'\\sample.csv' 
train =  filedir + '\\train.csv'

train_data = pd.read_csv(train)
sample_data = np.loadtxt(sample)


lam = [0.1, 1.0, 10.0,100,10000]

x = np.asarray(train_data.ix[:,2:])
y = np.asarray(train_data['y'])

kf = KFold(n_splits=10, shuffle=False)

def onceKfold(alpha):
    MRSE =0 
    for train_index, test_index in kf.split(x):
        X_train, X_test =x[train_index], x[test_index]
        y_train, y_test =y[train_index], y[test_index]
        reg = linear_model.Ridge (alpha =alpha)
        reg.fit(X_train,y_train)
        MRSE+=mean_squared_error(y_test,reg.predict(X_test))**0.5

    return MRSE/10

for i in lam:
    print(onceKfold(i))

