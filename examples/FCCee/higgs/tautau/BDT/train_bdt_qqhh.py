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

vars_list = ["n_RecoPhotons",
            "RecoEmiss_px",
            "RecoEmiss_py",
            "RecoEmiss_pz",
            "RecoEmiss_pt",
            "RecoEmiss_p",
            "RecoEmiss_e",
            "Jets_R5_sel_e",     
            "Jets_R5_sel_p",     
            "Jets_R5_sel_pt",     
            "Jets_R5_sel_px",   
            "Jets_R5_sel_py",   
            "Jets_R5_sel_pz",     
            "Jets_R5_sel_eta",    
            "Jets_R5_sel_theta",   
            "Jets_R5_sel_phi",     
            "Jets_R5_sel_mass",      
            "n_Jets_R5_sel",
            "RecoEmiss_eta",
            "RecoEmiss_phi",
            "RecoEmiss_theta",
            "RecoEmiss_y",
            "RecoEmiss_costheta",
            "RecoZ_px",
            "RecoZ_py",
            "RecoZ_pz",
            "RecoZ_p",
            "RecoZ_pt",
            "RecoZ_e",
            "RecoZ_eta",
            "RecoZ_phi",
            "RecoZ_theta",
            "RecoZ_y",
            "RecoZ_mass",
            "RecoZ1_px", 
            "RecoZ1_py",   
            "RecoZ1_pz",   
            "RecoZ1_p",    
            "RecoZ1_pt",   
            "RecoZ1_e",    
            "RecoZ1_eta",    
            "RecoZ1_phi",    
            "RecoZ1_theta",   
            "RecoZ1_y",     
            "RecoZ1_mass",   
            "RecoZ2_px",    
            "RecoZ2_py",   
            "RecoZ2_pz",   
            "RecoZ2_p",   
            "RecoZ2_pt",  
            "RecoZ2_e",     
            "RecoZ2_eta",   
            "RecoZ2_phi",   
            "RecoZ2_theta",    
            "RecoZ2_y",    
            "RecoZ2_mass",   
            "RecoH_px",
            "RecoH_py",
            "RecoH_pz",
            "RecoH_p",
            "RecoH_pt",
            "RecoH_e",
            "RecoH_eta",
            "RecoH_phi",
            "RecoH_theta",
            "RecoH_y",
            "RecoH_mass",
            "TauLead_px",    
            "TauLead_py",   
            "TauLead_pz",   
            "TauLead_p",   
            "TauLead_pt",   
            "TauLead_e",    
            "TauLead_eta",    
            "TauLead_phi",    
            "TauLead_theta",    
            "TauLead_y",    
            "TauLead_mass",
            "TauSub_px",    
            "TauSub_py",   
            "TauSub_pz",   
            "TauSub_p",   
            "TauSub_pt",   
            "TauSub_e",    
            "TauSub_eta",    
            "TauSub_phi",    
            "TauSub_theta",    
            "TauSub_y",    
            "TauSub_mass",
            "Tau_Acoplanarity",
            "Tau_DR",
            "Tau_cos",
            "Recoil",
            "Collinear_mass"]

sigs = [#'wzp6_ee_mumuH_Htautau_ecm240',
        'wzp6_ee_qqH_Htautau_ecm240',
        #'wzp6_ee_tautauH_Htautau_ecm240',
        'wzp6_ee_ssH_Htautau_ecm240',
        #'wzp6_ee_nunuH_Htautau_ecm240',
        'wzp6_ee_bbH_Htautau_ecm240',
        'wzp6_ee_ccH_Htautau_ecm240',
        #'wzp6_ee_eeH_Htautau_ecm240'
]

