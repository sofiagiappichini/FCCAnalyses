

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
from sklearn.metrics import roc_curve, auc, accuracy_score
import ROOT
import joblib
import glob
from matplotlib import rc
import pprint
from matplotlib.ticker import LogLocator, NullFormatter
import math


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

vars_list_QQLH_tag =["RecoEmiss_pz",
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
            "TauLepton_type",
            "TauHadron_type",
            "n_TauLepton_charged_constituents",
            "n_TauLepton_neutral_constituents",
            "n_TauHadron_charged_constituents",
            "n_TauHadron_neutral_constituents",
            "Tau_DPhi",
            "Tau_DR",
            "Tau_cos",
            "Tau_DEta",
            "Recoil",
            "Collinear_mass"]

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

#fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [1, 1], 'hspace':0})
colorDict = ['#8C0303', '#D04747', '#FFABAC', '#03028D', '#4E6BD3', '#9FB5D7']

#index for color list and label list
col = 0
label = []
#get gen number of events for each signal and backgorund file
for tag in TAG:
    for cat in CAT:
        for sub in SUBDIR:
            # Create the figure and plot
            fig, ax = plt.subplots(figsize=(8, 8))

            path = DIRECTORY + tag + "/"

            print(path)

            if "explicit" in tag:
                if "QQ" in cat:
                    vars_list = vars_list_QQ_explcit
                else:
                    vars_list = vars_list_NuNu_explicit
            else:
                if "QQ" in cat:
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

            
            print("Loading dataframes")

            train_df = joblib.load(f"{modelDir}/{tag}/train_data_{tag}_{cat}{sub}.pkl")
            test_df = joblib.load(f"{modelDir}/{tag}/test_data_{tag}_{cat}{sub}.pkl")

            test_sig = test_df[test_df["label"]==1]
            test_bkg = test_df[test_df["label"]==0]

            train_sig = train_df[train_df["label"]==1]
            train_bkg = train_df[train_df["label"]==0]

            print("Loading model")
            
            bdt = joblib.load(f"{modelDir}/{tag}/xgb_bdt_{tag}_{cat}{sub}.joblib")

            print("Testing model")

            pred_test_sig = bdt.predict_proba(test_sig[vars_list])
            pred_train_sig = bdt.predict_proba(train_sig[vars_list])
            pred_test_bkg = bdt.predict_proba(test_bkg[vars_list])
            pred_train_bkg = bdt.predict_proba(train_bkg[vars_list])
            p_test_sig = bdt.predict(test_sig[vars_list])
            p_train_sig = bdt.predict(train_sig[vars_list])
            p_test_bkg = bdt.predict(test_bkg[vars_list])
            p_train_bkg = bdt.predict(train_bkg[vars_list])
            
            #score 0 to 1 to how good signal/backgrounds are classified as respectively signal/background
            score_train_sig = accuracy_score(train_sig["label"],p_train_sig,normalize=True)
            score_test_sig = accuracy_score(test_sig["label"],p_test_sig,normalize=True)
            score_train_bkg = accuracy_score(train_bkg["label"],p_train_bkg,normalize=True)
            score_test_bkg = accuracy_score(test_bkg["label"],p_test_bkg,normalize=True)

            print("Making cuts")

            N_train = len(train_sig)
            N_test = len(test_sig)
            N_train_bkg = len(train_bkg)
            N_test_bkg = len(test_bkg)


            # Define BDT cut values and corresponding cut thresholds
            BDT_cuts = np.linspace(0., 5., 500)
            cut_vals = 1 - 10**(-BDT_cuts)  # Vector of thresholds

            # Extract scores
            sig_train_scores = pred_train_sig[:, 1]
            sig_test_scores = pred_test_sig[:, 1]
            bkg_train_scores = pred_train_bkg[:, 1]
            bkg_test_scores = pred_test_bkg[:, 1]

            # Helper to compute efficiencies with broadcasting
            def compute_efficiencies(scores, total_count):
                return np.maximum(1e-3, (scores[:, None] > cut_vals[None, :]).sum(axis=0) / total_count)

            # Compute all efficiencies
            eff_train      = compute_efficiencies(sig_train_scores, N_train)
            eff_test       = compute_efficiencies(sig_test_scores, N_test)
            eff_train_bkg  = compute_efficiencies(bkg_train_scores, N_train_bkg)
            eff_test_bkg   = compute_efficiencies(bkg_test_scores, N_test_bkg)

            print("Plotting")

            plt.title(f'{tag}, {leg_cat[cat]} {leg_sub[sub]}: FCC-ee Simulation IDEA Delphes', loc='right', fontsize=18)
            plt.plot(cut_vals, eff_train, color=colorDict[0], label=f'Trained signal, accuracy:'+str(round(score_train_sig,3)))
            plt.plot(cut_vals, eff_test, color=colorDict[1], label=f'Tested signal, accuracy:'+str(round(score_test_sig,3)), linestyle='dashed', linewidth='1.5')
            plt.plot(cut_vals, eff_train_bkg, color=colorDict[3], label=f'Trained background, accuracy:'+str(round(score_train_bkg,3)))
            plt.plot(cut_vals, eff_test_bkg, color=colorDict[4], label=f'Tested background, accuracy:'+str(round(score_test_bkg,3)), linestyle='dashed', linewidth='1.5')
            #draw vertical line corresponsing to last bin of the bdt score to visualise where most signal will be
            #if "QQ" in cat and "LL" in sub:
            #    plt.axvline(x =-math.log10(1./10), color = 'k', label = 'Last bin in BDT score', linewidth='1.5', linestyle='-.')
            #else:
            plt.axvline(x =-math.log10(1./200), color = 'k', label = 'Last bin in BDT score', linewidth='1.5', linestyle='-.')
            plt.xlabel("1 - BDT score",fontsize=18)
            plt.xticks([0, 1, 2, 3, 3.5], ["$10^0$", "$10^{-1}$", "$10^{-2}$", "$10^{-3}$", " "])
            plt.xlim(0,3.5)
            plt.ylim(10e-6,1)
            plt.ylabel("Efficiency",fontsize=18)
            plt.yscale('log') 
            plt.legend(loc="lower left", fontsize=15)
            plt.grid()
            plt.tight_layout()
            plt.savefig(f"{modelDir}/{tag}/{cat}{sub}_overtrain.pdf")
            plt.savefig(f"{modelDir}/{tag}/{cat}{sub}_overtrain.png")

            plt.clf()
            plt.hist(sig_test_scores, bins=100, alpha=0.6, label='Signal')
            plt.hist(bkg_test_scores, bins=100, alpha=0.6, label='Background')
            plt.xlabel("BDT score")
            plt.ylabel("Events")
            plt.yscale('log')
            plt.legend()
            plt.grid()
            plt.savefig(f"{modelDir}/{tag}/{cat}{sub}_score.pdf")
            plt.savefig(f"{modelDir}/{tag}/{cat}{sub}_score.png")

            print("Max BDT score - train signal:", sig_train_scores.max())
            print("Max BDT score - test signal:", sig_test_scores.max())
            print("Max BDT score - train background:", bkg_train_scores.max())
            print("Max BDT score - test background:", bkg_test_scores.max())


            print(f"Done: {tag}{cat}{sub}")