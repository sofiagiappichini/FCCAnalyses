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
DIRECTORY = "/ceph/sgiappic/HiggsCP/CP/final_id2/"

#directory where you want your plots to go
DIR_PLOTS = '/web/sgiappic/public_html/Higgs/CP/EEHH_id2/normalised/' 
#list of cuts you want to plot
CUTS = [
    "selReco",
 ] 
#labels for the cuts in the plots
LABELS = {
    "selReco": "No additional selection",
 }

ana_tex        = "e^{+}e^{-} #rightarrow Z H, H #rightarrow #tau#tau (#pi#pi^{0}#nu)"
energy         = 240
collider       = 'FCC-ee'
intLumi        = 10.8 #ab-1
LOGY = False

#now you can list all the histograms that you want to plot
VARIABLES_ALL = [
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
    "GenZ_e",
    "GenZ_p", 
    "GenZ_pt", 
    "GenZ_px", 
    "GenZ_py", 
    "GenZ_pz", 
    "GenZ_y", 
    "GenZ_mass",
    "GenZ_eta", 
    "GenZ_theta", 
    "GenZ_phi", 
    #"GenZ_charge", 

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
    "TauFromJet_R5_eta",
    "TauFromJet_R5_y",
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
    "TauFromJet_eta",
    "TauFromJet_y",
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

    "Tau_Acoplanarity",
    "Tau_DR",
    "Tau_cos",

    "Recoil",
    "Collinear_mass",

    "GenTau_DEta",
    "GenTau_Acoplanarity",
    "GenTau_absDEta",
    "GenTau_absAcoplanarity",
    "GenTau_cos",
    "GenTau_DR",

    "Tau_DEta", 
    "Tau_Acoplanarity", 
    "RecoDiElectron_DEta", 
    "RecoDiElectron_Acoplanarity", 

    "HRF_GenTau_px",  
    "HRF_GenTau_py",  
    "HRF_GenTau_pz", 
    "HRF_GenTau_p", 
    "HRF_GenTau_pt",  
    "HRF_GenTau_e",   
    "HRF_GenTau_eta", 
    "HRF_GenTau_phi",  
    "HRF_GenTau_theta",    
    "HRF_GenTau_y", 

    "HRF_GenTau_DEta", 
    "HRF_GenTau_Acoplanarity", 

    "GenThetastar",
    "GenTheta2",
    "GenPhi1", 
    "GenPhi", 
    "GenTheta1", 

    "GenThetastar_cos",
    "GenTheta2_cos",
    "GenPhi1_cos", 
    "GenPhi_cos", 
    "GenTheta1_cos", 

    "HRF_Tau_px",  
    "HRF_Tau_py",  
    "HRF_Tau_pz", 
    "HRF_Tau_p", 
    "HRF_Tau_pt",  
    "HRF_Tau_e",   
    "HRF_Tau_eta", 
    "HRF_Tau_phi",  
    "HRF_Tau_theta",    
    "HRF_Tau_y", 

    "HRF_Tau_DEta", 
    "HRF_Tau_Acoplanarity", 

    "ZRF_RecoElectron_px",  
    "ZRF_RecoElectron_py",  
    "ZRF_RecoElectron_pz", 
    "ZRF_RecoElectron_p", 
    "ZRF_RecoElectron_pt",  
    "ZRF_RecoElectron_e",   
    "ZRF_RecoElectron_eta", 
    "ZRF_RecoElectron_phi",  
    "ZRF_RecoElectron_theta",    
    "ZRF_RecoElectron_y", 

    "ZRF_RecoDiElectron_DEta", 
    "ZRF_RecoDiElectron_Acoplanarity", 

    "RecoThetastar",
    "RecoTheta2",
    "RecoPhi1", 
    "RecoPhi", 
    "RecoTheta1", 

    "RecoThetastar_cos",
    "RecoTheta2_cos",
    "RecoPhi1_cos", 
    "RecoPhi_cos", 
    "RecoTheta1_cos", 
]

VARIABLES_GEN = [
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
]