bkgs = ['p8_ee_WW_ecm240',
        'p8_ee_Zqq_ecm240',
        'p8_ee_ZZ_ecm240',
        'wzp6_ee_tautau_ecm240',
        'wzp6_ee_mumu_ecm240',
        'wzp6_ee_ee_Mee_30_150_ecm240',
#        'wzp6_ee_tautauH_Hbb_ecm240',
#        'wzp6_ee_tautauH_Hcc_ecm240',
#        'wzp6_ee_tautauH_Hss_ecm240',
#        'wzp6_ee_tautauH_Hgg_ecm240',
#        'wzp6_ee_tautauH_HWW_ecm240',
#        'wzp6_ee_tautauH_HZZ_ecm240',
#        'wzp6_egamma_eZ_Zmumu_ecm240',
#        'wzp6_egamma_eZ_Zee_ecm240',
#        'wzp6_gammae_eZ_Zmumu_ecm240',
#        'wzp6_gammae_eZ_Zee_ecm240',
#        'wzp6_gaga_tautau_60_ecm240',
#        'wzp6_gaga_mumu_60_ecm240',
#        'wzp6_gaga_ee_60_ecm240',
#        'wzp6_ee_nuenueZ_ecm240',
#        'wzp6_ee_nunuH_Hbb_ecm240',
#        'wzp6_ee_nunuH_Hcc_ecm240',
#        'wzp6_ee_nunuH_Hss_ecm240',
#        'wzp6_ee_nunuH_Hgg_ecm240',
#        'wzp6_ee_nunuH_HWW_ecm240',
#        'wzp6_ee_nunuH_HZZ_ecm240',
#        'wzp6_ee_eeH_Hbb_ecm240',
#        'wzp6_ee_eeH_Hcc_ecm240',
#        'wzp6_ee_eeH_Hss_ecm240',
#        'wzp6_ee_eeH_Hgg_ecm240',
#        'wzp6_ee_eeH_HWW_ecm240',
#        'wzp6_ee_eeH_HZZ_ecm240',
#        'wzp6_ee_mumuH_Hbb_ecm240',
#        'wzp6_ee_mumuH_Hcc_ecm240',
#        'wzp6_ee_mumuH_Hss_ecm240',
#        'wzp6_ee_mumuH_Hgg_ecm240',
#        'wzp6_ee_mumuH_HWW_ecm240',
#        'wzp6_ee_mumuH_HZZ_ecm240',
#        'wzp6_ee_bbH_Hbb_ecm240',
#        'wzp6_ee_bbH_Hcc_ecm240',
#        'wzp6_ee_bbH_Hss_ecm240',
#        'wzp6_ee_bbH_Hgg_ecm240',
#        'wzp6_ee_bbH_HWW_ecm240',
#        'wzp6_ee_bbH_HZZ_ecm240',
#        'wzp6_ee_ccH_Hbb_ecm240',
#        'wzp6_ee_ccH_Hcc_ecm240',
#        'wzp6_ee_ccH_Hss_ecm240',
#        'wzp6_ee_ccH_Hgg_ecm240',
#        'wzp6_ee_ccH_HWW_ecm240',
#        'wzp6_ee_ccH_HZZ_ecm240',
#        'wzp6_ee_ssH_Hbb_ecm240',
#        'wzp6_ee_ssH_Hcc_ecm240',
#        'wzp6_ee_ssH_Hss_ecm240',
#        'wzp6_ee_ssH_Hgg_ecm240',
#        'wzp6_ee_ssH_HWW_ecm240',
#        'wzp6_ee_ssH_HZZ_ecm240',
#        'wzp6_ee_qqH_Hbb_ecm240',
#        'wzp6_ee_qqH_Hcc_ecm240',
#        'wzp6_ee_qqH_Hss_ecm240',
#        'wzp6_ee_qqH_Hgg_ecm240',
#        'wzp6_ee_qqH_HWW_ecm240',
#        'wzp6_ee_qqH_HZZ_ecm240'
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
        'wzp6_ee_qqH_HZZ_ecm240':0.001409
}

xsec_tot = 0

path = "/ceph/awiedl/FCCee/HiggsCP/stage2/QQ/HH/"

N = {}
N_tot = 0
for i in sigs+bkgs:
    files = glob.glob(path+i+'/chunk_*.root')
    N[i] = 0
    for f in files:
        file = uproot.open(f)
        if file.keys()==['eventsProcessed;1']:
            continue
        else:
            for events in uproot.iterate(f+':events',expressions='n_FSGenElectron',library='pd'):
                N[i] += len(events)
    if i in bkgs: N_tot += N[i]

