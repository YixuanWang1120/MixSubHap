# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 20:17:20 2018

@author: Administrator
"""
import pandas as pd
with open(r'F:\\FILE\\rechain.txt') as f:
    line=f.readlines()
    hap00=[item for item in line[0]]
    hap01=[item for item in line[1]]
    hap10=[item for item in line[2]]
    hap11=[item for item in line[3]]
    hap20=[item for item in line[4]]
    hap21=[item for item in line[5]]
point=pd.read_excel("F:\\FILE\\variants_point.xlsx",header=None)    
ref=pd.read_excel("F:\\FILE\\ref.xlsx",header=None)
for i in range(11000):
    if hap00[i]==ref.values[int((point.values[i])/50),int(point.values[i])%50]:
        hap00[i]='A'
    else:
        hap00[i]='B'
for i in range(11000):
    if hap01[i]==ref.values[int((point.values[i])/50),int(point.values[i])%50]:
        hap01[i]='A'
    else:
        hap01[i]='B'
for i in range(11000):
    if hap10[i]==ref.values[int((point.values[i])/50),int(point.values[i])%50]:
        hap10[i]='A'
    else:
        hap10[i]='B'
for i in range(11000):
    if hap11[i]==ref.values[int((point.values[i])/50),int(point.values[i])%50]:
        hap11[i]='A'
    else:
        hap11[i]='B'
for i in range(11000):
    if hap20[i]==ref.values[int((point.values[i])/50),int(point.values[i])%50]:
        hap20[i]='A'
    else:
        hap20[i]='B'                
for i in range(11000):
    if hap21[i]==ref.values[int((point.values[i])/50),int(point.values[i])%50]:
        hap21[i]='A'
    else:
        hap21[i]='B'
file = open ('F:\\FILE\\rechainAB.txt', 'w')
for i in range(len(hap00)):
    file.write(hap00[i])  
for i in range(len(hap01)):
    file.write(hap01[i])
for i in range(len(hap10)):
    file.write(hap10[i])
for i in range(len(hap11)):
    file.write(hap11[i])
for i in range(len(hap20)):
    file.write(hap20[i])
for i in range(len(hap21)):
    file.write(hap21[i])
file.close()