#code adapted from FCCAnalyses/do_plots.py

import sys
import os
import os.path
import ntpath
import importlib
import copy
import re
import logging
import ROOT

# Set ROOT to batch mode so it doesn't open all the plots
ROOT.gROOT.SetBatch(True)

def file_exists(file_path):
    return os.path.isfile(file_path)

# directory with final stage files
DIRECTORY = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm365/final_250502/"
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
#list of cuts you want to plot
CUTS_LL = [
    "selReco",
    "selReco_100Coll150",
    "selReco_100Coll150_115Rec160",
    "selReco_100Coll150_115Rec160_1DR",
    "selReco_100Coll150_115Rec160_1DR_cos0.25",
    "selReco_100Coll150_115Rec160_1DR_cos0.25_misscos0.98",
    "selReco_100Coll150_115Rec160_1DR_cos0.25_misscos0.98_80Z100",
]
CUTS_NuNu = [
    "selReco",
    "selReco_180Me",
    "selReco_180Me_TauDPhi3",
    "selReco_180Me_TauDPhi3_1DR",
    "selReco_180Me_TauDPhi3_1DR_cos0.25",
    "selReco_180Me_TauDPhi3_1DR_cos0.25_misscos0.98",
    "selReco_180Me_TauDPhi3_1DR_cos0.25_misscos0.98_missy1",
]

CUTS = {
    'LL':CUTS_LL,
    'QQ':CUTS_LL,
    'NuNu':CUTS_NuNu,
}

#now you can list all the histograms that you want to plot
VARIABLES = [
    
    ######## Reconstructed particles #######
    #"RecoMC_PID",

    "n_RecoElectrons",
    "RecoElectron_e",
    "RecoElectron_p",
    "RecoElectron_pt",
    "RecoElectron_px",
    "RecoElectron_py",
    "RecoElectron_pz",
    "RecoElectron_y",
    "RecoElectron_eta",
    "RecoElectron_theta",
    "RecoElectron_phi",
    "RecoElectron_charge",
    "RecoElectron_mass",
    "RecoElectronTrack_absD0",
    "RecoElectronTrack_absZ0",
    "RecoElectronTrack_absD0sig",
    "RecoElectronTrack_absZ0sig",
    "RecoElectronTrack_D0cov",
    "RecoElectronTrack_Z0cov",

    "n_RecoElectrons_sel",
    "RecoElectron_sel_e",
    "RecoElectron_sel_p",
    "RecoElectron_sel_pt",
    "RecoElectron_sel_px",
    "RecoElectron_sel_py",
    "RecoElectron_sel_pz",
    "RecoElectron_sel_y",
    "RecoElectron_sel_eta",
    "RecoElectron_sel_theta",
    "RecoElectron_sel_phi",
    "RecoElectron_sel_charge",
    "RecoElectron_sel_mass",
    "RecoElectronTrack_sel_absD0",
    "RecoElectronTrack_sel_absZ0",
    "RecoElectronTrack_sel_absD0sig",
    "RecoElectronTrack_sel_absZ0sig",
    "RecoElectronTrack_sel_D0cov",
    "RecoElectronTrack_sel_Z0cov",

    "n_RecoMuons",
    "RecoMuon_e",
    "RecoMuon_p",
    "RecoMuon_pt",
    "RecoMuon_px",
    "RecoMuon_py",
    "RecoMuon_pz",
    "RecoMuon_y",
    "RecoMuon_eta",
    "RecoMuon_theta",
    "RecoMuon_phi",
    "RecoMuon_charge",
    "RecoMuon_mass",
    "RecoMuonTrack_absD0",
    "RecoMuonTrack_absZ0",
    "RecoMuonTrack_absD0sig",
    "RecoMuonTrack_absZ0sig",
    "RecoMuonTrack_D0cov",
    "RecoMuonTrack_Z0cov",

    "n_RecoMuons_sel",
    "RecoMuon_sel_e",
    "RecoMuon_sel_p",
    "RecoMuon_sel_pt",
    "RecoMuon_sel_px",
    "RecoMuon_sel_py",
    "RecoMuon_sel_pz",
    "RecoMuon_sel_y",
    "RecoMuon_sel_eta",
    "RecoMuon_sel_theta",
    "RecoMuon_sel_phi",
    "RecoMuon_sel_charge",
    "RecoMuon_sel_mass",
    "RecoMuonTrack_sel_absD0",
    "RecoMuonTrack_sel_absZ0",
    "RecoMuonTrack_sel_absD0sig",
    "RecoMuonTrack_sel_absZ0sig",
    "RecoMuonTrack_sel_D0cov",
    "RecoMuonTrack_sel_Z0cov",

    "n_RecoLeptons",
    "RecoLepton_e",
    "RecoLepton_p",
    "RecoLepton_pt",
    "RecoLepton_px",
    "RecoLepton_py",
    "RecoLepton_pz",
    "RecoLepton_y",
    "RecoLepton_eta",
    "RecoLepton_theta",
    "RecoLepton_phi",
    "RecoLepton_charge",
    "RecoLepton_mass",
    "RecoLeptonTrack_absD0",
    "RecoLeptonTrack_absZ0",
    "RecoLeptonTrack_absD0sig",
    "RecoLeptonTrack_absZ0sig",
    "RecoLeptonTrack_D0cov",
    "RecoLeptonTrack_Z0cov",

    "n_RecoLeptons_sel",
    "RecoLepton_sel_e",
    "RecoLepton_sel_p",
    "RecoLepton_sel_pt",
    "RecoLepton_sel_px",
    "RecoLepton_sel_py",
    "RecoLepton_sel_pz",
    "RecoLepton_sel_y",
    "RecoLepton_sel_eta",
    "RecoLepton_sel_theta",
    "RecoLepton_sel_phi",
    "RecoLepton_sel_charge",
    "RecoLepton_sel_mass",
    "RecoLeptonTrack_sel_absD0",
    "RecoLeptonTrack_sel_absZ0",
    "RecoLeptonTrack_sel_absD0sig",
    "RecoLeptonTrack_sel_absZ0sig",
    "RecoLeptonTrack_sel_D0cov",
    "RecoLeptonTrack_sel_Z0cov",

    "n_RecoPhotons",
    "RecoPhoton_e",
    "RecoPhoton_p",
    "RecoPhoton_pt",
    "RecoPhoton_px",
    "RecoPhoton_py",
    "RecoPhoton_pz",
    "RecoPhoton_y",
    "RecoPhoton_eta",
    "RecoPhoton_theta",
    "RecoPhoton_phi",
    "RecoPhoton_charge",
    "RecoPhoton_mass",

    "RecoEmiss_px",
    "RecoEmiss_py",
    "RecoEmiss_pz",
    "RecoEmiss_pt",
    "RecoEmiss_p",
    #"RecoEmiss_mass",
    "RecoEmiss_e",
    "RecoEmiss_eta",
    "RecoEmiss_phi",
    "RecoEmiss_theta",
    "RecoEmiss_y",
    "RecoEmiss_costheta",
]

