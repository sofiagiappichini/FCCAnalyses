# from https://github.com/mpresill/PlotsConfigurations/blob/matteo/Configurations/VBS_ZV/scripts/rebinning.py#L23-L66
# relevant lines for rebinning only: 23-66 
# https://root.cern/doc/master/classTH1.html#a9eef6f499230b88582648892e5e4e2ce on rebin 
# requires python3 from key4hep stack sourcing, not cmsenv

import os
import ROOT
import shutil
from matplotlib import pyplot as plt
import pandas as pd
import array
import sys
import os.path
import ntpath
import importlib
import copy
import re
import logging
import numpy as np
import uproot

def sorted_dict_values(dic: dict) -> list:
    ''''
    Sort values in the dictionary.
    '''
    keys = sorted(dic)
    return [dic[key] for key in keys]

def make_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory created successfully.")
    else:
        print(f"Directory already exists.")

DIRECTORY = '/eos/user/s/sgiappic/2HNL_ana/final_august/' 

CUTS = [
    "selReco_gen_notracks_2eh_M80_10MET_0cos",
 ] # cut to rebin

SUBCUTS = [
    "10gev",
    "20gev",
    "30gev",
    "40gev",
    "50gev",
    "60gev",
    "70gev",
 ]

VARIABLE = "RecoEmiss_e" # variable to rebin

