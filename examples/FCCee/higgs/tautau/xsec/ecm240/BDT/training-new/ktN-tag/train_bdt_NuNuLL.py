

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

sigs = [#'wzp6_ee_mumuH_Htautau_ecm240',
        #'wzp6_ee_qqH_Htautau_ecm240',
        #'wzp6_ee_ssH_Htautau_ecm240',
        'wzp6_ee_nunuH_Htautau_ecm240',
        #'wzp6_ee_bbH_Htautau_ecm240',
        #'wzp6_ee_ccH_Htautau_ecm240',
        #'wzp6_ee_eeH_Htautau_ecm240'
]

bkgs = ['p8_ee_WW_ecm240',
        'p8_ee_Zqq_ecm240',
        'p8_ee_ZZ_ecm240',
        'wzp6_ee_tautau_ecm240',
        'wzp6_ee_mumu_ecm240',
        'wzp6_ee_ee_Mee_30_150_ecm240',
        'wzp6_ee_tautauH_Htautau_ecm240',
        'wzp6_ee_tautauH_Hbb_ecm240',
        'wzp6_ee_tautauH_Hcc_ecm240',
        'wzp6_ee_tautauH_Hss_ecm240',
        'wzp6_ee_tautauH_Hgg_ecm240',
        'wzp6_ee_tautauH_HWW_ecm240',
        'wzp6_ee_tautauH_HZZ_ecm240',
        'wzp6_egamma_eZ_Zmumu_ecm240',
        'wzp6_egamma_eZ_Zee_ecm240',
        'wzp6_gammae_eZ_Zmumu_ecm240',
        'wzp6_gammae_eZ_Zee_ecm240',
        'wzp6_gaga_tautau_60_ecm240',
        'wzp6_gaga_mumu_60_ecm240',
        'wzp6_gaga_ee_60_ecm240',
        'wzp6_ee_nuenueZ_ecm240',
        'wzp6_ee_nunuH_Hbb_ecm240',
        'wzp6_ee_nunuH_Hcc_ecm240',
        'wzp6_ee_nunuH_Hss_ecm240',
        'wzp6_ee_nunuH_Hgg_ecm240',
        'wzp6_ee_nunuH_HWW_ecm240',
        'wzp6_ee_nunuH_HZZ_ecm240',
        'wzp6_ee_eeH_Hbb_ecm240',
        'wzp6_ee_eeH_Hcc_ecm240',
        'wzp6_ee_eeH_Hss_ecm240',
        'wzp6_ee_eeH_Hgg_ecm240',
        'wzp6_ee_eeH_HWW_ecm240',
        'wzp6_ee_eeH_HZZ_ecm240',
        'wzp6_ee_mumuH_Hbb_ecm240',
        'wzp6_ee_mumuH_Hcc_ecm240',
        'wzp6_ee_mumuH_Hss_ecm240',
        'wzp6_ee_mumuH_Hgg_ecm240',
        'wzp6_ee_mumuH_HWW_ecm240',
        'wzp6_ee_mumuH_HZZ_ecm240',
        'wzp6_ee_bbH_Hbb_ecm240',
        'wzp6_ee_bbH_Hcc_ecm240',
        'wzp6_ee_bbH_Hss_ecm240',
        'wzp6_ee_bbH_Hgg_ecm240',
        'wzp6_ee_bbH_HWW_ecm240',
        'wzp6_ee_bbH_HZZ_ecm240',
        'wzp6_ee_ccH_Hbb_ecm240',
        'wzp6_ee_ccH_Hcc_ecm240',
        'wzp6_ee_ccH_Hss_ecm240',
        'wzp6_ee_ccH_Hgg_ecm240',
        'wzp6_ee_ccH_HWW_ecm240',
        'wzp6_ee_ccH_HZZ_ecm240',
        'wzp6_ee_ssH_Hbb_ecm240',
        'wzp6_ee_ssH_Hcc_ecm240',
        'wzp6_ee_ssH_Hss_ecm240',
        'wzp6_ee_ssH_Hgg_ecm240',
        'wzp6_ee_ssH_HWW_ecm240',
        'wzp6_ee_ssH_HZZ_ecm240',
        'wzp6_ee_qqH_Hbb_ecm240',
        'wzp6_ee_qqH_Hcc_ecm240',
        'wzp6_ee_qqH_Hss_ecm240',
        'wzp6_ee_qqH_Hgg_ecm240',
        'wzp6_ee_qqH_HWW_ecm240',
        'wzp6_ee_qqH_HZZ_ecm240'
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
}

