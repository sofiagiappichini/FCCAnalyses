##configure variables and paths to train the NN
#source /cvmfs/sw.hsf.org/key4hep/setup.sh -r 2024-03-10


import sys,os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import roc_curve, auc
#from root_pandas import read_root
import uproot
import ROOT
import joblib
import glob
import torch
from torch.utils.data import DataLoader, TensorDataset

#Define training variables

train_vars_vtx = ["EVT_ThrustEmin_E",
                  "EVT_ThrustEmax_E",
                  "EVT_ThrustEmin_Echarged",
                  "EVT_ThrustEmax_Echarged",
                  "EVT_ThrustEmin_Eneutral",
                  "EVT_ThrustEmax_Eneutral",
                  "EVT_ThrustEmin_Ncharged",
                  "EVT_ThrustEmax_Ncharged",
                  "EVT_ThrustEmin_Nneutral",
                  "EVT_ThrustEmax_Nneutral",
                  "EVT_NtracksPV",
                  "EVT_NVertex",
                  "EVT_NTau23Pi",
                  "EVT_ThrustEmin_NDV",
                  "EVT_ThrustEmax_NDV",
                  "EVT_dPV2DVmin",
                  "EVT_dPV2DVmax",
                  "EVT_dPV2DVave"
                  ]

vars_list = train_vars_vtx


#construct filepaths

repo = "/ceph/xzuo/FCC_ntuples/BuBc2TauNu/stage1_pkl"

class loc : pass
loc.ROOT = repo+'/'

loc.DATA = loc.ROOT+''#data

loc.PKL = loc.DATA+'' #/pkl HIER passiert der spannende Teil


#Loaction of prod_04 tuples used in analysis
loc.PROD = f"{repo}/flatNtuples/spring2021/prod_04"

#Samples for first stage BDT training
loc.TRAIN = f"{loc.PROD}/Batch_Training_4stage1/"

mode_names = {"Bc2TauNu": "p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU",
              "Bu2TauNu": "p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU",
              "uds": "p8_ee_Zuds_ecm91",
              "cc": "p8_ee_Zcc_ecm91",
              "bb": "p8_ee_Zbb_ecm91"
              }


def data_preparation(debug = False):
    """
    prepares data in order to be used to train the test NN

    returns: train_loader, x_test_tensor, y_test_tensor
    
    """
    path = f"{loc.PKL}"
    df_sig = pd.read_pickle(f"{path}/Bc2TauNu.pkl")
    df_sig = df_sig[vars_list]
    print(f"Number of signal events: {len(df_sig)}")

    #Z -> qq inclusive
    n_tot_bkg = 1e6
    BF = {}
    BF["bb"] = 0.1512
    BF["cc"] = 0.1203
    BF["uds"] = 0.6991 - BF["bb"] - BF["cc"]

    # Efficiency of the pre-selection equirements on each bkg
    eff = {}
    #Number of generated events for each background type
    N = {}

    bkgs = ["uds","cc","bb"]

    #Loop over all background files and calculate total number of generated events
    for q in bkgs:
        path_gen = f"{loc.TRAIN}/{mode_names[q]}"

        #List of all sub-files in the path
        # files = glob.glob(f"{path_gen}/*.root") # somehow it appears, that with the given dataset there are no root files to be found here. This produces a problem in efficiency calculations down the line
      

        if q == "uds":
            N[q] = 2e8

        elif q == "cc":
            N[q] = 2e8

        elif q == "bb":
            N[q] = 6e8

    #     N[q] = 0
    #     for f in files:
    #         tree = uproot.open(f)["metadata"]
    #         df_gen = tree.arrays(library="pd")
    #         #df_gen = read_root(f,"metadata")
    #         N[q] = N[q] + df_gen.iloc[0]["eventsProcessed"]
    


    df_bkg = {}

    for q in bkgs:
        df_bkg[q] = pd.read_pickle(f"{path}/{q}.pkl")#,usecols=vars_list)
        df_bkg[q] = df_bkg[q][vars_list]
        print(f"Total size of {q} sample: {len(df_bkg[q])}")
        eff[q] = float(len(df_bkg[q]))/N[q]
        #eff[q] = float(len(df_bkg[q]))/100000
        print(f"Efficiency of pre-selection on {q} sample: {eff[q]}")
    BF_tot = eff["uds"]*BF["uds"] + eff["cc"]*BF["cc"] + eff["bb"]*BF["bb"]
    for q in bkgs:
        df_bkg[q] = df_bkg[q].sample(n=int(n_tot_bkg*(eff[q]*BF[q]/BF_tot)),random_state=10)
        print(f"Size of {q} in combined sample: {len(df_bkg[q])}")

    #Make a combined background sample according to BFs
    df_bkg_tot = df_bkg["uds"].append(df_bkg["cc"])
    df_bkg_tot = df_bkg_tot.append(df_bkg["bb"])
    #Shuffle the background so it is an even mixture of the modes
    df_bkg_tot = df_bkg_tot.sample(frac=1)

    #Signal and background labels
    df_sig["label"] = 1
    df_bkg_tot["label"] = 0

    #Combine the datasets
    df_tot = df_sig.append(df_bkg_tot)

    train, test = train_test_split(df_tot, train_size=0.7, test_size=0.3, random_state=12)

    # print('Training label')
    # print(train["label"][0:4])

    # print('Training variables:')
    # print(train[vars_list][0:4])

    # print('Testing variables:')
    # print(test[vars_list][0:4])


    #Split into class label (y) and training vars (x)
    y = train["label"]
    x = train[vars_list]

    y_test = test["label"]
    x_test = test[vars_list]

    #print(x_test[0:4])

    y_test = y_test.to_numpy() 
    x_test = x_test.to_numpy()
    # print('Test x')
    # print(x_test[0:4])

    y = y.to_numpy()
    x = x.to_numpy()

    # print('Train x')
    # print(x[0:4])

    #convert to tensor
    x_tensor = torch.tensor(x, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.float32)
    #w_tensor = torch.tensor(w, dtype=torch.float32)
    x_test_tensor = torch.tensor(x_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

    w = compute_sample_weight(class_weight='balanced', y=y) # I don't know if this is the correct calculation of these weights, this need FURTHER INVESTIGATION

    w_tensor = torch.tensor(w, dtype=torch.float32)


    
    

    dataset = TensorDataset(x_tensor, y_tensor, w_tensor)
    train_loader = DataLoader(dataset, batch_size=64, shuffle=debug) #shuffle needs to be activated for actual running !!!
    print('Dataprep done !')
    if debug == True:
        return x_tensor, y_tensor, x_test_tensor, y_test_tensor, w_tensor, train_loader
    train_features, train_labels,_ = next(iter(train_loader))
    print(train_features[0:1])
    return train_loader, x_test_tensor, y_test_tensor



def main():
    x,y,xt,yt, w_tensor, train = data_preparation(debug = True)
    print(x.size())
    train_features, train_labels,_ = next(iter(train))
    print(train_features.size())
    print(x[0:1])
    print(y[0:1])
    #print(yt[0:4])
    print(w_tensor[0:1])
    print(train_features[0:1])
    print(train_labels[0:1])
    print(_[0:1])

if __name__ == '__main__':
    main()