VARIABLES_TAG = [
    
    "TauTag_px", 
    "TauTag_py",    
    "TauTag_pz",      
    "TauTag_p",  
    "TauTag_pt",    
    "TauTag_phi", 
    "TauTag_eta",     
    "TauTag_theta",          
    "TauTag_e",     
    "TauTag_mass",        
    "TauTag_mass",        
    # "TauTag_charge",       
    "TauTag_mass",          
    # "TauTag_charge",       
    "n_TauTag",          
    "TauTag_isG",  
    "TauTag_isU",
    "TauTag_isD",   
    "TauTag_isS",  
    "TauTag_isC",
    "TauTag_isB",  
    "TauTag_isTAU",

    "QuarkTag_px", 
    "QuarkTag_py",    
    "QuarkTag_pz",      
    "QuarkTag_p",  
    "QuarkTag_pt",    
    "QuarkTag_phi", 
    "QuarkTag_eta",     
    "QuarkTag_theta",          
    "QuarkTag_e",     
    "QuarkTag_mass",        
    "QuarkTag_mass",        
    #"QuarkTag_charge",       
    "QuarkTag_mass",          
    #"QuarkTag_charge",       
    "n_QuarkTag",          
    "QuarkTag_isG",  
    "QuarkTag_isU",
    "QuarkTag_isD",   
    "QuarkTag_isS",  
    "QuarkTag_isC",
    "QuarkTag_isB",  
    "QuarkTag_isTAU",

    "TauLead_type",
    "n_TauLead_constituents",
    "n_TauLead_charged_constituents",
    "n_TauLead_neutral_constituents",

    "TauSub_type",
    "n_TauSub_constituents",
    "n_TauSub_charged_constituents",
    "n_TauSub_neutral_constituents",
]

