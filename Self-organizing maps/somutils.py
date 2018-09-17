"""
Homework: Self-organizing maps
Course  : Data Mining II (636-0019-00L)

Auxiliary functions to help in the implementation of an online version
of the self-organizing map (SOM) algorithm.
"""
# Author: Dean Bodenham, May 2016
# Modified by: Damian Roqueiro, May 2017

from sklearn import datasets
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import random

"""
A function to create the S curve
"""
def makeSCurve():
    n_points = 1000
    noise = 0.2
    X, color = datasets.samples_generator.make_s_curve(n_points, noise=noise, random_state=0)
    Y = np.array([X[:,0], X[:,2]])
    Y = Y.T
    # Stretch in all directions
    Y = Y * 2
    
    # Now add some background noise
    xMin = np.min(Y[:,0])
    xMax = np.max(Y[:,0])
    yMin = np.min(Y[:,1])
    yMax = np.max(Y[:,1])
    
    n_bg = int(n_points/5)
    Ybg = np.zeros(shape=(n_bg,2))
    Ybg[:,0] = np.random.uniform(low=xMin, high=xMax, size=n_bg)
    Ybg[:,1] = np.random.uniform(low=yMin, high=yMax, size=n_bg)
    
    Y = np.concatenate((Y, Ybg))
    return Y

"""
Plot the data and SOM for the S-curve
  data: 2 dimensional dataset (first two dimensions are plotted)
  buttons: N x 2 array of N buttons in 2D
  fileName: full path to the output file (figure) saved as .pdf or .png
"""
def plotDataAndSOM(data, buttons, fileName):
    fig = plt.figure(figsize=(8, 8))
    # Plot the data in grey
    plt.scatter(data[:,0], data[:,1], c='grey')
    # Plot the buttons in large red dots
    plt.plot(buttons[:,0], buttons[:,1], 'ro', markersize=10)
    # Label axes and figure
    plt.title('S curve dataset, with buttons in red')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.savefig(fileName)


# Important note:
# 
# Most of the functions below are currently just headers. Provide a function
# body for each of them. 
#
# In case you want to create your own functions with their own interfaces, adjust
# the rest of the code appropriately.

"""
Create a grid of points, dim p x q, and save grid in a (p*q, 2) array
  first column: x-coordinate
  second column: y-coordinate
"""
def createGrid(p, q):
    index=0
    grid=np.zeros(shape=(p*q, 2))
    for i in range(p):
        for j in range(q):
            index = i*q + j
            grid[index, 0] = i
            grid[index, 1] = j
    return grid

"""
A function to plot the crabs results
It applies a SOM previously computed (parameters grid and buttons) to a given
dataset (parameters data)

Parameters
 X : is the original data that was used to compute the SOM.
     Rows are samples and columns are features.
 idInfo : contains the information (sp and sex for the crab dataset) about
          each data point in X.
          The rows in idInfo match one-to-one to rows in X.
 grid, buttons : obtained from computing the SOM on X.
 fileName : full path to the output file (figure) saved as .pdf or .png
"""

def plotSOMCrabs(X, idInfo, grid, buttons, fileName):
    # Use the following colors for saples of each pair [species, sex]
    # Blue male:     dark blue #0038ff
    # Blue female:   cyan      #00eefd
    # Orange male:   orange    #ffa22f
    # Orange female: yellow    #e9e824

    # TODO replace statement below with function body
    output = pd.read_csv('output_som_crabs.txt',sep='\t')
    idInfo = output.iloc[:,0:2]
    idInfo['x'] = list(grid[i,0] for i in output.label)
    idInfo['y'] = list(grid[i,1] for i in output.label)
    for i in range(len(idInfo)):
        idInfo.x[i] = idInfo.x[i]+random.uniform(0,0.2)
        idInfo.y[i] = idInfo.y[i]+random.uniform(0,0.2)
    bm = idInfo[(idInfo.sp == 'B') & (idInfo.sex == 'M')]
    bf = idInfo[(idInfo.sp =='B') & (idInfo.sex == 'F')]
    om = idInfo[(idInfo.sp == 'O') & (idInfo.sex == 'M')]
    of = idInfo[(idInfo.sp == 'O') & (idInfo.sex == 'F')]
        
    fig,ax = plt.subplots()
    patches = []
    for i in range(len(grid)):
        patches.append(mpatches.Circle(grid[i],0.4))
    collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3)
    ax.add_collection(collection)
    ax.set_xlim(-0.5,5.5)
    ax.set_ylim(-0.5,7.5)

    plt.scatter(bm.x,bm.y,c = '', edgecolors = '#0038ff')
    plt.scatter(bf.x,bf.y,c = '', edgecolors = '#00eefd')
    plt.scatter(om.x,om.y,c = '', edgecolors = '#ffa22f')
    plt.scatter(of.x,of.y,c = '', edgecolors = '#e9e824')

    plt.savefig(fileName)
    pass


"""
Function for computing distance in grid space.
Use Euclidean distance.
"""
def getGridDist(z0, z1):
    # TODO replace statement below with function bodyd
    return np.sqrt(sum((z0-z1)**2))
    pass
"""
Function for computing distance in feature space.
Use Euclidean distance.
"""
def getFeatureDist(z0, z1):
    # TODO replace statement below with function body
    return np.sqrt(sum((z0-z1)**2))
    pass


