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
        os.system("cp /eos/user/s/sgiappic/www/index.php {}".format(directory)) #copy index to show plots in web page automatically
        print(f"Directory created successfully.")
    else:
        print(f"Directory already exists.")

def file_exists(file_path):
    return os.path.isfile(file_path)

# directory with final stage files
DIRECTORY = {
    'LL':"/ceph/awiedl/FCCee/HiggsCP/final/LL",
    'QQ':"/ceph/awiedl/FCCee/HiggsCP/final/QQ",,
    'NuNu':"/ceph/awiedl/FCCee/HiggsCP/final/NuNu",
}
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
CUTS = [
    "selReco",
 ] 

#now you can list all the histograms that you want to plot
VARIABLES = [
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

    #"n_ZFSGenMuon",
    #"ZFSGenMuon_e",
    #"ZFSGenMuon_p",
    #"ZFSGenMuon_pt",
    #"ZFSGenMuon_px",
    #"ZFSGenMuon_py",
    #"ZFSGenMuon_pz",
    #"ZFSGenMuon_y",
    #"ZFSGenMuon_eta",
    #"ZFSGenMuon_theta",
    #"ZFSGenMuon_phi",
    #"ZFSGenMuon_charge",
    #"ZFSGenMuon_mass",
    #"ZFSGenMuon_parentPDG",
    #"ZFSGenMuon_vertex_x",
    #"ZFSGenMuon_vertex_y",
    #"ZFSGenMuon_vertex_z",

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

    #"noFSRGenTau_parentPDG",

    "n_FSRGenTau",
    "FSRGenTau_e",
    "FSRGenTau_p",
    "FSRGenTau_pt",
    "FSRGenTau_px",
    "FSRGenTau_py",
    "FSRGenTau_pz",
    "FSRGenTau_y",
    "FSRGenTau_eta",
    "FSRGenTau_theta",
    "FSRGenTau_phi",
    "FSRGenTau_charge",
    "FSRGenTau_mass",
    "FSRGenTau_parentPDG",
    "FSRGenTau_vertex_x",
    "FSRGenTau_vertex_y",
    "FSRGenTau_vertex_z",

    "n_TauNeg_MuNuNu",       
    "n_TauNeg_MuNuNu_Phot",  
    "n_TauNeg_ENuNu",        
    "n_TauNeg_ENuNu_Phot",   
    "n_TauNeg_PiNu",         
    "n_TauNeg_PiNu_Phot",    
    "n_TauNeg_KNu",          
    "n_TauNeg_KNu_Phot",     
    "n_TauNeg_PiK0Nu",       
    "n_TauNeg_PiK0Nu_Phot",  
    "n_TauNeg_KK0Nu",        
    "n_TauNeg_KK0Nu_Phot",   
    "n_TauNeg_3PiNu",        
    "n_TauNeg_3PiNu_Phot",   
    "n_TauNeg_PiKKNu",       
    "n_TauNeg_PiKKNu_Phot",  

    "n_TauPos_MuNuNu",       
    "n_TauPos_MuNuNu_Phot",  
    "n_TauPos_ENuNu",        
    "n_TauPos_ENuNu_Phot",   
    "n_TauPos_PiNu",         
    "n_TauPos_PiNu_Phot",    
    "n_TauPos_KNu",          
    "n_TauPos_KNu_Phot",     
    "n_TauPos_PiK0Nu",       
    "n_TauPos_PiK0Nu_Phot",  
    "n_TauPos_KK0Nu",        
    "n_TauPos_KK0Nu_Phot",   
    "n_TauPos_3PiNu",        
    "n_TauPos_3PiNu_Phot",   
    "n_TauPos_PiKKNu",       
    "n_TauPos_PiKKNu_Phot", 

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

    #"n_GenZ",
    #"n_GenW",
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

    "RecoEmiss_px",
    "RecoEmiss_py",
    "RecoEmiss_pz",
    "RecoEmiss_pt",
    "RecoEmiss_p",
    "RecoEmiss_e",

    #"n_RecoTracks",
    #"RecoVertexObject",
    #"RecoVertex",
    #"n_PrimaryTracks",
    #"PrimaryVertexObject",
    #"PrimaryVertex", 
    #"PrimaryVertex_xyz",
    #"PrimaryVertes_xy",
    #"n_SecondaryTracks",
    #"SecondaryVertexObject",
    #"SecondaryVertex",
    #"SecondaryVertex_xyz",
    #"SecondaryVertes_xy",
    #"VertexObject", 
    #"RecoPartPID" ,
    #"RecoPartPIDAtVertex",

    "Jets_R5_e",     
    "Jets_R5_p",     
    "Jets_R5_pt",     
    "Jets_R5_px",   
    "Jets_R5_py",   
    "Jets_R5_pz",     
    "Jets_R5_eta",    
    "Jets_R5_theta",   
    "Jets_R5_phi",     
    "Jets_R5_mass",        
    "n_Jets_R5", 

    "Jets_excl4_e",     
    "Jets_excl4_p",     
    "Jets_excl4_pt",     
    "Jets_excl4_px",   
    "Jets_excl4_py",   
    "Jets_excl4_pz",     
    "Jets_excl4_eta",    
    "Jets_excl4_theta",   
    "Jets_excl4_phi",     
    "Jets_excl4_mass",        
    "n_Jets_excl4", 

    "TauFromJet_R5_p",
    "TauFromJet_R5_pt",
    "TauFromJet_R5_px",
    "TauFromJet_R5_py",
    "TauFromJet_R5_pz",
    "TauFromJet_R5_theta",
    "TauFromJet_R5_phi",
    "TauFromJet_R5_e",
    "TauFromJet_R5_charge",
    "TauFromJet_R5_type",
    "TauFromJet_R5_mass",
    "n_TauFromJet_R5",

    "TauFromJet_p",
    "TauFromJet_pt",
    "TauFromJet_px",
    "TauFromJet_py",
    "TauFromJet_pz",
    "TauFromJet_theta",
    "TauFromJet_phi",
    "TauFromJet_e",
    "TauFromJet_charge",
    "TauFromJet_type",
    "TauFromJet_mass",
    "n_TauFromJet",

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
]