VARIABLES_RECO = [

    ######## Reconstructed particles #######
    #"RecoMC_PID",

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

    "TauFromJet_R5_p",
    "TauFromJet_R5_pt",
    "TauFromJet_R5_px",
    "TauFromJet_R5_py",
    "TauFromJet_R5_pz",
    "TauFromJet_R5_theta",
    "TauFromJet_R5_phi",
    "TauFromJet_R5_e",
    "TauFromJet_R5_eta",
    "TauFromJet_R5_y",
    "TauFromJet_R5_charge",
    "TauFromJet_R5_type",
    "TauFromJet_R5_mass",
    "n_TauFromJet_R5",

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
    "Collinear_mass",
]

VARIABLES_CP = [
    "GenZ_e",
    "GenZ_p", 
    "GenZ_pt", 
    "GenZ_px", 
    "GenZ_py", 
    "GenZ_pz", 
    "GenZ_y", 
    "GenZ_mass",
    "GenZ_eta", 
    "GenZ_theta", 
    "GenZ_phi", 

    "ZRF_GenZDaughter_px",  
    "ZRF_GenZDaughter_py",  
    "ZRF_GenZDaughter_pz", 
    "ZRF_GenZDaughter_p", 
    "ZRF_GenZDaughter_pt",  
    "ZRF_GenZDaughter_e",   
    "ZRF_GenZDaughter_eta", 
    "ZRF_GenZDaughter_phi",  
    "ZRF_GenZDaughter_theta",    
    "ZRF_GenZDaughter_y", 

    "ZRF_GenZDaughter_DEta", 
    "ZRF_GenZDaughter_Acoplanarity", 
    
    "GenTau_DEta",
    "GenTau_Acoplanarity",
    "GenTau_cos",
    "GenTau_DR",

    "HRF_GenTau_px",  
    "HRF_GenTau_py",  
    "HRF_GenTau_pz", 
    "HRF_GenTau_p", 
    "HRF_GenTau_pt",  
    "HRF_GenTau_e",   
    "HRF_GenTau_eta", 
    "HRF_GenTau_phi",  
    "HRF_GenTau_theta",    
    "HRF_GenTau_y", 

    "HRF_GenTau_DEta", 
    "HRF_GenTau_Acoplanarity",

    "GenThetastar",
    "GenTheta2",
    "GenPhi1", 
    "GenPhi", 
    "GenTheta1", 

    "GenThetastar_cos",
    "GenTheta2_cos",
    "GenPhi1_cos", 
    "GenPhi_cos", 
    "GenTheta1_cos", 

    "Tau_DEta", 
    "Tau_Acoplanarity", 
    "RecoZDaughter_DEta", 
    "RecoZDaughter_Acoplanarity", 

    "HRF_Tau_px",  
    "HRF_Tau_py",  
    "HRF_Tau_pz", 
    "HRF_Tau_p", 
    "HRF_Tau_pt",  
    "HRF_Tau_e",   
    "HRF_Tau_eta", 
    "HRF_Tau_phi",  
    "HRF_Tau_theta",    
    "HRF_Tau_y", 

    "HRF_Tau_DEta", 
    "HRF_Tau_Acoplanarity", 

    "ZRF_RecoZDaughter_px",  
    "ZRF_RecoZDaughter_py",  
    "ZRF_RecoZDaughter_pz", 
    "ZRF_RecoZDaughter_p", 
    "ZRF_RecoZDaughter_pt",  
    "ZRF_RecoZDaughter_e",   
    "ZRF_RecoZDaughter_eta", 
    "ZRF_RecoZDaughter_phi",  
    "ZRF_RecoZDaughter_theta",    
    "ZRF_RecoZDaughter_y", 

    "ZRF_RecoZDaughter_DEta", 
    "ZRF_RecoZDaughter_Acoplanarity", 

    "RecoThetastar",
    "RecoTheta2",
    "RecoPhi1", 
    "RecoPhi", 
    "RecoTheta1", 

    "RecoThetastar_cos",
    "RecoTheta2_cos",
    "RecoPhi1_cos", 
    "RecoPhi_cos", 
    "RecoTheta1_cos", 

]

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

    "wzp6_ee_nunuH_HQQ_ecm240",
    "wzp6_ee_nunuH_Hgg_ecm240",
    "wzp6_ee_nunuH_HVV_ecm240",

    "wzp6_ee_eeH_HQQ_ecm240",
    "wzp6_ee_eeH_Hgg_ecm240",
    "wzp6_ee_eeH_HVV_ecm240",

    "wzp6_ee_mumuH_HQQ_ecm240",
    "wzp6_ee_mumuH_Hgg_ecm240",
    "wzp6_ee_mumuH_HVV_ecm240",

    "wzp6_ee_ZheavyH_HQQ_ecm240",
    "wzp6_ee_ZheavyH_Hgg_ecm240",
    "wzp6_ee_ZheavyH_HVV_ecm240",

    "wzp6_ee_ZlightH_HQQ_ecm240",
    "wzp6_ee_ZlightH_Hgg_ecm240",
    "wzp6_ee_ZlightH_HVV_ecm240",
]

