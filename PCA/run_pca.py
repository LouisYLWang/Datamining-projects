"""
Homework: Principal Component Analysis
Course  : Data Mining II (636-0019-00L)
"""

#import all necessary functions
from utils import *
from pca import *

'''
Main Function
'''

if __name__ in "__main__":
    #Initialise plotting defaults
    initPlotLib()

    ##################
    #Exercise 1:

    #Load Iris data
    data = loadIrisData()
    
    #Perform a PCA
    #1. Compute covariance matrix
    #2. Compute PCA by computing eigen values and eigen vectors
    #3. Transform your input data onto a 2-dimensional subspace using the first two PCs
    #4. Plot your transformed data and highlight the three different sample classes
    #5. How much variance can be explained with each principle component?
    var = sp.array([]) #Compute Variance Explained

    print("Variance Explained Exercise 1: ")
    for i in range(var.shape[0]):
        print("PC %d: %.2f"%(i+1,var[i]))
    print

    ##################
    #Exercise 2:
    
    #Simulate Data
    data = simulateData()
    #Perform a PCA
    #1. Compute covariance matrix
    #2. Compute PCA by computing eigen values and eigen vectors
    #3. Transform your input data onto a 2-dimensional subspace using the first two PCs
    #4. Plot your transformed data and highlight the three different sample classes
    #5. How much variance can be explained with each principle component?
    var = sp.array([]) #Compute Variance Explained
    print("Variance Explained Exercise 2.1: ")
    for i in range(15):
        print("PC %d: %.2f"%(i+1,var[i]))
    print
    #6. Plot cumulative variance explained per PC
    
    ##################
    #Exercise 2 Part 2:
    
    #1. normalise data
    #2. compute covariance matrix
    #3. compute PCA
    #4. Transform your input data inot a 2-dumensional subspace using the first two PCs
    #5. Plot your transformed data
    #6. Compute Variance Explained
    var = sp.array([]) #Compute Variance Explained
    print("Variance Explained Exercise 2.2: ")
    for i in range(15):
        print("PC %d: %.2f"%(i+1,var[i]))
    print
    #7. Plot Cumulative Variance
    