VARIABLES_LL = [

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

    "RecoZLead_px", 
    "RecoZLead_py",   
    "RecoZLead_pz",   
    "RecoZLead_p",    
    "RecoZLead_pt",   
    "RecoZLead_e",    
    "RecoZLead_eta",    
    "RecoZLead_phi",    
    "RecoZLead_theta",   
    "RecoZLead_y",     
    "RecoZLead_mass",   

    "RecoZSub_px",    
    "RecoZSub_py",   
    "RecoZSub_pz",   
    "RecoZSub_p",   
    "RecoZSub_pt",  
    "RecoZSub_e",     
    "RecoZSub_eta",   
    "RecoZSub_phi",   
    "RecoZSub_theta",    
    "RecoZSub_y",    
    "RecoZSub_mass",  

    "RecoZP_px", 
    "RecoZP_py",   
    "RecoZP_pz",   
    "RecoZP_p",    
    "RecoZP_pt",   
    "RecoZP_e",    
    "RecoZP_eta",    
    "RecoZP_phi",    
    "RecoZP_theta",   
    "RecoZP_y",     
    "RecoZP_mass",   

    "RecoZM_px",    
    "RecoZM_py",   
    "RecoZM_pz",   
    "RecoZM_p",   
    "RecoZM_pt",  
    "RecoZM_e",     
    "RecoZM_eta",   
    "RecoZM_phi",   
    "RecoZM_theta",    
    "RecoZM_y",    
    "RecoZM_mass",  

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

    #"TauP_px",    
    #"TauP_py",   
    #"TauP_pz",   
    #"TauP_p",   
    #"TauP_pt",   
    #"TauP_e",    
    #"TauP_eta",    
    #"TauP_phi",    
    #"TauP_theta",    
    #"TauP_y",    
    #"TauP_mass",
    #"TauP_type",
    #"n_TauP_constituents",
    #"n_TauP_charged_constituents",
    #"n_TauP_neutral_constituents",

    #"TauM_px",    
    #"TauM_py",   
    #"TauM_pz",   
    #"TauM_p",   
    #"TauM_pt",   
    #"TauM_e",    
    #"TauM_eta",    
    #"TauM_phi",    
    #"TauM_theta",    
    #"TauM_y",    
    #"TauM_mass",
    #"TauM_type",
    #"n_TauM_constituents",
    #"n_TauM_charged_constituents",
    #"n_TauM_neutral_constituents",

    "Recoil",
    "Collinear_mass", 

    "Tau_DR",
    "Tau_cos",
    "Tau_DEta", 
    "Tau_DPhi",
    
    "RecoZDaughter_DR", 
    "RecoZDaughter_cos", 
    "RecoZDaughter_DEta", 
    "RecoZDaughter_DPhi", 
]

VARIABLES_QQ = [

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

    "RecoZLead_px", 
    "RecoZLead_py",   
    "RecoZLead_pz",   
    "RecoZLead_p",    
    "RecoZLead_pt",   
    "RecoZLead_e",    
    "RecoZLead_eta",    
    "RecoZLead_phi",    
    "RecoZLead_theta",   
    "RecoZLead_y",     
    "RecoZLead_mass",   

    "RecoZSub_px",    
    "RecoZSub_py",   
    "RecoZSub_pz",   
    "RecoZSub_p",   
    "RecoZSub_pt",  
    "RecoZSub_e",     
    "RecoZSub_eta",   
    "RecoZSub_phi",   
    "RecoZSub_theta",    
    "RecoZSub_y",    
    "RecoZSub_mass",  

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

    #"TauP_px",    
    #"TauP_py",   
    #"TauP_pz",   
    #"TauP_p",   
    #"TauP_pt",   
    #"TauP_e",    
    #"TauP_eta",    
    #"TauP_phi",    
    #"TauP_theta",    
    #"TauP_y",    
    #"TauP_mass",
    #"TauP_type",
    #"n_TauP_constituents",
    #"n_TauP_charged_constituents",
    #"n_TauP_neutral_constituents",

    #"TauM_px",    
    #"TauM_py",   
    #"TauM_pz",   
    #"TauM_p",   
    #"TauM_pt",   
    #"TauM_e",    
    #"TauM_eta",    
    #"TauM_phi",    
    #"TauM_theta",    
    #"TauM_y",    
    #"TauM_mass",
    #"TauM_type",
    #"n_TauM_constituents",
    #"n_TauM_charged_constituents",
    #"n_TauM_neutral_constituents",

    "Recoil",
    "Collinear_mass", 

    "Tau_DR",
    "Tau_cos",
    "Tau_DEta", 
    "Tau_DPhi",
    
    "RecoZDaughter_DR", 
    "RecoZDaughter_cos", 
    "RecoZDaughter_DEta", 
    "RecoZDaughter_DPhi", 

    #"BDT_score_bkg",
]

