import pandas as pd
import numpy as np
import sklearn
from sklearn.neighbors import NearestNeighbors
import random

#SMOTE algorithm


newindex=0

def Smote(minority,N,k):
    #Number of minority class samples T; Amount of SMOTE N%; Number of nearest neighbors k
    #Output: (N/100) * T synthetic minority class samples
    #If N is less than 100%, randomize the minority class samples as only a random percent of them will be SMOTEd.
    if N<100:
        new=T.sample(frac=1)
        no_elements=(N/100)*len(T)
        T=df[:no_elements]

    n=int(N/100)
    newindex=0
    data= minority.as_matrix()
    #creating an empty array to store synthetic data
    X_syn= np.zeros((len(minor_x)*6, data.shape[1]))
    cols=minority.columns
    numattrs= len(cols)
        
    nbrs = NearestNeighbors(n_neighbors=7, algorithm='ball_tree').fit(data)
    distances, indices = nbrs.kneighbors(data)
    n_minority=len(data)

    k=0
    
    for i in range(n_minority):
        indice=indices[k]
        populate(n,i,indice, X_syn)
        k+=1
    
    # creating a dataframe from the matrix of synthetic data
    X_new= pd.DataFrame(X_syn)
    return X_new

# function to populate synthetic data points and store it in X_syn 
def populate(n, i, indices, X_syn):
    numattrs=21
    global newindex
    while n!=0:
        nn=random.randint(1,6)
        for attr in range(numattrs):
            c=int(indices[nn])
            temp=data[c][attr]
            temp2=data[i][attr]
            dif=data[c][attr]- data[i][attr]
            gap=np.random.random()
            X_syn[newindex][attr]=data[i][attr]+gap*dif
        newindex+=1
        n=n-1
        
    return X_syn