FILES = [
    #"p8_ee_Zee_ecm91",
    #"p8_ee_Zmumu_ecm91",
    #"p8_ee_Ztautau_ecm91",
    #"p8_ee_Zbb_ecm91",
    #"p8_ee_Zcc_ecm91",
    #"p8_ee_Zud_ecm91",
    #"p8_ee_Zss_ecm91",
    #"eenunu",
    #"mumununu",
    #"tatanunu",
    #"llnunu",
    
    "HNL_1.33e-7_10gev",
    "HNL_1.33e-7_20gev",
    "HNL_1.33e-7_30gev",
    "HNL_1.33e-7_40gev",
    "HNL_1.33e-7_50gev",
    "HNL_1.33e-7_60gev",
    "HNL_1.33e-7_70gev",
    "HNL_1.33e-7_80gev",

    "HNL_2.78e-8_10gev",
    "HNL_2.78e-8_20gev",
    "HNL_2.78e-8_30gev",
    "HNL_2.78e-8_40gev",
    "HNL_2.78e-8_50gev",
    "HNL_2.78e-8_60gev",
    "HNL_2.78e-8_70gev",
    "HNL_2.78e-8_80gev",

    "HNL_6.05e-9_10gev",
    "HNL_6.05e-9_20gev",
    "HNL_6.05e-9_30gev",
    "HNL_6.05e-9_40gev",
    "HNL_6.05e-9_50gev",
    "HNL_6.05e-9_60gev",
    "HNL_6.05e-9_70gev",
    "HNL_6.05e-9_80gev",

    "HNL_1.33e-9_10gev",
    "HNL_1.33e-9_20gev",
    "HNL_1.33e-9_30gev",
    "HNL_1.33e-9_40gev",
    "HNL_1.33e-9_50gev",
    "HNL_1.33e-9_60gev",
    "HNL_1.33e-9_70gev",
    "HNL_1.33e-9_80gev",

    "HNL_2.90e-10_10gev",
    "HNL_2.90e-10_20gev",
    "HNL_2.90e-10_30gev",
    "HNL_2.90e-10_40gev",
    "HNL_2.90e-10_50gev",
    "HNL_2.90e-10_60gev",
    "HNL_2.90e-10_70gev",
    "HNL_2.90e-10_80gev",

    "HNL_6.34e-11_10gev",
    "HNL_6.34e-11_20gev",
    "HNL_6.34e-11_30gev",
    "HNL_6.34e-11_40gev",
    "HNL_6.34e-11_50gev",
    "HNL_6.34e-11_60gev",
    "HNL_6.34e-11_70gev",
    "HNL_6.34e-11_80gev",

    "HNL_1.33e-11_10gev",
    "HNL_1.33e-11_20gev",
    "HNL_1.33e-11_30gev",
    "HNL_1.33e-11_40gev",
    "HNL_1.33e-11_50gev",
    "HNL_1.33e-11_60gev",
    "HNL_1.33e-11_70gev",
    "HNL_1.33e-11_80gev",

    

    "HNL_4e-8_10gev",
    "HNL_4e-8_20gev",
    "HNL_4e-8_30gev",
    "HNL_4e-8_40gev",
    "HNL_4e-8_50gev",
    "HNL_4e-8_60gev",
    "HNL_4e-8_70gev",
    "HNL_4e-8_80gev",

    "HNL_8.35e-9_10gev",
    "HNL_8.35e-9_20gev",
    "HNL_8.35e-9_30gev",
    "HNL_8.35e-9_40gev",
    "HNL_8.35e-9_50gev",
    "HNL_8.35e-9_60gev",
    "HNL_8.35e-9_70gev",
    "HNL_8.35e-9_80gev",

    "HNL_1.81e-9_10gev",
    "HNL_1.81e-9_20gev",
    "HNL_1.81e-9_30gev",
    "HNL_1.81e-9_40gev",
    "HNL_1.81e-9_50gev",
    "HNL_1.81e-9_60gev",
    "HNL_1.81e-9_70gev",
    "HNL_1.81e-9_80gev",

    "HNL_4e-10_10gev",
    "HNL_4e-10_20gev",
    "HNL_4e-10_30gev",
    "HNL_4e-10_40gev",
    "HNL_4e-10_50gev",
    "HNL_4e-10_60gev",
    "HNL_4e-10_70gev",
    "HNL_4e-10_80gev",

    "HNL_8.69e-11_10gev",
    "HNL_8.69e-11_20gev",
    "HNL_8.69e-11_30gev",
    "HNL_8.69e-11_40gev",
    "HNL_8.69e-11_50gev",
    "HNL_8.69e-11_60gev",
    "HNL_8.69e-11_70gev",
    "HNL_8.69e-11_80gev",

    "HNL_1.90e-11_10gev",
    "HNL_1.90e-11_20gev",
    "HNL_1.90e-11_30gev",
    "HNL_1.90e-11_40gev",
    "HNL_1.90e-11_50gev",
    "HNL_1.90e-11_60gev",
    "HNL_1.90e-11_70gev",
    "HNL_1.90e-11_80gev",

    "HNL_4e-12_10gev",
    "HNL_4e-12_20gev",
    "HNL_4e-12_30gev",
    "HNL_4e-12_40gev",
    "HNL_4e-12_50gev",
    "HNL_4e-12_60gev",
    "HNL_4e-12_70gev",
    "HNL_4e-12_80gev",

    

    "HNL_2.86e-8_10gev",
    "HNL_2.86e-8_20gev",
    "HNL_2.86e-8_30gev",
    "HNL_2.86e-8_40gev",
    "HNL_2.86e-8_50gev",
    "HNL_2.86e-8_60gev",
    "HNL_2.86e-8_70gev",
    "HNL_2.86e-8_80gev",

    "HNL_5.97e-9_10gev",
    "HNL_5.97e-9_20gev",
    "HNL_5.97e-9_30gev",
    "HNL_5.97e-9_40gev",
    "HNL_5.97e-9_50gev",
    "HNL_5.97e-9_60gev",
    "HNL_5.97e-9_70gev",
    "HNL_5.97e-9_80gev",

    "HNL_1.30e-9_10gev",
    "HNL_1.30e-9_20gev",
    "HNL_1.30e-9_30gev",
    "HNL_1.30e-9_40gev",
    "HNL_1.30e-9_50gev",
    "HNL_1.30e-9_60gev",
    "HNL_1.30e-9_70gev",
    "HNL_1.30e-9_80gev",

    "HNL_2.86e-10_10gev",
    "HNL_2.86e-10_20gev",
    "HNL_2.86e-10_30gev",
    "HNL_2.86e-10_40gev",
    "HNL_2.86e-10_50gev",
    "HNL_2.86e-10_60gev",
    "HNL_2.86e-10_70gev",
    "HNL_2.86e-10_80gev",

    "HNL_6.20e-11_10gev",
    "HNL_6.20e-11_20gev",
    "HNL_6.20e-11_30gev",
    "HNL_6.20e-11_40gev",
    "HNL_6.20e-11_50gev",
    "HNL_6.20e-11_60gev",
    "HNL_6.20e-11_70gev",
    "HNL_6.20e-11_80gev",

    "HNL_1.36e-11_10gev",
    "HNL_1.36e-11_20gev",
    "HNL_1.36e-11_30gev",
    "HNL_1.36e-11_40gev",
    "HNL_1.36e-11_50gev",
    "HNL_1.36e-11_60gev",
    "HNL_1.36e-11_70gev",
    "HNL_1.36e-11_80gev",

    "HNL_2.86e-12_10gev",
    "HNL_2.86e-12_20gev",
    "HNL_2.86e-12_30gev",
    "HNL_2.86e-12_40gev",
    "HNL_2.86e-12_50gev",
    "HNL_2.86e-12_60gev",
    "HNL_2.86e-12_70gev",
    "HNL_2.86e-12_80gev",

    ##inverted

    "HNL_5e-8_10gev",
    "HNL_5e-8_20gev",
    "HNL_5e-8_30gev",
    "HNL_5e-8_40gev",
    "HNL_5e-8_50gev",
    "HNL_5e-8_60gev",
    "HNL_5e-8_70gev",
    "HNL_5e-8_80gev",

    "HNL_1.04e-8_10gev",
    "HNL_1.04e-8_20gev",
    "HNL_1.04e-8_30gev",
    "HNL_1.04e-8_40gev",
    "HNL_1.04e-8_50gev",
    "HNL_1.04e-8_60gev",
    "HNL_1.04e-8_70gev",
    "HNL_1.04e-8_80gev",

    "HNL_2.27e-9_10gev",
    "HNL_2.27e-9_20gev",
    "HNL_2.27e-9_30gev",
    "HNL_2.27e-9_40gev",
    "HNL_2.27e-9_50gev",
    "HNL_2.27e-9_60gev",
    "HNL_2.27e-9_70gev",
    "HNL_2.27e-9_80gev",

    "HNL_5e-10_10gev",
    "HNL_5e-10_20gev",
    "HNL_5e-10_30gev",
    "HNL_5e-10_40gev",
    "HNL_5e-10_50gev",
    "HNL_5e-10_60gev",
    "HNL_5e-10_70gev",
    "HNL_5e-10_80gev",

    "HNL_1.09e-10_10gev",
    "HNL_1.09e-10_20gev",
    "HNL_1.09e-10_30gev",
    "HNL_1.09e-10_40gev",
    "HNL_1.09e-10_50gev",
    "HNL_1.09e-10_60gev",
    "HNL_1.09e-10_70gev",
    "HNL_1.09e-10_80gev",

    "HNL_2.38e-11_10gev",
    "HNL_2.38e-11_20gev",
    "HNL_2.38e-11_30gev",
    "HNL_2.38e-11_40gev",
    "HNL_2.38e-11_50gev",
    "HNL_2.38e-11_60gev",
    "HNL_2.38e-11_70gev",
    "HNL_2.38e-11_80gev",

    "HNL_5e-12_10gev",
    "HNL_5e-12_20gev",
    "HNL_5e-12_30gev",
    "HNL_5e-12_40gev",
    "HNL_5e-12_50gev",
    "HNL_5e-12_60gev",
    "HNL_5e-12_70gev",
    "HNL_5e-12_80gev",

    

    "HNL_6.67e-8_10gev",
    "HNL_6.67e-8_20gev",
    "HNL_6.67e-8_30gev",
    "HNL_6.67e-8_40gev",
    "HNL_6.67e-8_50gev",
    "HNL_6.67e-8_60gev",
    "HNL_6.67e-8_70gev",
    "HNL_6.67e-8_80gev",

    "HNL_1.39e-8_10gev",
    "HNL_1.39e-8_20gev",
    "HNL_1.39e-8_30gev",
    "HNL_1.39e-8_40gev",
    "HNL_1.39e-8_50gev",
    "HNL_1.39e-8_60gev",
    "HNL_1.39e-8_70gev",
    "HNL_1.39e-8_80gev",

    "HNL_3.02e-9_10gev",
    "HNL_3.02e-9_20gev",
    "HNL_3.02e-9_30gev",
    "HNL_3.02e-9_40gev",
    "HNL_3.02e-9_50gev",
    "HNL_3.02e-9_60gev",
    "HNL_3.02e-9_70gev",
    "HNL_3.02e-9_80gev",

    "HNL_6.67e-10_10gev",
    "HNL_6.67e-10_20gev",
    "HNL_6.67e-10_30gev",
    "HNL_6.67e-10_40gev",
    "HNL_6.67e-10_50gev",
    "HNL_6.67e-10_60gev",
    "HNL_6.67e-10_70gev",
    "HNL_6.67e-10_80gev",

    "HNL_1.45e-10_10gev",
    "HNL_1.45e-10_20gev",
    "HNL_1.45e-10_30gev",
    "HNL_1.45e-10_40gev",
    "HNL_1.45e-10_50gev",
    "HNL_1.45e-10_60gev",
    "HNL_1.45e-10_70gev",
    "HNL_1.45e-10_80gev",

    "HNL_3.17e-11_10gev",
    "HNL_3.17e-11_20gev",
    "HNL_3.17e-11_30gev",
    "HNL_3.17e-11_40gev",
    "HNL_3.17e-11_50gev",
    "HNL_3.17e-11_60gev",
    "HNL_3.17e-11_70gev",
    "HNL_3.17e-11_80gev",

    "HNL_6.67e-12_10gev",
    "HNL_6.67e-12_20gev",
    "HNL_6.67e-12_30gev",
    "HNL_6.67e-12_40gev",
    "HNL_6.67e-12_50gev",
    "HNL_6.67e-12_60gev",
    "HNL_6.67e-12_70gev",
    "HNL_6.67e-12_80gev",

    

    "HNL_2.86e-7_10gev",
    "HNL_2.86e-7_20gev",
    "HNL_2.86e-7_30gev",
    "HNL_2.86e-7_40gev",
    "HNL_2.86e-7_50gev",
    "HNL_2.86e-7_60gev",
    "HNL_2.86e-7_70gev",
    "HNL_2.86e-7_80gev",

    "HNL_5.97e-8_10gev",
    "HNL_5.97e-8_20gev",
    "HNL_5.97e-8_30gev",
    "HNL_5.97e-8_40gev",
    "HNL_5.97e-8_50gev",
    "HNL_5.97e-8_60gev",
    "HNL_5.97e-8_70gev",
    "HNL_5.97e-8_80gev",

    "HNL_1.30e-8_10gev",
    "HNL_1.30e-8_20gev",
    "HNL_1.30e-8_30gev",
    "HNL_1.30e-8_40gev",
    "HNL_1.30e-8_50gev",
    "HNL_1.30e-8_60gev",
    "HNL_1.30e-8_70gev",
    "HNL_1.30e-8_80gev",

    "HNL_2.86e-9_10gev",
    "HNL_2.86e-9_20gev",
    "HNL_2.86e-9_30gev",
    "HNL_2.86e-9_40gev",
    "HNL_2.86e-9_50gev",
    "HNL_2.86e-9_60gev",
    "HNL_2.86e-9_70gev",
    "HNL_2.86e-9_80gev",

    "HNL_6.20e-10_10gev",
    "HNL_6.20e-10_20gev",
    "HNL_6.20e-10_30gev",
    "HNL_6.20e-10_40gev",
    "HNL_6.20e-10_50gev",
    "HNL_6.20e-10_60gev",
    "HNL_6.20e-10_70gev",
    "HNL_6.20e-10_80gev",

    "HNL_1.36e-10_10gev",
    "HNL_1.36e-10_20gev",
    "HNL_1.36e-10_30gev",
    "HNL_1.36e-10_40gev",
    "HNL_1.36e-10_50gev",
    "HNL_1.36e-10_60gev",
    "HNL_1.36e-10_70gev",
    "HNL_1.36e-10_80gev",

    "HNL_2.86e-11_10gev",
    "HNL_2.86e-11_20gev",
    "HNL_2.86e-11_30gev",
    "HNL_2.86e-11_40gev",
    "HNL_2.86e-11_50gev",
    "HNL_2.86e-11_60gev",
    "HNL_2.86e-11_70gev",
    "HNL_2.86e-11_80gev",
]

for cut in CUTS:

    output_file = "/eos/user/s/sgiappic/2HNL_ana/" + cut + "_" + VARIABLE + "_minbin.txt"

    for file in FILES:

        #if "10gev" in file:
            
            histo_file_path = DIRECTORY + file + "_" + cut + "_DF_histo.root"

            # Get the selected leaf from the tree
            histo_file = uproot.open(histo_file_path)

            selected_leaf = histo_file[VARIABLE]

            # Get scaled number of events from histograms, array
            y_values = selected_leaf.values()

            # Get bin edges in arrays
            bin_edges = selected_leaf.axis().edges()

            entries = []

            for i in range(len(y_values)):
                if y_values[i]!=0:
                    entries.append(bin_edges[i])

            min = np.min(entries)

            with open(output_file, "a") as f:
                f.write("File {} has min bin non empty in {} \n".format(file, min))
