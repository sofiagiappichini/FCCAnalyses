import uproot
import awkward as ak
import numpy as np
from sklearn.model_selection import train_test_split
import csv
import matplotlib.pyplot as plt
import os
import glob
import pprint
import pandas as pd
import ROOT


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

vars_list = ["RecoEmiss_px",
            "RecoEmiss_py",
            "RecoEmiss_pz",
            "RecoEmiss_e",
            "RecoZP_px", 
            "RecoZP_py",   
            "RecoZP_pz",   
            "RecoZP_e",
            "RecoZP_PID", 
            "RecoZM_px", 
            "RecoZM_py",   
            "RecoZM_pz",   
            "RecoZM_e", 
            "RecoZM_PID",
            "TauP_px",    
            "TauP_py",   
            "TauP_pz",   
            "TauP_e", 
            #"OP_ImpactP_px",
            #"OP_ImpactP_py",
            #"OP_ImpactP_pz",
            "TauM_px",    
            "TauM_py",   
            "TauM_pz",   
            "TauM_e", 
            #"OP_ImpactM_px",
            #"OP_ImpactM_py",
            #"OP_ImpactM_pz",
            ]

sigs = ['wzp6_ee_mumuH_Htautau_ecm240',
        'wzp6_ee_eeH_Htautau_ecm240'
]

bkgs = ['p8_ee_WW_ecm240',
        'p8_ee_Zqq_ecm240',
        'p8_ee_ZZ_ecm240',
        'wzp6_ee_tautau_ecm240',
        'wzp6_ee_mumu_ecm240',
        'wzp6_ee_ee_Mee_30_150_ecm240',
]

