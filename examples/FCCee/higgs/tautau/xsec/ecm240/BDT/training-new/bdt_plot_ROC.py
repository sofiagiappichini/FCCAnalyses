

import sys,os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import awkward as ak
import pandas as pd
import uproot
#from root_pandas import read_root, to_root
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import roc_curve, auc
import ROOT
import joblib
import glob
from matplotlib import rc
import pprint
from matplotlib.ticker import LogLocator, NullFormatter


def get_entries(infilepath: str) -> tuple[int, int]:
    '''
    Get number of original entries and number of actual entries in the file
    '''
    events_processed = 0
    events_in_ttree = 0

    with ROOT.TFile(infilepath, 'READ') as infile:
        try:
            events_processed_obj = infile.Get('eventsProcessed')
            if events_processed_obj:
                events_processed = events_processed_obj.GetVal()
            events_ttree = infile.Get("events")
            if events_ttree:
                events_in_ttree = events_ttree.GetEntries()
            else:
                return None, None

        except AttributeError:
            return None, None

    return events_processed, events_in_ttree

vars_list_NuNu_explicit = [
            "RecoEmiss_pz",
            "RecoEmiss_pt",
            "RecoEmiss_p",
            "RecoEmiss_e",
            "RecoEmiss_costheta",
            "RecoH_pz",
            "RecoH_p",
            "RecoH_pt",
            "RecoH_e",
            "RecoH_eta",
            "TauLead_pz",   
            "TauLead_p",   
            "TauLead_pt",   
            "TauLead_e",    
            "TauLead_eta",    
            "TauLead_mass",
            "TauSub_pz",   
            "TauSub_p",   
            "TauSub_pt",   
            "TauSub_e",    
            "TauSub_eta",    
            "TauSub_mass", 
            "Tau_DPhi",
            "Tau_DR",
            "Tau_cos",
            "Tau_DEta",
            "Visible_mass",
            ]

vars_list_NuNuHH_tag = [
            "RecoEmiss_pz",
            "RecoEmiss_pt",
            "RecoEmiss_p",
            "RecoEmiss_e",
            "RecoEmiss_costheta",
            "RecoH_pz",
            "RecoH_p",
            "RecoH_pt",
            "RecoH_e",
            "RecoH_eta",    
            "TauLead_pz",   
            "TauLead_p",   
            "TauLead_pt",   
            "TauLead_e",    
            "TauLead_eta",    
            "TauLead_mass",
            "TauLead_type",
            "n_TauLead_charged_constituents",
            "n_TauLead_neutral_constituents",
            "TauSub_pz",   
            "TauSub_p",   
            "TauSub_pt",   
            "TauSub_e",    
            "TauSub_eta",  
            "TauSub_mass",
            "TauSub_type",
            "n_TauSub_charged_constituents",
            "n_TauSub_neutral_constituents",
            "Tau_DPhi",
            "Tau_DR",
            "Tau_cos",
            "Tau_DEta",
            "Visible_mass",
            ]

vars_list_NuNuLH_tag = [
            "RecoEmiss_pz",
            "RecoEmiss_pt",
            "RecoEmiss_p",
            "RecoEmiss_e",
            "RecoEmiss_costheta",
            "RecoH_pz",
            "RecoH_p",
            "RecoH_pt",
            "RecoH_e",
            "RecoH_eta",    
            "TauLead_pz",   
            "TauLead_p",   
            "TauLead_pt",   
            "TauLead_e",    
            "TauLead_eta",    
            "TauLead_mass",
            "TauSub_pz",   
            "TauSub_p",   
            "TauSub_pt",   
            "TauSub_e",    
            "TauSub_eta", 
            "TauSub_mass",
            "Tau_DPhi",
            "Tau_DR",
            "Tau_cos",
            "Tau_DEta",
            "Visible_mass",
            "TauLepton_type",
            "TauHadron_type",
            "n_TauLepton_charged_constituents",
            "n_TauHadron_charged_constituents",
            "n_TauLepton_neutral_constituents",
            "n_TauHadron_neutral_constituents",
            ]

vars_list_QQ_explcit = [
            "RecoEmiss_pz",
            "RecoEmiss_pt",
            "RecoEmiss_p",
            "RecoEmiss_e",
            "RecoEmiss_costheta",
            "RecoZ_pz",
            "RecoZ_p",
            "RecoZ_pt",
            "RecoZ_e",
            "RecoZ_eta",
            "RecoZ_mass",
            "RecoH_pz",
            "RecoH_p",
            "RecoH_pt",
            "RecoH_e",
            "RecoH_eta",
            "RecoH_mass",
            "Tau_DPhi",
            "Tau_DR",
            "Tau_cos",
            "Tau_DEta",
            "Recoil",
            "Collinear_mass"]

vars_list_QQHH_tag = [
            "RecoEmiss_pz",
            "RecoEmiss_pt",
            "RecoEmiss_p",
            "RecoEmiss_e",
            "RecoEmiss_costheta",
            "RecoZ_pz",
            "RecoZ_p",
            "RecoZ_pt",
            "RecoZ_e",
            "RecoZ_eta",
            "RecoZ_mass",
            "RecoH_pz",
            "RecoH_p",
            "RecoH_pt",
            "RecoH_e",
            "RecoH_eta",
            "RecoH_mass",
            "TauLead_type",
            "n_TauLead_charged_constituents",
            "n_TauLead_neutral_constituents", 
            "TauSub_type",
            "n_TauSub_charged_constituents",
            "n_TauSub_neutral_constituents",
            "Tau_DPhi",
            "Tau_DR",
            "Tau_cos",
            "Tau_DEta",
            "Recoil",
            "Collinear_mass"]

