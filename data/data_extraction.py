import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import math
import json

mat = scipy.io.loadmat('mixoutALL_shifted.mat')

def plotting_data(idx):
    global mat
    letters = mat.get('mixout')[0]
    data = []
    x = [sum(letters[idx][0][0:x:1]) for x in range(0, len(letters[idx][0])+1)]
    y = [sum(letters[idx][1][0:x:1]) for x in range(0, len(letters[idx][1])+1)]
    #x = x[1:]
    #y = y[1:]
    data.extend([x,y])
    plt.plot(data[0],data[1])
    plt.show()
    return 

def convert():
    global mat
    data = mat.get('mixout')[0]
    remapped_data = []
    for i in range(len(data)):
        circ_data = []
        phi_last = 0.0
        for ii in range(len(data[i][0])):
            deltaX = data[i][0][ii]
            deltaY = data[i][1][ii]
            phi = math.atan2(deltaY, deltaX)
            delta = phi - phi_last
            phi_last = phi
            length = math.sqrt(deltaX**2+deltaY**2)
            circ_data.append([length,angle])
        remapped_data.append(circ_data)
    return remapped_data
    
def getting_indexes(idx):
    index_1h = []
    index_2h = []
    items = list(range(1,21))
    for ii in items:
        for i in range(len(idx)-1,-1,-1):
            if idx[i] == ii:
                index_1h.append(i)
                break

    for ii in items:
        for i in range(len(idx)-1):
            if idx[i] == ii:
                index_2h.append(i)
                break
    index_2h.append(index_1h[-1])
    return index_2h

def getting_rawdata():
    global mat
    data = list(mat.get('mixout')[0])
    index_dig = list(mat.get('consts')[0][0][4][0])
    index_1 = getting_indexes(index_dig[0:1512])
    index_2 = [x+(index_1[-1]+1) for x in getting_indexes(index_dig[index_1[-1]+1:])]
    consts = list(mat.get('consts'))
    temp_keys = consts[0][0][3][0]
    keys = []
    for i in list(temp_keys):
        keys.append(i[0])
    letter_data_train = []
    letter_data_test = []
    for i in range(len(index_1)-1):
        temp1 = data[index_1[i]:index_1[i+1]]
        temp2 = data[index_2[i]:index_2[i+1]]
        letter_data_train.append(temp1)
        letter_data_test.append(temp2)
    circ_dict1 = dict(zip(keys,letter_data_train))
    circ_dict2 = dict(zip(keys,letter_data_test))
    return circ_dict1, circ_dict2


def getting_data():
    global mat
    data = convert()
    index_dig = list(mat.get('consts')[0][0][4][0])
    index_1 = getting_indexes(index_dig[0:1512])
    index_2 = [x+(index_1[-1]+1) for x in getting_indexes(index_dig[index_1[-1]+1:])]
    consts = list(mat.get('consts'))
    temp_keys = consts[0][0][3][0]
    keys = []
    for i in list(temp_keys):
        keys.append(i[0])
    letter_data_train = []
    letter_data_test = []
    for i in range(len(index_1)-1):
        temp1 = data[index_1[i]:index_1[i+1]]
        temp2 = data[index_2[i]:index_2[i+1]]
        letter_data_train.append(temp1)
        letter_data_test.append(temp2)
    circ_dict1 = dict(zip(keys,letter_data_train))
    circ_dict2 = dict(zip(keys,letter_data_test))
    return circ_dict1, circ_dict2


if __name__ == '__main__':
    data_input, data_input2 = getting_data()
    letter_a = data_input['a']

    print(len(data_input['a']),len(data_input2['a']))

    #print(type(letter_a))
    dict_a = {"a": letter_a}
    plotting_data(0)
    json = json.dumps(dict_a)
    file = open("dict_a.json", "w")
    file.write(json)
    file.close()



