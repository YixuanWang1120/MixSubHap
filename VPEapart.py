import re
# import numpy as np
sp = []
with open(r'F:\FILE\rd\200\VPE200_1500.txt') as f:
    for eachline in f:
#         print('\n')
#         print(eachline,end='')
#         print(re.findall(r'\d+\ +\D',eachline))
        a = re.findall(r'\d+\ +\D',eachline)
#         print('split string:',a[0])
        s = str(a[0])
        line = eachline.split(s)
#         print(line)
        line.append(a[0])
        length1 = len(line[2])
        length2 = length1-2
        s1 = str(line[0]+str(line[2][:length2]))
        s2 = str(line[2][length2+1:])+str(line[1])
        sp.append(s1)
        sp.append(s2)
#         print('s1:',s1)
#         print('s2:',s2)
f_write1 = open('medicaldata1','w')
f_write2 = open('medicaldata2','w')
num = len(sp)
for i in range(num):
    if i%2 == 0:
        f_write1.writelines(str(sp[i])+'\n')
    else:
        f_write2.writelines(str(sp[i]))
f_write1.close()
f_write2.close()
