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

# directory with final stage files
DIRECTORY = [
    '/final/LL',
    '/final/QQ',
    '/final/NuNu',
]
SUBDIR = [
    '/LL/',
    '/LH/',
    '/HH/',
]
#category to plot
CAT = [
    "QQ",
    "LL",
    "NuNu",
]

#directory where you want your plots to go
DIR_PLOTS = '/plots/' 
#list of cuts you want to plot
CUTS = [
    "selNone",
 ] 
#labels for the cuts in the plots
LABELS = {
    "selNone": "No additional selection",
 }

ana_tex        = "e^{+}e^{-} #rightarrow Z H, H #rightarrow #tau#tau"
energy         = 91
collider       = 'FCC-ee'
intLumi        = 10.8 #ab-1
LOGY = True

#now you can list all the histograms that you want to plot
VARIABLES = [
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
    "RecoElectron_PID",
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
    "RecoElectron_sel_PID",
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
    "RecoMuon_PID",
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
    "RecoMuon_sel_PID",
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
    "RecoLepton_PID",
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
    "RecoLepton_sel_PID",
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

    "n_RecoTracks",
    #"n_RecoVertex",
    "RecoVertexObject",
    "RecoVertex",
    "n_PrimaryTracks",
    "PrimaryVertexObject",
    "PrimaryVertex", 
    "PrimaryVertex_xyz",
    "PrimaryVertes_xy",
    "n_SecondaryTracks",
    "SecondaryVertexObject",
    "SecondaryVertex",
    "SecondaryVertex_xyz",
    "SecondaryVertes_xy",
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
    "Jets_R5_flavor",      
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
    "Jets_excl4_flavor",      
    "n_Jets_excl4", 

    "TauFromJet_R5_tau", 
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

    "TauFromJet_tau", 
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
    "Jets_R5_sel_flavor",      
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

#list of backgorunds, then legend and colors to be assigned to them
backgrounds_all = [
    'p8_ee_WW_ecm240',
    'p8_ee_Zqq_ecm240',
    'p8_ee_ZZ_ecm240',
    'wzp6_ee_tautau_ecm240',
]

backgrounds_TauTau = [
    'wzp6_ee_tautauH_Htautau_ecm240',
    'wzp6_ee_tautauH_Hbb_ecm240',
    'wzp6_ee_tautauH_Hcc_ecm240',
    'wzp6_ee_tautauH_Huu_ecm240',
    'wzp6_ee_tautauH_Hdd_ecm240',
    'wzp6_ee_tautauH_Hss_ecm240',
    'wzp6_ee_tautauH_HWW_ecm240',
    'wzp6_ee_tautauH_HZZ_ecm240',
]

backgrounds_QQ = [
    'wzp6_ee_bbH_Hbb_ecm240',
    'wzp6_ee_bbH_Hcc_ecm240',
    'wzp6_ee_bbH_Huu_ecm240',
    'wzp6_ee_bbH_Hdd_ecm240',
    'wzp6_ee_bbH_Hss_ecm240',
    'wzp6_ee_bbH_HWW_ecm240',
    'wzp6_ee_bbH_HZZ_ecm240',

    'wzp6_ee_ccH_Hbb_ecm240',
    'wzp6_ee_ccH_Hcc_ecm240',
    'wzp6_ee_ccH_Huu_ecm240',
    'wzp6_ee_ccH_Hdd_ecm240',
    'wzp6_ee_ccH_Hss_ecm240',
    'wzp6_ee_ccH_HWW_ecm240',
    'wzp6_ee_ccH_HZZ_ecm240',

    'wzp6_ee_ssH_Hbb_ecm240',
    'wzp6_ee_ssH_Hcc_ecm240',
    'wzp6_ee_ssH_Huu_ecm240',
    'wzp6_ee_ssH_Hdd_ecm240',
    'wzp6_ee_ssH_Hss_ecm240',
    'wzp6_ee_ssH_HWW_ecm240',
    'wzp6_ee_ssH_HZZ_ecm240',

    'wzp6_ee_qqH_Hbb_ecm240',
    'wzp6_ee_qqH_Hcc_ecm240',
    'wzp6_ee_qqH_Huu_ecm240',
    'wzp6_ee_qqH_Hdd_ecm240',
    'wzp6_ee_qqH_Hss_ecm240',
    'wzp6_ee_qqH_HWW_ecm240',
    'wzp6_ee_qqH_HZZ_ecm240',
]

backgrounds_LL =[
    'wzp6_ee_eeH_Hbb_ecm240',
    'wzp6_ee_eeH_Hcc_ecm240',
    'wzp6_ee_eeH_Huu_ecm240',
    'wzp6_ee_eeH_Hdd_ecm240',
    'wzp6_ee_eeH_Hss_ecm240',
    'wzp6_ee_eeH_HWW_ecm240',
    'wzp6_ee_eeH_HZZ_ecm240',

    'wzp6_ee_mumuH_Hbb_ecm240',
    'wzp6_ee_mumuH_Hcc_ecm240',
    'wzp6_ee_mumuH_Huu_ecm240',
    'wzp6_ee_mumuH_Hdd_ecm240',
    'wzp6_ee_mumuH_Hss_ecm240',
    'wzp6_ee_mumuH_HWW_ecm240',
    'wzp6_ee_mumuH_HZZ_ecm240',

    'wzp6_ee_tautauH_Hbb_ecm240',
    'wzp6_ee_tautauH_Hcc_ecm240',
    'wzp6_ee_tautauH_Huu_ecm240',
    'wzp6_ee_tautauH_Hdd_ecm240',
    'wzp6_ee_tautauH_Hss_ecm240',
    'wzp6_ee_tautauH_HWW_ecm240',
    'wzp6_ee_tautauH_HZZ_ecm240',
]

backgrounds_NuNu = [
    'wzp6_ee_eeH_Hbb_ecm240',
    'wzp6_ee_eeH_Hcc_ecm240',
    'wzp6_ee_eeH_Huu_ecm240',
    'wzp6_ee_eeH_Hdd_ecm240',
    'wzp6_ee_eeH_Hss_ecm240',
    'wzp6_ee_eeH_HWW_ecm240',
    'wzp6_ee_eeH_HZZ_ecm240',

    'wzp6_ee_mumuH_Hbb_ecm240',
    'wzp6_ee_mumuH_Hcc_ecm240',
    'wzp6_ee_mumuH_Huu_ecm240',
    'wzp6_ee_mumuH_Hdd_ecm240',
    'wzp6_ee_mumuH_Hss_ecm240',
    'wzp6_ee_mumuH_HWW_ecm240',
    'wzp6_ee_mumuH_HZZ_ecm240',

    'wzp6_ee_tautauH_Hbb_ecm240',
    'wzp6_ee_tautauH_Hcc_ecm240',
    'wzp6_ee_tautauH_Huu_ecm240',
    'wzp6_ee_tautauH_Hdd_ecm240',
    'wzp6_ee_tautauH_Hss_ecm240',
    'wzp6_ee_tautauH_HWW_ecm240',
    'wzp6_ee_tautauH_HZZ_ecm240',

    'wzp6_ee_nunuH_Hbb_ecm240',
    'wzp6_ee_nunuH_Hcc_ecm240',
    'wzp6_ee_nunuH_Huu_ecm240',
    'wzp6_ee_nunuH_Hdd_ecm240',
    'wzp6_ee_nunuH_Hss_ecm240',
    'wzp6_ee_nunuH_HWW_ecm240',
    'wzp6_ee_nunuH_HZZ_ecm240',
]

blegend = {
    'QQ':"Z #rightarrow QQ",
    'LL':"Z #rightarrow LL",
    'NuNu':"Z #rightarrow #nu#nu",
    'TauTau':"Z #rightarrow #tau#tau",
    'p8_ee_WW_ecm240':"WW",
    'p8_ee_Zqq_ecm240':"e^{+}e^{-} #rightarrow Z #rightarrow QQ",
    'p8_ee_ZZ_ecm240':"ZZ",
    'wzp6_ee_tautau_ecm240':"e^{+}e^{-} #rightarrow #tau#tau",
}

bcolors = {
    'QQ':41,
    'LL':33,
    'NuNu':29,
    'TauTau':38,
    'p8_ee_WW_ecm240':42,
    'p8_ee_Zqq_ecm240':44,
    'p8_ee_ZZ_ecm240':48,
    'wzp6_ee_tautau_ecm240':40,
}

#list of signals, then legend and colors to be assigned to them
signals_QQ = [
    'wzp6_ee_bbH_Htautau_ecm240',
    'wzp6_ee_ccH_Htautau_ecm240',
    'wzp6_ee_ssH_Htautau_ecm240',
    'wzp6_ee_qqH_Htautau_ecm240',
]

signals_LL = [
    'wzp6_ee_eeH_Htautau_ecm240',
    'wzp6_ee_mumuH_Htautau_ecm240',
]

signals_NuNu= [
    'wzp6_ee_nunuH_Htautau_ecm240',
]

slegend = {
    'QQ':"Z #rightarrow QQ",
    'LL':"Z #rightarrow LL",
    'NuNu':"Z #rightarrow #nu#nu",
}

scolors = {
    'QQ':ROOT.kOrange-3,
    'LL':ROOT.kAzure+7,
    'NuNu':ROOT.kGreen-6,
}

LIST_VAR = {
    "all": VARIABLES_all,
    "TauTau": VARIABLES_TauTau,
    "QQ": VARIABLES_QQ,
    "LL":VARIABLES_LL,
    "NuNu":VARIABLES_NuNu,
}

LIST_S = {
    "QQ": signals_QQ,
    "LL":signals_LL,
    "NuNu":signals_NuNu,
}

LIST_B = {
    "QQ": backgrounds_QQ,
    "LL":backgrounds_LL,
    "NuNu":backgrounds_NuNu,
}

for cut in CUTS:
    for directory in DIRECTORY:
        for cat in CAT:
            if cat in directory:
                VARIABLES = VARIABLES + LIST_VAR[cat]
                for variable in VARIABLES:

                    canvas = ROOT.TCanvas("", "", 800, 800)

                    nsig = 1
                    nbkg = 3 #half of the actual number (rounded up) beacuse they go into two colomuns 

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

                    leg2 = ROOT.TLegend(0.55, 0.70 - legsize2, 0.85, 0.70)
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

                    #loop over files for signals and backgrounds and assign corresponding colors and titles
                    #loop to merge different sources into one histograms for easier plotting
                    i = 0
                    hh = None
                    for s in LIST_S[cat]:
                        j = 0
                        for sub in SUBDIR:
                            fin = f"{directory}{sub}{s}_{cut}_histo.root"
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
                    colors.append(scolors[cat])
                    leg.AddEntry(histos[-1], slegend[cat], "l")

                    if nbkg!=0:
                        #add common and specific backgrounds based on the category
                        i = 0
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
                        leg2.AddEntry(histos[-1], blegend[cat], "f")

                        i = 0
                        hh = None
                        for b in backgrounds_TauTau:
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
                        colors.append(bcolors["TauTau"])
                        leg2.AddEntry(histos[-1], blegend["TauTau"], "f")

                        #for the common backgrounds i want to keep them separate into different histograms
                        hh = None
                        for b in backgrounds_all:
                            j = 0
                            for sub in SUBDIR:
                                fin = f"{directory}{sub}{b}_{cut}_histo.root"
                                if (j==0):
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
                            histos.append(hh)
                            colors.append(bcolors[b])
                            leg2.AddEntry(histos[-1], blegend[b], "f")
                    
                        #drawing stack for backgrounds
                        hStackBkg = ROOT.THStack("hStackBkg", "")
                        if LOGY==True :
                            hStackBkg.SetMinimum(1e-5) #change the range to be plotted
                            hStackBkg.SetMaximum(1e25) #leave some space on top for the legend
                        BgMCHistYieldsDic = {}
                        for i in range(nsig, nsig+nbkg):
                            h = histos[i]
                            h.SetLineWidth(1)
                            h.SetLineColor(ROOT.kBlack)
                            h.SetFillColor(colors[i])
                            if h.Integral() > 0:
                                BgMCHistYieldsDic[h.Integral()] = h
                            else:
                                BgMCHistYieldsDic[-1*nbkg] = h

                        # sort stack by yields (smallest to largest)
                        BgMCHistYieldsDic = sorted_dict_values(BgMCHistYieldsDic)
                        for h in BgMCHistYieldsDic:
                            hStackBkg.Add(h)

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
                        #hStackBkg.GetYaxis().SetTitleOffset(1.5)
                        hStackBkg.GetXaxis().SetTitleOffset(1.2)
                        #hStackBkg.GetXaxis().SetLimits(1, 1000)

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
                                #h.GetXaxis().SetTitle("{}".format(variable))
                                h.GetYaxis().SetRangeUser(1e-6,1e8) #range to set if only working with signals
                                #h.GetYaxis().SetTitleOffset(1.5)
                                h.GetXaxis().SetTitleOffset(1.2)
                                #h.GetXaxis().SetLimits(1, 1000)
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

                    text = '#bf{#it{' + ana_tex + '}}'
                    latex.SetTextSize(0.03)
                    latex.DrawLatex(0.18, 0.80, text)

                    text = '#bf{#it{' + extralab + '}}'
                    latex.SetTextSize(0.02)
                    latex.DrawLatex(0.18, 0.74, text)

                    latex.SetTextAlign(31)
                    text = '#it{' + leftText + '}'
                    latex.SetTextSize(0.03)
                    latex.DrawLatex(0.92, 0.92, text)

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

                        dir = DIR_PLOTS + SUBDIR + "/" + cut + "/"
                        make_dir_if_not_exists(dir)

                        canvas.SaveAs(dir + variable + "_log.png")
                        canvas.SaveAs(dir + variable + "_log.pdf")
                    else:
                        canvas.SetTicks(1, 1)
                        canvas.SetLeftMargin(0.14)
                        canvas.SetRightMargin(0.08)
                        canvas.GetFrame().SetBorderSize(12)

                        canvas.RedrawAxis()
                        canvas.Modified()
                        canvas.Update()

                        dir = DIR_PLOTS + SUBDIR + "/" + cut + "/"
                        make_dir_if_not_exists(dir)

                        canvas.SaveAs(dir + variable + ".png")
                        canvas.SaveAs(dir + variable + ".pdf")