VARIABLES_NuNu = [

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

    #"TauP_px",    
    #"TauP_py",   
    #"TauP_pz",   
    #"TauP_p",   
    #"TauP_pt",   
    #"TauP_e",    
    #"TauP_eta",    
    #"TauP_phi",    
    #"TauP_theta",    
    #"TauP_y",    
    #"TauP_mass",
    #"TauP_type",
    #"n_TauP_constituents",
    #"n_TauP_charged_constituents",
    #"n_TauP_neutral_constituents",

    #"TauM_px",    
    #"TauM_py",   
    #"TauM_pz",   
    #"TauM_p",   
    #"TauM_pt",   
    #"TauM_e",    
    #"TauM_eta",    
    #"TauM_phi",    
    #"TauM_theta",    
    #"TauM_y",    
    #"TauM_mass",
    #"TauM_type",
    #"n_TauM_constituents",
    #"n_TauM_charged_constituents",
    #"n_TauM_neutral_constituents",
    
    "Tau_DR",
    "Tau_cos",
    "Tau_DEta", 
    "Tau_DPhi",
    "Visible_mass",

    #"BDT_score_bkg",
    #"BDT_score_VBF",
    #"BDT_score_ZH",
]

LIST_VAR = {
    "QQ": VARIABLES_QQ,
    "LL":VARIABLES_LL,
    "NuNu":VARIABLES_NuNu,
}

#list of backgrounds, then legend and colors to be assigned to them
backgrounds_1 = [
    'wzp6_ee_mumu_ecm365',
    'wzp6_ee_ee_Mee_30_150_ecm365',
]
backgrounds_2 = [
    'wzp6_egamma_eZ_Zmumu_ecm365',
    'wzp6_egamma_eZ_Zee_ecm365',
    'wzp6_gammae_eZ_Zmumu_ecm365',
    'wzp6_gammae_eZ_Zee_ecm365',
]
backgrounds_3 = [
    'wzp6_gaga_mumu_60_ecm365',
    'wzp6_gaga_ee_60_ecm365',
]
backgrounds_4 = [
    'wzp6_ee_tautauH_Hbb_ecm365',
    'wzp6_ee_tautauH_Hcc_ecm365',
    'wzp6_ee_tautauH_Hss_ecm365',
]
backgrounds_5 = [
    'wzp6_ee_tautauH_HWW_ecm365',
    'wzp6_ee_tautauH_HZZ_ecm365',
]
backgrounds_6 = [
    'wzp6_ee_VBF_nunuH_Hbb_ecm365',
    'wzp6_ee_VBF_nunuH_Hcc_ecm365',
    'wzp6_ee_VBF_nunuH_Hss_ecm365',
]
backgrounds_7 = [
    'wzp6_ee_VBF_nunuH_HWW_ecm365',
    'wzp6_ee_VBF_nunuH_HZZ_ecm365',
]
backgrounds_8 = [
    'wzp6_ee_eeH_Hbb_ecm365',
    'wzp6_ee_eeH_Hcc_ecm365',
    'wzp6_ee_eeH_Hss_ecm365',

    'wzp6_ee_mumuH_Hbb_ecm365',
    'wzp6_ee_mumuH_Hcc_ecm365',
    'wzp6_ee_mumuH_Hss_ecm365',
]
backgrounds_9 = [
    'wzp6_ee_eeH_HWW_ecm365',
    'wzp6_ee_eeH_HZZ_ecm365',

    'wzp6_ee_mumuH_HWW_ecm365',
    'wzp6_ee_mumuH_HZZ_ecm365',
]
backgrounds_10 = [
    'wzp6_ee_eeH_Hbb_ecm365',
    'wzp6_ee_eeH_Hcc_ecm365',
    'wzp6_ee_eeH_Hss_ecm365',
]
backgrounds_11 = [
    'wzp6_ee_eeH_HWW_ecm365',
    'wzp6_ee_eeH_HZZ_ecm365',
]
backgrounds_12 = [
    'wzp6_ee_mumuH_Hbb_ecm365',
    'wzp6_ee_mumuH_Hcc_ecm365',
    'wzp6_ee_mumuH_Hss_ecm365',
]
backgrounds_13 = [
    'wzp6_ee_mumuH_HWW_ecm365',
    'wzp6_ee_mumuH_HZZ_ecm365',
]
backgrounds_14 = [
    'wzp6_ee_bbH_Hbb_ecm365',
    'wzp6_ee_bbH_Hcc_ecm365',
    'wzp6_ee_bbH_Hss_ecm365',

    'wzp6_ee_ccH_Hbb_ecm365',
    'wzp6_ee_ccH_Hcc_ecm365',
    'wzp6_ee_ccH_Hss_ecm365',

    'wzp6_ee_ssH_Hbb_ecm365',
    'wzp6_ee_ssH_Hcc_ecm365',
    'wzp6_ee_ssH_Hss_ecm365',

    'wzp6_ee_qqH_Hbb_ecm365',
    'wzp6_ee_qqH_Hcc_ecm365',
    'wzp6_ee_qqH_Hss_ecm365',
]
backgrounds_15 = [
    'wzp6_ee_bbH_Hbb_ecm365',
    'wzp6_ee_bbH_Hcc_ecm365',
    'wzp6_ee_bbH_Hss_ecm365',

    'wzp6_ee_ccH_Hbb_ecm365',
    'wzp6_ee_ccH_Hcc_ecm365',
    'wzp6_ee_ccH_Hss_ecm365',
]
backgrounds_16 = [
    'wzp6_ee_ssH_Hbb_ecm365',
    'wzp6_ee_ssH_Hcc_ecm365',
    'wzp6_ee_ssH_Hss_ecm365',

    'wzp6_ee_qqH_Hbb_ecm365',
    'wzp6_ee_qqH_Hcc_ecm365',
    'wzp6_ee_qqH_Hss_ecm365',
]
backgrounds_17 = [
    'wzp6_ee_bbH_HWW_ecm365',
    'wzp6_ee_bbH_HZZ_ecm365',

    'wzp6_ee_ccH_HWW_ecm365',
    'wzp6_ee_ccH_HZZ_ecm365',

    'wzp6_ee_ssH_HWW_ecm365',
    'wzp6_ee_ssH_HZZ_ecm365',
    
    'wzp6_ee_qqH_HWW_ecm365',
    'wzp6_ee_qqH_HZZ_ecm365',
]
backgrounds_18 = [
    'wzp6_ee_bbH_HWW_ecm365',
    'wzp6_ee_bbH_HZZ_ecm365',

    'wzp6_ee_ccH_HWW_ecm365',
    'wzp6_ee_ccH_HZZ_ecm365',
]
backgrounds_19 = [    
    'wzp6_ee_ssH_HWW_ecm365',
    'wzp6_ee_ssH_HZZ_ecm365',
    
    'wzp6_ee_qqH_HWW_ecm365',
    'wzp6_ee_qqH_HZZ_ecm365',
]
backgrounds_20 = [
    'wzp6_ee_bbH_Hgg_ecm365',
    'wzp6_ee_ccH_Hgg_ecm365',
    'wzp6_ee_ssH_Hgg_ecm365',
    'wzp6_ee_qqH_Hgg_ecm365',
]
backgrounds_21 = [
    'wzp6_ee_bbH_Hgg_ecm365',
    'wzp6_ee_ccH_Hgg_ecm365',
]
backgrounds_22 = [
    'wzp6_ee_ssH_Hgg_ecm365',
    'wzp6_ee_qqH_Hgg_ecm365',
]
backgrounds_23 = [
    'wzp6_ee_eeH_Hgg_ecm365',
    'wzp6_ee_mumuH_Hgg_ecm365',
]
backgrounds_28 = [
    'p8_ee_Zbb_ecm365',
    'p8_ee_Zcc_ecm365',
    'p8_ee_Zss_ecm365',
    'p8_ee_Zqq_ecm365', #only u d in this sample
]

