# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
point1=pd.read_excel("F:\\FILE\\rd\\100\\VPE100_1000_100point1.xlsx",header=None)
vpoint1=pd.read_excel("F:\\FILE\\rd\\100\\VPE100_1000_100vpoint1.xlsx",header=None)
point2=pd.read_excel("F:\\FILE\\rd\\100\\VPE100_1000_100point2.xlsx",header=None)
vpoint2=pd.read_excel("F:\\FILE\\rd\\100\\VPE100_1000_100vpoint2.xlsx",header=None)
ref=pd.read_excel("F:\\FILE\\ref.xlsx",header=None)

for i in range(20000):
    for j in range(50):
        if ref.values[i,j]=='a' or ref.values[i,j]=='t' or ref.values[i,j]=='c' or ref.values[i,j]=='g' :
                ref.values[i,j]=str.upper(ref.values[i,j])     

for i in range(vpoint1.iloc[:,0].size):
    for j in range(vpoint1.columns.size):
        if vpoint1.values[i,j] is not np.nan and vpoint1.values[i,j]!='N':
            if vpoint1.values[i,j]!=ref.values[int(point1.values[i,j]/50),int(point1.values[i,j])%50]:
                vpoint1.values[i,j]='B'
            else:
                vpoint1.values[i,j]='A'
        else:
            break       
for i in range(vpoint2.iloc[:,0].size):
    for j in range(vpoint2.columns.size):
        if vpoint2.values[i,j] is not np.nan and vpoint2.values[i,j]!='N':
            if vpoint2.values[i,j]!=ref.values[int(point2.values[i,j]/50),int(point2.values[i,j])%50]:
                vpoint2.values[i,j]='B'
            else:
                vpoint2.values[i,j]='A'
        else:
            break   

vpoint1.to_excel('F:\\FILE\\rd\\100\\VPE100_1000_100vpointAB1.xlsx',sheet_name='Sheet1')  
vpoint2.to_excel('F:\\FILE\\rd\\100\\VPE100_1000_100vpointAB2.xlsx',sheet_name='Sheet1')  