blegend = {
    'p8_ee_WW_ecm240':"WW",
    'p8_ee_Zqq_ecm240':"Z #rightarrow QQ",
    'p8_ee_ZZ_ecm240':"ZZ",

    'wzp6_ee_LL_ecm240':"ll",
    'wzp6_ee_tautau_ecm240':"#tau#tau",

    "wzp6_ee_nuenueZ_ecm240":"#nu_e#nu_e Z",

    "wzp6_ee_egamma_eZ_ZLL_ecm240":"e#gamma #rightarrow eZ(ll)",
    
    "wzp6_ee_gaga_LL_60_ecm240":"#gamma#gamma #rightarrow ll",
    "wzp6_ee_gaga_tautau_60_ecm240":"#gamma#gamma #rightarrow #tau#tau",

    "wzp6_ee_tautauH_Htautau_ecm240":"Z(#tau#tau)H(#tau#tau)",
    "wzp6_ee_tautauH_HQQ_ecm240":"Z(#tau#tau)H(QQ)",
    "wzp6_ee_tautauH_Hgg_ecm240":"Z(#tau#tau)H(gg)",
    "wzp6_ee_tautauH_HVV_ecm240":"Z(#tau#tau)H(VV)",

    "wzp6_ee_nunuH_HQQ_ecm240":"Z(#nu#nu)H(QQ)",
    "wzp6_ee_nunuH_Hgg_ecm240":"Z(#nu#nu)H(gg)",
    "wzp6_ee_nunuH_HVV_ecm240":"Z(#nu#nu)H(VV)",

    "wzp6_ee_eeH_HQQ_ecm240":"Z(ee)H(QQ)",
    "wzp6_ee_eeH_Hgg_ecm240":"Z(ee)H(gg)",
    "wzp6_ee_eeH_HVV_ecm240":"Z(ee)H(VV)",

    "wzp6_ee_mumuH_HQQ_ecm240":"Z(#mu#mu)H(QQ)",
    "wzp6_ee_mumuH_Hgg_ecm240":"Z(#mu#mu)H(gg)",
    "wzp6_ee_mumuH_HVV_ecm240":"Z(#mu#mu)H(VV)",

    "wzp6_ee_ZheavyH_HQQ_ecm240":"Z(bb, cc)H(QQ)",
    "wzp6_ee_ZheavyH_Hgg_ecm240":"Z(bb, cc)H(gg)",
    "wzp6_ee_ZheavyH_HVV_ecm240":"Z(bb, cc)H(VV)",

    "wzp6_ee_ZlightH_HQQ_ecm240":"Z(uu, dd, ss)H(QQ)",
    "wzp6_ee_ZlightH_Hgg_ecm240":"Z(uu, dd, ss)H(gg)",
    "wzp6_ee_ZlightH_HVV_ecm240":"Z(uu, dd, ss)H(VV)",
}