backgrounds_29 = [
    'wzp6_ee_ZH_nunuH_Hbb_ecm365',
    'wzp6_ee_ZH_nunuH_Hcc_ecm365',
    'wzp6_ee_ZH_nunuH_Hss_ecm365',
]
backgrounds_30 = [
    'wzp6_ee_ZH_nunuH_HWW_ecm365',
    'wzp6_ee_ZH_nunuH_HZZ_ecm365',
]

#signals
backgrounds_24 = [
    'wzp6_ee_eeH_Htautau_ecm365',
    'wzp6_ee_mumuH_Htautau_ecm365',
]
backgrounds_25 = [
    'wzp6_ee_bbH_Htautau_ecm365',
    'wzp6_ee_ccH_Htautau_ecm365',

    'wzp6_ee_ssH_Htautau_ecm365',
    'wzp6_ee_qqH_Htautau_ecm365',
]
backgrounds_26 = [
    'wzp6_ee_bbH_Htautau_ecm365',
    'wzp6_ee_ccH_Htautau_ecm365',
]
backgrounds_27 = [
    'wzp6_ee_ssH_Htautau_ecm365',
    'wzp6_ee_qqH_Htautau_ecm365',
]

legend = {
    1:"wzp6_ee_LL_ecm365",

    2:"wzp6_ee_egamma_eZ_ZLL_ecm365",
    3:"wzp6_ee_gaga_LL_60_ecm365",

    4:"wzp6_ee_tautauH_HQQ_ecm365",
    5:"wzp6_ee_tautauH_HVV_ecm365",

    6:"wzp6_ee_VBF_nunuH_HQQ_ecm365",
    7:"wzp6_ee_VBF_nunuH_HVV_ecm365",

    8:"wzp6_ee_LLH_HQQ_ecm365",
    9:"wzp6_ee_LLH_HVV_ecm365",
    10:"wzp6_ee_eeH_HQQ_ecm365",
    11:"wzp6_ee_eeH_HVV_ecm365",
    12:"wzp6_ee_mumuH_HQQ_ecm365",
    13:"wzp6_ee_mumuH_HVV_ecm365",

    14:"wzp6_ee_QQH_HQQ_ecm365",
    15:"wzp6_ee_ZheavyH_HQQ_ecm365",
    16:"wzp6_ee_ZlightQH_HQQ_ecm365",
    17:"wzp6_ee_QQH_HVV_ecm365",
    18:"wzp6_ee_ZheavyH_HVV_ecm365",
    19:"wzp6_ee_ZlightH_HVV_ecm365",

    20:"wzp6_ee_QQH_Hgg_ecm365",
    21:"wzp6_ee_ZheavyH_Hgg_ecm365",
    22:"wzp6_ee_ZlightH_Hgg_ecm365",

    23:"wzp6_ee_LLH_Hgg_ecm365",

    28:"p8_ee_ZQQ_ecm365",
    29:"wzp6_ee_ZH_nunuH_HQQ_ecm365",
    30:"wzp6_ee_ZH_nunuH_HVV_ecm365",
    #signals
    24:"wzp6_ee_LLH_Htautau_ecm365",

    25:"wzp6_ee_QQH_Htautau_ecm365",
    26:"wzp6_ee_ZheavyH_Htautau_ecm365",
    27:"wzp6_ee_ZlightH_Htautau_ecm365",
}

