

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

sigs = ['wzp6_ee_mumuH_Htautau_ecm240',
        'wzp6_ee_qqH_Htautau_ecm240',
        'wzp6_ee_ssH_Htautau_ecm240',
        'wzp6_ee_nunuH_Htautau_ecm240',
        'wzp6_ee_bbH_Htautau_ecm240',
        'wzp6_ee_ccH_Htautau_ecm240',
        'wzp6_ee_eeH_Htautau_ecm240'
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

path = "/ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/"

output_file = "/work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/output_NuNuLH.txt"

train_tree = True
full_test = False

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
    if N_min[i]==N[i] and weight[i]>0 and N[i]>0:
        N_sig_new = N_min[i] * tot_weight_sig / weight[i]

with open(output_file, "a") as file:
    file.write(f"Adjusted size of signal: {N_sig_new}\n\n")

if train_tree == True:
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
                if "events;1" not in f.keys():
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
    
    '''y = df_train["label"]
    y_test = df_test["label"]
    
    #flattening input
    x = np.empty([1,len(df_train)])
    x_test = np.empty([1,len(df_test)])
    for i in vars_list:
        j = df_train[i].to_numpy()
        k = df_test[i].to_numpy()
        if(j.ndim==1):
            j = np.expand_dims(j,axis=1) 
            k = np.expand_dims(k,axis=1) 
        x = np.append(x,j.T,axis=0) 
        x_test = np.append(x_test,k.T,axis=0) 
    x = np.delete(x, 0, 0)
    x_test = np.delete(x_test, 0, 0)
    y = y.to_numpy()
    y_test = y_test.to_numpy()
    x = x.T
    x_test = x_test.T'''

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
    
    #BDT
    config_dict = {
                "n_estimators": 200,
                "learning_rate": 0.3,
                "max_depth": 2,
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
    #fit on the correctly weighted events
    bdt.fit(x, y, sample_weight=weights)
    
    feature_importances = pd.DataFrame(bdt.feature_importances_,
                                       index = vars_list,
                                       columns=['importance']).sort_values('importance',ascending=False)
    
    with open(output_file, "a") as file:
        file.write("Feature importances \n")
        file.write(f"{feature_importances.to_string()}\n")
    
    #Write the model to a ROOT file for application elsewhere in FCCAnalyses
    out = '/work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/models' 
    
    print("Testing model")
    pred_test = bdt.predict_proba(x_test)

    # Calculate FPR, TPR, and AUC
    fpr, tpr, thresholds = roc_curve(y_test, pred_test[:, 1], pos_label=1)
    roc_auc = auc(fpr, tpr)

    # Create the figure and plot
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_title('FCC-ee Simulation IDEA Delphes', loc='right', fontsize=20)

    # Plot the ROC curve
    plt.plot(fpr, tpr, lw=1.5, color="k", label=f'Htautau ROC (area = {roc_auc:.3f}) for NuNuLH')

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
    fig.savefig("/web/awiedl/public_html/ML/BDT/NuNuLH_ROC_ktN-explicit_stage2_241202_cut.pdf")

    #Write model to joblib file
    joblib.dump(bdt, f"{out}/xgb_bdt_ktN-explicit_stage2_241202_cut_NuNuLH.joblib")

    #Also dump as json for ROOT interpretation
    #booster = bdt.get_booster()
    #booster.dump_model(f"{out}/xgb_bdt_stage2_cut_NuNuLH.json", dump_format='json')

    # comment TMVA form output. TMVA Experimental only supports binary at the moment.
    print("Writing xgboost model to ROOT file")
    ROOT.TMVA.Experimental.SaveXGBoost(bdt, "Htautau", f"{out}/xgb_bdt_ktN-explicit_stage2_241202_cut_NuNuLH.root", num_inputs=len(vars_list))

    bdt.save_model(f"{out}/xgb_bdt_ktN-explicit_stage2_241202_cut_NuNuLH_model.json")
    # ROC curve plotting accomplished in the plotting script and not here.

true_pred = {}
false_pred = {}

if full_test==True:
    bdt = xgb.XGBClassifier()
    bdt.load_model("xgb_bdt_ktN-explicit_stage2_241202_cut_NuNuLH_model.json")
    for q in bkgs:
        true_pred[q]=0
        false_pred[q]=0
        files = glob.glob(path+q+'/chunk_*.root')
        for f in files:
            file = uproot.open(f)
            if file.keys()==['eventsProcessed;1']:
                files.remove(f)
        files = [f + ':events' for f in files]
        if(files==[] or N[q]==0):
            break
        for events in uproot.iterate(files, expressions=vars_list, library='pd', how='zip'):
            x = np.empty([1,len(events)])
            for i in vars_list:
                j = events[i].to_numpy()
                if(j.ndim==1):
                    j = np.expand_dims(j,axis=1) 
                x = np.append(x,j.T,axis=0) 
            x = np.delete(x, 0, 0)
            x = x.T
      
            lab = bdt.predict(x)
            unique, counts = np.unique(lab, return_counts = True)
            print(unique)
            print(counts)
            true_pred[q]+=counts[0]
        print(q)
        print(N[q])
        print(true_pred[q])
        #print(false_pred[q])
    
#    for q in sigs:
#        true_pred[q]=0
#        false_pred[q]=0
#        files = glob.glob(path+q+'/chunk_*.root')
#        for f in files:
#            file = uproot.open(f)
#            if file.keys()==['eventsProcessed;1']:
#                files.remove(f)
#        files = [f + ':events' for f in files]
#        if(files==[] or N[q]==0):
#            break
#        for events in uproot.iterate(files, expressions=vars_list, library='pd', how='zip'):
#            x = np.empty([1,len(events)])
#            for i in vars_list:
#                j = events[i].to_numpy()
#                if(j.ndim==1):
#                    j = np.expand_dims(j,axis=1) 
#                x = np.append(x,j.T,axis=0) 
#            x = np.delete(x, 0, 0)
#            x = x.T
#            lab = bdt.predict(x) 
#            unique, counts = np.unique(lab, return_counts = True)
#             print(unique)
#             print(counts)
#            true_pred[q]+=counts[0]
#         print(q)
#         print(N[q])
#         print(true_pred[q])
#         print(false_pred[q])
