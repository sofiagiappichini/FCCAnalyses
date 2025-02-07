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

def sorted_dict_values(dic: dict) -> list:
    ''''
    Sort values in the dictionary.
    '''
    keys = sorted(dic)
    return [dic[key] for key in keys]

def make_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        os.system("cp /web/sgiappic/public_html/index.php {}".format(directory)) #copy index to show plots in web page automatically
        print(f"Directory created successfully.")
    else:
        print(f"Directory already exists.")

def file_exists(file_path):
    return os.path.isfile(file_path)

# directory with final stage files
DIRECTORY = "/ceph/awiedl/FCCee/HiggsCP/ecm240/"
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
    #"QQ",
    #"LL",
    "NuNu",
]

#list of cuts you want to plot
CUTS_LLHH = [
    #"selReco",
    #"selReco_100Coll150",
    #"selReco_100Coll150_115Rec160",
    #"selReco_100Coll150_115Rec160_2DR",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_4Emiss",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_4Emiss", 
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_4Emiss_Zp54",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.96_80Z100_4Emiss_Zp54",
]

CUTS_LLLH = [
    #"selReco",
    #"selReco_100Coll150",
    #"selReco_100Coll150_115Rec160",
    #"selReco_100Coll150_115Rec160_2DR",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_4Emiss",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_84Z100_4Emiss", 
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_84Z100_4Emiss_Zp54",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.88_84Z100_4Emiss_Zp54",
]

CUTS_LLLL = [
    #"selReco",
    #"selReco_100Coll150",
    #"selReco_100Coll150_115Rec160",
    #"selReco_100Coll150_115Rec160_2DR",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_40Emiss",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_40Emiss", 
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_40Emiss_Zp54",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.9_80Z100_40Emiss_Zp54",
]

CUTS_QQHH = [
    #"selReco_0.5BDT",
    #"selReco_100Coll150",
    #"selReco_100Coll150_115Rec160",
    #"selReco_100Coll150_115Rec160_2DR",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_8Emiss",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_8Emiss_Zp52",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.86_70Z100_8Emiss_Zp52",
]

CUTS_QQLH = [
    #"selReco",
    #"selReco_100Coll150",
    #"selReco_100Coll150_115Rec160",
    #"selReco_100Coll150_115Rec160_2DR",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_36Emiss",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_36Emiss",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_36Emiss_Zp52",
]

CUTS_QQLL = [
    #"selReco",
    #"selReco_100Coll150",
    #"selReco_100Coll150_115Rec160",
    #"selReco_100Coll150_115Rec160_2DR",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_52Emiss",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_52Emiss_Zp52",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.92_70Z100_52Emiss_Zp52",
]
    
CUTS_NuNuHH = [
    #"selReco",
    #"selReco_100Me",
    #"selReco_100Me_TauDPhi3",
    #"selReco_100Me_TauDPhi3_2DR",
    #"selReco_100Me_TauDPhi3_2DR_cos0.4",
    #"selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    #"selReco_112Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    #"selReco_112Me_TauDPhi3_2DR_cos0.4_misscos0.88_missy1",
]

CUTS_NuNuLH = [
    #"selReco",
    #"selReco_100Me",
    #"selReco_100Me_TauDPhi3",
    #"selReco_100Me_TauDPhi3_2DR",
    #"selReco_100Me_TauDPhi3_2DR_cos0.4",
    #"selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    #"selReco_140Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    #"selReco_140Me_TauDPhi3_2DR_cos0.4_misscos0.94_missy1",
]

CUTS_NuNuLL = [
    #"selReco",
    #"selReco_100Me",
    #"selReco_100Me_TauDPhi3",
    #"selReco_100Me_TauDPhi3_2DR",
    #"selReco_100Me_TauDPhi3_2DR_cos0.4",
    #"selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    #"selReco_152Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    #"selReco_152Me_TauDPhi3_2DR_cos0.4_misscos0.92_missy1",
]

CUTS = {
    'LLLL':CUTS_LLLL,
    'LLLH':CUTS_LLLH,
    'LLHH':CUTS_LLHH,
    'QQLL':CUTS_QQLL,
    'QQLH':CUTS_QQLH,
    'QQHH':CUTS_QQHH,
    'NuNuLL':CUTS_NuNuLL,
    'NuNuLH':CUTS_NuNuLH,
    'NuNuHH':CUTS_NuNuHH,
}