train_tree = False
if train_tree == True:
    df_sig = pd.DataFrame()
    for p in sigs:
        for events in uproot.iterate(path+p+'/chunk_*.root:events',expressions=vars_list, library='pd', how='zip'):
            df_sig = pd.concat([df_sig,events])
            
    print(f"Total size of signal sample: {len(df_sig)}")
    
    df_bkg = pd.DataFrame()
    for q in bkgs:
        files = glob.glob(path+q+'/chunk_*.root')
        for f in files:
            file = uproot.open(f)
            if file.keys()==['eventsProcessed;1']:
                files.remove(f)
        files = [f + ':events' for f in files]
        if(files==[] or int(len(df_sig)*N[q]/N_tot)==0):
            break
        for events in uproot.iterate(files, expressions=vars_list, step_size=int(len(df_sig)*N[q]/N_tot), library='pd', how='zip'):
            df_bkg = pd.concat([df_bkg,events])
            break
    print(f"Total size of bkg sample: {len(df_bkg)}")
    
    #set Signal and background labels
    df_sig["label"] = 1
    df_bkg["label"] = 0
    
    print ("sample size each")
    print (len(df_sig))
    print (len(df_bkg))
    
    #save some data for testing later
    train_sig, test_sig = train_test_split(df_sig, test_size=0.3)
    train_bkg, test_bkg = train_test_split(df_bkg, test_size=0.3)
    
    #Combine the datasets
    df_train = pd.concat([train_sig,train_bkg])
    df_train = df_train.sample(frac=1)
    df_test = pd.concat([test_sig,test_bkg])
    
    print ("sample size train")
    print (len(df_train))
    print ("sample size test")
    print (len(df_test))
    
    #Split into class label (y) and training vars (x)
    y = df_train["label"]
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
    x_test = x_test.T
    print("effective input shape for training")
    print(x.shape)
    print(y.shape)
    #Sample weights to balance the classes
    weights = compute_sample_weight(class_weight='balanced', y=y)
    
    #BDT
    config_dict = {
                "n_estimators": 1000, #1000,
                "learning_rate": 0.3,
                "max_depth": 3, #5,
                }
    
    bdt = xgb.XGBClassifier(n_estimators=config_dict["n_estimators"],
                            max_depth=config_dict["max_depth"],
                            learning_rate=config_dict["learning_rate"],
                            objective='binary:logistic'
                            )
    
    #Fit the model
    print("Training model")
    bdt.fit(x, y, sample_weight=weights)
    
    #feature_importances = pd.DataFrame(bdt.feature_importances_,
    #                                   index = vars_list2,
    #                                   columns=['importance']).sort_values('importance',ascending=False)
    
    print("Feature importances")
    print(bdt.feature_importances_)
    
    #Write the model to a ROOT file for application elsewhere in FCCAnalyses
    out = '/work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/BDT/' 
    
    print("Testing model")
    pred_test = bdt.predict_proba(x_test)
    fpr, tpr, thresholds = roc_curve(y_test, pred_test[:,1], pos_label=1)
    roc_auc = auc(fpr, tpr)
    fig, ax = plt.subplots(figsize=(8,8))
    ax.set_title('FCC-ee Simulation IDEA Delphes', loc='right', fontsize=20)
    plt.plot(fpr, tpr, lw=1.5, color="k", label='Htautau ROC (area = %0.3f) for QQHH'%(roc_auc))
    plt.plot([0.45, 1.], [0.45, 1.], linestyle="--", color="k", label='50/50')
    plt.xlim(0.45,1.)
    plt.ylim(0.45,1.)
    plt.ylabel('Background rejection',fontsize=30)
    plt.xlabel('Signal efficiency',fontsize=30)
    ax.tick_params(axis='both', which='major', labelsize=25)
    plt.legend(loc="lower left",fontsize=20)
    plt.grid()
    plt.tight_layout()
    fig.savefig("/web/awiedl/public_html/ML/BDT/QQHH_ROC_stage2.pdf")

true_pred = {}
false_pred = {}
full_test = True

if full_test==True:
    bdt = xgb.XGBClassifier()
    bdt.load_model("model.json")
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
        print(false_pred[q])
    
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
#            print(unique)
#            print(counts)
#            true_pred[q]+=counts[0]
#        print(q)
#        print(N[q])
#        print(true_pred[q])
#        print(false_pred[q])

#Write model to joblib file
#joblib.dump(bdt, f"{out}/xgb_bdt_stage2_QQHH.joblib")

#Also dump as json for ROOT interpretation
#bdt.dump_model(f"{out}/xgb_bdt_stage2_QQHH.json", dump_format='json')

# comment TMVA form output. TMVA Experimental only supports binary at the moment.
#print("Writing xgboost model to ROOT file")
#ROOT.TMVA.Experimental.SaveXGBoost(bdt, "Htautau", f"{out}/xgb_bdt_stage2_QQHH.root", num_inputs=len(vars_list))

#bdt.save_model(f"{out}/model.json")
# ROC curve plotting accomplished in the plotting script and not here.
