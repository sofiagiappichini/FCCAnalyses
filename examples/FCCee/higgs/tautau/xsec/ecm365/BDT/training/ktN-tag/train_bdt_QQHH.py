

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

def file_exists(file_path):
    return os.path.isfile(file_path)

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

# not separating here ZH from VBF in nunuH but only using ZH from numunumuH * 3 (cross-section), there should not be any event anyway
sigs = [#'wzp6_ee_nuenueH_Htautau_ecm365',
        #'wzp6_ee_numunumuH_Htautau_ecm365',
        #'wzp6_ee_nunuH_Htautau_ecm365',
        #'wzp6_ee_tautauH_Htautau_ecm365',
        #'wzp6_ee_mumuH_Htautau_ecm365',
        #'wzp6_ee_eeH_Htautau_ecm365',
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

    'wzp6_ee_numunumuH_Htautau_ecm365':0.0005184,
    'wzp6_ee_numunumuH_Hbb_ecm365':0.004814,
    'wzp6_ee_numunumuH_Hcc_ecm365':0.0002389,
    'wzp6_ee_numunumuH_Hss_ecm365':1.653e-6,
    'wzp6_ee_numunumuH_Hgg_ecm365':0.0006767,
    'wzp6_ee_numunumuH_HWW_ecm365':0.001779,
    'wzp6_ee_numunumuH_HZZ_ecm365':0.0002183,
}

path = "/ceph/sgiappic/HiggsCP/ecm365/ktN-tag/stage2_280125_cut/QQ/HH/"

output_file = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/BDT/outputs/ktN-tag/output_QQHH.txt"

out = '/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/BDT/models/ktN-tag/' 

model = f"{out}/xgb_bdt_ktN-tag_QQHH.joblib"

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

#Sample weights to balance the classes
weights = compute_sample_weight(class_weight='balanced', y=y)

#Fit the model
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

print("Training model")
#fit on the correctly weighted events
bdt.fit(x, y, sample_weight=weights)

feature_importances = pd.DataFrame(bdt.feature_importances_,
                                    index = vars_list,
                                    columns=['importance']).sort_values('importance',ascending=False)

with open(output_file, "a") as file:
    file.write("Feature importances \n")
    file.write(f"{feature_importances.to_string()}\n")

#Write model to joblib file
joblib.dump(bdt, f"{model}")

#Also dump as json for ROOT interpretation
#booster = bdt.get_booster()
#booster.dump_model(f"{out}/xgb_bdt_stage2_cut_QQHH.json", dump_format='json')

# comment TMVA form output. TMVA Experimental only supports binary at the moment.
print("Writing xgboost model to ROOT file")
ROOT.TMVA.Experimental.SaveXGBoost(bdt, "Htautau", f"{out}/xgb_bdt_ktN-tag_QQHH.root", num_inputs=len(vars_list))

bdt.save_model(f"{out}/xgb_bdt_ktN-tag_QQHH_model.json")

#Write the model to a ROOT file for application elsewhere in FCCAnalyses
print("Testing model")
pred_test = bdt.predict_proba(x_test)

# Calculate FPR, TPR, and AUC
fpr, tpr, thresholds = roc_curve(y_test, pred_test[:, 1], pos_label=1)
roc_auc = auc(fpr, tpr)

# Create the figure and plot
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_title('FCC-ee Simulation IDEA Delphes', loc='right', fontsize=20)

# Plot the ROC curve
plt.plot(fpr, tpr, lw=1.5, color="k", label=f'Htautau ROC (area = {roc_auc:.3f}) for QQHH')

# Plot the baseline for random classifier
plt.plot([0., 1.], [0., 1.], linestyle="--", color="k", label='50/50')

# Set limits and labels
plt.xlim(0., 1.)
plt.ylim(0., 1.)
plt.ylabel('Background rejection', fontsize=30)  # 1 - FPR
plt.xlabel('Signal efficiency', fontsize=30)  # TPR

# Adjust ticks and legend
ax.tick_params(axis='both', which='major', labelsize=25)
plt.legend(loc="lower left", fontsize=20)
plt.grid()
plt.tight_layout()

# Save the figure
print("Saving ROC plot")
fig.savefig("/web/sgiappic/public_html/Higgs_xsec/ecm365/ktN-tag/BDT/QQHH_ROC_ktN-tag.pdf")
