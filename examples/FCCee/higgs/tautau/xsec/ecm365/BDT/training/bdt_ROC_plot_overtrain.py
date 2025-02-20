

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

sigs = [#'wzp6_ee_nuenueH_Htautau_ecm365',
        'wzp6_ee_numunumuH_Htautau_ecm365',
        #'wzp6_ee_nunuH_Htautau_ecm365',
        #'wzp6_ee_tautauH_Htautau_ecm365',
        'wzp6_ee_mumuH_Htautau_ecm365',
        'wzp6_ee_eeH_Htautau_ecm365',
        'wzp6_ee_qqH_Htautau_ecm365',
        'wzp6_ee_ssH_Htautau_ecm365',
        'wzp6_ee_bbH_Htautau_ecm365',
        'wzp6_ee_ccH_Htautau_ecm365',
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

    #'wzp6_ee_nunuH_Hbb_ecm365',
    #'wzp6_ee_nunuH_Hcc_ecm365',
    #'wzp6_ee_nunuH_Hss_ecm365',
    #'wzp6_ee_nunuH_Hgg_ecm365',
    #'wzp6_ee_nunuH_HWW_ecm365',
    #'wzp6_ee_nunuH_HZZ_ecm365',

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
    #"R5-explicit",
    #"R5-tag",
    #"ktN-explicit",
    "ktN-tag",
]
SUBDIR = [
    #'LL',
    #'LH',
    'HH',
]
#category to plot
CAT = [
    "QQ",
    #"LL",
    #"NuNu",
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

            N = {}
            N_gen = {}
            eff = {}
            weight = {}
            N_bkg = 0
            N_bkg_gen = 0
            tot_weight_bkg = 0
            N_sig = 0
            N_sig_gen = 0
            tot_weight_sig = 0
            eff_tot_bkg = 0
            eff_tot_sig = 0
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
                weight[i] = xsec[i] * eff[i] * 10.8e6

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

            #minumum number between the events in the samples and the one we expect to have in the signal composition
            N_min = {}
            N_sig_new = N_sig
            for i in sigs:
                N_min[i] = min(N[i], N_sig * weight[i] / tot_weight_sig) 
                if N_min[i]==N[i] and weight[i]>0 and N[i]>0:
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

                    valid_files = []

                    for file in files:
                        f = uproot.open(file)
                        if "events;1" in f.keys():
                            valid_files.append(file)

                    files = [f for f in valid_files]
                    if files==[]:
                        break
                    else:
                        for file in files:
                            f = uproot.open(file)
                            tree = f["events;1"]
                            temp_df = tree.arrays(expressions=vars_list, library="pd")
                            df = pd.concat([df, temp_df])

                            # Check if we have enough events to meet the target
                            if len(df) >= target_events:
                                break 

                    df = df.head(target_events)
                    df_sig = pd.concat([df_sig, df])
            
            #now for backgrounds
            df_bkg = pd.DataFrame()
            for q in bkgs:
                prev = len(df_bkg)
                target_events = int(N_sig_new * weight[q] / tot_weight_bkg)
                
                # Only takes the samples that actually have any events remaining  
                if N[q] > target_events and target_events>0: 
                    files = glob.glob(path + q + '/chunk_*.root')
                    df = pd.DataFrame()

                    valid_files = []

                    for file in files:
                        f = uproot.open(file)
                        if "events;1" in f.keys():
                            valid_files.append(file)

                    files = [f for f in valid_files]
                    if files==[]:
                        break
                    else:
                        for file in files:
                            f = uproot.open(file)
                            tree = f["events;1"]
                            temp_df = tree.arrays(expressions=vars_list, library="pd")
                            df = pd.concat([df, temp_df])

                            # Check if we have enough events to meet the target
                            if len(df) >= target_events:
                                break 

                    df = df.head(target_events)
                    df_bkg = pd.concat([df_bkg, df])
            
            #set Signal and background labels
            df_sig["label"] = 1
            df_bkg["label"] = 0

            
            #save some data for testing later
            df_sig = df_sig.sample(frac=1, random_state=1)
            df_bkg = df_bkg.sample(frac=1, random_state=1)
            train_sig, test_sig = train_test_split(df_sig, test_size=0.3)
            train_bkg, test_bkg = train_test_split(df_bkg, test_size=0.3)
            
            bdt = joblib.load(f"{modelDir}/{tag}/xgb_bdt_{tag}_{cat}{sub}.joblib")

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
            
            N_train = len(train_sig)
            N_test = len(test_sig)
            N_train_bkg = len(train_bkg)
            N_test_bkg = len(test_bkg)
            
            eff_train = []
            eff_test  = []
            eff_train_bkg = []
            eff_test_bkg  = []
            BDT_cuts = np.linspace(0.,5.,500)
            cut_vals = []
            for i in BDT_cuts:
                cut_val = float(i)
                cut_vals.append(cut_val)
                #cuts on the bdt 1-score in scale between 0 and 1-10^-5= 0.99999. so the x is 0 (cut at 1-10^0=0, takes everything) to 5 (cut at 1-10^-5=0.99999 takes nothing), log scale for 1-score
                #in the plotting/combine histos we have 200 bins betwen 0 and 1 so one bin is 1/200=0.005 and the last bin corresponds to 0.995 or cut_val=0.00217
                cut_val = 1 - pow(10, -cut_val)
                #efficiency for signal events considered as signal with various cuts on the 1-score in log scale
                eff_train.append( max( 1e-3, float(len(list(filter(lambda j: j>cut_val,pred_train_sig[:,1])))))/ N_train)
                eff_test.append( max( 1e-3, float(len(list(filter(lambda j: j>cut_val,pred_test_sig[:,1])))))/ N_test)
                #efficiency for background events considered as signal
                eff_train_bkg.append( max( 1e-3, float(len(list(filter(lambda j: j>cut_val,pred_train_bkg[:,1])))))/ N_train_bkg)
                eff_test_bkg.append( max( 1e-3, float(len(list(filter(lambda j: j>cut_val,pred_test_bkg[:,1])))))/ N_test_bkg)

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
            plt.savefig(f"/web/sgiappic/public_html/Higgs_xsec/ecm365/{tag}/BDT/{cat}{sub}_overtrain.pdf")
            plt.savefig(f"/web/sgiappic/public_html/Higgs_xsec/ecm365/{tag}/BDT/{cat}{sub}_overtrain.png")

            print(f"Done: {tag}{cat}{sub}")