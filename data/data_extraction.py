import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import math
from mdp.drawspace import DrawSpace
import json

def getting_data():
    mat = scipy.io.loadmat('mixoutALL_shifted.mat')
    letters = mat.get('mixout')[0]

    data = []
    for i in range(len(letters)):
        x = []
        y = []
        x = [sum(letters[i][0][0:x:1]) for x in range(0, len(letters[i][0])+1)]#cummulattive sum
        y = [sum(letters[i][1][0:x:1]) for x in range(0, len(letters[i][1])+1)]


        data.append([x,y])
    plt.plot(data[70][0],data[70][1])
    plt.show()
    consts = list(mat.get('consts'))
    idx = consts[0][0][4][0]
    temp = consts[0][0][3][0]
    keys = []
    for i in list(temp):
        keys.append(i[0])
    #res = dict(zip(keys, list(d.values()))) # final dictinary with x-y cumulative distances and as values and letters as keys
    remapped_data = []
    for i in range(len(data)):
        circ_data = []
        length = 0.0
        angle = 0.0
        for ii in range(len(data[i][0])-1):
            deltaX = data[i][0][ii+1] - data[i][0][ii]
            deltaY = data[i][1][ii+1] - data[i][1][ii]
            delta_angle = math.atan2(deltaY, deltaX) #from x,y to l, theta
            delta_length = math.sqrt(deltaX**2+deltaY**2)
            length = delta_length + length
            angle = delta_angle + angle
            circ_data.append(((length, angle),(delta_length, delta_angle)))
        #circ_data.append([math.sqrt((-data[i][0][-1])**2+(-data[i][1][-1])**2),math.atan2(-data[i][1][-1],data[i][0][-1])]) #adding 0-last point
        remapped_data.append(circ_data)
    index = []
    items = list(range(1,21))
    for ii in items:
        for i in range(len(idx)-1,-1,-1):
            if idx[i] == ii:
                index.append(i)
                break
    inf = 0
    letter_data = []
    for i in index:
        letter_data.append(remapped_data[inf:i+1])
        inf = i+1
    circ_dict = dict(zip(keys, letter_data))
    return circ_dict #dict with letters and their new representation
    #'a', 'b', 'c', 'd', 'e', 'g', 'h', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 'u', 'v', 'w', 'y', 'z'


if __name__=='__main__':
    data_input = getting_data()
    letter_a = data_input['a']
    print(type(letter_a))
    dict_a = {"a": letter_a}

    json = json.dumps(dict_a)
    file = open("dict_a.json", "w")
    file.write(json)
    file.close()



