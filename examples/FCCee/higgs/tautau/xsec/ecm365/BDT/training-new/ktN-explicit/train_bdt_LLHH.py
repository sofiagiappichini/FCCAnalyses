

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

vars_list = ["RecoEmiss_pz",
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

sigs = ['wzp6_ee_mumuH_Htautau_ecm365',
        #'wzp6_ee_qqH_Htautau_ecm365',
        #'wzp6_ee_ssH_Htautau_ecm365',
        #'wzp6_ee_nunuH_Htautau_ecm240',
        #'wzp6_ee_bbH_Htautau_ecm365',
        #'wzp6_ee_ccH_Htautau_ecm365',
        'wzp6_ee_eeH_Htautau_ecm365'
]

bkgs = ['p8_ee_WW_ecm365',
    'p8_ee_WW_tautau_ecm365',
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

    'wzp6_ee_numunumuH_Hbb_ecm365',
    'wzp6_ee_numunumuH_Hcc_ecm365',
    'wzp6_ee_numunumuH_Hss_ecm365',
    'wzp6_ee_numunumuH_Hgg_ecm365',
    'wzp6_ee_numunumuH_HWW_ecm365',
    'wzp6_ee_numunumuH_HZZ_ecm365',

    'wzp6_ee_VBF_nunuH_Hbb_ecm365',
    'wzp6_ee_VBF_nunuH_Hcc_ecm365',
    'wzp6_ee_VBF_nunuH_Hss_ecm365',
    'wzp6_ee_VBF_nunuH_Hgg_ecm365',
    'wzp6_ee_VBF_nunuH_HWW_ecm365',
    'wzp6_ee_VBF_nunuH_HZZ_ecm365',
]

xsec = {'p8_ee_WW_ecm365':10.7165,
    'p8_ee_WW_tautau_ecm365':0.131,  
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

    'wzp6_ee_numunumuH_Htautau_ecm365':0.0005184*3,
    'wzp6_ee_numunumuH_Hbb_ecm365':0.004814*3,
    'wzp6_ee_numunumuH_Hcc_ecm365':0.0002389*3,
    'wzp6_ee_numunumuH_Hss_ecm365':1.653e-6*3,
    'wzp6_ee_numunumuH_Hgg_ecm365':0.0006767*3,
    'wzp6_ee_numunumuH_HWW_ecm365':0.001779*3,
    'wzp6_ee_numunumuH_HZZ_ecm365':0.0002183*3,

    'wzp6_ee_VBF_nunuH_Hbb_ecm365':0.01807,
    'wzp6_ee_VBF_nunuH_Hcc_ecm365':0.0008968,
    'wzp6_ee_VBF_nunuH_Hss_ecm365':7.445e-06,
    'wzp6_ee_VBF_nunuH_Hgg_ecm365':0.00254,
    'wzp6_ee_VBF_nunuH_HWW_ecm365':0.006676,
    'wzp6_ee_VBF_nunuH_HZZ_ecm365':0.0008193,

    'wzp6_ee_VBF_nunuH_Htautau_ecm365':0.001946,
}

N_gen = {
'p8_ee_WW_ecm365': 101754213,
'p8_ee_WW_tautau_ecm365': 6000000,
'p8_ee_Zqq_ecm365': 55742194,
'p8_ee_ZZ_ecm365': 61470944,
'p8_ee_Zbb_ecm365': 55932700,
'p8_ee_Zcc_ecm365': 55879156,
'p8_ee_Zss_ecm365': 55848129,
'p8_ee_tt_ecm365': 2700000,
'wzp6_ee_tautau_ecm365': 12800000,
'wzp6_ee_mumu_ecm365': 6600000,
'wzp6_ee_ee_Mee_30_150_ecm365': 3000000,
'wzp6_ee_tautauH_Htautau_ecm365': 1100000,
'wzp6_ee_tautauH_Hbb_ecm365': 1200000,
'wzp6_ee_tautauH_Hcc_ecm365': 1200000,
'wzp6_ee_tautauH_Hss_ecm365': 900000,
'wzp6_ee_tautauH_Hgg_ecm365': 1000000,
'wzp6_ee_tautauH_HWW_ecm365': 1100000,
'wzp6_ee_tautauH_HZZ_ecm365': 1200000,
'wzp6_egamma_eZ_Zmumu_ecm365': 5900000,
'wzp6_egamma_eZ_Zee_ecm365': 1500000,
'wzp6_gammae_eZ_Zmumu_ecm365': 2400000,
'wzp6_gammae_eZ_Zee_ecm365': 2400000,
'wzp6_gaga_tautau_60_ecm365': 20800000,
'wzp6_gaga_mumu_60_ecm365': 6700000,
'wzp6_gaga_ee_60_ecm365': 20400000,
'wzp6_ee_nuenueZ_ecm365': 1400000,
'wzp6_ee_nunuH_Htautau_ecm365': 1200000,
'wzp6_ee_nunuH_Hbb_ecm365': 1200000,
'wzp6_ee_nunuH_Hcc_ecm365': 1200000,
'wzp6_ee_nunuH_Hss_ecm365': 1200000,
'wzp6_ee_nunuH_Hgg_ecm365': 1200000,
'wzp6_ee_nunuH_HWW_ecm365': 900000,
'wzp6_ee_nunuH_HZZ_ecm365': 1200000,
'wzp6_ee_eeH_Htautau_ecm365': 1200000,
'wzp6_ee_eeH_Hbb_ecm365': 1200000,
'wzp6_ee_eeH_Hcc_ecm365': 900000,
'wzp6_ee_eeH_Hss_ecm365': 1122800,
'wzp6_ee_eeH_Hgg_ecm365': 1200000,
'wzp6_ee_eeH_HWW_ecm365': 1100000,
'wzp6_ee_eeH_HZZ_ecm365': 1200000,
'wzp6_ee_mumuH_Htautau_ecm365': 900000,
'wzp6_ee_mumuH_Hbb_ecm365': 1000000,
'wzp6_ee_mumuH_Hcc_ecm365': 1100000,
'wzp6_ee_mumuH_Hss_ecm365': 1000000,
'wzp6_ee_mumuH_Hgg_ecm365': 900000,
'wzp6_ee_mumuH_HWW_ecm365': 1100000,
'wzp6_ee_mumuH_HZZ_ecm365': 800000,
'wzp6_ee_bbH_Htautau_ecm365': 1000000,
'wzp6_ee_bbH_Hbb_ecm365': 1200000,
'wzp6_ee_bbH_Hcc_ecm365': 1200000,
'wzp6_ee_bbH_Hss_ecm365': 1200000,
'wzp6_ee_bbH_Hgg_ecm365': 1200000,
'wzp6_ee_bbH_HWW_ecm365': 1200000,
'wzp6_ee_bbH_HZZ_ecm365': 1000000,
'wzp6_ee_ccH_Htautau_ecm365': 1200000,
'wzp6_ee_ccH_Hbb_ecm365': 900000,
'wzp6_ee_ccH_Hcc_ecm365': 1100000,
'wzp6_ee_ccH_Hss_ecm365': 1100000,
'wzp6_ee_ccH_Hgg_ecm365': 1200000,
'wzp6_ee_ccH_HWW_ecm365': 1200000,
'wzp6_ee_ccH_HZZ_ecm365': 1000000,
'wzp6_ee_ssH_Htautau_ecm365': 1200000,
'wzp6_ee_ssH_Hbb_ecm365': 1200000,
'wzp6_ee_ssH_Hcc_ecm365': 900000,
'wzp6_ee_ssH_Hss_ecm365': 1200000,
'wzp6_ee_ssH_Hgg_ecm365': 1200000,
'wzp6_ee_ssH_HWW_ecm365': 1000000,
'wzp6_ee_ssH_HZZ_ecm365': 1100000,
'wzp6_ee_qqH_Htautau_ecm365': 1200000,
'wzp6_ee_qqH_Hbb_ecm365': 1200000,
'wzp6_ee_qqH_Hcc_ecm365': 1100000,
'wzp6_ee_qqH_Hss_ecm365': 1100000,
'wzp6_ee_qqH_Hgg_ecm365': 1100000,
'wzp6_ee_qqH_HWW_ecm365': 1100000,
'wzp6_ee_qqH_HZZ_ecm365': 1200000,
'wzp6_ee_nuenueH_Htautau_ecm365': 1200000,
'wzp6_ee_nuenueH_Hbb_ecm365': 1200000,
'wzp6_ee_nuenueH_Hcc_ecm365': 1200000,
'wzp6_ee_nuenueH_Hss_ecm365': 1200000,
'wzp6_ee_nuenueH_Hgg_ecm365': 1200000,
'wzp6_ee_nuenueH_HWW_ecm365': 1200000,
'wzp6_ee_nuenueH_HZZ_ecm365': 1200000,
'wzp6_ee_numunumuH_Htautau_ecm365': 1200000,
'wzp6_ee_numunumuH_Hbb_ecm365': 1200000,
'wzp6_ee_numunumuH_Hcc_ecm365': 1200000,
'wzp6_ee_numunumuH_Hss_ecm365': 1200000,
'wzp6_ee_numunumuH_Hgg_ecm365': 1200000,
'wzp6_ee_numunumuH_HWW_ecm365': 1200000,
'wzp6_ee_numunumuH_HZZ_ecm365': 1200000,
'wzp6_ee_VBF_nunuH_Htautau_ecm365': 1200000,
'wzp6_ee_VBF_nunuH_Hbb_ecm365': 1200000,
'wzp6_ee_VBF_nunuH_Hcc_ecm365': 1169920,
'wzp6_ee_VBF_nunuH_Hss_ecm365': 1200000,
'wzp6_ee_VBF_nunuH_Hgg_ecm365': 1200000,
'wzp6_ee_VBF_nunuH_HWW_ecm365': 1200000,
'wzp6_ee_VBF_nunuH_HZZ_ecm365': 1200000,
 }

path = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm365/stage1_250502/ktN-explicit/LL/HH/"

out = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm365/BDT_250502/ktN-explicit/"
output_file = out + "/output_LLHH.txt"

##upload signals into a dataframe
df_sig = pd.DataFrame()
for q in sigs:
    prev = len(df_sig)
    
    files = glob.glob(path + q + '/chunk_*.root')
    df = pd.DataFrame()

    for file in files:
        f = uproot.open(file)
        if f.keys()==['eventsProcessed;1']:
            files.remove(file)
            continue
        tree = f["events"]
        temp_df = tree.arrays(expressions=vars_list, library="pd")
        temp_df = temp_df[temp_df["Collinear_mass"] > 100]
        temp_df = temp_df[temp_df["Collinear_mass"] < 150]
        temp_df["weight"] = xsec[q] * 3e6 / N_gen[q]
        df = pd.concat([df, temp_df])

    df_sig = pd.concat([df_sig, df])

    with open(output_file, "a") as file:
        file.write(f"Number of events in the dataframe of {q}: {len(df_sig) - prev}\n\n")
        
with open(output_file, "a") as file:
    file.write(f"Total size of signal sample: {len(df_sig)}\n")
print(f"Total size of signal sample: {len(df_sig)}\n")

#now for backgrounds
N_sig = len(df_sig)
tot_weight_sig = df_sig["weight"].sum()

#now for backgrounds
df_bkg = pd.DataFrame()
weight = {}
all_bkg_data = {}

for q in bkgs:
    files = glob.glob(path + q + '/chunk_*.root')
    df_list = []

    for file in files:
        f = uproot.open(file)
        if f.keys()==[]:
            continue
        if f.keys() == ['eventsProcessed;1']:
            continue
        tree = f["events"]
        temp_df = tree.arrays(expressions=vars_list, library="pd")
        temp_df = temp_df[(temp_df["Collinear_mass"] > 100) & (temp_df["Collinear_mass"] < 150)]
        temp_df["weight"] = xsec[q] * 3e6 / N_gen[q]
        df_list.append(temp_df)

    if not df_list:
        continue

    df = pd.concat(df_list, ignore_index=True)
    weight[q] = df["weight"].sum()
    all_bkg_data[q] = df

tot_weight_bkg = sum(weight.values())

# Second loop: sample proportionally
for q in bkgs:
    if q not in all_bkg_data:
        continue
        
    prev = len(df_bkg)
    df = all_bkg_data[q]
    if df.empty:
        continue

    target_events = int(N_sig * weight[q] / tot_weight_bkg)
    if len(df) >= target_events:
        df = df.sample(n=target_events, random_state=2)
    df_bkg = pd.concat([df_bkg, df], ignore_index=True)

    with open(output_file, "a") as file:
        file.write(f"Number of events in the dataframe of {q}: {len(df_bkg) - prev}\n\n")

with open(output_file, "a") as file:
    file.write(f"Total size of bkg sample: {len(df_bkg)}\n\n")
print(f"Total size of bkg sample: {len(df_bkg)}\n")

#set Signal and background labels
df_sig["label"] = 1
df_bkg["label"] = 0

#save some data for testing later
df_sig = df_sig.sample(frac=1, random_state=1)
df_bkg = df_bkg.sample(frac=1, random_state=1)
train_sig, test_sig = train_test_split(df_sig, test_size=0.5)
train_bkg, test_bkg = train_test_split(df_bkg, test_size=0.5)

#Combine the datasets
df_train = pd.concat([train_sig,train_bkg])
#shuffle the rows so they are mixed between signal and background
df_train = df_train.sample(frac=1)
df_test = pd.concat([test_sig,test_bkg])

#Save dataframes so later I don't waste time making them again, need signal and background separated but i can use the label later
joblib.dump(df_train, out + 'train_data_ktN-explicit_LLHH.pkl')
joblib.dump(df_test, out+ 'test_data_ktN-explicit_LLHH.pkl')

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

#BDT
config_dict = {
            "n_estimators": 200, #1000,
            "learning_rate": 0.3,
            "max_depth": 2, #5,
            }

with open(output_file, "a") as file:
    file.write(f"{config_dict}\n")

bdt = xgb.XGBClassifier(n_estimators=config_dict["n_estimators"],
                        max_depth=config_dict["max_depth"],
                        learning_rate=config_dict["learning_rate"],
                        objective='binary:logistic'
                        )

#Fit the model
print("Training model")
#Sample weights to balance the classes
weights = compute_sample_weight(class_weight='balanced', y=y)

bdt.fit(x, y, sample_weight=weights)

feature_importances = pd.DataFrame(bdt.feature_importances_,
                                    index = vars_list,
                                    columns=['importance']).sort_values('importance',ascending=False)

with open(output_file, "a") as file:
    file.write("Feature importances \n")
    file.write(f"{feature_importances.to_string()}\n")

#Write the model to a ROOT file for application elsewhere in FCCAnalyses
#Write model to joblib file
joblib.dump(bdt, f"{out}/xgb_bdt_ktN-explicit_LLHH.joblib")

#Also dump as json for ROOT interpretation
#booster = bdt.get_booster()
#booster.dump_model(f"{out}/xgb_bdt_stage2_cut_LLHH.json", dump_format='json')

# comment TMVA form output. TMVA Experimental only supports binary at the moment.
print("Writing xgboost model to ROOT file")
ROOT.TMVA.Experimental.SaveXGBoost(bdt, "Htautau", f"{out}/xgb_bdt_ktN-explicit_LLHH.root", num_inputs=len(vars_list))

bdt.save_model(f"{out}/xgb_bdt_ktN-explicit_LLHH_model.json")
# ROC curve plotting accomplished in the plotting script and not here.