list = {
    1:backgrounds_1,
    2:backgrounds_2,
    3:backgrounds_3,
    4:backgrounds_4,
    5:backgrounds_5,
    6:backgrounds_6,
    7:backgrounds_7,
    8:backgrounds_8,
    9:backgrounds_9,
    10:backgrounds_10,
    11:backgrounds_11,
    12:backgrounds_12,
    13:backgrounds_13,
    14:backgrounds_14,
    15:backgrounds_15,
    16:backgrounds_16,
    17:backgrounds_17,
    18:backgrounds_18,
    19:backgrounds_19,
    20:backgrounds_20,
    21:backgrounds_21,
    22:backgrounds_22,
    23:backgrounds_23,
    24:backgrounds_24,
    25:backgrounds_25,
    26:backgrounds_26,
    27:backgrounds_27,
    28:backgrounds_28,
    29:backgrounds_29,
    30:backgrounds_30,
}

nunuH = [
    'wzp6_ee_nunuH_Htautau_ecm365',
    'wzp6_ee_nunuH_Hbb_ecm365',
    'wzp6_ee_nunuH_Hcc_ecm365',
    'wzp6_ee_nunuH_Hss_ecm365',
    'wzp6_ee_nunuH_Hgg_ecm365',
    'wzp6_ee_nunuH_HWW_ecm365',
    'wzp6_ee_nunuH_HZZ_ecm365',
]
    
nuenueH = [
    'wzp6_ee_nuenueH_Htautau_ecm365',
    'wzp6_ee_nuenueH_Hbb_ecm365',
    'wzp6_ee_nuenueH_Hcc_ecm365',
    'wzp6_ee_nuenueH_Hss_ecm365',
    'wzp6_ee_nuenueH_Hgg_ecm365',
    'wzp6_ee_nuenueH_HWW_ecm365',
    'wzp6_ee_nuenueH_HZZ_ecm365',  
]

numunumuH = [
    'wzp6_ee_numunumuH_Htautau_ecm365',
    'wzp6_ee_numunumuH_Hbb_ecm365',
    'wzp6_ee_numunumuH_Hcc_ecm365',
    'wzp6_ee_numunumuH_Hss_ecm365',
    'wzp6_ee_numunumuH_Hgg_ecm365',
    'wzp6_ee_numunumuH_HWW_ecm365',
    'wzp6_ee_numunumuH_HZZ_ecm365',  
    ]

legend_ZH = {
    0:'wzp6_ee_ZH_nunuH_Htautau_ecm365',
    1:'wzp6_ee_ZH_nunuH_Hbb_ecm365',
    2:'wzp6_ee_ZH_nunuH_Hcc_ecm365',
    3:'wzp6_ee_ZH_nunuH_Hss_ecm365',
    4:'wzp6_ee_ZH_nunuH_Hgg_ecm365',
    5:'wzp6_ee_ZH_nunuH_HWW_ecm365',
    6:'wzp6_ee_ZH_nunuH_HZZ_ecm365', 
}

legend_VBF = {
    0:'wzp6_ee_VBFnunu_Htautau_ecm365',
    1:'wzp6_ee_VBFnunu_Hbb_ecm365',
    2:'wzp6_ee_VBFnunu_Hcc_ecm365',
    3:'wzp6_ee_VBFnunu_Hss_ecm365',
    4:'wzp6_ee_VBFnunu_Hgg_ecm365',
    5:'wzp6_ee_VBFnunu_HWW_ecm365',
    6:'wzp6_ee_VBFnunu_HZZ_ecm365', 
}

