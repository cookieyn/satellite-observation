import numpy as np

class satellite:
    def __init__(self,num_sate):
        self.num_sate = num_sate
    
    def differ_update(self,differ_data):
        self.differ = np.zeros((differ_data.shape[0],differ_data.shape[1]))
        for i in range(differ_data.shape[0]):
            for j in range(differ_data.shape[1]):
                self.differ[i,j] = differ_data[i,j]