bcolors = {
    'p8_ee_WW_ecm240':ROOT.kGreen-2,
    'p8_ee_Zqq_ecm240':ROOT.kMagenta-2,
    'p8_ee_ZZ_ecm240':ROOT.kGreen-3,

    'wzp6_ee_LL_ecm240':ROOT.kCyan-2,
    'wzp6_ee_tautau_ecm240':ROOT.kRed-2,

    "wzp6_ee_nuenueZ_ecm240":ROOT.kOrange-2,

    "wzp6_ee_egamma_eZ_ZLL_ecm240":ROOT.kOrange+1,
    
    "wzp6_ee_gaga_LL_60_ecm240":ROOT.kOrange-3,
    "wzp6_ee_gaga_tautau_60_ecm240":ROOT.kOrange+2,

    "wzp6_ee_tautauH_Htautau_ecm240":ROOT.kViolet+6,
    "wzp6_ee_tautauH_HQQ_ecm240":ROOT.kViolet+5,
    "wzp6_ee_tautauH_Hgg_ecm240":ROOT.kViolet-4,
    "wzp6_ee_tautauH_HVV_ecm240":ROOT.kViolet+1,

    "wzp6_ee_nunuH_HQQ_ecm240":ROOT.kGreen-5,
    "wzp6_ee_nunuH_Hgg_ecm240":ROOT.kGreen-8,
    "wzp6_ee_nunuH_HVV_ecm240":ROOT.kGreen-10,

    "wzp6_ee_eeH_HQQ_ecm240":ROOT.kCyan-5,
    "wzp6_ee_eeH_Hgg_ecm240":ROOT.kCyan-8,
    "wzp6_ee_eeH_HVV_ecm240":ROOT.kCyan-10,

    "wzp6_ee_mumuH_HQQ_ecm240":ROOT.kBlue-5,
    "wzp6_ee_mumuH_Hgg_ecm240":ROOT.kBlue-8,
    "wzp6_ee_mumuH_HVV_ecm240":ROOT.kBlue-10,

    "wzp6_ee_ZheavyH_HQQ_ecm240":ROOT.kRed-5,
    "wzp6_ee_ZheavyH_Hgg_ecm240":ROOT.kRed-8,
    "wzp6_ee_ZheavyH_HVV_ecm240":ROOT.kRed-10,

    "wzp6_ee_ZlightH_HQQ_ecm240":ROOT.kMagenta-5,
    "wzp6_ee_ZlightH_Hgg_ecm240":ROOT.kMagenta-8,
    "wzp6_ee_ZlightH_HVV_ecm240":ROOT.kMagenta-10,
}

#list of signals, then legend and colors to be assigned to them
signals = [
    'noISR_e+e-_noCuts_EWonly',
    'noISR_e+e-_noCuts_cehim_m1',
    'noISR_e+e-_noCuts_cehim_p1',
    'noISR_e+e-_noCuts_cehre_m1',
    'noISR_e+e-_noCuts_cehre_p1',
]

slegend = {
    'noISR_e+e-_noCuts_EWonly':"Z(ee)H(#tau#tau), SM",
    'noISR_e+e-_noCuts_cehim_m1':"Z(ee)H(#tau#tau), CPC -1",
    'noISR_e+e-_noCuts_cehim_p1':"Z(ee)H(#tau#tau), CPC +1",
    'noISR_e+e-_noCuts_cehre_m1':"Z(ee)H(#tau#tau), CPV -1",
    'noISR_e+e-_noCuts_cehre_p1':"Z(ee)H(#tau#tau), CPV +1",
}

scolors = {
    'noISR_e+e-_noCuts_EWonly':ROOT.kRed-9,
    'noISR_e+e-_noCuts_cehim_m1':ROOT.kBlue-9,
    'noISR_e+e-_noCuts_cehim_p1':ROOT.kBlue-7,
    'noISR_e+e-_noCuts_cehre_m1':ROOT.kGreen-8,
    'noISR_e+e-_noCuts_cehre_p1':ROOT.kGreen-6,
}

