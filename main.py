import numpy as np
import math
import random
from sate import satellite
from sate_orbit import orbit_generator, param_generator
from baseline import overlaparea_base, differ_base
from model import decision

num_orbit = 72
num_per_sate = 22
inclination = 0.294 * math.pi /2
h = 550
R = 6371
num_obser = 1000
min_threld = 0.05
obser_radius = 5
sigma = 5
min_monitor = 10
method = "population"
filename = "exp1"
batch_num = 500
wstar = 10000
Astar = 5
size = 1
t = 1
tl = 1
tdds = 1e-6
hr = 0.3
h = 1

sate = orbit_generator(num_orbit, num_per_sate, inclination, h, R, num_obser, min_threld, obser_radius,sigma, min_monitor, method)
num_obser = []
max_monitor = []
for i in range(batch_num):
    tobser,tmoni = param_generator(num_orbit, num_per_sate, inclination, h, R, num_obser, min_threld, obser_radius,sigma, min_monitor, method, i, filename)
    num_obser.append(tobser)
    max_monitor.append(tmoni)
for i in range(batch_num):
    tdiffer = np.load(filename+'\differ_'+str(i)+'.npy')
    tArea = np.load(filename+'\Area_'+str(i)+'.npy')
    tmatch = np.load(filename+'\match_'+str(i)+'.npy')
    decision(wstar, Astar, size, t, tl, tdds, hr, h, tdiffer, tArea, tmatch, num_obser[i], max_monitor[i])
    overlaparea_base(wstar, Astar, size, t, tl, tdds, hr, h, tdiffer, tArea, tmatch, num_obser[i], max_monitor[i])
    differ_base(wstar, Astar, size, t, tl, tdds, hr, h, tdiffer, tArea, tmatch, num_obser[i], max_monitor[i])