N_gen = {
 'p8_ee_WW_ecm240': 373375386,
 'p8_ee_ZZ_ecm240': 56162093,
 'p8_ee_Zqq_ecm240': 100559248,
 'wzp6_ee_bbH_HWW_ecm240': 1000000,
 'wzp6_ee_bbH_HZZ_ecm240': 1000000,
 'wzp6_ee_bbH_Hbb_ecm240': 100000,
 'wzp6_ee_bbH_Hcc_ecm240': 400000,
 'wzp6_ee_bbH_Hgg_ecm240': 200000,
 'wzp6_ee_bbH_Hss_ecm240': 400000,
 'wzp6_ee_bbH_Htautau_ecm240': 400000,
 'wzp6_ee_ccH_HWW_ecm240': 1200000,
 'wzp6_ee_ccH_HZZ_ecm240': 1200000,
 'wzp6_ee_ccH_Hbb_ecm240': 200000,
 'wzp6_ee_ccH_Hcc_ecm240': 400000,
 'wzp6_ee_ccH_Hgg_ecm240': 400000,
 'wzp6_ee_ccH_Hss_ecm240': 300000,
 'wzp6_ee_ccH_Htautau_ecm240': 400000,
 'wzp6_ee_eeH_HWW_ecm240': 300000,
 'wzp6_ee_eeH_HZZ_ecm240': 400000,
 'wzp6_ee_eeH_Hbb_ecm240': 300000,
 'wzp6_ee_eeH_Hcc_ecm240': 300000,
 'wzp6_ee_eeH_Hgg_ecm240': 200000,
 'wzp6_ee_eeH_Hss_ecm240': 352836,
 'wzp6_ee_eeH_Htautau_ecm240': 400000,
 'wzp6_ee_ee_Mee_30_150_ecm240': 85100000,
 'wzp6_ee_mumuH_HWW_ecm240': 300000,
 'wzp6_ee_mumuH_HZZ_ecm240': 400000,
 'wzp6_ee_mumuH_Hbb_ecm240': 200000,
 'wzp6_ee_mumuH_Hcc_ecm240': 400000,
 'wzp6_ee_mumuH_Hgg_ecm240': 200000,
 'wzp6_ee_mumuH_Hss_ecm240': 400000,
 'wzp6_ee_mumuH_Htautau_ecm240': 400000,
 'wzp6_ee_mumu_ecm240': 51700000,
 'wzp6_ee_nuenueZ_ecm240': 2000000,
 'wzp6_ee_nunuH_HWW_ecm240': 1200000,
 'wzp6_ee_nunuH_HZZ_ecm240': 1200000,
 'wzp6_ee_nunuH_Hbb_ecm240': 1200000,
 'wzp6_ee_nunuH_Hcc_ecm240': 1100000,
 'wzp6_ee_nunuH_Hgg_ecm240': 1055845,
 'wzp6_ee_nunuH_Hss_ecm240': 1008052,
 'wzp6_ee_nunuH_Htautau_ecm240': 1200000,
 'wzp6_ee_qqH_HWW_ecm240': 1100000,
 'wzp6_ee_qqH_HZZ_ecm240': 1200000,
 'wzp6_ee_qqH_Hbb_ecm240': 500000,
 'wzp6_ee_qqH_Hcc_ecm240': 200000,
 'wzp6_ee_qqH_Hgg_ecm240': 400000,
 'wzp6_ee_qqH_Hss_ecm240': 400000,
 'wzp6_ee_qqH_Htautau_ecm240': 200000,
 'wzp6_ee_ssH_HWW_ecm240': 1200000,
 'wzp6_ee_ssH_HZZ_ecm240': 600000,
 'wzp6_ee_ssH_Hbb_ecm240': 200000,
 'wzp6_ee_ssH_Hcc_ecm240': 300000,
 'wzp6_ee_ssH_Hgg_ecm240': 400000,
 'wzp6_ee_ssH_Hss_ecm240': 300000,
 'wzp6_ee_ssH_Htautau_ecm240': 400000,
 'wzp6_ee_tautauH_HWW_ecm240': 400000,
 'wzp6_ee_tautauH_HZZ_ecm240': 330996,
 'wzp6_ee_tautauH_Hbb_ecm240': 400000,
 'wzp6_ee_tautauH_Hcc_ecm240': 400000,
 'wzp6_ee_tautauH_Hgg_ecm240': 400000,
 'wzp6_ee_tautauH_Hss_ecm240': 400000,
 'wzp6_ee_tautauH_Htautau_ecm240': 400000,
 'wzp6_ee_tautau_ecm240': 52400000,
 'wzp6_egamma_eZ_Zee_ecm240': 6000000,
 'wzp6_egamma_eZ_Zmumu_ecm240': 5700000,
 'wzp6_gaga_ee_60_ecm240': 11200000,
 'wzp6_gaga_mumu_60_ecm240': 18500000,
 'wzp6_gaga_tautau_60_ecm240': 33400000,
 'wzp6_gammae_eZ_Zee_ecm240': 6000000,
 'wzp6_gammae_eZ_Zmumu_ecm240': 5600000
 }

path = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/stage1_250502/ktN-tag/NuNu/LL/"

out = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/BDT_250502/ktN-tag/"
output_file = out + "/output_NuNuLL.txt"

#upload signals into a dataframe
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
        temp_df = temp_df[temp_df["RecoEmiss_e"] > 100]
        temp_df["weight"] = xsec[q] * 10.8e6 / N_gen[q]
        df = pd.concat([df, temp_df])

    df_sig = pd.concat([df_sig, df])

    with open(output_file, "a") as file:
        file.write(f"Number of events in the dataframe of {q}: {len(df_sig) - prev}\n\n")
        
with open(output_file, "a") as file:
    file.write(f"Total size of signal sample: {len(df_sig)}\n")
print(f"Total size of signal sample: {len(df_sig)}\n")

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
        if f.keys() == ['eventsProcessed;1']:
            continue
        tree = f["events"]
        temp_df = tree.arrays(expressions=vars_list, library="pd")
        temp_df = temp_df[temp_df["RecoEmiss_e"] > 100]
        temp_df["weight"] = xsec[q] * 10.8e6 / N_gen[q]
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
        file.write(f"Number of events in the dataframe of {q}: {len(df_bkg) - prev}\n")
        file.write(f"Total number of events for {q}: {len(df)}\n")
        file.write(f"Requested number of events for {q}: {target_events}\n\n")

with open(output_file, "a") as file:
    file.write(f"Total size of bkg sample: {len(df_bkg)}\n\n")
print(f"Total size of bkg sample: {len(df_bkg)}\n")

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

#Save dataframes so later I don't waste time making them again, need signal and background separated but i can use the label later
joblib.dump(df_train, out + 'train_data_ktN-tag_NuNuLL.pkl')
joblib.dump(df_test, out+ 'test_data_ktN-tag_NuNuLL.pkl')

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
joblib.dump(bdt, f"{out}/xgb_bdt_ktN-tag_NuNuLL.joblib")

#Also dump as json for ROOT interpretation
#booster = bdt.get_booster()
#booster.dump_model(f"{out}/xgb_bdt_stage2_cut_NuNuLL.json", dump_format='json')

# comment TMVA form output. TMVA Experimental only supports binary at the moment.
print("Writing xgboost model to ROOT file")
ROOT.TMVA.Experimental.SaveXGBoost(bdt, "Htautau", f"{out}/xgb_bdt_ktN-tag_NuNuLL.root", num_inputs=len(vars_list))

bdt.save_model(f"{out}/xgb_bdt_ktN-tag_NuNuLL_model.json")
# ROC curve plotting accomplished in the plotting script and not here.

