import scipy.io as scio
import numpy as np
import copy
import pandas as pd
#read the weight matrix of unweighted graph
dict1 = scio.loadmat(r'F:\FILE\file\numlib\4lib100-50-50-50\ww_nonezero.mat')
dic2 = scio.loadmat(r'F:\FILE\file\numlib\4lib100-50-50-50\aww.mat')
weight_matrix = dict1['ww']  
point2=dic2['aa']
cluster=pd.read_excel("F:\\FILE\\cluster.xlsx",header=None)
#find points with the maximum absolute weight value linked to the point i
result = []
num = len(weight_matrix[0])               #the number of points
for i in range(num):
    list1 = []
    list1.append(i)                       #add the point into the list
    a = weight_matrix[i].max()            #find the maximum weight
    b = weight_matrix[i].min()            #find the minmum weight
    if a+b >= 0:                          #find the maximum absolute weight value
        list1.append(weight_matrix[i].argmax()) 
        list1.append(a)                         
        result.append(list1)
        continue
    else:                                 
        list1.append(weight_matrix[i].argmin())
        list1.append(b)
        result.append(list1)
#find all the linked points
L = []
for i in range(num):
    link = []
    for j in range(num):
        if weight_matrix[i][j] != 0 :
            link.append(j)
    L.append(link)
#find all the linked points with the maximum absolute weight value
M = []
for i in range(num):
    m = []
    for j in range(num):
        if abs(round(result[i][2],2))- abs(round(weight_matrix[i][j],2)) < 0.0000001 :
            m.append(j)
    M.append(m)

m1 = copy.deepcopy(np.array(L))
m2 = copy.deepcopy(np.array(M))
M1 = m1.tolist()
M2 = m2.tolist()


#find all the sub-graphs
def judge(list1,list2):                                 #judge if list1 belong to list2
    l1 = list1
    l2 = list2
    result = []
    t = True
    for each in l1:
        if each not in l2:
            result.append(each)
    if result != []:
        t = False
    return result,t
list_p = []                                    
list_i = []
i = 0
while i<num:
    if i not in list_p:                                 
        if M1[i] != []:
            for each in M1[i]:
                print(each)
                res,t = judge(M1[each],M1[i])
                if (M1[each]!=[]) and (not t):
                    M1[i].extend(res)
                elif M1[each] != [] and M1[i].index(each) < len(M1[i]):
                    continue
                elif M1[each] == [] and M1[i].index(each) < len(M1[i]):
                    continue
                else:
                    break
            list_p.extend(M1[i])
        i = i + 1
    else:
        list_i.append(i)
        i = i + 1
new_index = []                                           #points of sub-graphs
for i in range(num):      
    if i not in list_i :
        temp = list(set(M1[i]))
        temp = sorted(temp)
        new_index.append(temp)
       
#find the starting points of sub-graphs      
mi = []
for each in new_index:
    mi.append(each[0])

#generate the maximum spanning tree
for each in new_index:
    print('\neach:',each)
    length_of_each = len(each)
    copy_of_each = each[:]
    for i in range(length_of_each):
        length_of_M2 = len(list(set(M2[each[i]])))
        print('each[i]:',each[i])
        print('length_of_M2:',length_of_M2)
        if length_of_M2 > 0:
            max_M2 = max(M2[each[i]])
            print('max_M2:',max_M2)
            result[each[i]][1] = max_M2
            copy_of_each.remove(each[i])
            print('copy_of_each:',copy_of_each)
        else:
            break
