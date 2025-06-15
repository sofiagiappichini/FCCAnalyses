#This adapts train_xgb.py for training of a NN inststead

import sys,os, argparse
#import json
import numpy as np
import matplotlib.pyplot as plt
#import awkward as ak
import pandas as pd
#import uproot
#from root_pandas import read_root, to_root
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import roc_curve, auc
# import ROOT
# import joblib
#import glob
from matplotlib import rc
#import pprint
#from higgs_config import *
#from topVts_config import *
#from training_variables import *
#from model import CNN_Model
#from model import DNN

import torch
from torch.utils.data import DataLoader, TensorDataset
import torch.optim as optim
import torch.nn as nn

#import shap #we'll need that later

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

#import local code

from models import Linear_Learning
from NN_user_config import train_vars_vtx, loc, mode_names, data_preparation

#from userConfig import loc,  train_vars, train_vars_vtx, mode_names probably a seperate config makes sense here



def Test_train(train_loader, model = Linear_Learning(len(train_vars_vtx)), num_epochs = 2):
    """
    Training loop for the NN
    inputs:


    returns:
    
    """


    #log_file = ''
    print('training func started') # when executing this is still printed but the next print isn't there is an error pertaining to onnx format that isn't even used, this is even the case when commenting all code in between
    
    model.train()
    # Loss function ans optimizer
    criterion = nn.BCELoss(reduction='none')
    
    optimizer = optim.Adam(model.parameters(), lr=0.0001)

    print("Training model")
    # Traingloop
    

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        n_batches = 0
        print('Start Epoch')
        for batch_idx, (inputs, labels, weights) in enumerate(train_loader): 

                # iput data
                  # new form: (batch_size, 1, num_input_params)
                labels = labels.unsqueeze(1)
                # Forward-Pass
                #print(labels)



                #look at input data 

                
                outputs = model(inputs)
                #print(outputs)
                
                # apply losses of the individual events
                loss = criterion(outputs, labels)
                print(loss)
                #weighted_loss = loss * event_weights

                # calculate loss for the batch (sum of the weighted losses)
                batch_loss = (weights*loss).mean()
                #print(batch_loss)
                # Backward-Pass and optimization
                optimizer.zero_grad()  # reset gradient
                batch_loss.backward()  # calculate gradient
                optimizer.step()  # update parameters

                # cumulate loss
                running_loss += batch_loss.item()

            # Ausgabe des Verlusts nach jeder Epoche
        print(f'Epoche [{epoch+1}/{num_epochs}], Verlust: {running_loss/len(train_loader):.4f}')
            
    #Saving Model
    model.eval()
    #torch_input = torch.randn(64,1,globals()[f'num_vars_{c+s}']) ???
    
    print('Saving model')
    torch.save(model.state_dict(), '/work/awiedl/FCCAnalyses/Testing_NN/trained_model.pt')

def model_test (num , model_path = '/work/awiedl/FCCAnalyses/Testing_NN/trained_model.pt' ,  model = Linear_Learning):
    """
    evaluates performance of the NN previously trained. 
    inputs: model_path
            num --> number of training variables

    outputs
    """
    model = model(num)
    model.load_state_dict(torch.load(model_path)) #loads previously trained model
    model.eval()
       
    #initialize eval variables
    corr = 0
    incorr = 0

    #
    explainer = shap.DeepExplainer(model, x_test[:1000])  
    shap_values = explainer.shap_values(x_test[:1000], check_additivity = False) 
    shap_values = np.squeeze(shap_values)

    shap.summary_plot(shap_values, x_test[:1000], feature_names = train_vars_vtx , max_display = num) # MODIFY

    plt.savefig(f'/work/awiedl/FCCAnalyses/Testing_NN/trained_model_eval.pdf') #INSERT file path
    plt.close()

    dataset = TensorDataset(x_test, y_test) 
    for data, label in dataset:
        #if model_struct == 'CNN': why does thies exist ??
        #    data = data.unsqueeze(0).unsqueeze(1)
        y_pred = model(data).flatten()
        if (y_pred >= 0.5 and label == 1):
            corr += 1
        elif (y_pred <= 0.5 and label == 0):
            corr += 1 
        else: 
            incorr += 1
        print('Acc:', corr/(corr+incorr))
        #with open(log_file, "a") as file:
        #    file.write(f"       Acc: {corr/(corr+false)}\n")

        x_test, y_test = dataset.tensors
        x_test = x_test.unsqueeze(1)
        pred_test = model(x_test)
        y_test = y_test.detach().numpy()
        pred_test = pred_test.detach().numpy().flatten()
        
        # Calculate FPR, TPR, and AUC
        fpr, tpr, thresholds = roc_curve(y_test, pred_test, pos_label=1)
        roc_auc = auc(fpr, tpr)

        # Create the figure and plot
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_title('TITLE', loc='right', fontsize=20)

        # Plot the ROC curve
        plt.plot(fpr, tpr, lw=1.5, color="k", label=f'ROC (area = {roc_auc:.3f})')

        # Plot the baseline for random classifier
        plt.plot([0., 1.], [0., 1.], linestyle="--", color="k", label='50/50')

        # Set limits and labels
        plt.xlim(0., 1.)
        plt.ylim(0., 1.)
        plt.ylabel('Background rejection', fontsize=30)  # 1 - FPR
        plt.xlabel('Signal efficiency', fontsize=30)  # TPR

        # Adjust ticks and legend
        ax.tick_params(axis='both', which='major', labelsize=25)
        plt.legend(loc="lower left", fontsize=20)
        plt.grid()
        plt.tight_layout()

        # Save the figure
        fig.savefig(f"/work/awiedl/FCCAnalyses/Testing_NN/model_eval_fig.pdf")

    
    
    

def main(): # needs modification for specifics required
    parser = argparse.ArgumentParser(description='Train NN for Bc -> tau nu vs. Z -> qq, cc, bb')
    parser.add_argument("--Purpose", choices=["train","evaluate"],required=False,help="Event-level vars (normal) or added vertex vars (vtx)",default="train")
    args = parser.parse_args()


    train_loader, test_datasetx, test_datasety = data_preparation()


    if args.Purpose == "train":
        print('Start traininf func ')
        Test_train(train_loader)

    #if args.Purpose == "evaluate":
    #    model_test(test_dataset)

    else:
        print('Something went wrong')

    

if __name__ == '__main__':
    main()