other_signal = [
    'wzp6_ee_eeH_Htautau_ecm365',
    'wzp6_ee_mumuH_Htautau_ecm365',
    'wzp6_ee_qqH_Htautau_ecm365',
    'wzp6_ee_ssH_Htautau_ecm365',
    'wzp6_ee_bbH_Htautau_ecm365',
    'wzp6_ee_ccH_Htautau_ecm365',
]

################# VBF - ZH nu nu ##################

'''for tag in TAG:
    for cat in CAT:
        for sub in SUBDIR:

            CUT = CUTS[cat]

            for cut in CUT:

                if "tag" in tag:
                    variables = VARIABLES + VARIABLES_TAG +LIST_VAR[cat]
                else: 
                    variables = VARIABLES + LIST_VAR[cat] 

                directory = DIRECTORY + tag + subdir + cat + "/" + sub + "/"

                # VBF = nuenueH - numunumuH
                for i in range(len(nunuH)):
                    output = f"{directory}{legend_VBF[i]}_{cut}_histo.root"
                    #print(output)
                    outFile = ROOT.TFile.Open(output, "RECREATE")
                    check = False
                    for var in variables:
                        file1 = f"{directory}{nuenueH[i]}_{cut}_histo.root"
                        file2 = f"{directory}{numunumuH[i]}_{cut}_histo.root"
                        hh1, hh2 = None, None
                        if file_exists(file1):
                            check = True
                            tf1 = ROOT.TFile.Open(file1, "READ")
                            h1 = tf1.Get(var)
                            hh1 = copy.deepcopy(h1)
                            hh1.SetDirectory(0)
                            tf1.Close()
                            if file_exists(file2):
                                tf2 = ROOT.TFile.Open(file2, "READ")
                                h2 = tf2.Get(var)
                                hh2 = copy.deepcopy(h2)
                                hh2.SetDirectory(0)
                                hh1.Add(hh2, -1)
                                tf2.Close()
                            
                        #write the histogram in the file   
                        if check==True:
                            outFile.cd()
                            hh1.Write()
                            print(f"{tag}, {cat}, {sub}, {cut}, {i}, {var} VBF")
                        
                    outFile.Close()
                    if check==False: #if nothing was written i don't want the file saved at all
                        os.remove(output)

                # ZH = nunuH - VBF = nunuH -nuenueH + numunumuH
                for i in range(len(nunuH)):
                    output = f"{directory}{legend_ZH[i]}_{cut}_histo.root"
                    #print(output)
                    outFile = ROOT.TFile.Open(output, "RECREATE")
                    check = False
                    for var in variables:
                        file = f"{directory}{nunuH[i]}_{cut}_histo.root"
                        file1 = f"{directory}{nuenueH[i]}_{cut}_histo.root"
                        file2 = f"{directory}{numunumuH[i]}_{cut}_histo.root"
                        hh, hh1, hh2 = None, None, None
                        if file_exists(file):
                            check = True
                            tf = ROOT.TFile.Open(file, "READ")
                            h = tf.Get(var)
                            hh = copy.deepcopy(h)
                            hh.SetDirectory(0)
                            tf.Close()
                            if file_exists(file1):
                                tf1 = ROOT.TFile.Open(file1, "READ")
                                h1 = tf1.Get(var)
                                hh1 = copy.deepcopy(h1)
                                hh1.SetDirectory(0)
                                hh.Add(hh1, -1)
                                tf1.Close()
                                if file_exists(file2):
                                    tf2 = ROOT.TFile.Open(file2, "READ")
                                    h2 = tf2.Get(var)
                                    hh2 = copy.deepcopy(h2)
                                    hh2.SetDirectory(0)
                                    hh.Add(hh2)
                                    tf2.Close()
                                
                        #write the histogram in the file   
                        if check==True:
                            outFile.cd()
                            hh.Write()
                            print(f"{tag}, {cat}, {sub}, {cut}, {i}, {var} ZH")

                    outFile.Close()
                    if check==False: #if nothing was written i don't want the file saved at all
                        os.remove(output)'''

