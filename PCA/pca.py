"""
Homework: Principal Component Analysis
Course  : Data Mining II (636-0019-00L)
"""
import scipy as sp
import scipy.linalg as linalg
import pylab as pl

os.chdir(r"C:\Users\ym559sz\Desktop\pddzml\DM#2\homework_1_handout")
from utils import plot_color

'''############################'''
'''Principle Component Analyses'''
'''############################'''

'''
Compute Covariance Matrix
Input: Matrix of size #samples x #features
Output: Covariance Matrix of size #features x #features
Note: Do not use scipy or numpy cov. Implement the function yourself.
      You can of course add an assert to check your covariance function
      with those implemented in scipy/numpy.
'''
def computeCov(X=None):
	# Please fill this function
    count = len(X)-1
    result = list()
    adjX = X-np.mean(X,axis=0)

    def cov(va,vb):
        return (va*(vb.T)/count).tolist()[0][0]
        
    for row1 in adjX.T:
        box = list()
        for row2 in adjX.T:
            box.append(cov(row1,row2))
        
        result.append(box)
    return result
    pass


test = np.asmatrix([[2.5,0.5,2.2,1.9,3.1,2.3,2,1,1.5,1.1],[2.4,0.7,2.9,2.2,3.0,2.7,1.6,1.1,1.6,0.9]]).T
computeCov(test)

#np.array([2,7])*np.array([1.2]).T


'''

Compute PCA
Input: Covariance Matrix
Output: [eigen_values,eigen_vectors] sorted in such a why that eigen_vectors[:,0] is the first principle component
        eigen_vectors[:,1] the second principle component etc...
Note: Do not use an already implemented PCA algorithm. However, you are allowed to use an implemented solver 
      to solve the eigenvalue problem!
'''
def computePCA(matrix=None):
	# Please fill this function
    return linalg.eig(matrix)
    pass


a = computePCA(computeCov(test))

'''
Transform Input Data Onto New Subspace
Input: pcs: matrix containing the first x principle components
       data: input data which should be transformed onto the new subspace
Output: transformed input data. Should now have the dimensions #samples x #components_used_for_transformation
'''
def transformData(pcs=None,data=None):
    # Please fill this function
    return np.dot(data-np.mean(data,axis=0),pcs)
    pass


'''
Compute Variance Explaiend
Input: eigen_values
Output: return vector with varianced explained values. Hint: values should be between 0 and 1 and should sum up to 1.
'''
def computeVarianceExplained(evals=None):
    # Please fill this function
    
    pass

'''############################'''
'''Different Plotting Functions'''
'''############################'''

'''
Plot Cumulative Explained Variance
Input: var: variance explained vector
       filename: filename to store the file
'''
def plotCumSumVariance(var=None,filename="cumsum.pdf"):
    #PLOT FIGURE
    #You can use plot_color[] to obtain different colors for your plots
    #Save file
    pl.savefig(filename)

'''
Plot Transformed Data
Input: transformed: data matrix (#sampels x 2)
       labels: target labels, class labels for the samples in data matrix
       filename: filename to store the plot
'''
def plotTransformedData(transformed=None,labels=None,filename="exercise1.pdf"):
    #PLOT FIGURE
    #You can use plot_color[] to obtain different colors for your plots
    #Save File
    pl.savefig(filename)

'''############################'''
'''Data Preprocessing Functions'''
'''############################'''

'''
Exercise 2
Data Normalisation (Zero Mean, Unit Variance)
'''
def dataNormalisation(X=None):
    # Please fill this function
    pass