"""
Create distance matrix between points numbered 1,2,...,K=p*q from grid
"""
def createGridDistMatrix(grid):
    # TODO replace statement below with function body
    grid_dm = np.zeros([len(grid),len(grid)])
    for i in range(len(grid)):
        for j in range(len(grid)):
            grid_dm[i,j] = getGridDist(grid[i,:],grid[j,:])
    return grid_dm
    pass

"""
Create array for epsilon. Values in the array decrease to 1.
"""
def createEpsilonArray(epsilon_max, N):
    # TODO replace statement below with function body
    return np.linspace(epsilon_max,1,N)
    pass


"""
Create array for alpha. Values in the array decrease to 0.
"""
def createAlphaArray(alpha_max, N):
    # TODO replace statement below with function body
    return np.linspace(alpha_max,0,N)
    pass


"""
X is whole data set, K is number of buttons to choose
"""
def initButtons(X, K):
    # TODO replace statement below with function body
    return X[np.random.choice(len(X),K,replace = False),:]
    pass


"""
x is one data point, buttons is the grid in FEATURE SPACE
"""
def findNearestButtonIndex(x, buttons):
    # TODO replace statement below with function body
    distance=[]
    for i in buttons:
        distance.append(getFeatureDist(x,i))
    return distance.index(min(distance))
    pass

"""
Find all buttons within a neighborhood of epsilon of index IN GRID SPACE 
(return a boolean vector)
"""
def findButtonsInNhd(index, epsilon, buttonDist):
    # TODO replace statement below with function body
    with_eps=[]
    for i in buttonDist[index,:]:
        with_eps.append(i<epsilon)
    return with_eps
    pass


"""
Do gradient descent step, update each button position IN FEATURE SPACE
"""
def updateButtonPosition(button, x, alpha):
    # TODO replace statement below with function body
    return button+alpha*(x-button)
    pass

"""
Compute the squared distance between data points and their nearest button
"""
def computeError(data, buttons):
    # TODO replace statement below with function body
    label=[]
    for i in range(len(data)):
        label.append(findNearestButtonIndex(data[i,:],buttons))
    error = 0
    for i in range(len(data)):
        error+=sum((data[i,:]-buttons[label[i]])**2)
    return error
    pass

"""
Implementation of the self-organizing map (SOM)

Parameters
 X : data, rows are samples and columns are features
 p, q : dimensions of the grid
 N : number of iterations
 alpha_max : upper limit for learning rate
 epsilon_max : upper limit for radius
 compute_error : boolean flag to determine if the error is computed.
                 The computation of the error is time-consuming and may
                 not be necessary every time the function is called.
                 
Returns
 buttons, grid : the buttons and grid of the newly created SOM
 error : a vector with error values. This vector will contain zeros if 
         compute_error is False

TODO: Complete the missing parts in this function following the pseudocode
      in the homework sheet
"""
np.random.seed(100)
def SOM(X, p, q, N, alpha_max, epsilon_max, compute_error=False):
    # 1. Create grid and compute pairwise distances
    grid = createGrid(p, q)
    buttondist = createGridDistMatrix(grid)

    # 2. Randomly select K out of d data points as initial positions
    #    of the buttons
    K = p * q
    d = X.shape[0]
    buttons = initButtons(X, K)
    
    # 3. Create a vector of size N for learning rate alpha
    lr = createAlphaArray(alpha_max,N)
    # 4. Create a vector of size N for epsilon 
    eps = createEpsilonArray(epsilon_max,N)
    # Initialize a vector with N zeros for the error
    # This vector may be returned empty if compute_error is False
    error = np.zeros(N)

    # 5. Iterate N times
    for i in range(N):
        # 6. Initialize/update alpha and epsilon
        alpha = lr[i]
        epsilon = eps[i]
        # 7. Choose a random index t in {1, 2, ..., d}
        t = np.random.choice(range(d))
        x_t = X[t,:]
        # 8. Find button m_star that is nearest to x_t in F 
        index = findNearestButtonIndex(x_t,buttons)
        # 9. Find all grid points in epsilon-nhd of m_star in GRID SPACE 
        nhd = findButtonsInNhd(index,epsilon,buttondist)
        with_eps = [i for i in range(len(nhd)) if nhd[i] == True]
        # 10. Update position (in FEATURE SPACE) of all buttons m_j
        #     in epsilon-nhd of m_star, including m_star
        for j in with_eps:
            buttons[j] = updateButtonPosition(buttons[j],x_t,alpha)
        # Compute the error 
        # Note: The computation takes place only if compute_error is True
        #       Replace the statement below with your code
        error[i] = computeError(X,buttons)
        #pass

    # 11. Return buttons, grid and error
    return (buttons, grid, error)


def ploterror(error, fileName):
    fig = plt.figure(figsize=(8, 8))
    plt.plot(range(1,101),error,'r-')
    plt.xlabel('Iteration')
    plt.ylabel('Reconstruction Error')
    plt.savefig(fileName)


crab = pd.read_csv('crabs.txt',sep='\t')
X=crab.iloc[:,4:8].values
buttons,grid,error = SOM(crab.iloc[:,4:8].values,6,8,1000,1,3)
idInfo
plotSOMCrabs(X, idInfo, grid, buttons, fileName)


#
#label=[]
#for i in range(len(X)):
 #   label.append(findNearestButtonIndex(X[i,:],buttons))
#df=crab.iloc[:,0:3]    
#df['label']=label
#df.to_csv('output_som_crabs.txt',sep='\t',index=False)