#now you can list all the histograms that you want to plot
VARIABLES_GEN = [
    ######## Monte-Carlo particles #######
    "n_FSGenElectron",
    "FSGenElectron_e",
    "FSGenElectron_p",
    "FSGenElectron_pt",
    "FSGenElectron_px",
    "FSGenElectron_py",
    "FSGenElectron_pz",
    "FSGenElectron_y",
    "FSGenElectron_eta",
    "FSGenElectron_theta",
    "FSGenElectron_phi",
    "FSGenElectron_charge",
    "FSGenElectron_mass",
    "FSGenElectron_parentPDG",
    "FSGenElectron_vertex_x",
    "FSGenElectron_vertex_y",
    "FSGenElectron_vertex_z",

    "n_FSGenMuon",
    "FSGenMuon_e",
    "FSGenMuon_p",
    "FSGenMuon_pt",
    "FSGenMuon_px",
    "FSGenMuon_py",
    "FSGenMuon_pz",
    "FSGenMuon_y",
    "FSGenMuon_eta",
    "FSGenMuon_theta",
    "FSGenMuon_phi",
    "FSGenMuon_charge",
    "FSGenMuon_mass",
    "FSGenMuon_parentPDG",
    "FSGenMuon_vertex_x",
    "FSGenMuon_vertex_y",
    "FSGenMuon_vertex_z",

    #"n_AllGenTau",
    #"AllGenTau_e",
    #"AllGenTau_p",
    #"AllGenTau_pt",
    #"AllGenTau_px",
    #"AllGenTau_py",
    #"AllGenTau_pz",
    #"AllGenTau_y",
    #"AllGenTau_eta",
    #"AllGenTau_theta",
    #"AllGenTau_phi",
    #"AllGenTau_charge",
    #"AllGenTau_mass",
    #"AllGenTau_parentPDG",
    #"AllGenTau_vertex_x",
    #"AllGenTau_vertex_y",
    #"AllGenTau_vertex_z",

    "n_HiggsGenTau",
    "HiggsGenTau_e",
    "HiggsGenTau_p",
    "HiggsGenTau_pt",
    "HiggsGenTau_px",
    "HiggsGenTau_py",
    "HiggsGenTau_pz",
    "HiggsGenTau_y",
    "HiggsGenTau_eta",
    "HiggsGenTau_theta",
    "HiggsGenTau_phi",
    "HiggsGenTau_charge",
    "HiggsGenTau_mass",
    "HiggsGenTau_parentPDG",
    "HiggsGenTau_vertex_x",
    "HiggsGenTau_vertex_y",
    "HiggsGenTau_vertex_z",

    "n_FSGenNeutrino",
    "FSGenNeutrino_e",
    "FSGenNeutrino_p",
    "FSGenNeutrino_pt",
    "FSGenNeutrino_px",
    "FSGenNeutrino_py",
    "FSGenNeutrino_pz",
    "FSGenNeutrino_y",
    "FSGenNeutrino_eta",
    "FSGenNeutrino_theta",
    "FSGenNeutrino_phi",
    "FSGenNeutrino_charge",
    #"FSGenNeutrino_parentPDG",

    "n_FSGenPhoton",
    "FSGenPhoton_e",
    "FSGenPhoton_p",
    "FSGenPhoton_pt",
    "FSGenPhoton_px",
    "FSGenPhoton_py",
    "FSGenPhoton_pz",
    "FSGenPhoton_y",
    "FSGenPhoton_eta",
    "FSGenPhoton_theta",
    "FSGenPhoton_phi",
    "FSGenPhoton_charge",
    #"FSGenPhoton_parentPDG",

    "n_GenHiggs",
    "GenHiggs_e",
    "GenHiggs_p", 
    "GenHiggs_pt", 
    "GenHiggs_px", 
    "GenHiggs_py", 
    "GenHiggs_pz", 
    "GenHiggs_y", 
    "GenHiggs_mass",
    "GenHiggs_eta", 
    "GenHiggs_theta", 
    "GenHiggs_phi", 
    "GenHiggs_charge", 
]

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

    "n_NeutralHadrons",
    "NeutralHadrons_e",
    "NeutralHadrons_p",
    "NeutralHadrons_pt",
    "NeutralHadrons_px",
    "NeutralHadrons_py",
    "NeutralHadrons_pz",
    "NeutralHadrons_eta",
    "NeutralHadrons_theta",
    "NeutralHadrons_phi",
    "NeutralHadrons_charge",
    "NeutralHadrons_mass",

    #"n_NoEfficiency",
    #"NoEfficiency_e",
    #"NoEfficiency_p",
    #"NoEfficiency_pt",
    #"NoEfficiency_px",
    #"NoEfficiency_py",
    #"NoEfficiency_pz",
    #"NoEfficiency_eta",
    #"NoEfficiency_theta",
    #"NoEfficiency_phi",
    #"NoEfficiency_charge",
    #"NoEfficiency_type",
    #"NoEfficiency_mass",

    "RecoEmiss_px",
    "RecoEmiss_py",
    "RecoEmiss_pz",
    "RecoEmiss_pt",
    "RecoEmiss_p",
    "RecoEmiss_e",

    #"TagJet_R5_px", 
    #"TagJet_R5_py",    
    #"TagJet_R5_pz",      
    #"TagJet_R5_p",  
    #"TagJet_R5_pt",    
    #"TagJet_R5_phi", 
    #"TagJet_R5_eta",     
    #"TagJet_R5_theta",          
    #"TagJet_R5_e",     
    #"TagJet_R5_mass",        
    #"TagJet_R5_charge",  
    #"n_TagJet_R5_constituents",   
    #"n_TagJet_R5_charged_constituents",   
    #"n_TagJet_R5_neutral_constituents",   
    #"n_TagJet_R5",           

    #"TagJet_R5_isG",  
    #"TagJet_R5_isU",
    #"TagJet_R5_isD",   
    #"TagJet_R5_isS",  
    #"TagJet_R5_isC",
    #"TagJet_R5_isB",  
    #"TagJet_R5_isTAU",

    #"TauFromJet_R5_p",
    #"TauFromJet_R5_pt",
    #"TauFromJet_R5_px",
    #"TauFromJet_R5_py",
    #"TauFromJet_R5_pz",
    #"TauFromJet_R5_theta",
    #"TauFromJet_R5_phi",
    #"TauFromJet_R5_e",
    #"TauFromJet_R5_eta",
    #"TauFromJet_R5_y",
    #"TauFromJet_R5_charge",
    #"TauFromJet_R5_type",
    #"TauFromJet_R5_mass",
    #"n_TauFromJet_R5",

    #"TagJet_R5_sel_e",     
    #"TagJet_R5_sel_p",     
    #"TagJet_R5_sel_pt",     
    #"TagJet_R5_sel_px",   
    #"TagJet_R5_sel_py",   
    #"TagJet_R5_sel_pz",     
    #"TagJet_R5_sel_eta",    
    #"TagJet_R5_sel_theta",   
    #"TagJet_R5_sel_phi",     
    #"TagJet_R5_sel_mass",      
    #"n_TagJet_R5_sel", 
    
    #"TagJet_kt4_px", 
    #"TagJet_kt4_py",    
    #"TagJet_kt4_pz",      
    #"TagJet_kt4_p",  
    #"TagJet_kt4_pt",    
    #"TagJet_kt4_phi", 
    #"TagJet_kt4_eta",     
    #"TagJet_kt4_theta",          
    #"TagJet_kt4_e",     
    #"TagJet_kt4_mass",        
    #"TagJet_kt4_charge",  
    #"n_TagJet_kt4_constituents",   
    #"n_TagJet_kt4_charged_constituents",   
    #"n_TagJet_kt4_neutral_constituents",   
    #"n_TagJet_kt4",          

    #"TagJet_kt4_isG",  
    #"TagJet_kt4_isU",
    #"TagJet_kt4_isD",   
    #"TagJet_kt4_isS",  
    #"TagJet_kt4_isC",
    #"TagJet_kt4_isB",  
    #"TagJet_kt4_isTAU",

    #"TauFromJet_kt4_p",
    #"TauFromJet_kt4_pt",
    #"TauFromJet_kt4_px",
    #"TauFromJet_kt4_py",
    #"TauFromJet_kt4_pz",
    #"TauFromJet_kt4_theta",
    #"TauFromJet_kt4_phi",
    #"TauFromJet_kt4_e",
    #"TauFromJet_kt4_eta",
    #"TauFromJet_kt4_y",
    #"TauFromJet_kt4_charge",
    #"TauFromJet_kt4_type",
    #"TauFromJet_kt4_mass",
    #"n_TauFromJet_kt4",

    #"TagJet_kt4_sel_e",     
    #"TagJet_kt4_sel_p",     
    #"TagJet_kt4_sel_pt",     
    #"TagJet_kt4_sel_px",   
    #"TagJet_kt4_sel_py",   
    #"TagJet_kt4_sel_pz",     
    #"TagJet_kt4_sel_eta",    
    #"TagJet_kt4_sel_theta",   
    #"TagJet_kt4_sel_phi",     
    #"TagJet_kt4_sel_mass",      
    #"n_TagJet_kt4_sel",

    #"TagJet_kt3_px", 
    #"TagJet_kt3_py",    
    #"TagJet_kt3_pz",      
    #"TagJet_kt3_p",  
    #"TagJet_kt3_pt",    
    #"TagJet_kt3_phi", 
    #"TagJet_kt3_eta",     
    #"TagJet_kt3_theta",          
    #"TagJet_kt3_e",     
    #"TagJet_kt3_mass",        
    #"TagJet_kt3_charge",       
    #"n_TagJet_kt3_constituents",   
    #"n_TagJet_kt3_charged_constituents",   
    #"n_TagJet_kt3_neutral_constituents",   
    #"n_TagJet_kt3",          

    #"TagJet_kt3_isG",  
    #"TagJet_kt3_isU",
    #"TagJet_kt3_isD",   
    #"TagJet_kt3_isS",  
    #"TagJet_kt3_isC",
    #"TagJet_kt3_isB",  
    #"TagJet_kt3_isTAU",

    #"TauFromJet_kt3_p",
    #"TauFromJet_kt3_pt",
    #"TauFromJet_kt3_px",
    #"TauFromJet_kt3_py",
    #"TauFromJet_kt3_pz",
    #"TauFromJet_kt3_theta",
    #"TauFromJet_kt3_phi",
    #"TauFromJet_kt3_e",
    #"TauFromJet_kt3_eta",
    #"TauFromJet_kt3_y",
    #"TauFromJet_kt3_charge",
    #"TauFromJet_kt3_type",
    #"TauFromJet_kt3_mass",
    #"n_TauFromJet_kt3",

    #"TagJet_kt3_sel_e",     
    #"TagJet_kt3_sel_p",     
    #"TagJet_kt3_sel_pt",     
    #"TagJet_kt3_sel_px",   
    #"TagJet_kt3_sel_py",   
    #"TagJet_kt3_sel_pz",     
    #"TagJet_kt3_sel_eta",    
    #"TagJet_kt3_sel_theta",   
    #"TagJet_kt3_sel_phi",     
    #"TagJet_kt3_sel_mass",      
    #"n_TagJet_kt3_sel",

    #"TagJet_kt2_px", 
    #"TagJet_kt2_py",    
    #"TagJet_kt2_pz",      
    #"TagJet_kt2_p",  
    #"TagJet_kt2_pt",    
    #"TagJet_kt2_phi", 
    #"TagJet_kt2_eta",     
    #"TagJet_kt2_theta",          
    #"TagJet_kt2_e",     
    #"TagJet_kt2_mass",        
    #"TagJet_kt2_charge",    
    #"n_TagJet_kt2_constituents",   
    #"n_TagJet_kt2_charged_constituents",   
    #"n_TagJet_kt2_neutral_constituents",   
    #"n_TagJet_kt2",          

    #"TagJet_kt2_isG",  
    #"TagJet_kt2_isU",
    #"TagJet_kt2_isD",   
    #"TagJet_kt2_isS",  
    #"TagJet_kt2_isC",
    #"TagJet_kt2_isB",  
    #"TagJet_kt2_isTAU",

    #"TauFromJet_kt2_p",
    #"TauFromJet_kt2_pt",
    #"TauFromJet_kt2_px",
    #"TauFromJet_kt2_py",
    #"TauFromJet_kt2_pz",
    #"TauFromJet_kt2_theta",
    #"TauFromJet_kt2_phi",
    #"TauFromJet_kt2_e",
    #"TauFromJet_kt2_eta",
    #"TauFromJet_kt2_y",
    #"TauFromJet_kt2_charge",
    #"TauFromJet_kt2_type",
    #"TauFromJet_kt2_mass",
    #"n_TauFromJet_kt2",

    #"TagJet_kt2_sel_e",     
    #"TagJet_kt2_sel_p",     
    #"TagJet_kt2_sel_pt",     
    #"TagJet_kt2_sel_px",   
    #"TagJet_kt2_sel_py",   
    #"TagJet_kt2_sel_pz",     
    #"TagJet_kt2_sel_eta",    
    #"TagJet_kt2_sel_theta",   
    #"TagJet_kt2_sel_phi",     
    #"TagJet_kt2_sel_mass",      
    #"n_TagJet_kt2_sel",

    #"TagJet_kt1_px", 
    #"TagJet_kt1_py",    
    #"TagJet_kt1_pz",      
    #"TagJet_kt1_p",  
    #"TagJet_kt1_pt",    
    #"TagJet_kt1_phi", 
    #"TagJet_kt1_eta",     
    #"TagJet_kt1_theta",          
    #"TagJet_kt1_e",     
    #"TagJet_kt1_mass",        
    #"TagJet_kt1_charge",   
    #"n_TagJet_kt1_constituents",   
    #"n_TagJet_kt1_charged_constituents",   
    #"n_TagJet_kt1_neutral_constituents",   
    #"n_TagJet_kt1",          

    #"TagJet_kt1_isG",  
    #"TagJet_kt1_isU",
    #"TagJet_kt1_isD",   
    #"TagJet_kt1_isS",  
    #"TagJet_kt1_isC",
    #"TagJet_kt1_isB",  
    #"TagJet_kt1_isTAU",

    #"TauFromJet_kt1_p",
    #"TauFromJet_kt1_pt",
    #"TauFromJet_kt1_px",
    #"TauFromJet_kt1_py",
    #"TauFromJet_kt1_pz",
    #"TauFromJet_kt1_theta",
    #"TauFromJet_kt1_phi",
    #"TauFromJet_kt1_e",
    #"TauFromJet_kt1_eta",
    #"TauFromJet_kt1_y",
    #"TauFromJet_kt1_charge",
    #"TauFromJet_kt1_type",
    #"TauFromJet_kt1_mass",
    #"n_TauFromJet_kt1",

    #"TagJet_kt1_sel_e",     
    #"TagJet_kt1_sel_p",     
    #"TagJet_kt1_sel_pt",     
    #"TagJet_kt1_sel_px",   
    #"TagJet_kt1_sel_py",   
    #"TagJet_kt1_sel_pz",     
    #"TagJet_kt1_sel_eta",    
    #"TagJet_kt1_sel_theta",   
    #"TagJet_kt1_sel_phi",     
    #"TagJet_kt1_sel_mass",      
    #"n_TagJet_kt1_sel",

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

    #"BDT_score",
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

    #"BDT_score",
]