#sp assignment
initial_data = [0,1,1,0,1,0,1,1,1,1,0,0,0,1,1,1,0,1,0,1,0,1,0,0,1,1,1,1,1,0,1,1] 
for each in new_index:
    length = len(each)
    loc = new_index.index(each)
    for i in range(length):
        if i == 0:
            result[each[i]].append(initial_data[loc])
            p = result[each[i]][2]
            if p > 0:
                result[each[i+1]].append(initial_data[loc])
            else:
                result[each[i+1]].append(1-initial_data[loc])
        else:
            curr = each[i]
            print('current point：',each[i])
            if len(result[each[i]]) == 4:
                #print('step1')
                curr_value = result[each[i]][3]
                print('value of the current point：',result[each[i]][3])
                a = result[each[i]][1]
                print('linked point：',a)
                weight = result[each[i]][2]
                print('weight:',weight)
                if len(result[a]) < 4: 
                    if weight > 0 :
                        print('value of the linked point：',curr_value)
                        result[a].append(curr_value)
                    else:
                        print('value of the linked point：',1-curr_value)
                        result[a].append(1-curr_value)
                else:
                    continue
            elif len(result[each[i]]) ==3:
                #print('step2')
                a = result[each[i]][1]
                print('other linked point2：',a)
                if len(result[a]) == 4:
                    #print('step3')
                    weight2 = result[a][2]
                    print('weight2:',weight2)
                    curr_value2 = result[a][3]
                    print('value of the current point2：',result[a][3])
                    if weight > 0 :
                        print('value of the linked point2：',curr_value2)
                        result[each[i]].append(curr_value2)
                    else:
                        print('value of the linked point2：',1-curr_value2)
                        result[each[i]].append(1-curr_value2)
                else:
                    #print('step4')
                    for succ in M[each[i]]:
                        if len(result[succ]) == 4:
                            #print('step5')
                            print('the next point：',succ)
                            succ_value = result[succ][3]
                            print('value of the next point：',succ_value)
                            succ_weight = result[succ][2]
                            print('weight：',succ_weight)
                            if succ_weight > 0:
                                print('value of the current point2：',succ_value)
                                result[each[i]].append(succ_value)
                            else:
                                print('value of the current point2：',1-succ_value)
                                result[each[i]].append(1-succ_value)  
                            break
                        else:
                            #print('step6')
                            if weight_matrix[each[i]][a] > 0:
                                result[each[i]].append(1)
                            else:
                                result[each[i]].append(0)
            else:
                continue
#final result
A =[]
k=0
for i in range(num):
    if len(result[i]) < 4:
        A.append('N')
        k+=1
    else:
        A.append(result[i][3])
print(A)
print('new_index:',new_index)
B = []
for each1 in new_index:
    l1 = []
    for each2 in each1:
        l1.append(result[each2][3])
    B.append(l1)
print('B:',B)  

#reconstruction
h00=['N']*11000
h01=['N']*11000
h10=['N']*11000
h11=['N']*11000
h20=['N']*11000
h21=['N']*11000
for i in range(num):
    if A[i] == 0:
        h20[int(point2[i]-1)]='A'
    if A[i] == 1:
        h20[int(point2[i]-1)]='B'
for i in range(len(h00)):
    if cluster.values[i,0]==0:
        h00[i]=h20[i]
    elif h20[i] != 'N':
        h00[i] = 'A'
for i in range(len(h00)):
    if cluster.values[i,0]==0 or cluster.values[i,0]==1:
        h10[i]=h20[i]
    elif h20[i] != 'N':
        h10[i] = 'A'

for i in range(len(h00)):
    if cluster.values[i,0]==0:
        if h00[i] == 'A':
            h01[i] = 'B'
        if h00[i] == 'B':
            h01[i] = 'A'
    else:
        h01[i] = h00[i]      
for i in range(len(h00)):
    if cluster.values[i,0]==0 or cluster.values[i,0]==1:
        if h10[i] == 'A':
            h11[i] = 'B'
        if h10[i] == 'B':
            h11[i] = 'A'
    else:
        h11[i] = h10[i]
for i in range(len(h00)):
    if h20[i] == 'A':
        h21[i] = 'B'
    if h20[i] == 'B':
        h21[i] = 'A'   
        
file = open ('F:\\FILE\\chainAB.txt', 'w')
for i in range(len(h00)):
    file.write(h00[i]) 
file.write('\n')
for i in range(len(h00)):
    file.write(h01[i])
file.write('\n')
for i in range(len(h00)):
    file.write(h10[i])
file.write('\n')
for i in range(len(h00)):
    file.write(h11[i])
file.write('\n')
for i in range(len(h00)):
    file.write(h20[i])
file.write('\n')
for i in range(len(h00)):
    file.write(h21[i])
file.write('\n')
file.close()     