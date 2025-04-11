

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

## 27
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

## 33
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

## 33
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

## 23
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

## 29
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

## 29
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

sigs_QQ = [
        'wzp6_ee_qqH_Htautau_ecm365',
        'wzp6_ee_ssH_Htautau_ecm365',
        'wzp6_ee_bbH_Htautau_ecm365',
        'wzp6_ee_ccH_Htautau_ecm365',
]
sigs_ZH = [
    #'wzp6_ee_nuenueH_Htautau_ecm365',
    'wzp6_ee_numunumuH_Htautau_ecm365',
]

sigs_VBF = [
    'wzp6_ee_nuenueH_Htautau_ecm365',
    #'wzp6_ee_numunumuH_Htautau_ecm365',
]

bkgs = ['p8_ee_WW_ecm365',
    'p8_ee_Zqq_ecm365',
    'p8_ee_ZZ_ecm365',
    'p8_ee_Zbb_ecm365',
    'p8_ee_Zcc_ecm365',
    'p8_ee_Zss_ecm365',
    'p8_ee_tt_ecm365',
    
    'wzp6_ee_tautau_ecm365',
    'wzp6_ee_mumu_ecm365',
    'wzp6_ee_ee_Mee_30_150_ecm365',

    'wzp6_ee_tautauH_Htautau_ecm365',
    'wzp6_ee_tautauH_Hbb_ecm365',
    'wzp6_ee_tautauH_Hcc_ecm365',
    'wzp6_ee_tautauH_Hss_ecm365',
    'wzp6_ee_tautauH_Hgg_ecm365',
    'wzp6_ee_tautauH_HWW_ecm365',
    'wzp6_ee_tautauH_HZZ_ecm365',

    'wzp6_egamma_eZ_Zmumu_ecm365',
    'wzp6_egamma_eZ_Zee_ecm365',
    'wzp6_gammae_eZ_Zmumu_ecm365',
    'wzp6_gammae_eZ_Zee_ecm365',

    'wzp6_gaga_tautau_60_ecm365',
    'wzp6_gaga_mumu_60_ecm365',
    'wzp6_gaga_ee_60_ecm365',

    'wzp6_ee_nuenueZ_ecm365',

    'wzp6_ee_nunuH_Hbb_ecm365',
    'wzp6_ee_nunuH_Hcc_ecm365',
    'wzp6_ee_nunuH_Hss_ecm365',
    'wzp6_ee_nunuH_Hgg_ecm365',
    'wzp6_ee_nunuH_HWW_ecm365',
    'wzp6_ee_nunuH_HZZ_ecm365',

    'wzp6_ee_eeH_Hbb_ecm365',
    'wzp6_ee_eeH_Hcc_ecm365',
    'wzp6_ee_eeH_Hss_ecm365',
    'wzp6_ee_eeH_Hgg_ecm365',
    'wzp6_ee_eeH_HWW_ecm365',
    'wzp6_ee_eeH_HZZ_ecm365',

    'wzp6_ee_mumuH_Hbb_ecm365',
    'wzp6_ee_mumuH_Hcc_ecm365',
    'wzp6_ee_mumuH_Hss_ecm365',
    'wzp6_ee_mumuH_Hgg_ecm365',
    'wzp6_ee_mumuH_HWW_ecm365',
    'wzp6_ee_mumuH_HZZ_ecm365',

    'wzp6_ee_bbH_Hbb_ecm365',
    'wzp6_ee_bbH_Hcc_ecm365',
    'wzp6_ee_bbH_Hss_ecm365',
    'wzp6_ee_bbH_Hgg_ecm365',
    'wzp6_ee_bbH_HWW_ecm365',
    'wzp6_ee_bbH_HZZ_ecm365',

    'wzp6_ee_ccH_Hbb_ecm365',
    'wzp6_ee_ccH_Hcc_ecm365',
    'wzp6_ee_ccH_Hss_ecm365',
    'wzp6_ee_ccH_Hgg_ecm365',
    'wzp6_ee_ccH_HWW_ecm365',
    'wzp6_ee_ccH_HZZ_ecm365',

    'wzp6_ee_ssH_Hbb_ecm365',
    'wzp6_ee_ssH_Hcc_ecm365',
    'wzp6_ee_ssH_Hss_ecm365',
    'wzp6_ee_ssH_Hgg_ecm365',
    'wzp6_ee_ssH_HWW_ecm365',
    'wzp6_ee_ssH_HZZ_ecm365',

    'wzp6_ee_qqH_Hbb_ecm365',
    'wzp6_ee_qqH_Hcc_ecm365',
    'wzp6_ee_qqH_Hss_ecm365',
    'wzp6_ee_qqH_Hgg_ecm365',
    'wzp6_ee_qqH_HWW_ecm365',
    'wzp6_ee_qqH_HZZ_ecm365',

    #'wzp6_ee_nuenueH_Hbb_ecm365',
    #'wzp6_ee_nuenueH_Hcc_ecm365',
    #'wzp6_ee_nuenueH_Hss_ecm365',
    #'wzp6_ee_nuenueH_Hgg_ecm365',
    #'wzp6_ee_nuenueH_HWW_ecm365',
    #'wzp6_ee_nuenueH_HZZ_ecm365',  

    #'wzp6_ee_numunumuH_Hbb_ecm365',
    #'wzp6_ee_numunumuH_Hcc_ecm365',
    #'wzp6_ee_numunumuH_Hss_ecm365',
    #'wzp6_ee_numunumuH_Hgg_ecm365',
    #'wzp6_ee_numunumuH_HWW_ecm365',
    #'wzp6_ee_numunumuH_HZZ_ecm365',
]