LIST_VAR = {
    "QQ": VARIABLES_QQ,
    "LL":VARIABLES_LL,
    "NuNu":VARIABLES_NuNu,
}

#directory where you want your plots to go
DIR_PLOTS = '/web/sgiappic/public_html/Higgs_xsec/' 

#labels for the cuts in the plots
LABELS = {
    "selReco": "No additional selection",
    "selReco_100Coll150": "100<M_{collinear}<150 GeV",
    "selReco_100Coll150_115Rec160": "100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV",
    "selReco_100Coll150_115Rec160_10Me": "100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV",

    "selReco_100Coll150_115Rec160_2DR": "100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2",
    "selReco_100Coll150_115Rec160_2DR_cos0.6": "100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_10ME": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>10 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_QTAU0.5": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_QTAU0.5_10ME": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>10 GeV}",

    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_4Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>4 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_4Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 80<M_{Z}<100 GeV, E_{miss}>4 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_4Emiss_Zp54": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 80<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<54 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.96_80Z100_4Emiss_Zp54": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.96, 80<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<54 GeV}",
    
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_84Z100_4Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 84<M_{Z}<100 GeV, E_{miss}>4 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_84Z100_4Emiss_Zp54": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 84<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<54 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.88_84Z100_4Emiss_Zp54": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.88, 84<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<54 GeV}",
    
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_40Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>40 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_40Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 80<M_{Z}<100 GeV, E_{miss}>40 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_40Emiss_Zp54": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 80<M_{Z}<100 GeV, E_{miss}>40 GeV, p_{Z}<54 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.9_80Z100_40Emiss_Zp54": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.9, 80<M_{Z}<100 GeV, E_{miss}>40 GeV, p_{Z}<54 GeV}",

    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_8Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>4 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_8Emiss_Zp52": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<52 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.86_70Z100_8Emiss_Zp52": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.86, 70<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<52 GeV}",

    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_8Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 75<M_{Z}<100 GeV, E_{miss}>4 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_8Emiss_Zp52": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 75<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<52 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.86_75Z100_8Emiss_Zp52": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.86, 75<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<52 GeV}",
    
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_36Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>36 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_36Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 75<M_{Z}<100 GeV, E_{miss}>36 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_36Emiss_Zp52": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 75<M_{Z}<100 GeV, E_{miss}>36 GeV, p_{Z}<52 GeV}",

    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_52Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>52 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_52Emiss_Zp52": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>52 GeV, p_{Z}<52 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.92_70Z100_52Emiss_Zp52": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.92, 70<M_{Z}<100 GeV, E_{miss}>52 GeV, p_{Z}<52 GeV}",

    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_86Z100_4Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 86<M_{Z}<100 GeV, E_{miss}>4 GeV",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_86Z100_4Emiss_Zp54": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 86<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<54 GeV",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.96_86Z100_4Emiss_Zp54": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.96, 86<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<54 GeV",

    #cuts for LL
    "selReco_100Coll150_115Rec160_10Me_70Z100": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{70<M_{Z}<110 GeV}",
    "selReco_100Coll150_115Rec160_10Me_70Z100_2DR": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{70<M_{Z}<110 GeV, #Delta R_{#tau}>2}",
    "selReco_100Coll150_115Rec160_10Me_70Z100_2DR_cos0.6": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{70<M_{Z}<110 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6}",
    "selReco_100Coll150_115Rec160_10Me_70Z100_2DR_cos0.6_misscos0.98": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{70<M_{Z}<110 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6, |cos#theta_{miss}|<0.98}",

    #cuts for QQ
    "selReco_100Coll150_115Rec160_10Me_80Z95": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{80<M_{Z}<95 GeV}",
    "selReco_100Coll150_115Rec160_10Me_80Z95_2DR": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{80<M_{Z}<95 GeV, #Delta R_{#tau}>2}",
    "selReco_100Coll150_115Rec160_10Me_80Z95_2DR_cos0.6": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{80<M_{Z}<95 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6}",
    "selReco_100Coll150_115Rec160_10Me_80Z95_2DR_cos0.6_misscos0.98": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{80<M_{Z}<95 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6, |cos#theta_{miss}|<0.98}",
    
    "selReco_0.5BDT":"100<M_{collinear}<150 GeV, BDT score>0.5",
    "selReco_0.6BDT":"100<M_{collinear}<150 GeV, BDT score>0.6",
    "selReco_0.7BDT":"100<M_{collinear}<150 GeV, BDT score>0.7",

    #cuts for NuNu
    "selReco_100Me": "E_{miss}>100 GeV",
    "selReco_100Me_TauDPhi3": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3",
    "selReco_100Me_TauDPhi3_2DR": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2",
    "selReco_100Me_TauDPhi3_2DR_cos0.4": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.98",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.98, |y_{miss}|<1",

    "selReco_112Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1": "E_{miss}>112 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.98, |y_{miss}|<1",
    "selReco_112Me_TauDPhi3_2DR_cos0.4_misscos0.88_missy1": "E_{miss}>112 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.88, |y_{miss}|<1",
     
    "selReco_140Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1": "E_{miss}>112 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.98, |y_{miss}|<1",
    "selReco_140Me_TauDPhi3_2DR_cos0.4_misscos0.94_missy1": "E_{miss}>112 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.94, |y_{miss}|<1",

    "selReco_152Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1": "E_{miss}>112 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.98, |y_{miss}|<1",
    "selReco_152Me_TauDPhi3_2DR_cos0.4_misscos0.92_missy1": "E_{miss}>112 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.92, |y_{miss}|<1",

    #"selReco_0.5BDT":"E_{miss}>100 GeV, BDT score>0.5",
    #"selReco_0.6BDT":"E_{miss}>100 GeV, BDT score>0.6",
    #"selReco_0.7BDT":"E_{miss}>100 GeV, BDT score>0.7",

 }

ana_tex_cat = {
    'LL':"e^{+}e^{-} #rightarrow Z H, Z #rightarrow LL, ",
    'QQ':"e^{+}e^{-} #rightarrow Z H, Z #rightarrow qq, ",
    'NuNu':"e^{+}e^{-} #rightarrow Z H, Z #rightarrow #nu#nu, ",
    }

ana_tex_sub = {
    'LL':"H #rightarrow #tau_{L}#tau_{L}",
    'LH':"H #rightarrow #tau_{L}#tau_{h}",
    'HH':"H #rightarrow #tau_{h}#tau_{h}",
    }

energy         = 240
collider       = 'FCC-ee'
intLumi        = 10.8 #ab-1
LOGY = True

#list of backgorunds, then legend and colors to be assigned to them
backgrounds_all = [
    "p8_ee_WW_ecm240",
    "p8_ee_Zqq_ecm240",
    "p8_ee_ZZ_ecm240",

    "wzp6_ee_LL_ecm240",
    "wzp6_ee_tautau_ecm240",

    "wzp6_ee_nuenueZ_ecm240",

    "wzp6_ee_egamma_eZ_ZLL_ecm240",
    
    "wzp6_ee_gaga_LL_60_ecm240",
    "wzp6_ee_gaga_tautau_60_ecm240",

    "wzp6_ee_tautauH_Htautau_ecm240",
    "wzp6_ee_tautauH_HQQ_ecm240",
    "wzp6_ee_tautauH_Hgg_ecm240",
    "wzp6_ee_tautauH_HVV_ecm240",

    #"wzp6_ee_nunuH_Htautau_ecm240",
    "wzp6_ee_nunuH_HQQ_ecm240",
    "wzp6_ee_nunuH_Hgg_ecm240",
    "wzp6_ee_nunuH_HVV_ecm240",

    #"wzp6_ee_LLH_Htautau_ecm240",
    "wzp6_ee_LLH_HQQ_ecm240",
    "wzp6_ee_LLH_Hgg_ecm240",
    "wzp6_ee_LLH_HVV_ecm240",

    #"wzp6_ee_QQH_Htautau_ecm240",
    "wzp6_ee_QQH_HQQ_ecm240",
    "wzp6_ee_QQH_Hgg_ecm240",
    "wzp6_ee_QQH_HVV_ecm240",

    #"wzp6_ee_eeH_Htautau_ecm240",
    #"wzp6_ee_eeH_HQQ_ecm240",
    #"wzp6_ee_eeH_Hgg_ecm240",
    #"wzp6_ee_eeH_HVV_ecm240",

    #"wzp6_ee_mumuH_Htautau_ecm240",
    #"wzp6_ee_mumuH_HQQ_ecm240",
    #"wzp6_ee_mumuH_Hgg_ecm240",
    #"wzp6_ee_mumuH_HVV_ecm240",

    #"wzp6_ee_ZheavyH_Htautau_ecm240",
    #"wzp6_ee_ZheavyH_HQQ_ecm240",
    #"wzp6_ee_ZheavyH_Hgg_ecm240",
    #"wzp6_ee_ZheavyH_HVV_ecm240",

    #"wzp6_ee_ZlightH_Htautau_ecm240",
    #"wzp6_ee_ZlightH_HQQ_ecm240",
    #"wzp6_ee_ZlightH_Hgg_ecm240",
    #"wzp6_ee_ZlightH_HVV_ecm240",
]

legend = {
    'p8_ee_WW_ecm240':"WW",
    'p8_ee_Zqq_ecm240':"Z #rightarrow QQ",
    'p8_ee_ZZ_ecm240':"ZZ",

    'wzp6_ee_LL_ecm240':"e^{+}e^{-}#rightarrow ll",
    'wzp6_ee_tautau_ecm240':"e^{+}e^{-}#rightarrow #tau#tau",

    "wzp6_ee_nuenueZ_ecm240":"e^{+}e^{-}#rightarrow #nu_{e}#nu_{e} Z",

    "wzp6_ee_egamma_eZ_ZLL_ecm240":"e#gamma #rightarrow eZ(ll)",
    
    "wzp6_ee_gaga_LL_60_ecm240":"#gamma#gamma #rightarrow ll",
    "wzp6_ee_gaga_tautau_60_ecm240":"#gamma#gamma #rightarrow #tau#tau",

    "wzp6_ee_tautauH_Htautau_ecm240":"Z(#tau#tau)H(#tau#tau)",
    "wzp6_ee_tautauH_HQQ_ecm240":"Z(#tau#tau)H(QQ)",
    "wzp6_ee_tautauH_Hgg_ecm240":"Z(#tau#tau)H(gg)",
    "wzp6_ee_tautauH_HVV_ecm240":"Z(#tau#tau)H(VV)",

    'wzp6_ee_nunuH_Htautau_ecm240':"Z(#nu#nu)H(#tau#tau)",
    "wzp6_ee_nunuH_HQQ_ecm240":"Z(#nu#nu)H(QQ)",
    "wzp6_ee_nunuH_Hgg_ecm240":"Z(#nu#nu)H(gg)",
    "wzp6_ee_nunuH_HVV_ecm240":"Z(#nu#nu)H(VV)",

    'wzp6_ee_eeH_Htautau_ecm240':"Z(ee)H(#tau#tau)",
    "wzp6_ee_eeH_HQQ_ecm240":"Z(ee)H(QQ)",
    "wzp6_ee_eeH_Hgg_ecm240":"Z(ee)H(gg)",
    "wzp6_ee_eeH_HVV_ecm240":"Z(ee)H(VV)",

    'wzp6_ee_mumuH_Htautau_ecm240':"Z(#mu#mu)H(#tau#tau)",
    "wzp6_ee_mumuH_HQQ_ecm240":"Z(#mu#mu)H(QQ)",
    "wzp6_ee_mumuH_Hgg_ecm240":"Z(#mu#mu)H(gg)",
    "wzp6_ee_mumuH_HVV_ecm240":"Z(#mu#mu)H(VV)",

    'wzp6_ee_ZheavyH_Htautau_ecm240':"Z(bb, cc)H(#tau#tau)",
    "wzp6_ee_ZheavyH_HQQ_ecm240":"Z(bb, cc)H(QQ)",
    "wzp6_ee_ZheavyH_Hgg_ecm240":"Z(bb, cc)H(gg)",
    "wzp6_ee_ZheavyH_HVV_ecm240":"Z(bb, cc)H(VV)",

    'wzp6_ee_ZlightH_Htautau_ecm240':"Z(uu, dd, ss)H(#tau#tau)",
    "wzp6_ee_ZlightH_HQQ_ecm240":"Z(uu, dd, ss)H(QQ)",
    "wzp6_ee_ZlightH_Hgg_ecm240":"Z(uu, dd, ss)H(gg)",
    "wzp6_ee_ZlightH_HVV_ecm240":"Z(uu, dd, ss)H(VV)",

    'wzp6_ee_LLH_Htautau_ecm240':"Z(ll)H(#tau#tau)",
    "wzp6_ee_LLH_HQQ_ecm240":"Z(ll)H(QQ)",
    "wzp6_ee_LLH_Hgg_ecm240":"Z(ll)H(gg)",
    "wzp6_ee_LLH_HVV_ecm240":"Z(ll)H(VV)",

    'wzp6_ee_QQH_Htautau_ecm240':"Z(qq)H(#tau#tau)",
    "wzp6_ee_QQH_HQQ_ecm240":"Z(qq)H(QQ)",
    "wzp6_ee_QQH_Hgg_ecm240":"Z(qq)H(gg)",
    "wzp6_ee_QQH_HVV_ecm240":"Z(qq)H(VV)",
}

legcolors = {
    'p8_ee_WW_ecm240':ROOT.kSpring+2,
    'p8_ee_Zqq_ecm240':ROOT.kMagenta-8,
    'p8_ee_ZZ_ecm240':ROOT.kSpring+3,

    'wzp6_ee_LL_ecm240':ROOT.kMagenta-6,
    'wzp6_ee_tautau_ecm240':ROOT.kPink+1,

    "wzp6_ee_nuenueZ_ecm240":ROOT.kPink-4,

    "wzp6_ee_egamma_eZ_ZLL_ecm240":ROOT.kOrange-4,
    
    "wzp6_ee_gaga_LL_60_ecm240":ROOT.kOrange-9,
    "wzp6_ee_gaga_tautau_60_ecm240":ROOT.kOrange+6,

    "wzp6_ee_tautauH_Htautau_ecm240":ROOT.kViolet+6,
    "wzp6_ee_tautauH_HQQ_ecm240":ROOT.kViolet+5,
    "wzp6_ee_tautauH_Hgg_ecm240":ROOT.kViolet-4,
    "wzp6_ee_tautauH_HVV_ecm240":ROOT.kViolet+1,

    'wzp6_ee_nunuH_Htautau_ecm240':ROOT.kGreen-3,
    "wzp6_ee_nunuH_HQQ_ecm240":ROOT.kGreen-5,
    "wzp6_ee_nunuH_Hgg_ecm240":ROOT.kGreen-8,
    "wzp6_ee_nunuH_HVV_ecm240":ROOT.kGreen-10,

    'wzp6_ee_eeH_Htautau_ecm240':ROOT.kBlue-9,
    "wzp6_ee_eeH_HQQ_ecm240":ROOT.kCyan-5,
    "wzp6_ee_eeH_Hgg_ecm240":ROOT.kCyan-8,
    "wzp6_ee_eeH_HVV_ecm240":ROOT.kCyan-10,

    'wzp6_ee_mumuH_Htautau_ecm240':ROOT.kBlue-3,
    "wzp6_ee_mumuH_HQQ_ecm240":ROOT.kBlue-5,
    "wzp6_ee_mumuH_Hgg_ecm240":ROOT.kBlue-8,
    "wzp6_ee_mumuH_HVV_ecm240":ROOT.kBlue-10,

    'wzp6_ee_ZheavyH_Htautau_ecm240':ROOT.kRed-3,
    "wzp6_ee_ZheavyH_HQQ_ecm240":ROOT.kRed-5,
    "wzp6_ee_ZheavyH_Hgg_ecm240":ROOT.kRed-8,
    "wzp6_ee_ZheavyH_HVV_ecm240":ROOT.kRed-10,

    'wzp6_ee_ZlightH_Htautau_ecm240':ROOT.kRed-9,
    "wzp6_ee_ZlightH_HQQ_ecm240":ROOT.kMagenta-5,
    "wzp6_ee_ZlightH_Hgg_ecm240":ROOT.kMagenta-8,
    "wzp6_ee_ZlightH_HVV_ecm240":ROOT.kMagenta-10,

    'wzp6_ee_LLH_Htautau_ecm240':ROOT.kBlue-9,
    "wzp6_ee_LLH_HQQ_ecm240":ROOT.kCyan-5,
    "wzp6_ee_LLH_Hgg_ecm240":ROOT.kCyan-8,
    "wzp6_ee_LLH_HVV_ecm240":ROOT.kCyan-10,

    'wzp6_ee_QQH_Htautau_ecm240':ROOT.kRed-9,
    "wzp6_ee_QQH_HQQ_ecm240":ROOT.kMagenta-5,
    "wzp6_ee_QQH_Hgg_ecm240":ROOT.kMagenta-8,
    "wzp6_ee_QQH_HVV_ecm240":ROOT.kMagenta-10,

}

#list of signals, then legend and colors to be assigned to them
signals = [
    #'wzp6_ee_ZheavyH_Htautau_ecm240',
    #'wzp6_ee_ZlightH_Htautau_ecm240',
    'wzp6_ee_QQH_Htautau_ecm240',
    #'wzp6_ee_eeH_Htautau_ecm240',
    #'wzp6_ee_mumuH_Htautau_ecm240',
    'wzp6_ee_LLH_Htautau_ecm240',
    'wzp6_ee_nunuH_Htautau_ecm240',
]

for tag in TAG:
    for cat in CAT:
        if "tag" in tag:
                variables = VARIABLES + VARIABLES_TAG +LIST_VAR[cat] #+ ["BDT_score"]
        else: 
            variables = VARIABLES + LIST_VAR[cat] #+["BDT_score"]
        #variables = ["RecoEmiss_e",]

        for sub in SUBDIR:
                    directory = DIRECTORY + tag + "/final_241202/" + cat + "/" + sub + "/"

                    CUT = CUTS[cat+sub]

                    if "ktN-tag" in tag and "LL" in cat and "HH" in sub:
                        CUT = [
                            #"selReco",
                            #"selReco_100Coll150",
                            #"selReco_100Coll150_115Rec160",
                            #"selReco_100Coll150_115Rec160_2DR",
                            #"selReco_100Coll150_115Rec160_2DR_cos0.6",
                            #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
                            "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
                            #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_4Emiss",
                            #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_86Z100_4Emiss", 
                            #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_86Z100_4Emiss_Zp54",
                            #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.96_86Z100_4Emiss_Zp54",
                        ]

                    if "tag" in tag and "QQ" in cat and "HH" in sub:
                        CUT = [
                            #"selReco",
                            #"selReco_100Coll150",
                            #"selReco_100Coll150_115Rec160",
                            #"selReco_100Coll150_115Rec160_2DR",
                            #"selReco_100Coll150_115Rec160_2DR_cos0.6",
                            #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
                            "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
                            #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_8Emiss",
                            #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_8Emiss",
                            #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_8Emiss_Zp52",
                            #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.86_75Z100_8Emiss_Zp52",
                        ]

                    for cut in CUT:
                        for variable in variables:

                            print(variable, cut, directory)

                            canvas = ROOT.TCanvas("", "", 800, 800)

                            nsig = len(signals)
                            nbkg = len(backgrounds_all) #put to zero if you only want to look at signals

                            #legend coordinates and style
                            legsize = 0.04*nsig
                            legsize2 = 0.04*nbkg
                            leg = ROOT.TLegend(0.16, 0.70 - legsize, 0.45, 0.70)
                            leg.SetFillColor(0)
                            leg.SetFillStyle(0)
                            leg.SetLineColor(0)
                            leg.SetShadowColor(0)
                            leg.SetTextSize(0.025)
                            leg.SetTextFont(42)

                            leg2 = ROOT.TLegend(0.45, 0.70 - legsize2, 0.90, 0.70)
                            leg2.SetNColumns(2)
                            leg2.SetFillColor(0)
                            leg2.SetFillStyle(0)
                            leg2.SetLineColor(0)
                            leg2.SetShadowColor(0)
                            leg2.SetTextSize(0.025)
                            leg2.SetTextFont(42)

                            #global arrays for histos and colors
                            histos = []
                            colors = []
                            leg_bkg = []

                            #loop over files for signals and backgrounds and assign corresponding colors and titles
                            #loop to merge different sources into one histograms for easier plotting

                            for s in signals:
                                fin = f"{directory}{s}_{cut}_histo.root"
                                #print(fin)
                                if file_exists(fin): #might be an empty file after stage2 
                                    tf = ROOT.TFile.Open(fin, 'READ')
                                    h = tf.Get(variable)
                                    hh = copy.deepcopy(h)
                                    hh.SetDirectory(0)
                                    histos.append(hh)
                                    colors.append(legcolors[s])
                                    leg.AddEntry(histos[-1], legend[s], "l")
                                    leg_bkg.append(0)
                            nsig=len(histos)

                            if nbkg!=0:
                                #for the common backgrounds i want to keep them separate into different histograms
                                #no need to have the ones that are empty
                                for b in backgrounds_all:
                                    fin = f"{directory}{b}_{cut}_histo.root"
                                    if file_exists(fin):
                                        tf = ROOT.TFile.Open(fin, 'READ')
                                        h = tf.Get(variable)
                                        hh = copy.deepcopy(h)
                                        hh.SetDirectory(0)
                                        histos.append(hh)
                                        colors.append(legcolors[b])
                                        leg_bkg.append(b)

                                #merge backgrounds in plotting
                                '''i = 0
                                hh = None
                                for b in LIST_B[cat]:
                                    j = 0
                                    for sub in SUBDIR:
                                        fin = f"{directory}{sub}{b}_{cut}_histo.root"
                                        if (i==0 and j==0):
                                            with ROOT.TFile(fin) as tf:
                                                h = tf.Get(variable)
                                                hh = copy.deepcopy(h)
                                                hh.SetDirectory(0)
                                        else:
                                            with ROOT.TFile(fin) as tf:
                                                h = tf.Get(variable)
                                                hh1 = copy.deepcopy(h)
                                                hh1.SetDirectory(0)
                                            hh.Add(hh1)
                                        j += 1
                                    i += 1
                                histos.append(hh)
                                colors.append(bcolors[cat])
                                leg2.AddEntry(histos[-1], blegend[cat], "f")'''
                                
                                #drawing stack for backgrounds
                                hStackBkg = ROOT.THStack("hStackBkg", "")

                                BgMCHistYieldsDic = {}
                                for i in range(nsig, len(histos)):
                                    h = histos[i]
                                    h.SetLineWidth(1)
                                    h.SetLineColor(ROOT.kBlack)
                                    h.SetFillColor(colors[i])
                                    #making sure only histograms with integral positive get added to the stack and legend
                                    if h.Integral() > 0:
                                        BgMCHistYieldsDic[h.Integral()] = h
                                        leg2.AddEntry(h, legend[leg_bkg[i]], "f")
                                    else:
                                        BgMCHistYieldsDic[-1*nbkg] = h

                                # sort stack by yields (smallest to largest)
                                BgMCHistYieldsDic = sorted_dict_values(BgMCHistYieldsDic)
                                for h in BgMCHistYieldsDic:
                                    hStackBkg.Add(h)

                                if LOGY==True :
                                    hStackBkg.SetMinimum(1e-5) #change the range to be plotted
                                    hStackBkg.SetMaximum(1e20) #leave some space on top for the legend
                                else:
                                    #h = hStackBkg.GetHists() #list of histograms 
                                    last = 0
                                    for i in range(len(histos)):
                                        if (last<histos[i].GetMaximum()):
                                            last = histos[i].GetMaximum() 
                                        # Set the y-axis range with additional white space
                                    #hStackBkg.SetMinimum(0)
                                    hStackBkg.SetMaximum(last*2.5)

                                #draw the histograms
                                hStackBkg.Draw("HIST")

                                # add the signal histograms
                                for i in range(nsig):
                                    h = histos[i]
                                    h.SetLineWidth(3)
                                    h.SetLineColor(colors[i])
                                    h.Draw("HIST SAME")

                                hStackBkg.GetYaxis().SetTitle("Events")
                                hStackBkg.GetXaxis().SetTitle(histos[0].GetXaxis().GetTitle()) #get x axis label from final stage
                                #hStackBkg.GetXaxis().SetTitle("TAU score")
                                #hStackBkg.GetYaxis().SetTitleOffset(1.5)
                                hStackBkg.GetXaxis().SetTitleOffset(1.2)
                                
                                #hStackBkg.GetXaxis().SetLimits(100, 240)

                            else: 
                                # add the signal histograms
                                for i in range(nsig):
                                    h = histos[i]
                                    h.SetLineWidth(3)
                                    h.SetLineColor(colors[i])
                                    if i == 0:
                                        h.Draw("HIST")
                                        h.GetYaxis().SetTitle("Events")
                                        h.GetXaxis().SetTitle(histos[i].GetXaxis().GetTitle())
                                        #h.GetYaxis().SetTitleOffset(1.5)
                                        h.GetXaxis().SetTitleOffset(1.2)
                                        #h.GetXaxis().SetLimits(1, 1000)
                                        if LOGY==True :
                                            h.GetYaxis().SetRangeUser(1e-6,1e8) #range to set if only working with signals
                                        else:
                                            max_y = h.GetMaximum() 
                                            h.GetYaxis().SetRangeUser(0, max_y*1.5 )
                                    else: 
                                        h.Draw("HIST SAME")

                            #labels around the plot
                            extralab = LABELS[cut]

                            if 'ee' in collider:
                                leftText = 'FCCAnalyses: FCC-ee Simulation (Delphes)'
                            rightText = f'#sqrt{{s}} = {energy} GeV, L={intLumi} ab^{{-1}}'

                            latex = ROOT.TLatex()
                            latex.SetNDC()

                            text = '#bf{#it{'+rightText+'}}'
                            latex.SetTextSize(0.03)
                            latex.DrawLatex(0.18, 0.84, text)

                            text = '#bf{#it{' + ana_tex_cat[cat] + ana_tex_sub[sub] + '}}'
                            latex.SetTextSize(0.03)
                            latex.DrawLatex(0.18, 0.80, text)

                            text = '#bf{#it{' + extralab + '}}'
                            latex.SetTextSize(0.025)
                            latex.DrawLatex(0.18, 0.74, text)

                            latex.SetTextAlign(31)
                            text = '#it{' + leftText + '}'
                            latex.SetTextSize(0.03)
                            latex.DrawLatex(0.92, 0.92, text)

                            #fix legened height after having the correct number of processes

                            legsize = 0.04*nsig
                            legsize2 = 0.03*(len(histos)-nsig)/2
                            leg.SetY1(0.70 - legsize)

                            leg2.SetY1(0.70 - legsize2)

                            leg.Draw()
                            leg2.Draw()

                            # Set Logarithmic scales for both x and y axes
                            if LOGY == True:
                                canvas.SetLogy()
                                canvas.SetTicks(1, 1)
                                canvas.SetLeftMargin(0.14)
                                canvas.SetRightMargin(0.08)
                                canvas.GetFrame().SetBorderSize(12)

                                canvas.RedrawAxis()
                                canvas.Modified()
                                canvas.Update()

                                dir = DIR_PLOTS + tag + "/" 
                                make_dir_if_not_exists(dir)

                                canvas.SaveAs(dir + variable + "_" + cat + sub + ".png")
                                canvas.SaveAs(dir + variable + "_" + cat + sub + ".pdf")
                            else:
                                canvas.SetTicks(1, 1)
                                canvas.SetLeftMargin(0.14)
                                canvas.SetRightMargin(0.08)
                                canvas.GetFrame().SetBorderSize(12)

                                canvas.RedrawAxis()
                                canvas.Modified()
                                canvas.Update()

                                dir = DIR_PLOTS + tag + "/" + cat + "/" + sub + "/lin/" + cut + "/"
                                make_dir_if_not_exists(dir)

                                canvas.SaveAs(dir + variable + "_" + cat + sub + ".png")
                                canvas.SaveAs(dir + variable + "_" + cat + sub + ".pdf")