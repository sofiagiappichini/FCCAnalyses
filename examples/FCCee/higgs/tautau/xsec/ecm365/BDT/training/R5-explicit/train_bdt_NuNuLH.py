

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
            #"TauLead_type", 
            #"TauSub_type",        
            ]

sigs_ZH = [
        'wzp6_ee_numunumuH_Htautau_ecm365',
        #'wzp6_ee_mumuH_Htautau_ecm365',
        #'wzp6_ee_qqH_Htautau_ecm365',
        #'wzp6_ee_ssH_Htautau_ecm365',
        #'wzp6_ee_nunuH_Htautau_ecm365',
        #'wzp6_ee_bbH_Htautau_ecm365',
        #'wzp6_ee_ccH_Htautau_ecm365',
        #'wzp6_ee_eeH_Htautau_ecm365',
]

sigs_VBF = ['wzp6_ee_nuenueH_Htautau_ecm365']

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

path = "/ceph/sgiappic/HiggsCP/ecm365/R5-explicit/stage2_280125_cut/NuNu/LH/"

output_file = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/BDT/outputs/R5-explicit/output_NuNuLH.txt"

out = '/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/BDT/models/R5-explicit/'

model = f"{out}/xgb_bdt_R5-explicit_NuNuLH.joblib"

#get gen number of events for each signal and backgorund file
# Initialize variables
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
df_train = pd.concat([train_sig, train_bkg]).sample(frac=1)
df_test = pd.concat([test_sig, test_bkg])

# Prepare input features and labels
x_train, y_train = df_train[vars_list].to_numpy(), df_train['label'].to_numpy()
x_test, y_test = df_test[vars_list].to_numpy(), df_test['label'].to_numpy()

# Compute sample weights
weights = compute_sample_weight(class_weight='balanced', y=y_train)

# Train XGBoost Model
config_dict = {"n_estimators": 200, "learning_rate": 0.3, "max_depth": 2}
bdt = xgb.XGBClassifier(n_estimators=config_dict["n_estimators"],
                        max_depth=config_dict["max_depth"],
                        learning_rate=config_dict["learning_rate"],
                        objective='multi:softprob'
                        )

print("Training model")
bdt.fit(x_train, y_train, sample_weight=weights)

# Feature importances
feature_importances = pd.DataFrame(bdt.feature_importances_,
                                    index=vars_list,
                                    columns=['importance']).sort_values('importance', ascending=False)
with open(output_file, "a") as file:
    file.write("Feature importances \n")
    file.write(f"{feature_importances.to_string()}\n")

#Write model to joblib file
joblib.dump(bdt, f"{model}")

#Also dump as json for ROOT interpretation
#booster = bdt.get_booster()
#booster.dump_model(f"{out}/xgb_bdt_stage2_cut_NuNuLH.json", dump_format='json')

# comment TMVA form output. TMVA Experimental only supports binary at the moment.
print("Writing model")

# Save to a .root file in the TMVA format
ROOT.TMVA.Experimental.SaveXGBoost(bdt, "Htautau", f"{out}/xgb_bdt_R5-explicit_NuNuLH.root", num_inputs=len(vars_list))

bdt.save_model(f"{out}/xgb_bdt_R5-explicit_NuNuLH_model.json")

#bdt = xgb.XGBClassifier()
#bdt.load_model(f"{out}/xgb_bdt_R5-explicit_NuNuLH_model.json")

print("Testing model")
pred_test = bdt.predict_proba(x_test)  # Get probabilities

# Define colors and labels for multi-class case
labels = ["Background", "Signal ZH", "Signal VBF"]
colors = ["red", "blue", "green"]
fig, ax = plt.subplots(figsize=(8, 8))

# Loop through each class (ignoring background, index=0)
for i in range(1, 3):
    fpr, tpr, _ = roc_curve(y_test, pred_test[:, i], pos_label=i)
    roc_auc = auc(fpr, tpr)
    
    ax.plot(fpr, tpr, lw=2, color=colors[i], label=f'{labels[i]} (AUC = {roc_auc:.3f})')

# Compute ROC for ZH vs VBF (label 1 vs label 2)
fpr_zh_vbf, tpr_zh_vbf, _ = roc_curve((y_test == 1).astype(int), (y_test == 2).astype(int))
roc_auc_zh_vbf = auc(fpr_zh_vbf, tpr_zh_vbf)

# Plot ZH vs VBF ROC curve
ax.plot(fpr_zh_vbf, tpr_zh_vbf, lw=2, color="purple", label=f'ZH vs VBF (AUC = {roc_auc_zh_vbf:.3f})')

# Plot random classifier baseline
ax.plot([0., 1.], [0., 1.], linestyle="--", color="black", label="Random Classifier")

# Formatting
ax.set_xlim(0., 1.)
ax.set_ylim(0., 1.)
ax.set_xlabel("False Positive Rate (FPR)", fontsize=20)
ax.set_ylabel("True Positive Rate (TPR)", fontsize=20)
ax.set_title("FCC-ee Simulation IDEA Delphes", loc="right", fontsize=18)
ax.tick_params(axis="both", which="major", labelsize=15)
ax.legend(loc="lower right", fontsize=14)
ax.grid(True, linestyle="--", linewidth=0.5)
plt.tight_layout()

# Save the figure
print("Saving ROC plot")
fig.savefig("/web/sgiappic/public_html/Higgs_xsec/ecm365/R5-explicit/BDT/NuNuLH_ROC.pdf")
