import gurobipy as gp
from gurobipy import GRB
import numpy as np
import random
import time

def decision(wstar, Astar, size, t, tl, tdds, hr, h, tdiffer, tArea, tmatch, num_obser, max_monitor, num_sate):
    differ = tdiffer.copy()
    Area = tArea.copy()
    match = tmatch.copy()
    m = gp.Model('control')
    m.setParam('TimeLimit', 40)
    X = {}
    lr = {}
    y = {}
    for i in range(num_obser):
        for j in range(max_monitor):
            X[i,j] = m.addVar(0,1,vtype = GRB.BINARY, name = "picture"+str(i)+'-'+str(j))
    for i in range(num_obser):
        for j in range(max_monitor):
            lr[i,j] = m.addVar(0,1,vtype = GRB.CONTINUOUS,name = "low-resolution"+str(i)+'-'+str(j))
    for i in range(num_obser):
        for j in range(max_monitor):
            y[i,j] = m.addVar(0,1,vtype = GRB.CONTINUOUS,name = "interact"+str(i)+'-'+str(j))
    print("xishu")

    for i in range(num_obser):
        num = 0
        for j in range(max_monitor):
            if match[i,j] == -1:
                m.addConstr(X[i,j] == 0, name = "constr")
                num = num + 1
        #if num > 0 :
            #print(num)

    # lhs1 = gp.LinExpr(0)
    # c1 =  h * hr *size
    # for i in range(num_obser):
    #     for j in range(max_monitor):
    #         lhs1.addTerms(c1/t,X[i,j])  
    #         lhs1.addTerms(size/t,y[i,j])
    # m.addConstr(lhs1 <= wstar, name= "bandwidth") 

    lhs1 = [gp.LinExpr(0) for i in range(num_sate)]
    c1 =  h * hr *size
    for i in range(num_obser):
        for j in range(max_monitor):
            if match[i,j] > -1 :
                lhs1[int(match[i,j])].addTerms(c1/t,X[i,j])
                lhs1[int(match[i,j])].addTerms(size/t,y[i,j])
    for i in range(num_sate):
        m.addConstr(lhs1[i] <= wstar, name = "bandwidth"+str(i)+"-"+str(j))

    lhs2 = gp.LinExpr(0) 
    c2 = tdds
    for i in range(num_obser):
        for j in range(max_monitor):
            lhs2.addTerms(c2,y[i,j])  
    m.addConstr(lhs2 <= tl, name= "latency") 

    for i in range(num_obser):
        lhs3 = gp.LinExpr(0) 
        for j in range(max_monitor):
            lhs3.addTerms(c1/t,X[i,j])
            lhs3.addTerms(size/t,y[i,j])
        m.addConstr(lhs3 >= Astar, name= "accuracy"+str(j))

    for i in range(num_obser):
        for j in range(max_monitor):
            m.addConstr(y[i,j] <= X[i,j], name= "handle1"+str(i)+str(j)) 
            m.addConstr(y[i,j] <= lr[i,j], name= "handle2"+str(i)+str(j)) 
            m.addConstr(y[i,j] >= lr[i,j] + X[i,j] - 1, name= "handle3"+str(i)+str(j)) 

    obj = gp.LinExpr(0)
    for i in range(num_obser):
        for j in range(max_monitor):
            obj.addConstant(differ[i,j])
            obj.addTerms(-1*differ[i,j], y[i,j])
    m.setObjective(obj, GRB.MINIMIZE)  
    print("yuesu")
    time1=time.time()
    m.optimize()
    print("\n\n-----optimal value-----")
    try : 
        print(m.ObjVal)
    except AttributeError :
        return "No"
    else :
        return "Yes"

            


        
        
