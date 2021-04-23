import numpy as np
import math
import random
from sate import satellite
from sate_orbit_ver2 import orbit_generator, param_generator
from baseline import overlaparea_base, differ_base
from model import decision
import xlwt
import xlrd

num_orbit = 72
num_per_sate = 22
inclination = 0.294 * math.pi /2
h = 550
R = 6371
#num_obser = 1000
min_threld = 0.05
obser_radius = 20
sigma = 20
min_monitor = 10
method = "population"
filename = "exp1"
batch_num = 50
wstar = 15000
Astar = 5
size = 1
t = 1
tl = 1
tdds = 1e-6
hr = 0.3
h = 1

sate,num_sate = orbit_generator(num_orbit, num_per_sate, inclination, h, R, min_threld, obser_radius,sigma, min_monitor, method)
f = xlwt.Workbook()
for total in range(1000,10000,1000):
    filename = "exp2_"+str(total)
    sheet1 = f.add_sheet(u'sheet'+str(total)+'obser',cell_overwrite_ok=True) 
    sheet2 = f.add_sheet(u'sheet'+str(total)+'max',cell_overwrite_ok=True) 
    for i in range(batch_num):
        tobser,tmoni = param_generator(sate, num_sate, R, total, min_threld, obser_radius,sigma, min_monitor, method, i, filename)
        print(tobser,tmoni)
        sheet1.write(i,0,tobser)
        sheet2.write(i,0,tmoni)
f.save("global_ver2.xls")

#workbook = xlrd.open_workbook(r'global.xls')
#for total in range(1000,10000,1000):
    #fexp = open('res/exp'+str(total)+'.txt','w')
    #filename = "exp" + str(total)
    #sheet1 = workbook.sheet_by_name('sheet'+str(total)+'obser')
    #sheet2 = workbook.sheet_by_name('sheet'+str(total)+'max')
    #obsernum = sheet1.col_values(0)
    #maxnum = sheet2.col_values(0)
    #for i in range(batch_num):
    #    tdiffer = np.load(filename+'/differ_'+str(i)+'.npy')
    #    tArea = np.load(filename+'/area_'+str(i)+'.npy')
    #    tmatch = np.load(filename+'/match_'+str(i)+'.npy')
    #    res = decision(wstar, Astar, size, t, tl, tdds, hr, h, tdiffer, tArea, tmatch, int(obsernum[i]), int(maxnum[i]))
    #    #overlaparea_base(wstar, Astar, size, t, tl, tdds, hr, h, tdiffer, tArea, tmatch, num_obser[i], max_monitor[i])
    #    count = differ_base(wstar, Astar, size, t, tl, tdds, hr, h, tdiffer, tArea, tmatch, int(obsernum[i]), int(maxnum[i]))
    #    if res == "Yes":
    #        fexp.write(str(1))
    #    else :
    #        fexp.write(str(0))
    #    fexp.write("    ")
    #    fexp.write(str(count))
    #    fexp.write('\n')
    #fexp.close()