vars_list_QQLH_tag = [
            "RecoEmiss_pz",
            "RecoEmiss_pt",
            "RecoEmiss_p",
            "RecoEmiss_e",
            "RecoEmiss_costheta",
            "RecoZ_pz",
            "RecoZ_p",
            "RecoZ_pt",
            "RecoZ_e",
            "RecoZ_eta",
            "RecoZ_mass",
            "RecoH_pz",
            "RecoH_p",
            "RecoH_pt",
            "RecoH_e",
            "RecoH_eta",
            "RecoH_mass",
            "Tau_DPhi",
            "Tau_DR",
            "Tau_cos",
            "Tau_DEta",
            "Recoil",
            "Collinear_mass",
            "TauLepton_type",
            "TauHadron_type",
            "n_TauLepton_charged_constituents",
            "n_TauLepton_neutral_constituents",
            "n_TauHadron_charged_constituents",
            "n_TauHadron_neutral_constituents",
            ]

DIRECTORY = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm365/BDT_250502/"

TAG = [
    #"R5-explicit",
    #"R5-tag",
    "ktN-explicit",
    "ktN-tag",
]
SUBDIR = [
    'LL',
    'LH',
    'HH',
]
#category to plot
CAT = [
    "QQ",
    "LL",
    "NuNu",
]

leg_cat = {
    "QQ": r"$Z \to qq,$",  # Use raw string and format for LaTeX
    "NuNu": r"$Z \to \nu \nu,$",
    "LL": r"$Z \to \ell\ell,$",
}

leg_sub = {
    "LL": r"$H \to \tau_\ell \tau_\ell$",
    "LH": r"$H \to \tau_\ell \tau_h$",
    "HH": r"$H \to \tau_h \tau_h$",
}

output_file = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm365/BDT_250502/output_overtraining.txt"

modelDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm365/BDT_250502/"

plotDir = "/eos/user/s/sgiappic/www/Higgs_xsec/ecm365/"

colorDict = [
    # Violets (more magenta-toned)
    '#5E2A84', 
    '#9A4DCC', 
    '#D6A7F2',

    # Blues (cooler, more cyan/indigo)
    '#03028D', 
    '#4E6BD3', 
    '#9FB5D7', 

    # Greens (as before, still distinct)
    '#004d00',  # Dark green
    '#4CAF50',  # Medium green
    '#B2FFB2'   # Light mint green
]

#get gen number of events for each signal and backgorund file
for tag in TAG:
    # Create the figure and plot
    fig, ax = plt.subplots(figsize=(8, 8))
    #index for color list and label list
    col = 0
    label = []
    for cat in CAT:
        for sub in SUBDIR:

            path = DIRECTORY + tag + "/"

            print(path)

            if "explicit" in tag:
                if "QQ" in cat or "LL" in cat:
                    vars_list = vars_list_QQ_explcit
                else:
                    vars_list = vars_list_NuNu_explicit
            else:
                if "QQ" in cat or "LL" in cat:
                    if "HH" in sub:
                        vars_list = vars_list_QQHH_tag
                    elif "LH" in sub:
                        vars_list = vars_list_QQLH_tag
                    else:
                        vars_list = vars_list_QQ_explcit
                else:
                    if "HH" in sub:
                        vars_list = vars_list_NuNuHH_tag
                    elif "LH" in sub:
                        vars_list = vars_list_NuNuLH_tag
                    else:
                        vars_list = vars_list_NuNu_explicit


            #Split into class label (y) and training vars (x)
            df_train = joblib.load(f"{modelDir}/{tag}/train_data_{tag}_{cat}{sub}.pkl")
            df_test = joblib.load(f"{modelDir}/{tag}/test_data_{tag}_{cat}{sub}.pkl")
            
            y = df_train["label"]
            x = df_train[vars_list]

            y_test = df_test["label"]
            x_test = df_test[vars_list]
            
            #import bdt already trained and test it 
            bdt = joblib.load(f"{modelDir}/{tag}/xgb_bdt_{tag}_{cat}{sub}.joblib")

            pred_test = bdt.predict_proba(x_test)

            # Calculate FPR, TPR, and AUC
            fpr, tpr, thresholds = roc_curve(y_test, pred_test[:, 1], pos_label=1)
            roc_auc = auc(fpr, tpr)

            # Plot the ROC curve
            plt.plot(fpr, tpr, lw=2, color=colorDict[col])

            col += 1
            print(leg_cat[cat], leg_sub[sub])

            label.append(f'{leg_cat[cat]} {leg_sub[sub]}, AUC={roc_auc:.3f}')

            print(f"Done: {cat}{sub}")

    # Plot the baseline for random classifier
    plt.plot([0., 1.], [0., 1.], linestyle="--", color="k", label='50/50')
    label.append('50/50')

    # Set limits and labels
    #plt.xlim(0., 1.)
    plt.ylim(0., 1.)
    plt.xscale('log')

    plt.ylabel('True Positive Rate', fontsize=18)  # 1 - FPR
    plt.xlabel('False Positive Rate', fontsize=18)  # TPR
    plt.title(f'FCC-ee Simulation (Delphes)', loc='right', fontsize=18)

    # Adjust ticks and legend
    ax.tick_params(axis='both', which='major', labelsize=15)
    plt.legend(label, loc="lower right", fontsize=15)
    plt.grid()
    plt.tight_layout()

    # Save the figure
    fig.savefig(f"{plotDir}/{tag}/BDT/BDT_ROC.pdf")
    fig.savefig(f"{plotDir}/{tag}/BDT/BDT_ROC.png")