VARIABLES_LL = [
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

    "Recoil",
    "Collinear_mass",
]

VARIABLES_QQ = [
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

    "Recoil",
    "Collinear_mass",
]

VARIABLES_NuNu = [
    "RecoEmiss_eta",
    "RecoEmiss_phi",
    "RecoEmiss_theta",
    "RecoEmiss_y",
    "RecoEmiss_costheta",

    #"RecoZ_px",
    #"RecoZ_py",
    #"RecoZ_pz",
    #"RecoZ_p",
    #"RecoZ_pt",
    #"RecoZ_e",
    #"RecoZ_eta",
    #"RecoZ_phi",
    #"RecoZ_theta",
    #"RecoZ_y",
    #"RecoZ_mass",

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

    #"Recoil",
    "Collinear_mass",
    "Visible_mass",
]

LIST_VAR = {
    "QQ": VARIABLES_QQ,
    "LL":VARIABLES_LL,
    "NuNu":VARIABLES_NuNu,
}

#list of backgrounds, then legend and colors to be assigned to them
backgrounds_1 = [
    'wzp6_ee_mumu_ecm240',
    'wzp6_ee_ee_Mee_30_150_ecm240',
]

backgrounds_2 = [
    'wzp6_egamma_eZ_Zmumu_ecm240',
    'wzp6_egamma_eZ_Zee_ecm240',
    'wzp6_gammae_eZ_Zmumu_ecm240',
    'wzp6_gammae_eZ_Zee_ecm240',
]

backgrounds_3 = [
    'wzp6_gaga_mumu_60_ecm240',
    'wzp6_gaga_ee_60_ecm240',
]

backgrounds_4 = [
    'wzp6_ee_tautauH_Hbb_ecm240',
    'wzp6_ee_tautauH_Hcc_ecm240',
    'wzp6_ee_tautauH_Hss_ecm240',
]

backgrounds_5 = [
    'wzp6_ee_tautauH_HWW_ecm240',
    'wzp6_ee_tautauH_HZZ_ecm240',
]

backgrounds_6 = [
    'wzp6_ee_nunuH_Hbb_ecm240',
    'wzp6_ee_nunuH_Hcc_ecm240',
    'wzp6_ee_nunuH_Hss_ecm240',
]

