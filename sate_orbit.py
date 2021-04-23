import numpy as np
import random
import math
import xlrd

def createOrbit(num_orbit, num_per_sate, inclination, h, R):
    r = R + h
    per_orbit = 2 * math.pi / num_orbit
    per_sate = 2 * math.pi / num_per_sate
    num_sate = num_orbit * num_per_sate
    satellite = np.zeros((num_sate, 3))
    order = 0
    for i in range(num_orbit):
        e1 = [math.cos(i*per_orbit),-math.sin(i*per_orbit),0]
        e2 = [math.sin(i*per_orbit) * math.cos(inclination), math.cos(i*per_orbit) * math.cos(inclination), math.sin(inclination)]
        for j in range(num_per_sate):
            persate = [r * math.cos(j*per_sate) * e1[k] + r * math.sin(j*per_sate) * e2[k] for k in range(3)]
            S_r = math.sqrt(persate[0] ** 2 + persate[1] ** 2 + persate[2] ** 2)
            if persate[2] == 0 :
                S_theta = math.pi / 2
            else :
                S_theta = math.atan(math.sqrt(persate[0] ** 2 + persate[1] ** 2)/persate[2])
            if persate[0] == 0 :
                S_fi = math.pi / 2
            else :
                S_fi = math.atan(persate[1]/persate[0])
            satellite[order,0] = S_r
            satellite[order,1] = S_theta
            satellite[order,2] = S_fi
            order = order + 1
    return satellite

def addOrbit(num_orbit, num_per_sate, inclination, h, satellite, R):
    r = R + h
    per_orbit = 2 * math.pi / num_orbit
    per_sate = 2 * math.pi / num_per_sate
    num_sate = num_orbit * num_per_sate
    order = 0
    for i in range(num_orbit):
        e1 = [math.cos(i*per_orbit),-math.sin(i*per_orbit),0]
        e2 = [math.sin(i*per_orbit) * math.cos(inclination), math.cos(i*per_orbit) * math.cos(inclination), math.sin(inclination)]
        for j in range(num_per_sate):
            persate = [R * math.cos(j*per_sate) * e1[k] + R * math.sin(j*per_sate) * e2[k] for k in range(3)]
            S_r = math.sqrt(persate[0] ** 2 + persate[1] ** 2 + persate[2] ** 2)
            if persate[2] == 0 :
                S_theta = math.pi / 2
            else :
                S_theta = math.atan(math.sqrt(persate[0] ** 2 + persate[1] ** 2)/persate[2])
            if persate[0] == 0 :
                S_fi = math.pi / 2
            else :
                S_fi = math.atan(persate[1]/persate[0])
            satellite = np.append(satellite, np.array([[S_r,S_theta,S_fi]]),axis = 0 )
            order = order + 1
    return satellite
    
def computeArea(satellite,observation,i,j,obser_raius,R):
    a = obser_raius
    #b = math.sqrt(satellite[j,0] ** 2 - R **2) * R / satellite[j,0]
    b = 500
    x1 = observation[i,0] * math.sin(observation[i,1]) * math.cos(observation[i,2])
    y1 = observation[i,0] * math.sin(observation[i,1]) * math.sin(observation[i,2])
    z1 = observation[i,0] * math.cos(observation[i,1])
    x2 = satellite[j,0] * math.sin(satellite[j,1]) * math.cos(satellite[j,2])
    y2 = satellite[j,0] * math.sin(satellite[j,1]) * math.sin(satellite[j,2])
    z2 = satellite[j,0] * math.cos(satellite[j,1])
    c = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
    #print(a,b,c)
    if c > (a + b):
        area = 0
    elif b > (a + c):
        area = 1
    elif a > (b + c):
        area = b **2 / a ** 2
    else:
        beta1 = math.acos((a ** 2 + c ** 2 - b ** 2) / (2*a*c))
        beta2 = math.acos((b ** 2 + c ** 2 - a ** 2) / (2*b*c))
        overlapa = a ** 2 * beta1 + b ** 2 * beta2 - a * b * math.sin(beta1 + beta2)
        area = overlapa / (math.pi * a ** 2)
    return area