##################### nunu ZH ###########################
for tag in TAG:
    for cat in CAT:
        for sub in SUBDIR:
            print("ZH")

            CUT = CUTS[cat]

            for cut in CUT:

                if "tag" in tag:
                    variables = VARIABLES + VARIABLES_TAG +LIST_VAR[cat]
                else: 
                    variables = VARIABLES + LIST_VAR[cat] 

                directory = DIRECTORY + tag + "/" + cat + "/" + sub + "/"

                # ZH = 3*numunumuH
                for i in range(len(nunuH)):
                    output = f"{directory}{legend_ZH[i]}_{cut}_histo.root"
                    #print(output)
                    outFile = ROOT.TFile.Open(output, "RECREATE")
                    check = False
                    for var in variables:
                        file2 = f"{directory}{numunumuH[i]}_{cut}_histo.root"
                        hh2 = None
                        if file_exists(file2):
                            tf2 = ROOT.TFile.Open(file2, "READ")
                            h2 = tf2.Get(var)
                            hh2 = copy.deepcopy(h2)
                            hh2.SetDirectory(0)
                            hh2.Scale(3.)
                            tf2.Close()
                                
                        #write the histogram in the file   
                        if check==True:
                            outFile.cd()
                            hh2.Write()
                            #print(f"{tag}, {cat}, {sub}, {cut}, {i}, {var} ZH")

                    outFile.Close()
                    if check==False: #if nothing was written i don't want the file saved at all
                        os.remove(output)

##################### ZH signal #########################

for tag in TAG:
    for cat in CAT:
        for sub in SUBDIR:

            CUT = CUTS[cat]

            for cut in CUT:

                if "tag" in tag:
                    variables = VARIABLES + VARIABLES_TAG +LIST_VAR[cat]
                else: 
                    variables = VARIABLES + LIST_VAR[cat] 

                directory = DIRECTORY + tag + "/" + cat + "/" + sub + "/"

                # ZH_nunu + all other ZH signals for Htautau
                output = f"{directory}wzp6_ee_ZH_Htautau_ecm365_{cut}_histo.root"
                #print(output)
                outFile = ROOT.TFile.Open(output, "RECREATE")
                check = False
                for var in variables:
                    file = f"{directory}wzp6_ee_ZH_nunuH_Htautau_ecm365_{cut}_histo.root"
                    hh = None
                    if file_exists(file):
                        print(file)
                        tf = ROOT.TFile.Open(file, "READ")
                        h = tf.Get(var)
                        check = True
                        hh = copy.deepcopy(h)
                        hh.SetDirectory(0)
                        tf.Close()
                    for s in other_signal:
                        file3 = f"{directory}{s}_{cut}_histo.root"
                        if file_exists(file3):
                            tf3 = ROOT.TFile.Open(file3, "READ")
                            h3 = tf3.Get(var)
                            print(f"variable {var} in file {s}")
                            hh3 = copy.deepcopy(h3)
                            hh3.SetDirectory(0)
                            if hh:  
                                #print(f"ZHnunu already present")
                                hh.Add(hh3)
                            else:
                                #print(f"no ZHnunu, adding histo now")
                                hh = copy.deepcopy(h3)
                            check = True
                            tf3.Close()
                                
                    #write the histogram in the file   
                    if check: #either there is ZH nunu or the rest so it's safe to use the file for combine only, plotting them separately as usual
                        outFile.cd()
                        hh.Write()
                        print(f"{tag}, {cat}, {sub}, {cut}, {var} ZH")

                outFile.Close()
                if check==False: #if nothing was written i don't want the file saved at all
                    os.remove(output)

#################### now add the decays for all #####################
for tag in TAG:
    print(tag)
    for cat in CAT:
        print(cat)
        for sub in SUBDIR:
            print(sub)

            CUT = CUTS[cat]

            for cut in CUT:

                if "tag" in tag:
                    variables = VARIABLES + VARIABLES_TAG +LIST_VAR[cat]
                else: 
                    variables = VARIABLES + LIST_VAR[cat] 

                directory = DIRECTORY + tag + "/" + cat + "/" + sub + "/"
            
                for num in range(1,31):
                    output = f"{directory}{legend[num]}_{cut}_histo.root"
                    #print(output)
                    outFile = ROOT.TFile.Open(output, "RECREATE")
                    check = False
                    for var in variables:
                        #loop to merge different sources into one histograms for easier plotting
                        j = 0
                        hh = None
                        #print(list)
                        for b in list[num]:
                            #print(var)
                            #print(b)
                            file = f"{directory}{b}_{cut}_histo.root"
                            #print(file)
                            if file_exists(file):
                                check = True
                                tf = ROOT.TFile.Open(file, "READ")
                                if (j==0):
                                    h = tf.Get(var)
                                    hh = copy.deepcopy(h)
                                    hh.SetDirectory(0)
                                else:
                                    h = tf.Get(var)
                                    hh1 = copy.deepcopy(h)
                                    hh1.SetDirectory(0)
                                    hh.Add(hh1)
                                j += 1
                                tf.Close()
                        #write the histogram in the file   
                        if check==True:
                            outFile.cd()
                            hh.Write()
                        #print(f"{tag}, {cat}, {sub}, {cut}, {num}, {var}")
                        
                    outFile.Close()
                    if check==False: #if nothing was written i don't want the file saved at all
                        os.remove(output)

