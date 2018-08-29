# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 20:07:14 2018

@author: Administrator
"""
import numpy as np
import pandas as pd
import itertools
import scipy.io as scio  

pointAB=pd.read_excel("F:\\FILE\\rd\\100\\pointAB.xlsx",header=None)
vpointAB=pd.read_excel("F:\\FILE\\rd\\100\\vpointAB.xlsx",header=None)
cluster=pd.read_excel("F:\\FILE\\cluster.xlsx",header=None)
w0=np.mat(np.zeros((11000 , 11000)))
w1=np.mat(np.zeros((11000 , 11000)))
f0=np.mat(np.zeros((11000 , 11000)))
f1=np.mat(np.zeros((11000 , 11000)))
for i in range(pointAB.iloc[:,0].size):
    for j in itertools.combinations(list(range(pointAB.columns.size)),2):
        if vpointAB.values[i, j[0]] is not np.nan and vpointAB.values[i, j[1]] is not np.nan:
            if vpointAB.values[i, j[0]]==vpointAB.values[i, j[1]]:
                w0[int(pointAB.values[i,j[0]]) , int(pointAB.values[i,j[1]])]+=1
            else:
                w1[int(pointAB.values[i,j[0]]) , int(pointAB.values[i,j[1]])]+=1

err=0.1
a=(1-err)**2+err**2
b=2*err*(1-err)
N0=a*w0+b*w1
N1=a*w1+b*w0
F=w0+w1
for i in range(11000):
    for j in range(11000):
        if F[i, j]!=0:
            f0[i, j]=N0[i, j]/F[i, j]
            f1[i, j]=N1[i, j]/F[i, j]

w=f0-f1

for i in range(11000):
    for j in range(11000):
        if F[i, j]<=2:
            w[i, j]=0
w += w.T - np.diag(w.diagonal())

ws0=np.copy(w)
ws1=np.copy(w)
ws2=np.copy(w)
for i in range(11000):
    if cluster.values[i,0]!=0:
        ws0[i,:]=0
        ws0[:,i]=0
for i in range(11000):
    if cluster.values[i,0]!=1:
        ws1[i,:]=0
        ws1[:,i]=0
for i in range(11000):
    if cluster.values[i,0]!=2:
        ws2[i,:]=0
        ws2[:,i]=0

scio.savemat('F:\\FILE\\file\\w.mat', {'matrix': w})  
scio.savemat('F:\\FILE\\file\\w0.mat', {'matrix': ws0})  
 
w00=np.mat(np.zeros((11000 , 11000)))
w10=np.mat(np.zeros((11000 , 11000))) 
f00=np.mat(np.zeros((11000 , 11000)))
f10=np.mat(np.zeros((11000 , 11000)))

ratio=[0.3,0.5,0.2]
for j in range(11000):
    for k in range(11000):
        R1=0
        R2=0
        for i in range(cluster.values[k,0]):
            R1+=ratio[i]
        for i in range(cluster.values[k,0], cluster.values[j,0]):
            R2+=ratio[i]/2            
        w00[j,k]=max(w0[j,k]-F[j,k]*(R1+R2) , 0)
        w10[j,k]=max(w1[j,k]-F[j,k]*R2 , 0)
N00=a*w00+b*w10
N10=a*w10+b*w00
F0=w00+w10
for i in range(11000):
    for j in range(11000):
        if F0[i, j]!=0:
            f00[i, j]=N00[i, j]/F0[i, j]
            f10[i, j]=N10[i, j]/F0[i, j]
ww=f00-f10
for i in range(11000):
    for j in range(11000):
        if F0[i, j]<=2:
            ww[i, j]=0       
ww += ww.T - np.diag(ww.diagonal())
scio.savemat('F:\\FILE\\file\\ww.mat', {'matrix': ww}) 
ll = len(ww)
for i in range(ll):
    if ww[i][i]!=0:
        print(ww[i][i])
