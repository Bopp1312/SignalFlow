import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import math

def getting_data():
    mat = scipy.io.loadmat('mixoutALL_shifted.mat')
    letters = mat.get('mixout')[0]

    data = []
    for i in range(len(letters)):
        x = []
        y = []
        x = [sum(letters[i][0][0:x:1]) for x in range(0, len(letters[i][0])+1)]#cummulattive sum
        y = [sum(letters[i][1][0:x:1]) for x in range(0, len(letters[i][1])+1)]
        x = x[1:]
        y = y[1:]
        data.append([x,y])
    #plt.plot(data[70][0],data[70][1])
    #plt.show()
    consts = list(mat.get('consts'))
    idx = consts[0][0][4][0]
    temp = consts[0][0][3][0]
    keys = []
    for i in list(temp):
        keys.append(i[0])
    d = dict(zip(idx,data))
    res = dict(zip(keys, list(d.values()))) # final dictinary with x-y cumulative distances and as values and letters as keys
    remapped_data = []
    for i in range(len(data)):
        circ_data = []
        for ii in range(len(data[i][0])-1):
            deltaX = data[i][0][ii+1] - data[i][0][ii]
            deltaY = data[i][1][ii+1] - data[i][1][ii]
            angle = math.atan2(deltaY, deltaX) #from x,y to l, theta
            length = math.sqrt(deltaX**2+deltaY**2)
            circ_data.append([length,angle])
        circ_data.append([math.sqrt((-data[i][0][-1])**2+(-data[i][1][-1])**2),math.atan2(-data[i][1][-1],data[i][0][-1])]) #adding 0-last point
        remapped_data.append(circ_data)
    d2 = dict(zip(idx,remapped_data))
    circ_dict = dict(zip(keys, list(d2.values())))
    print(circ_dict)
    return circ_dict #dict with letters and their new representation
    #'a', 'b', 'c', 'd', 'e', 'g', 'h', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 'u', 'v', 'w', 'y', 'z'


if __name__=='__main__':
    data_input = getting_data()

