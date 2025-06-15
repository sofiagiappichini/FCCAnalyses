##define NN 

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# local code


#First basic, linear NN for testing

class Linear_Learning(nn.Module):
    """ 
    NN only relying on linear learning, i.e. nn.Linear module; entirely for testing purposes
    
    nn.Module:

    functions:
    __init__(self, num_input_params): initializes instance of the class, calls __init_ of the parent class and creates Layers with nn.Linear; takes inputs self and num_input_parameters 
    forward(self, x) specifies operations on input data, is called upon automatically when passing data to the model; do NOT call explicitly (see pytorch Tutorial)


    """
    def __init__(self, num_input_params):
        """
        initializes instance of the class, calls __init_ of the parent class and creates Layers with nn.Linear
        takes inputs self and num_input_parameters 
        """
        super(Linear_Learning, self).__init__()
        self.fcin = nn.Linear(num_input_params,  num_input_params)
        
        self.fc1 = nn.Linear( num_input_params, 4 ) #* num_input_params
        #self.fc2 = nn.Linear(4 * num_input_params, 4)

        self.out = nn.Linear(4,1)


    def forward(self, x):
        """
        specifies operations on input data, is called upon automatically when passing data to the model; do NOT call explicitly (see pytorch Tutorial)
        Variables:
        self: class instance
        x : 

        returns: x

        """

        x = torch.relu(self.fcin(x))
        x = torch.relu(self.fc1(x))
        #x = torch.relu(self.fc2(x))
        x = torch.sigmoid(self.out(x))

        return x 