for cut in CUTS:
    VARIABLES = VARIABLES_RECO + VARIABLES_LL + VARIABLES_CP
    for variable in VARIABLES:

        canvas = ROOT.TCanvas("", "", 1000, 1000)
        #canvas.SetTicks(1, 1)

        pad = ROOT.TPad("", "", 0.0, 0.3, 1.0, 1.0)
        
        pad2 = ROOT.TPad("", "", 0.0, 0.0, 1.0, 0.3)

        pad.Draw()
        pad2.Draw()
        canvas.cd()
        pad.cd()

        nsig = len(signals)

        #legend coordinates and style
        legsize = 0.04*nsig
        leg = ROOT.TLegend(0.16, 0.70 - legsize, 0.45, 0.70)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetLineColor(0)
        leg.SetShadowColor(0)
        leg.SetTextSize(0.025)
        leg.SetTextFont(42)

        #global arrays for histos and colors
        histos = []
        colors = []
        legend = []

        #loop over files for signals and backgrounds and assign corresponding colors and titles
        for s in signals:
            fin = f"{DIRECTORY}{s}_{cut}_histo.root"
            with ROOT.TFile(fin) as tf:
                h = tf.Get(variable)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
            histos.append(hh)
            colors.append(scolors[s])
            leg.AddEntry(histos[-1], slegend[s], "l")

        # add the signal histograms

        for i in range(nsig):
            h = histos[i]
            h.SetLineWidth(3)
            h.SetLineColor(colors[i])
            if i == 0:
                h.Draw("HIST")
                h.GetYaxis().SetTitle("Events")
                #h.GetXaxis().SetTitle(histos[0].GetXaxis().GetTitle())
                #h.GetXaxis().SetTitleOffset(1.2)
                if h.Integral()>0:
                    h.Scale(1./(h.Integral()))
                max_y = h.GetMaximum() 
                h.GetYaxis().SetRangeUser(0, max_y*2.5)
            else: 
                if h.Integral()>0:
                    h.Scale(1./(h.Integral()))
                h.Draw("HIST SAME")
        
        extralab = LABELS[cut]

        #labels around the plot
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

        leg.Draw()

        latex.SetTextAlign(31)
        text = '#it{' + leftText + '}'
        latex.SetTextSize(0.03)


        pad.SetLeftMargin(0.14)
        pad.SetRightMargin(0.08)
        pad.GetFrame().SetBorderSize(12)
        pad.SetBottomMargin(0)

        canvas.cd()
        
        #### ratio plot ####
        pad2.cd()
 
        legend2size = 0.1*(nsig-1)
        legend2 = ROOT.TLegend(0.16, 0.90 - legend2size, 0.45, 0.74)
        legend2.SetFillColor(0)
        legend2.SetFillStyle(0)
        legend2.SetLineColor(0)
        legend2.SetShadowColor(0)
        legend2.SetTextSize(0.04)
        legend2.SetTextFont(42)

        #dummy plot
        dummy = histos[0].Clone("")
        for i in range(dummy.GetNbinsX()):
            dummy.SetBinContent(i,1.0)
        dummy.SetLineColor(0)
        dummy.SetMarkerColor(0)
        dummy.SetLineWidth(0)
        dummy.SetMarkerSize(0)

        dummy.GetYaxis().SetTitle("Ratio")
        dummy.GetYaxis().SetTitleSize(0.08)
        dummy.GetYaxis().CenterTitle()
        #adjust the range for the ratio here
        dummy.GetYaxis().SetRangeUser(0.5,1.5)
        dummy.GetYaxis().SetLabelSize(0.08)
        dummy.GetYaxis().SetNdivisions(5)
        dummy.GetYaxis().SetTitleOffset(0.5)

        dummy.GetXaxis().SetTitle(histos[0].GetXaxis().GetTitle())
        dummy.GetXaxis().SetTitleSize(0.08)
        dummy.GetXaxis().SetLabelSize(0.08)
        dummy.GetXaxis().SetTitleOffset(1.2)
        dummy.Draw("hist")
            
        ratio_list = []
        for i in range(3,nsig):  
            ratio = histos[i].Clone("")
            ratio.Divide(histos[0])
            ratio.SetLineWidth(3)
            ratio.SetLineColor(colors[i])
            #print(f"{legend[i]}")
            ratio.Draw("hist same")
            ratio_list.append(ratio)
            #legend2.AddEntry(ratio, legend[i], "l")

        #legend2.Draw()
        
        pad2.SetLeftMargin(0.14)
        pad2.SetRightMargin(0.08)
        pad2.GetFrame().SetBorderSize(12)
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(0.3)
        #pad2.SetLogy()

        #canvas.cd()

        #canvas.RedrawAxis()
        #canvas.Modified()
        #canvas.Update()

        dir = DIR_PLOTS + "/" + cut + "/"
        make_dir_if_not_exists(dir)

        if (LOGY == True):

            canvas.SaveAs(dir + variable + "_log.png")
            canvas.SaveAs(dir+ variable + "_log.pdf")

        else:

            canvas.SaveAs(dir + variable + ".png")
            canvas.SaveAs(dir+ variable + ".pdf")