xsec = {'p8_ee_WW_ecm365':10.7165,
    'p8_ee_Zqq_ecm365':8.679,
    'p8_ee_ZZ_ecm365':0.6428,
    'p8_ee_Zbb_ecm365':4.056,
    'p8_ee_Zcc_ecm365':4.506,
    'p8_ee_Zss_ecm365':4.084,
    'p8_ee_tt_ecm365':0.8,
    
    'wzp6_ee_tautau_ecm365':2.017,
    'wzp6_ee_mumu_ecm365':2.287,
    'wzp6_ee_ee_Mee_30_150_ecm365':1.53,

    'wzp6_ee_tautauH_Htautau_ecm365':0.0002617,
    'wzp6_ee_tautauH_Hbb_ecm365':0.00243,
    'wzp6_ee_tautauH_Hcc_ecm365':0.0001206,
    'wzp6_ee_tautauH_Hss_ecm365':8.345e-7,
    'wzp6_ee_tautauH_Hgg_ecm365':0.0003416,
    'wzp6_ee_tautauH_HWW_ecm365':0.0008979,
    'wzp6_ee_tautauH_HZZ_ecm365':0.0001102,

    'wzp6_egamma_eZ_Zmumu_ecm365':0.14,
    'wzp6_egamma_eZ_Zee_ecm365':0.069932,
    'wzp6_gammae_eZ_Zmumu_ecm365':0.14,
    'wzp6_gammae_eZ_Zee_ecm365':0.0700717,

    'wzp6_gaga_tautau_60_ecm365':1.537,
    'wzp6_gaga_mumu_60_ecm365':2.843,
    'wzp6_gaga_ee_60_ecm365':2.0063,

    'wzp6_ee_nuenueZ_ecm365':0.12624,
    'wzp6_ee_nunuH_Htautau_ecm365':0.003385,
    'wzp6_ee_nunuH_Hbb_ecm365':0.03143,
    'wzp6_ee_nunuH_Hcc_ecm365':0.00156,
    'wzp6_ee_nunuH_Hss_ecm365':1.079e-5,
    'wzp6_ee_nunuH_Hgg_ecm365':0.004418,
    'wzp6_ee_nunuH_HWW_ecm365':0.01161,
    'wzp6_ee_nunuH_HZZ_ecm365':0.001425,

    'wzp6_ee_eeH_Htautau_ecm365':0.0004634,
    'wzp6_ee_eeH_Hbb_ecm365':0.004303,
    'wzp6_ee_eeH_Hcc_ecm365':0.0002136,
    'wzp6_ee_eeH_Hss_ecm365':1.478e-6,
    'wzp6_ee_eeH_Hgg_ecm365':0.0006049,
    'wzp6_ee_eeH_HWW_ecm365':0.00159,
    'wzp6_ee_eeH_HZZ_ecm365':0.0001951,

    'wzp6_ee_mumuH_Htautau_ecm365':0.0002625,
    'wzp6_ee_mumuH_Hbb_ecm365':0.002438,
    'wzp6_ee_mumuH_Hcc_ecm365':0.000121,
    'wzp6_ee_mumuH_Hss_ecm365':8.371e-7,
    'wzp6_ee_mumuH_Hgg_ecm365':0.0003426,
    'wzp6_ee_mumuH_HWW_ecm365':0.0009007,
    'wzp6_ee_mumuH_HZZ_ecm365':0.0001105,

    'wzp6_ee_bbH_Htautau_ecm365':0.001153,
    'wzp6_ee_bbH_Hbb_ecm365':0.01071,
    'wzp6_ee_bbH_Hcc_ecm365':0.0005316,
    'wzp6_ee_bbH_Hss_ecm365':3.678e-6,
    'wzp6_ee_bbH_Hgg_ecm365':0.001506,
    'wzp6_ee_bbH_HWW_ecm365':0.003957,
    'wzp6_ee_bbH_HZZ_ecm365':0.0004857,

    'wzp6_ee_ccH_Htautau_ecm365':0.0009054,
    'wzp6_ee_ccH_Hbb_ecm365':0.008407,
    'wzp6_ee_ccH_Hcc_ecm365':0.0004173,
    'wzp6_ee_ccH_Hss_ecm365':2.887e-6,
    'wzp6_ee_ccH_Hgg_ecm365':0.001182,
    'wzp6_ee_ccH_HWW_ecm365':0.003107,
    'wzp6_ee_ccH_HZZ_ecm365':0.0003813,

    'wzp6_ee_ssH_Htautau_ecm365':0.001163,
    'wzp6_ee_ssH_Hbb_ecm365':0.0108,
    'wzp6_ee_ssH_Hcc_ecm365':0.0005359,
    'wzp6_ee_ssH_Hss_ecm365':3.708e-6,
    'wzp6_ee_ssH_Hgg_ecm365':0.001518,
    'wzp6_ee_ssH_HWW_ecm365':0.003989,
    'wzp6_ee_ssH_HZZ_ecm365':0.0004896,

    'wzp6_ee_qqH_Htautau_ecm365':0.00207,
    'wzp6_ee_qqH_Hbb_ecm365':0.01922,
    'wzp6_ee_qqH_Hcc_ecm365':0.000954,
    'wzp6_ee_qqH_Hss_ecm365':6.599e-6,
    'wzp6_ee_qqH_Hgg_ecm365':0.002701,
    'wzp6_ee_qqH_HWW_ecm365':0.007101,
    'wzp6_ee_qqH_HZZ_ecm365':0.0008715,

    'wzp6_ee_nuenueH_Htautau_ecm365':0.002349,
    'wzp6_ee_nuenueH_Hbb_ecm365':0.02181,
    'wzp6_ee_nuenueH_Hcc_ecm365':0.001083,
    'wzp6_ee_nuenueH_Hss_ecm365':7.49e-6,
    'wzp6_ee_nuenueH_Hgg_ecm365':0.003066,
    'wzp6_ee_nuenueH_HWW_ecm365':0.008059,
    'wzp6_ee_nuenueH_HZZ_ecm365':0.000989,  

    'wzp6_ee_numunumuH_Htautau_ecm365':0.0005184*3,
    'wzp6_ee_numunumuH_Hbb_ecm365':0.004814*3,
    'wzp6_ee_numunumuH_Hcc_ecm365':0.0002389*3,
    'wzp6_ee_numunumuH_Hss_ecm365':1.653e-6*3,
    'wzp6_ee_numunumuH_Hgg_ecm365':0.0006767*3,
    'wzp6_ee_numunumuH_HWW_ecm365':0.001779*3,
    'wzp6_ee_numunumuH_HZZ_ecm365':0.0002183*3,
}