xsec = {'p8_ee_WW_ecm240':16.4385,
        'p8_ee_Zqq_ecm240':52.6539,
        'p8_ee_ZZ_ecm240':1.35899,
        'wzp6_ee_tautau_ecm240':4.668,
        'wzp6_ee_mumu_ecm240':5.288,
        'wzp6_ee_ee_Mee_30_150_ecm240':8.305,
        'wzp6_ee_tautauH_Hbb_ecm240':0.003932,
        'wzp6_ee_tautauH_Hcc_ecm240':0.0001952,
        'wzp6_ee_tautauH_Hss_ecm240':1.62e-06,
        'wzp6_ee_tautauH_Hgg_ecm240':0.0005528,
        'wzp6_ee_tautauH_HWW_ecm240':0.001453,
        'wzp6_ee_tautauH_HZZ_ecm240':0.0001783,
        'wzp6_egamma_eZ_Zmumu_ecm240':0.10368,
        'wzp6_egamma_eZ_Zee_ecm240':0.05198,
        'wzp6_gammae_eZ_Zmumu_ecm240':0.10368,
        'wzp6_gammae_eZ_Zee_ecm240':0.05198,
        'wzp6_gaga_tautau_60_ecm240':0.836,
        'wzp6_gaga_mumu_60_ecm240':1.5523,
        'wzp6_gaga_ee_60_ecm240':0.873,
        'wzp6_ee_nuenueZ_ecm240':0.033274,
        'wzp6_ee_nunuH_Hbb_ecm240':0.0269,
        'wzp6_ee_nunuH_Hcc_ecm240':0.001335,
        'wzp6_ee_nunuH_Hss_ecm240':1.109e-05,
        'wzp6_ee_nunuH_Hgg_ecm240':0.003782,
        'wzp6_ee_nunuH_HWW_ecm240':0.00994,
        'wzp6_ee_nunuH_HZZ_ecm240':0.001425,
        'wzp6_ee_eeH_Hbb_ecm240':0.004171,
        'wzp6_ee_eeH_Hcc_ecm240':0.000207,
        'wzp6_ee_eeH_Hss_ecm240':1.718e-06,
        'wzp6_ee_eeH_Hgg_ecm240':0.0005863,
        'wzp6_ee_eeH_HWW_ecm240':0.001541,
        'wzp6_ee_eeH_HZZ_ecm240':0.0001891,
        'wzp6_ee_mumuH_Hbb_ecm240':0.00394,
        'wzp6_ee_mumuH_Hcc_ecm240':0.0001956,
        'wzp6_ee_mumuH_Hss_ecm240':1.624e-06,
        'wzp6_ee_mumuH_Hgg_ecm240':0.0005538,
        'wzp6_ee_mumuH_HWW_ecm240':0.001456,
        'wzp6_ee_mumuH_HZZ_ecm240':0.0001786,
        'wzp6_ee_bbH_Hbb_ecm240':0.01745,
        'wzp6_ee_bbH_Hcc_ecm240':0.0008664,
        'wzp6_ee_bbH_Hss_ecm240':7.193e-06,
        'wzp6_ee_bbH_Hgg_ecm240':0.002454,
        'wzp6_ee_bbH_HWW_ecm240':0.00645,
        'wzp6_ee_bbH_HZZ_ecm240':0.0007915,
        'wzp6_ee_ccH_Hbb_ecm240':0.01359,
        'wzp6_ee_ccH_Hcc_ecm240':0.0006747,
        'wzp6_ee_ccH_Hss_ecm240':5.607e-06,
        'wzp6_ee_ccH_Hgg_ecm240':0.001911,
        'wzp6_ee_ccH_HWW_ecm240':0.005023,
        'wzp6_ee_ccH_HZZ_ecm240':0.0006164,
        'wzp6_ee_ssH_Hbb_ecm240':0.01745,
        'wzp6_ee_ssH_Hcc_ecm240':0.0008661,
        'wzp6_ee_ssH_Hss_ecm240':7.19e-06,
        'wzp6_ee_ssH_Hgg_ecm240':0.002453,
        'wzp6_ee_ssH_HWW_ecm240':0.006447,
        'wzp6_ee_ssH_HZZ_ecm240':0.0007912,
        'wzp6_ee_qqH_Hbb_ecm240':0.03107,
        'wzp6_ee_qqH_Hcc_ecm240':0.001542,
        'wzp6_ee_qqH_Hss_ecm240':1.28e-05,
        'wzp6_ee_qqH_Hgg_ecm240':0.004367,
        'wzp6_ee_qqH_HWW_ecm240':0.01148,
        'wzp6_ee_qqH_HZZ_ecm240':0.001409,
        "wzp6_ee_bbH_Htautau_ecm240":0.00188,
        "wzp6_ee_ccH_Htautau_ecm240":0.001464,
        "wzp6_ee_qqH_Htautau_ecm240":0.003346,
        "wzp6_ee_ssH_Htautau_ecm240":0.001879,
        "wzp6_ee_eeH_Htautau_ecm240":0.0004491,
        "wzp6_ee_mumuH_Htautau_ecm240":0.0004243,
        "wzp6_ee_tautauH_Htautau_ecm240":0.0004235,
        "wzp6_ee_nunuH_Htautau_ecm240":0.002897,
        "p8_ee_llH_Hpinu_even":7.033e-06,
        "p8_ee_llH_Hpinu_odd":7.033e-06,
}

sig_CP = [
    "p8_ee_llH_Hpinu_even",
    "p8_ee_llH_Hpinu_odd",
]

path = "/ceph/awiedl/FCCee/HiggsCP/stage2_tutorial/LL/HH/"
#path = "/ceph/sgiappic/HiggsCP/CPReco/stage2_explicit_new/"
#path = "/ceph/sgiappic/HiggsCP/tutorial/stage2/"

output_file = "/ceph/sgiappic/HiggsCP/tutorial/dataframe.pkl"

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
eff_tot_sig = 0
eff_tot_bkg = 0
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

pprint.pprint(N)
pprint.pprint(N_gen)
pprint.pprint(eff)
print(f"Events of backgrounds: {N_bkg}\n")
print(f"Events of signals: {N_sig}\n")
print(f"Weight of backgrounds: {tot_weight_bkg}\n")
print(f"Weight of signals: {tot_weight_sig}\n")
print(f"Efficiency of backgrounds: {eff_tot_bkg}\n")
print(f"Efficiency of signals: {eff_tot_sig}\n\n")

