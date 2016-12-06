import pandas as pd
import numpy as np
import sklearn
from sklearn import cross_validation
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import LogisticRegression
import random
df=pd.read_excel('/users/mohit/downloads/Round2.xlsx')
del df['Customer']
del df['Effective To Date']
df.drop(df.index[-1:], inplace=True)

column=df.columns.tolist()
col=[]
for i in column:
    col.append(str(i))
del col[2]
d = {'Yes': 1, 'No': 0}
df['Response']=df['Response'].map(d)
d2={'Basic': 1, 'Extended': 2, 'Premium': 3}
df['Coverage']=df['Coverage'].map(d2)
d3={'Bachelor': 1, 'College': 2, 'Master': 3, 'High School or Below': 4}
df['Education']=df['Education'].map(d3)
d4={'Employed': 1 ,'Unemployed': 2 , 'Medical Leave': 3 , 'Disabled': 4 }
df['EmploymentStatus']=df['EmploymentStatus'].map(d4)
d5={'M': 1 , 'F': 2}
df['Gender']=df['Gender'].map(d5)
d6={'Suburban': 1 , 'Rural': 2 , 'Urban': 3}
df['Location Code']=df['Location Code'].map(d6)
d7={'Married': 1 , 'Single': 2 , 'Divorced': 3}
df['Marital Status']=df['Marital Status'].map(d7)
d8={'Corporate Auto': 1 , 'Personal Auto': 2 , 'Special Auto': 3}
df['Policy Type']=df['Policy Type'].map(d8)
d9={'Corporate L3': 6 , 'Personal L3': 3 , 'Corporate L2': 5 , 'Personal L1': 1 ,
       'Special L2': 8 , 'Corporate L1': 4, 'Personal L2': 2,  'Special L1': 7,
       'Special L3': 9}
df['Policy']=df['Policy'].map(d9)
d10={'Offer1': 1, 'Offer3': 3, 'Offer2': 2, 'Offer4': 4}
df['Renew Offer Type']=df['Renew Offer Type'].map(d10)
d11={'Agent': 1 , 'Call Center': 2 , 'Web': 3 , 'Branch': 4}
df['Sales Channel']=df['Sales Channel'].map(d11)
d12={'Medsize': 2, 'Small': 1, 'Large': 3}
df['Vehicle Size']=df['Vehicle Size'].map(d12)
d13={'Two-Door Car': 1, 'Four-Door Car': 2, 'SUV': 5, 'Luxury SUV': 6,
       'Sports Car': 3, 'Luxury Car': 4}
df['Vehicle Class']=df['Vehicle Class'].map(d13)
d14={'Washington':1, 'Arizona': 2, 'Nevada': 3, 'California': 4, 'Oregon': 5}
df['State']=df['State'].map(d14)

null_data = df[df.isnull().any(axis=1)]
df['Education'].fillna(df['Education'].median(), inplace=True)
df['EmploymentStatus'].fillna(df['EmploymentStatus'].median(), inplace= True)
df.describe()
df['Response'].value_counts()
df.sort_values(by=['Response'], inplace= True)
df2=df.drop_duplicates()
df2['Response'].value_counts()
major_class, minor_class = df2[:7088], df2[7088:] 
temp='Response'
major_y=major_class[temp]
temp=list(major_class.columns.values)
del temp[2]
major_x=major_class[temp]
temp='Response'
minor_y=minor_class[temp]
temp=list(minor_class.columns.values)
del temp[2]
minor_x=minor_class[temp]


#SMOTE algorithm
#newindex=0


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
    
    X_new= pd.DataFrame(X_syn)
    return X_new

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

newindex=0
Synthetic_data=Smote(minor_x, 600, 5)
Synthetic_data.head(20)