DIRECTORY = "/ceph/sgiappic/HiggsCP/ecm365/"

TAG = [
    "R5-explicit",
    "R5-tag",
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
    #"LL",
    "NuNu",
]

leg_cat = {
    "QQ": r"$Z \to qq,$",  # Use raw string and format for LaTeX
    "NuNu": r"$Z \to \nu \nu,$",
}

leg_sub = {
    "LL": r"$H \to \tau_\ell \tau_\ell$",
    "LH": r"$H \to \tau_\ell \tau_h$",
    "HH": r"$H \to \tau_h \tau_h$",
}

output_file = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/BDT/output_overtraining.txt"

modelDir = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/BDT/models/"

#get gen number of events for each signal and backgorund file
for tag in TAG:
    # Create the figure and plot
    fig, ax = plt.subplots(figsize=(8, 8))
    #fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [1, 1], 'hspace':0})
    colorDict = ['#8C0303', '#D04747', '#FFABAC', '#03028D', '#4E6BD3', '#9FB5D7']

    #index for color list and label list
    col = 0
    label = []
    for cat in CAT:
        for sub in SUBDIR:

            path = DIRECTORY + tag + "/stage2_280125_cut/" + cat + "/" + sub + "/"

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

            if 'QQ' in cat:
                sigs = sigs_QQ

                N = {}
                N_gen = {}
                eff = {}
                weight = {}
                N_bkg = 0
                N_bkg_gen = 0
                tot_weight_bkg = 0
                N_sig = 0
                N_sig_gen = 0
                eff_tot_bkg = 0
                eff_tot_sig = 0
                tot_weight_sig = 0
                #get gen number of events for each signal and backgorund file
                for i in sigs+bkgs:
                    files = glob.glob(path + i + '/chunk_*.root')
                    N[i] = 0
                    N_gen[i] = 0
                    eff[i] = 0
                    for f in files:
                        #getting the raw number of events in this way only works if there are some events in the trees themselves 
                        #but here it doesn't matter as we don't use those samples anyway
                        events_processed, events_in_ttree = get_entries(f)
                        if events_processed is not None and events_in_ttree is not None:
                            N[i] += events_in_ttree
                            N_gen[i] += events_processed

                    #calculate efficiency of each sample    
                    if N_gen[i]!=0:
                        eff[i] = N[i] / N_gen[i]
                    weight[i] = xsec[i] * eff[i] * 2.65e6

                    #commulative number of events for background
                    if i in bkgs: 
                        N_bkg += N[i]
                        N_bkg_gen += N_gen[i]
                        tot_weight_bkg += weight[i]
                    if N_bkg_gen!=0:
                        eff_tot_bkg = N_bkg / N_bkg_gen
                    if i in sigs: 
                        N_sig += N[i]
                        N_sig_gen += N_gen[i]
                        tot_weight_sig += weight[i]
                    if N_sig_gen!=0:
                        eff_tot_sig = N_sig / N_sig_gen

                #pprint.pprint(N)
                #pprint.pprint(N_gen)
                #pprint.pprint(eff)
                with open(output_file, "a") as file:
                    file.write(f"Events of backgrounds: {N_bkg}\n")
                    file.write(f"Events of signals: {N_sig}\n")
                    file.write(f"Weight of backgrounds: {tot_weight_bkg}\n")
                    file.write(f"Weight of signals: {tot_weight_sig}\n")
                    file.write(f"Efficiency of backgrounds: {eff_tot_bkg}\n")
                    file.write(f"Efficiency of signals: {eff_tot_sig}\n\n")

                #minumum number between the events in the samples and the one we expect to have in the signal composition
                N_min = {}
                N_sig_new = N_sig
                for i in sigs:
                    N_min[i] = min(N[i], N_sig * weight[i] / tot_weight_sig) 
                    if N_min[i]==N[i]:
                        if weight[i] == 0:
                            continue
                        N_sig_new = N_min[i] * tot_weight_sig / weight[i]

                with open(output_file, "a") as file:
                    file.write(f"Adjusted size of signal: {N_sig_new}\n\n")

                #upload signals into a dataframe
                df_sig = pd.DataFrame()
                for q in sigs:
                    prev = len(df_sig)
                    target_events = int(N_sig_new * weight[q] / tot_weight_sig)
                    
                    # Only takes the samples that actually have any events remaining  
                    if N[q] > 0: 
                        files = glob.glob(path + q + '/chunk_*.root')
                        df = pd.DataFrame()

                        for file in files:
                            f = uproot.open(file)
                            if f.keys()==['eventsProcessed;1']:
                                files.remove(file)
                                continue
                            tree = f["events"]
                            temp_df = tree.arrays(expressions=vars_list, library="pd")
                            df = pd.concat([df, temp_df])

                            # Check if we have enough events to meet the target
                            if len(df) >= target_events:
                                break 

                        df = df.head(target_events)
                        df_sig = pd.concat([df_sig, df])

                        with open(output_file, "a") as file:
                            file.write(f"Weight of {q}: {weight[q]}\n")
                            file.write(f"Relative weight of {q}: {weight[q] / tot_weight_sig}\n")
                            file.write(f"Requested size of {q}: {N_sig * weight[q] / tot_weight_sig}\n")
                            file.write(f"Events after stage2 of {q}: {N[q]}\n")
                            file.write(f"Number of events in the dataframe of {q}: {len(df_sig) - prev}\n\n")
                        
                with open(output_file, "a") as file:
                    file.write(f"Total size of signal sample: {len(df_sig)}\n")
                #print(f"Total size of signal sample: {len(df_sig)}\n")

                #now for backgrounds
                df_bkg = pd.DataFrame()
                for q in bkgs:
                    prev = len(df_bkg)
                    target_events = int(N_sig_new * weight[q] / tot_weight_bkg)
                    
                    # Only takes the samples that actually have any events remaining  
                    if N[q] > target_events and target_events>0: 
                        files = glob.glob(path + q + '/chunk_*.root')
                        df = pd.DataFrame()

                        for file in files:
                            f = uproot.open(file)
                            if f.keys()==['eventsProcessed;1']:
                                files.remove(file)
                                continue
                            tree = f["events"]
                            temp_df = tree.arrays(expressions=vars_list, library="pd")
                            df = pd.concat([df, temp_df])

                            # Check if we have enough events to meet the target
                            if len(df) >= target_events:
                                break 

                        df = df.head(target_events)
                        df_bkg = pd.concat([df_bkg, df])

                        with open(output_file, "a") as file:
                            file.write(f"Weight of {q}: {weight[q]}\n")
                            file.write(f"Relative weight of {q}: {weight[q] / tot_weight_bkg}\n")
                            file.write(f"Requested size of {q}: {len(df_sig) * weight[q] / tot_weight_bkg}\n")
                            file.write(f"Events after stage2 of {q}: {N[q]}\n")
                            file.write(f"Number of events in the dataframe of {q}: {len(df_bkg) - prev}\n\n")

                with open(output_file, "a") as file:
                    file.write(f"Total size of bkg sample: {len(df_bkg)}\n\n")
                #print(f"Total size of bkg sample: {len(df_bkg)}\n")

                #set Signal and background labels
                df_sig["label"] = 1
                df_bkg["label"] = 0

                #save some data for testing later
                df_sig = df_sig.sample(frac=1, random_state=1)
                df_bkg = df_bkg.sample(frac=1, random_state=1)
                train_sig, test_sig = train_test_split(df_sig, test_size=0.3)
                train_bkg, test_bkg = train_test_split(df_bkg, test_size=0.3)

                #Combine the datasets
                df_train = pd.concat([train_sig,train_bkg])
                #shuffle the rows so they are mixed between signal and background
                df_train = df_train.sample(frac=1)
                df_test = pd.concat([test_sig,test_bkg])

                with open(output_file, "a") as file:
                    file.write("Normalised sample size \n")
                    file.write(f"Training: {len(df_train)}\n")
                    file.write(f"Test: {len(df_test)}\n\n")

                #Split into class label (y) and training vars (x)
                y = df_train["label"]
                x = df_train[vars_list]

                y = y.to_numpy()
                x = x.to_numpy()

                y_test = df_test["label"]
                x_test = df_test[vars_list]

                y_test = y_test.to_numpy()
                x_test = x_test.to_numpy()
                with open(output_file, "a") as file:
                    file.write("Effective input shape for training \n")
                    file.write(f"X: {x.shape}\n")
                    file.write(f"Y: {y.shape}\n\n")
                
                #import bdt already trained and test it 
                bdt = joblib.load(f"{modelDir}/{tag}/xgb_bdt_{tag}_{cat}{sub}.joblib")

                pred_test = bdt.predict_proba(x_test)

                # Calculate FPR, TPR, and AUC
                fpr, tpr, thresholds = roc_curve(y_test, pred_test[:, 1], pos_label=1)
                roc_auc = auc(fpr, tpr)

                # Plot the ROC curve
                plt.plot(fpr, tpr, lw=1.5, color=colorDict[col])
                #ax1.plot(fpr, 1-tpr, lw=1.5, color=colorDict[col])  # Log plot (0.8 to 1)
                #ax2.plot(fpr, 1-tpr, lw=1.5, color=colorDict[col])  # Linear plot (0 to 0.8)
                
                col += 1
                print(leg_cat[cat], leg_sub[sub])

                label.append(f'{leg_cat[cat]} {leg_sub[sub]}, AUC={roc_auc:.3f}')

                with open(output_file, "a") as file:
                    file.write(f"AUC:{roc_auc} \n\n")
                    file.write("-----------------------------------------\n")

                print(f"Done: {cat}{sub}")

            else:
                N, N_gen, eff, weight = {}, {}, {}, {}
                N_bkg, N_bkg_gen, tot_weight_bkg = 0, 0, 0
                N_sig_ZH, N_sig_ZH_gen, tot_weight_sig_ZH = 0, 0, 0
                N_sig_VBF, N_sig_VBF_gen, tot_weight_sig_VBF = 0, 0, 0

                for i in sigs_ZH + sigs_VBF + bkgs:
                    files = glob.glob(path + i + '/chunk_*.root')
                    N[i], N_gen[i], eff[i] = 0, 0, 0
                    
                    for f in files:
                        events_processed, events_in_ttree = get_entries(f)
                        if events_processed and events_in_ttree:
                            N[i] += events_in_ttree
                            N_gen[i] += events_processed
                    
                    if N_gen[i]:
                        eff[i] = N[i] / N_gen[i]
                    weight[i] = xsec[i] * eff[i] * 2.65e6
                    
                    if i in bkgs:
                        N_bkg += N[i]
                        N_bkg_gen += N_gen[i]
                        tot_weight_bkg += weight[i]
                    elif i in sigs_ZH:
                        N_sig_ZH += N[i]
                        N_sig_ZH_gen += N_gen[i]
                        tot_weight_sig_ZH += weight[i]
                    elif i in sigs_VBF:
                        N_sig_VBF += N[i]
                        N_sig_VBF_gen += N_gen[i]
                        tot_weight_sig_VBF += weight[i]

                # Compute total efficiencies
                if N_bkg_gen:
                    eff_tot_bkg = N_bkg / N_bkg_gen
                if N_sig_ZH_gen or N_sig_VBF_gen:
                    eff_tot_sig = (N_sig_ZH + N_sig_VBF) / (N_sig_VBF_gen + N_sig_ZH_gen)


                # Adjust sample sizes
                N_min = {}
                N_sig_ZH_new, N_sig_VBF_new = N_sig_ZH, N_sig_VBF
                for i in sigs_ZH:
                    N_min[i] = min(N[i], N_sig_ZH * weight[i] / tot_weight_sig_ZH)
                    if N_min[i] == N[i] and weight[i] > 0:
                        N_sig_ZH_new = N_min[i] * tot_weight_sig_ZH / weight[i]
                for i in sigs_VBF:
                    N_min[i] = min(N[i], N_sig_VBF * weight[i] / tot_weight_sig_VBF)
                    if N_min[i] == N[i] and weight[i] > 0:
                        N_sig_VBF_new = N_min[i] * tot_weight_sig_VBF / weight[i]
                N_sig_new = N_sig_VBF_new + N_sig_ZH_new

                with open(output_file, "a") as file:
                    file.write(f"Events of backgrounds: {N_bkg}\n")
                    file.write(f"Events of signals: {N_sig_ZH+N_sig_VBF}\n")
                    file.write(f"Weight of backgrounds: {tot_weight_bkg}\n")
                    file.write(f"Weight of signals: {tot_weight_sig_ZH+tot_weight_sig_VBF}\n")
                    file.write(f"Efficiency of backgrounds: {eff_tot_bkg}\n")
                    file.write(f"Efficiency of signals: {eff_tot_sig}\n\n")
                    file.write(f"Adjusted size of signal: {N_sig_new}\n\n")

                df_sig_ZH, df_sig_VBF, df_bkg = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

                # Load signal and background samples
                for q in sigs_ZH + sigs_VBF:
                    target_events = int(N_sig_ZH_new * weight[q] / tot_weight_sig_ZH) if q in sigs_ZH else (
                                    int(N_sig_VBF_new * weight[q] / tot_weight_sig_VBF) )
                    
                    if N[q] > 0:
                        files = glob.glob(path + q + '/chunk_*.root')
                        df = pd.DataFrame()

                        for file in files:
                            f = uproot.open(file)
                            if f.keys()==['eventsProcessed;1']:
                                files.remove(file)
                                continue
                            tree = f["events"]
                            temp_df = tree.arrays(expressions=vars_list, library="pd")
                            df = pd.concat([df, temp_df])

                            # Check if we have enough events to meet the target
                            if len(df) >= target_events:
                                break 

                        df = df.head(target_events)

                        if q in sigs_ZH:
                            prev = len(df_sig_ZH)
                            df_sig_ZH = pd.concat([df_sig_ZH, df])
                        else:
                            prev = len(df_sig_VBF)
                            df_sig_VBF = pd.concat([df_sig_VBF, df])

                        with open(output_file, "a") as file:
                            file.write(f"Weight of {q}: {weight[q]}\n")
                            file.write(f"Relative weight of {q}: {(weight[q] / tot_weight_sig_ZH) if q in sigs_ZH else ((weight[q] / tot_weight_sig_VBF))}\n")
                            file.write(f"Requested size of {q}: {int(N_sig_ZH_new * weight[q] / tot_weight_sig_ZH) if q in sigs_ZH else (int(N_sig_VBF_new * weight[q] / tot_weight_sig_VBF))}\n")
                            file.write(f"Events after stage2 of {q}: {N[q]}\n")
                            file.write(f"Number of events in the dataframe of {q}: {(len(df_sig_ZH) - prev) if q in sigs_ZH else ((len(df_sig_VBF) - prev))}\n\n")


                with open(output_file, "a") as file:
                    file.write(f"Total size of signal sample: {len(df_sig_VBF)+len(df_sig_ZH)}\n")

                for q in bkgs:
                    target_events = int(N_sig_new * weight[q] / tot_weight_bkg)
                    
                    if N[q] > target_events and target_events>0: 
                        files = glob.glob(path + q + '/chunk_*.root')
                        df = pd.DataFrame()

                        for file in files:
                            f = uproot.open(file)
                            if f.keys()==['eventsProcessed;1']:
                                files.remove(file)
                                continue
                            tree = f["events"]
                            temp_df = tree.arrays(expressions=vars_list, library="pd")
                            df = pd.concat([df, temp_df])

                            # Check if we have enough events to meet the target
                            if len(df) >= target_events:
                                break 

                        df = df.head(target_events)
                        df_bkg = pd.concat([df_bkg, df])
                        prev = len(df_bkg)

                        with open(output_file, "a") as file:
                            file.write(f"Weight of {q}: {weight[q]}\n")
                            file.write(f"Relative weight of {q}: {weight[q] / tot_weight_bkg}\n")
                            file.write(f"Requested size of {q}: {N_sig_new * weight[q] / tot_weight_bkg}\n")
                            file.write(f"Events after stage2 of {q}: {N[q]}\n")
                            file.write(f"Number of events in the dataframe of {q}: {len(df_bkg) - prev}\n\n")

                with open(output_file, "a") as file:
                    file.write(f"Total size of bkg sample: {len(df_bkg)}\n\n")

                # Assign labels
                df_sig_ZH['label'] = 1
                df_sig_VBF['label'] = 2
                df_bkg['label'] = 0

                # Shuffle and split datasets
                df_sig_ZH = df_sig_ZH.sample(frac=1, random_state=1)
                df_sig_VBF = df_sig_VBF.sample(frac=1, random_state=1)
                df_bkg = df_bkg.sample(frac=1, random_state=1)
                df_sig = pd.concat([df_sig_ZH, df_sig_VBF])

                train_sig, test_sig = train_test_split(df_sig, test_size=0.3)
                train_bkg, test_bkg = train_test_split(df_bkg, test_size=0.3)
                df_train = pd.concat([train_sig, train_bkg]).sample(frac=1, random_state=1)
                df_test = pd.concat([test_sig, test_bkg])

                # Prepare input features and labels
                x_train, y_train = df_train[vars_list].to_numpy(), df_train['label'].to_numpy()
                x_test, y_test = df_test[vars_list].to_numpy(), df_test['label'].to_numpy()

                joblib.dump((x_train, x_test, y_train, y_test), f"{modelDir}/training_data_{tag}_{cat}{sub}.pkl")

                #if model and dataframes are already present
                #x_train, x_test, y_train, y_test = joblib.load(f"{modelDir}/training_data_{tag}_{cat}{sub}.pkl")

                bdt = xgb.XGBClassifier()
                bdt.load_model(f"{modelDir}/{tag}/xgb_bdt_{tag}_{cat}{sub}_model.json")

                pred_test = bdt.predict_proba(x_test)  # Get probabilities

                #only plot background vs signal ROC
                fpr, tpr, _ = roc_curve(y_test, pred_test[:, 0], pos_label=0)
                roc_auc = auc(fpr, tpr)
                
                plt.plot(fpr, tpr, lw=1.5, color=colorDict[col])

                col += 1
                print(leg_cat[cat], leg_sub[sub])

                label.append(f'{leg_cat[cat]} {leg_sub[sub]}, AUC={roc_auc:.3f}')

                with open(output_file, "a") as file:
                    file.write(f"AUC:{roc_auc} \n\n")
                    file.write("-----------------------------------------\n")

                print(f"Done: {cat}{sub}")

                '''
                # Compute ROC for ZH vs VBF (label 1 vs label 2)
                prob_test = bdt.predict_proba(x_test)
                y_test_ZH_VBF = y_test[y_test != 0]  # Remove true background
                prob_test_ZH_VBF = prob_test[y_test != 0, 1]  # Get ZH scores for ZH or VBF true events: [event,i] where 1 is the label with predict_proba, 1D with predict(only label of events instead of probabilities for each class)
                fpr_zh_vbf, tpr_zh_vbf, _ = roc_curve(y_test_ZH_VBF, prob_test_ZH_VBF, pos_label=1) 
                #False Positive Rate (FPR): Probability that a VBF event is misclassified as ZH. 
                #True Positive Rate (TPR): Probability that a ZH event is correctly classified as ZH.
                roc_auc_zh_vbf = auc(fpr, tpr)

                # Plot ZH vs VBF ROC curve
                ax.plot(fpr_zh_vbf, tpr_zh_vbf, lw=2, color="purple", label=f'ZH vs VBF (AUC = {roc_auc_zh_vbf:.3f})')

                # Plot random classifier baseline
                ax.plot([0., 1.], [0., 1.], linestyle="--", color="black", label="Random Classifier")'''

    # Plot the baseline for random classifier
    plt.plot([0., 1.], [0., 1.], linestyle="--", color="k")
    label.append(f'50/50')

    # Set limits and labels
    #plt.xlim(0., 1.)
    plt.ylim(0., 1.)
    plt.xscale('log')

    plt.ylabel('True Positive Rate', fontsize=18)  # 1 - FPR
    plt.xlabel('False Positive Rate', fontsize=18)  # TPR
    plt.title(f'{tag}   FCC-ee Simulation IDEA Delphes', loc='right', fontsize=18)

    # Adjust ticks and legend
    ax.tick_params(axis='both', which='major', labelsize=15)
    plt.legend(label, loc="lower right", fontsize=15)
    plt.grid()

    plt.tight_layout()

    # Save the figure
    fig.savefig(f"/web/sgiappic/public_html/Higgs_xsec/ecm365/{tag}/BDT/BDT_ROC.pdf")
    fig.savefig(f"/web/sgiappic/public_html/Higgs_xsec/ecm365/{tag}/BDT/BDT_ROC.png")