#minumum number between the events in the samples and the one we expect to have in the signal composition
N_min = {}
N_sig_new = N_sig
for i in sigs:
    N_min[i] = min(N[i], N_sig * weight[i] / tot_weight_sig) 
    if N_min[i]==N[i]:
        if weight[i] == 0:
            continue
        N_sig_new = N_min[i] * tot_weight_sig / weight[i]

print(f"Adjusted size of signal: {N_sig_new}\n\n")

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
            if 'events;1' in f.keys():
                tree = f["events"]
                temp_df = tree.arrays(expressions=vars_list, library="pd")
                temp_df["Process"] = f"{q}"
                temp_df["N_gen"] = N_gen[q]
                temp_df["CrossSection"] = xsec[q]
                temp_df["Tau1_charge"] = 1
                temp_df["Tau2_charge"] = -1
                #temp_df["Tau1_DM"] = 0
                #temp_df["Tau2_DM"] = 0
                df = pd.concat([df, temp_df])

            # Check if we have enough events to meet the target
            #if len(df) >= target_events:
            #    break 

        df = df.head(target_events)
        df_sig = pd.concat([df_sig, df])

        print(f"Weight of {q}: {weight[q]}\n")
        print(f"Relative weight of {q}: {weight[q] / tot_weight_sig}\n")
        print(f"Requested size of {q}: {N_sig * weight[q] / tot_weight_sig}\n")
        print(f"Events after stage2 of {q}: {N[q]}\n")
        print(f"Number of events in the dataframe of {q}: {len(df_sig) - prev}\n\n")
        
print(f"Total size of signal sample: {len(df_sig)}\n")

#now for backgrounds
df_bkg = pd.DataFrame()
for q in bkgs:
    prev = len(df_bkg)
    target_events = int(N_sig_new * weight[q] / tot_weight_bkg)
    
    # Only takes the samples that actually have any events remaining  
    if N[q] > 0: 
        files = glob.glob(path + q + '/chunk_*.root')
        df = pd.DataFrame()

        for file in files:
            f = uproot.open(file)
            if 'events;1' in f.keys():
                tree = f["events"]
                temp_df = tree.arrays(expressions=vars_list, library="pd")
                temp_df["Process"] = f"{q}"
                temp_df["N_gen"] = N_gen[q]
                temp_df["CrossSection"] = xsec[q]
                temp_df["Tau1_charge"] = 1
                temp_df["Tau2_charge"] = -1
                #temp_df["Tau1_DM"] = 0
                #temp_df["Tau2_DM"] = 0
                df = pd.concat([df, temp_df])

            # Check if we have enough events to meet the target
            #if len(df) >= target_events:
            #    break 

        df = df.head(target_events)
        df_bkg = pd.concat([df_bkg, df])

        print(f"Weight of {q}: {weight[q]}\n")
        print(f"Relative weight of {q}: {weight[q] / tot_weight_bkg}\n")
        print(f"Requested size of {q}: {len(df_sig) * weight[q] / tot_weight_bkg}\n")
        print(f"Events after stage2 of {q}: {N[q]}\n")
        print(f"Number of events in the dataframe of {q}: {len(df_bkg) - prev}\n\n")

print(f"Total size of bkg sample: {len(df_bkg)}\n")

#save some data for testing later
df_sig = df_sig.sample(frac=1, random_state=1)
df_bkg = df_bkg.sample(frac=1, random_state=1)

#Combine the datasets
df = pd.concat([df_sig,df_bkg])
#shuffle the rows so they are mixed between signal and background
df = df.sample(frac=1)

df.columns = [col.replace("TauP_", "Tau1_").replace("TauM_", "Tau2_").replace("OP_ImpactP_p", "Tau1_d").replace("OP_ImpactM_p", "Tau2_d").replace("RecoZP_", "Lep1_").replace("RecoZM_", "Lep2_").replace("RecoEmiss", "MissE") for col in df.columns]

df.to_pickle(output_file)