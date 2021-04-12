import numpy as np
import time
import random

def overlaparea_base(wstar, Astar, size, t, tl, tdds, hr, h, tdiffer, tArea, tmatch, num_obser, max_monitor):
    differ = tdiffer.copy()
    Area = tArea.copy()
    match = tmatch.copy()
    minloss = np.inf
    l_num = int(wstar/((h * hr + 1)*size/t*num_obser))+1
    for X1 in range(l_num,max_monitor):
        temploss = 0
        param = (wstar / num_obser - h * X1) / X1
        for i in range(num_obser):
            nonobser = 0
            index = np.argsort(-Area[i,:])
            ii = 0
            eff = 0
            while eff < X1 and ii < max_monitor:
                if match[i,index[ii]] >= 0:
                    temploss += (1 - param) * differ[i,index[ii]] * Area[i,index[ii]]
                    eff = eff + 1
                ii = ii + 1
            if ii == max_monitor:
                nonobser = nonobser + 1
            for iii in range(ii,max_monitor):
                temploss += differ[i,index[iii]] * Area[i,index[iii]]
        if temploss < minloss:
            minloss = temploss
            totalnonobser = nonobser
    print("overlap:")
    print(minloss)
    print(totalnonobser)


def differ_base(wstar, Astar, size, t, tl, tdds, hr, h, tdiffer, tArea, tmatch, num_obser, max_monitor):
    differ = tdiffer.copy()
    Area = tArea.copy()
    match = tmatch.copy()
    choose = np.zeros((num_obser,max_monitor))
    minloss = 0
    tempdiffer = differ.copy()
    i = 0
    ti = 0 
    while i < wstar/((h * hr + 1)*size/t) and ti < num_obser * max_monitor:
        #print(ti)
        index = np.unravel_index(differ.argmax(), differ.shape)
        differ[index] = -1
        if match[index] >= 0 :
            tempdiffer[index] = 0
            choose[index] = 1
            i = i + 1    
        ti = ti + 1
    print(ti,i)
    for i in range(num_obser):
        for j in range(max_monitor):
            minloss += Area[i,j] * tempdiffer[i,j]
            
    count = 0
    for i in range(num_obser):
        acc = 0
        for j in range(max_monitor):
            if choose[i,j] == 1:
                acc += h * hr *size/t
                acc += size/t
        if acc < Astar:
            count += 1
    print("differ")
    print(minloss)
    print(count)