def match_change(num_obser,num_sate,max_monitor,totalarea,totaldiffer,min_threld):
    match = np.zeros((num_obser,max_monitor))
    for i in range(num_obser):
        for j in range(max_monitor):
            match[i,j] = -1
    overlap_area = np.zeros((num_obser,max_monitor))
    tempdiffer = np.zeros((num_obser,max_monitor))
    for i in range(num_obser):
        order = 0
        for j in range(num_sate):
            o_area = totalarea[i,j]
            if o_area > min_threld:
                #print(o_area)
                match[i,order] = j
                overlap_area[i,order] = o_area
                tempdiffer[i,order] = totaldiffer[i,j]
                order = order + 1
    return match,overlap_area,tempdiffer

def createObser(num,R,method):
    observation = np.zeros((num,3))
    if method == "random":
        for i in range(num):
            observation[i,0] = R
            observation[i,1] = 0.206 * math.pi + random.random() * 0.41 * math.pi
            observation[i,2] = random.random() * 2 * math.pi
    if method == "population":
        latitude = [x*math.pi/180 for x in range(0, 180)]
        longitude = [x*math.pi/180 for x in range(0, 360)]
        xl = xlrd.open_workbook(r'population.xlsx')
        table = xl.sheets()[0]
        p_lati = table.col_values(0)[:180]
        p_logi = table.col_values(1)
        #还要变换成pi形式
        for i in range(num):
            observation[i,0] = R
            observation[i,1] = np.random.choice(latitude, p = p_lati) + random.random() * 1 / 180 * math.pi
            observation[i,2] = np.random.choice(longitude, p = p_logi) + random.random() * 1 / 180 * math.pi
    return observation

def creatediffer(num_obser,num_sate,sigma,area):
    differ = np.zeros((num_obser,num_sate))
    for i in range(num_obser):
        for j in range(num_sate):
            tdiffer = max(0,random.gauss(10*area[i,j],sigma))
            differ[i,j] = tdiffer
    return differ

def orbit_generator(num_orbit, num_per_sate, inclination, h, R, min_threld, obser_radius,sigma, min_monitor, method):
    num_sate = num_orbit * num_per_sate
    sate = createOrbit(num_orbit, num_per_sate, inclination, h, R)
    sate = addOrbit(32, 50, 0.294*math.pi, 1110, sate, R)
    num_sate = num_sate + 32 * 50 
    return sate,num_sate

def param_generator(sate, num_sate, R, num_obser, min_threld, obser_radius,sigma, min_monitor, method, ind, filename):
    totalarea = np.zeros((num_obser,num_sate))
    obser = createObser(num_obser,R,method)
   
    max_monitor = -np.inf
    non_monitor = []
    total_num = 0
    for i in range(num_obser):
        #print(i)
        num_order = 0
        for j in range(num_sate):
            totalarea[i,j] = computeArea(sate,obser,i,j,obser_radius,R)
            
            #print(totalarea[i,j])
            if totalarea[i,j] > min_threld:
                num_order = num_order + 1
        if num_order <= min_monitor :
            non_monitor.append(i)
        if num_order > max_monitor:
            max_monitor = num_order
        total_num = total_num + num_order
    print("avarage sate:")
    print(total_num/num_obser)
    print("non sate:")
    print(len(non_monitor))
    obser = np.delete(obser,[non_monitor],axis = 0)
    totalarea = np.delete(totalarea,[non_monitor],axis = 0)
    num_obser = num_obser - len(non_monitor)
    print("shape,obser number,max monitor:")
    print(totalarea.shape)
    print(num_obser)
    print(max_monitor)
    
    totaldiffer = creatediffer(num_obser,num_sate,sigma,totalarea)
    resmatch,resarea,resdiffer = match_change(num_obser,num_sate,max_monitor,totalarea,totaldiffer,min_threld)
    
    np.save(filename+'/match_'+str(ind)+'.npy',resmatch)
    np.save(filename+'/differ_'+str(ind)+'.npy',resdiffer)
    np.save(filename+'/area_'+str(ind)+'.npy',resarea)

    return num_obser,max_monitor