backgrounds_7 = [
    'wzp6_ee_nunuH_HWW_ecm240',
    'wzp6_ee_nunuH_HZZ_ecm240',
]

backgrounds_8 = [
    'wzp6_ee_eeH_Hbb_ecm240',
    'wzp6_ee_eeH_Hcc_ecm240',
    'wzp6_ee_eeH_Hss_ecm240',

    'wzp6_ee_mumuH_Hbb_ecm240',
    'wzp6_ee_mumuH_Hcc_ecm240',
    'wzp6_ee_mumuH_Hss_ecm240',
]

backgrounds_9 = [
    'wzp6_ee_eeH_HWW_ecm240',
    'wzp6_ee_eeH_HZZ_ecm240',

    'wzp6_ee_mumuH_HWW_ecm240',
    'wzp6_ee_mumuH_HZZ_ecm240',
]

backgrounds_10 = [
    'wzp6_ee_eeH_Hbb_ecm240',
    'wzp6_ee_eeH_Hcc_ecm240',
    'wzp6_ee_eeH_Hss_ecm240',
]

backgrounds_11 = [
    'wzp6_ee_eeH_HWW_ecm240',
    'wzp6_ee_eeH_HZZ_ecm240',
]

backgrounds_12 = [
    'wzp6_ee_mumuH_Hbb_ecm240',
    'wzp6_ee_mumuH_Hcc_ecm240',
    'wzp6_ee_mumuH_Hss_ecm240',
]

backgrounds_13 = [
    'wzp6_ee_mumuH_HWW_ecm240',
    'wzp6_ee_mumuH_HZZ_ecm240',
]

backgrounds_14 = [
    'wzp6_ee_bbH_Hbb_ecm240',
    'wzp6_ee_bbH_Hcc_ecm240',
    'wzp6_ee_bbH_Hss_ecm240',

    'wzp6_ee_ccH_Hbb_ecm240',
    'wzp6_ee_ccH_Hcc_ecm240',
    'wzp6_ee_ccH_Hss_ecm240',

    'wzp6_ee_ssH_Hbb_ecm240',
    'wzp6_ee_ssH_Hcc_ecm240',
    'wzp6_ee_ssH_Hss_ecm240',

    'wzp6_ee_qqH_Hbb_ecm240',
    'wzp6_ee_qqH_Hcc_ecm240',
    'wzp6_ee_qqH_Hss_ecm240',
]

backgrounds_15 = [
    'wzp6_ee_bbH_Hbb_ecm240',
    'wzp6_ee_bbH_Hcc_ecm240',
    'wzp6_ee_bbH_Hss_ecm240',

    'wzp6_ee_ccH_Hbb_ecm240',
    'wzp6_ee_ccH_Hcc_ecm240',
    'wzp6_ee_ccH_Hss_ecm240',
]

backgrounds_16 = [
    'wzp6_ee_ssH_Hbb_ecm240',
    'wzp6_ee_ssH_Hcc_ecm240',
    'wzp6_ee_ssH_Hss_ecm240',

    'wzp6_ee_qqH_Hbb_ecm240',
    'wzp6_ee_qqH_Hcc_ecm240',
    'wzp6_ee_qqH_Hss_ecm240',
]
backgrounds_17 = [
    'wzp6_ee_bbH_HWW_ecm240',
    'wzp6_ee_bbH_HZZ_ecm240',

    'wzp6_ee_ccH_HWW_ecm240',
    'wzp6_ee_ccH_HZZ_ecm240',

    'wzp6_ee_ssH_HWW_ecm240',
    'wzp6_ee_ssH_HZZ_ecm240',
    
    'wzp6_ee_qqH_HWW_ecm240',
    'wzp6_ee_qqH_HZZ_ecm240',
]

backgrounds_18 = [
    'wzp6_ee_bbH_HWW_ecm240',
    'wzp6_ee_bbH_HZZ_ecm240',

    'wzp6_ee_ccH_HWW_ecm240',
    'wzp6_ee_ccH_HZZ_ecm240',
]

backgrounds_19 = [    
    'wzp6_ee_ssH_HWW_ecm240',
    'wzp6_ee_ssH_HZZ_ecm240',
    
    'wzp6_ee_qqH_HWW_ecm240',
    'wzp6_ee_qqH_HZZ_ecm240',
]

