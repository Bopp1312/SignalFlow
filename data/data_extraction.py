import scipy.io
import numpy as np
import matplotlib.pyplot as plt
def getting_data():
    mat = scipy.io.loadmat('mixoutALL_shifted.mat')
    letters = mat.get('mixout')[0]

    data = []
    for i in range(len(letters)):
        x = []
        y = []
        x = [sum(letters[i][0][0:x:1]) for x in range(0, len(letters[i][0])+1)]
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
    return res