backgrounds_20 = [
    'wzp6_ee_bbH_Hgg_ecm240',
    'wzp6_ee_ccH_Hgg_ecm240',
    'wzp6_ee_ssH_Hgg_ecm240',
    'wzp6_ee_qqH_Hgg_ecm240',
]

backgrounds_21 = [
    'wzp6_ee_bbH_Hgg_ecm240',
    'wzp6_ee_ccH_Hgg_ecm240',
]

backgrounds_22 = [
    'wzp6_ee_ssH_Hgg_ecm240',
    'wzp6_ee_qqH_Hgg_ecm240',
]

backgrounds_23 = [
    'wzp6_ee_eeH_Hgg_ecm240',
    'wzp6_ee_mumuH_Hgg_ecm240',
]
#signals
backgrounds_24 = [
    'wzp6_ee_eeH_Htautau_ecm240',
    'wzp6_ee_mumuH_Htautau_ecm240',
]
backgrounds_25 = [
    'wzp6_ee_bbH_Htautau_ecm240',
    'wzp6_ee_ccH_Htautau_ecm240',

    'wzp6_ee_ssH_Htautau_ecm240',
    'wzp6_ee_qqH_Htautau_ecm240',
]

backgrounds_26 = [
    'wzp6_ee_bbH_Htautau_ecm240',
    'wzp6_ee_ccH_Htautau_ecm240',
]

backgrounds_27 = [
    'wzp6_ee_ssH_Htautau_ecm240',
    'wzp6_ee_qqH_Htautau_ecm240',
]

legend = {
    1:"wzp6_ee_LL_ecm240",

    2:"wzp6_ee_egamma_eZ_ZLL_ecm240",
    3:"wzp6_ee_gaga_LL_60_ecm240",

    4:"wzp6_ee_tautauH_HQQ_ecm240",
    5:"wzp6_ee_tautauH_HVV_ecm240",

    6:"wzp6_ee_nunuH_HQQ_ecm240",
    7:"wzp6_ee_nunuH_HVV_ecm240",

    8:"wzp6_ee_LLH_HQQ_ecm240",
    9:"wzp6_ee_LLH_HVV_ecm240",
    10:"wzp6_ee_eeH_HQQ_ecm240",
    11:"wzp6_ee_eeH_HVV_ecm240",
    12:"wzp6_ee_mumuH_HQQ_ecm240",
    13:"wzp6_ee_mumuH_HVV_ecm240",

    14:"wzp6_ee_QQH_HQQ_ecm240",
    15:"wzp6_ee_ZheavyH_HQQ_ecm240",
    16:"wzp6_ee_ZlightQH_HQQ_ecm240",
    17:"wzp6_ee_QQH_HVV_ecm240",
    18:"wzp6_ee_ZheavyH_HVV_ecm240",
    19:"wzp6_ee_ZlightH_HVV_ecm240",

    20:"wzp6_ee_QQH_Hgg_ecm240",
    21:"wzp6_ee_ZheavyH_Hgg_ecm240",
    22:"wzp6_ee_ZlightH_Hgg_ecm240",

    23:"wzp6_ee_LLH_Hgg_ecm240",
    #signals
    24:"wzp6_ee_LLH_Htautau_ecm240",

    25:"wzp6_ee_QQH_Htautau_ecm240",
    26:"wzp6_ee_ZheavyH_Htautau_ecm240",
    27:"wzp6_ee_ZlightH_Htautau_ecm240",
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
}

for cut in CUTS:
    for cat in CAT:
        variables = VARIABLES + LIST_VAR[cat] 
        directory = DIRECTORY[cat]
        for sub in SUBDIR:
            for num in range(1,28):
                output = f"{directory}/{sub}/{legend[num]}_{cut}_histo.root"
                #print(output)
                outFile = ROOT.TFile.Open(output, "RECREATE")
                check = False
                for var in variables:
                    #loop to merge different sources into one histograms for easier plotting
                    j = 0
                    hh = None
                    #print(list)
                    for b in list[num]:
                        #print(b)
                        file = f"{directory}/{sub}/{b}_{cut}_histo.root"
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
                #print(check)
                    
                outFile.Close()
                if check==False: #if nothing was written i don't want the file saved at all
                    os.remove(output)
