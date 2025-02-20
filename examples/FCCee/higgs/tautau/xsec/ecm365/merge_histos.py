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
DIRECTORY = "/ceph/sgiappic/HiggsCP/ecm365/"
TAG = [
    #"R5-explicit",
    #"R5-tag",
    #"ktN-explicit",
    "ktN-tag",
]
SUBDIR = [
    'LL',
    'LH',
    #'HH',
]
#category to plot
CAT = [
    #"QQ",
    "LL",
    #"NuNu",
]
#list of cuts you want to plot
CUTS_LL = [
    "selReco",
    "selReco_100Coll150",
    "selReco_100Coll150_115Rec160",
    "selReco_100Coll150_115Rec160_1DR",
    "selReco_100Coll150_115Rec160_1DR_cos0.25",
    "selReco_100Coll150_115Rec160_1DR_cos0.25_misscos0.98",
    "selReco_100Coll150_115Rec160_1DR_cos0.25_misscos0.98_70Z100",
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
    "RecoEmiss_eta",
    "RecoEmiss_phi",
    "RecoEmiss_theta",
    "RecoEmiss_y",
    "RecoEmiss_costheta",

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

    #"Jets_R5_e",     
    #"Jets_R5_p",     
    #"Jets_R5_pt",     
    #"Jets_R5_px",   
    #"Jets_R5_py",   
    #"Jets_R5_pz",     
    #"Jets_R5_eta",    
    #"Jets_R5_theta",   
    #"Jets_R5_phi",     
    #"Jets_R5_mass",        
    #"n_Jets_R5", 

    #"Jets_excl4_e",     
    #"Jets_excl4_p",     
    #"Jets_excl4_pt",     
    #"Jets_excl4_px",   
    #"Jets_excl4_py",   
    #"Jets_excl4_pz",     
    #"Jets_excl4_eta",    
    #"Jets_excl4_theta",   
    #"Jets_excl4_phi",     
    #"Jets_excl4_mass",        
    #"n_Jets_excl4", 

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

    #"TauFromJet_p",
    #"TauFromJet_pt",
    #"TauFromJet_px",
    #"TauFromJet_py",
    #"TauFromJet_pz",
    #"TauFromJet_theta",
    #"TauFromJet_phi",
    #"TauFromJet_eta",
    #"TauFromJet_y",
    #"TauFromJet_e",
    #"TauFromJet_charge",
    #"TauFromJet_type",
    #"TauFromJet_mass",
    #"n_TauFromJet",

    #"Jets_R5_sel_e",     
    #"Jets_R5_sel_p",     
    #"Jets_R5_sel_pt",     
    #"Jets_R5_sel_px",   
    #"Jets_R5_sel_py",   
    #"Jets_R5_sel_pz",     
    #"Jets_R5_sel_eta",    
    #"Jets_R5_sel_theta",   
    #"Jets_R5_sel_phi",     
    #"Jets_R5_sel_mass",      
    #"n_Jets_R5_sel", 
]

VAR_JET = [

    "TagJet_R5_px", 
    "TagJet_R5_py",    
    "TagJet_R5_pz",      
    "TagJet_R5_p",  
    "TagJet_R5_pt",    
    "TagJet_R5_phi", 
    "TagJet_R5_eta",     
    "TagJet_R5_theta",          
    "TagJet_R5_e",     
    "TagJet_R5_mass",        
    "TagJet_R5_charge",  
    "n_TagJet_R5_constituents",   
    "n_TagJet_R5_charged_constituents",   
    "n_TagJet_R5_neutral_constituents",   
    "n_TagJet_R5",           

    "TagJet_R5_isG",  
    "TagJet_R5_isU",
    "TagJet_R5_isD",   
    "TagJet_R5_isS",  
    "TagJet_R5_isC",
    "TagJet_R5_isB",  
    "TagJet_R5_isTAU",

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

    "TagJet_R5_sel_e",     
    "TagJet_R5_sel_p",     
    "TagJet_R5_sel_pt",     
    "TagJet_R5_sel_px",   
    "TagJet_R5_sel_py",   
    "TagJet_R5_sel_pz",     
    "TagJet_R5_sel_eta",    
    "TagJet_R5_sel_theta",   
    "TagJet_R5_sel_phi",     
    "TagJet_R5_sel_mass",      
    "n_TagJet_R5_sel", 
    
    "TagJet_kt4_px", 
    "TagJet_kt4_py",    
    "TagJet_kt4_pz",      
    "TagJet_kt4_p",  
    "TagJet_kt4_pt",    
    "TagJet_kt4_phi", 
    "TagJet_kt4_eta",     
    "TagJet_kt4_theta",          
    "TagJet_kt4_e",     
    "TagJet_kt4_mass",        
    "TagJet_kt4_charge",  
    "n_TagJet_kt4_constituents",   
    "n_TagJet_kt4_charged_constituents",   
    "n_TagJet_kt4_neutral_constituents",   
    "n_TagJet_kt4",          

    "TagJet_kt4_isG",  
    "TagJet_kt4_isU",
    "TagJet_kt4_isD",   
    "TagJet_kt4_isS",  
    "TagJet_kt4_isC",
    "TagJet_kt4_isB",  
    "TagJet_kt4_isTAU",

    "TauFromJet_kt4_p",
    "TauFromJet_kt4_pt",
    "TauFromJet_kt4_px",
    "TauFromJet_kt4_py",
    "TauFromJet_kt4_pz",
    "TauFromJet_kt4_theta",
    "TauFromJet_kt4_phi",
    "TauFromJet_kt4_e",
    "TauFromJet_kt4_eta",
    "TauFromJet_kt4_y",
    "TauFromJet_kt4_charge",
    "TauFromJet_kt4_type",
    "TauFromJet_kt4_mass",
    "n_TauFromJet_kt4",

    "TagJet_kt4_sel_e",     
    "TagJet_kt4_sel_p",     
    "TagJet_kt4_sel_pt",     
    "TagJet_kt4_sel_px",   
    "TagJet_kt4_sel_py",   
    "TagJet_kt4_sel_pz",     
    "TagJet_kt4_sel_eta",    
    "TagJet_kt4_sel_theta",   
    "TagJet_kt4_sel_phi",     
    "TagJet_kt4_sel_mass",      
    "n_TagJet_kt4_sel",

    "TagJet_kt3_px", 
    "TagJet_kt3_py",    
    "TagJet_kt3_pz",      
    "TagJet_kt3_p",  
    "TagJet_kt3_pt",    
    "TagJet_kt3_phi", 
    "TagJet_kt3_eta",     
    "TagJet_kt3_theta",          
    "TagJet_kt3_e",     
    "TagJet_kt3_mass",        
    "TagJet_kt3_charge",       
    "n_TagJet_kt3_constituents",   
    "n_TagJet_kt3_charged_constituents",   
    "n_TagJet_kt3_neutral_constituents",   
    "n_TagJet_kt3",          

    "TagJet_kt3_isG",  
    "TagJet_kt3_isU",
    "TagJet_kt3_isD",   
    "TagJet_kt3_isS",  
    "TagJet_kt3_isC",
    "TagJet_kt3_isB",  
    "TagJet_kt3_isTAU",

    "TauFromJet_kt3_p",
    "TauFromJet_kt3_pt",
    "TauFromJet_kt3_px",
    "TauFromJet_kt3_py",
    "TauFromJet_kt3_pz",
    "TauFromJet_kt3_theta",
    "TauFromJet_kt3_phi",
    "TauFromJet_kt3_e",
    "TauFromJet_kt3_eta",
    "TauFromJet_kt3_y",
    "TauFromJet_kt3_charge",
    "TauFromJet_kt3_type",
    "TauFromJet_kt3_mass",
    "n_TauFromJet_kt3",

    "TagJet_kt3_sel_e",     
    "TagJet_kt3_sel_p",     
    "TagJet_kt3_sel_pt",     
    "TagJet_kt3_sel_px",   
    "TagJet_kt3_sel_py",   
    "TagJet_kt3_sel_pz",     
    "TagJet_kt3_sel_eta",    
    "TagJet_kt3_sel_theta",   
    "TagJet_kt3_sel_phi",     
    "TagJet_kt3_sel_mass",      
    "n_TagJet_kt3_sel",

    "TagJet_kt2_px", 
    "TagJet_kt2_py",    
    "TagJet_kt2_pz",      
    "TagJet_kt2_p",  
    "TagJet_kt2_pt",    
    "TagJet_kt2_phi", 
    "TagJet_kt2_eta",     
    "TagJet_kt2_theta",          
    "TagJet_kt2_e",     
    "TagJet_kt2_mass",        
    "TagJet_kt2_charge",    
    "n_TagJet_kt2_constituents",   
    "n_TagJet_kt2_charged_constituents",   
    "n_TagJet_kt2_neutral_constituents",   
    "n_TagJet_kt2",          

    "TagJet_kt2_isG",  
    "TagJet_kt2_isU",
    "TagJet_kt2_isD",   
    "TagJet_kt2_isS",  
    "TagJet_kt2_isC",
    "TagJet_kt2_isB",  
    "TagJet_kt2_isTAU",

    "TauFromJet_kt2_p",
    "TauFromJet_kt2_pt",
    "TauFromJet_kt2_px",
    "TauFromJet_kt2_py",
    "TauFromJet_kt2_pz",
    "TauFromJet_kt2_theta",
    "TauFromJet_kt2_phi",
    "TauFromJet_kt2_e",
    "TauFromJet_kt2_eta",
    "TauFromJet_kt2_y",
    "TauFromJet_kt2_charge",
    "TauFromJet_kt2_type",
    "TauFromJet_kt2_mass",
    "n_TauFromJet_kt2",

    "TagJet_kt2_sel_e",     
    "TagJet_kt2_sel_p",     
    "TagJet_kt2_sel_pt",     
    "TagJet_kt2_sel_px",   
    "TagJet_kt2_sel_py",   
    "TagJet_kt2_sel_pz",     
    "TagJet_kt2_sel_eta",    
    "TagJet_kt2_sel_theta",   
    "TagJet_kt2_sel_phi",     
    "TagJet_kt2_sel_mass",      
    "n_TagJet_kt2_sel",

    "TagJet_kt1_px", 
    "TagJet_kt1_py",    
    "TagJet_kt1_pz",      
    "TagJet_kt1_p",  
    "TagJet_kt1_pt",    
    "TagJet_kt1_phi", 
    "TagJet_kt1_eta",     
    "TagJet_kt1_theta",          
    "TagJet_kt1_e",     
    "TagJet_kt1_mass",        
    "TagJet_kt1_charge",   
    "n_TagJet_kt1_constituents",   
    "n_TagJet_kt1_charged_constituents",   
    "n_TagJet_kt1_neutral_constituents",   
    "n_TagJet_kt1",          

    "TagJet_kt1_isG",  
    "TagJet_kt1_isU",
    "TagJet_kt1_isD",   
    "TagJet_kt1_isS",  
    "TagJet_kt1_isC",
    "TagJet_kt1_isB",  
    "TagJet_kt1_isTAU",

    "TauFromJet_kt1_p",
    "TauFromJet_kt1_pt",
    "TauFromJet_kt1_px",
    "TauFromJet_kt1_py",
    "TauFromJet_kt1_pz",
    "TauFromJet_kt1_theta",
    "TauFromJet_kt1_phi",
    "TauFromJet_kt1_e",
    "TauFromJet_kt1_eta",
    "TauFromJet_kt1_y",
    "TauFromJet_kt1_charge",
    "TauFromJet_kt1_type",
    "TauFromJet_kt1_mass",
    "n_TauFromJet_kt1",

    "TagJet_kt1_sel_e",     
    "TagJet_kt1_sel_p",     
    "TagJet_kt1_sel_pt",     
    "TagJet_kt1_sel_px",   
    "TagJet_kt1_sel_py",   
    "TagJet_kt1_sel_pz",     
    "TagJet_kt1_sel_eta",    
    "TagJet_kt1_sel_theta",   
    "TagJet_kt1_sel_phi",     
    "TagJet_kt1_sel_mass",      
    "n_TagJet_kt1_sel",

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
    'wzp6_ee_VBFnunuH_Hbb_ecm365',
    'wzp6_ee_VBFnunuH_Hcc_ecm365',
    'wzp6_ee_VBFnunuH_Hss_ecm365',
]
backgrounds_7 = [
    'wzp6_ee_VBFnunuH_HWW_ecm365',
    'wzp6_ee_VBFnunuH_HZZ_ecm365',
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
    'wzp6_ee_ZH_Znunu_Hbb_ecm365',
    'wzp6_ee_ZH_Znunu_Hcc_ecm365',
    'wzp6_ee_ZH_Znunu_Hss_ecm365',
]
backgrounds_30 = [
    'wzp6_ee_ZH_Znunu_HWW_ecm365',
    'wzp6_ee_ZH_Znunu_HZZ_ecm365',
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

    6:"wzp6_ee_VBFnunuH_HQQ_ecm365",
    7:"wzp6_ee_VBFnunuH_HVV_ecm365",

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
    29:"wzp6_ee_ZH_Znunu_HQQ_ecm365",
    30:"wzp6_ee_ZH_Znunu_HVV_ecm365",
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
    0:'wzp6_ee_ZH_Znunu_Htautau_ecm365',
    1:'wzp6_ee_ZH_Znunu_Hbb_ecm365',
    2:'wzp6_ee_ZH_Znunu_Hcc_ecm365',
    3:'wzp6_ee_ZH_Znunu_Hss_ecm365',
    4:'wzp6_ee_ZH_Znunu_Hgg_ecm365',
    5:'wzp6_ee_ZH_Znunu_HWW_ecm365',
    6:'wzp6_ee_ZH_Znunu_HZZ_ecm365', 
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

################# VBF - ZH ##################

for tag in TAG:
    for cat in CAT:
        for sub in SUBDIR:

            CUT = CUTS[cat]

            for cut in CUT:

                if "tag" in tag:
                    variables = VARIABLES + VARIABLES_TAG +LIST_VAR[cat]
                else: 
                    variables = VARIABLES + LIST_VAR[cat] 

                directory = DIRECTORY + tag + "/final_280125/" + cat + "/" + sub + "/"

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
                        os.remove(output)

                    

#################### now add the decays #####################

for tag in TAG:
    for cat in CAT:
        for sub in SUBDIR:

            CUT = CUTS[cat]

            for cut in CUT:

                if "tag" in tag:
                    variables = VARIABLES + VARIABLES_TAG +LIST_VAR[cat]
                else: 
                    variables = VARIABLES + LIST_VAR[cat] 

                directory = DIRECTORY + tag + "/final_280125/" + cat + "/" + sub + "/"
            
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
                        print(f"{tag}, {cat}, {sub}, {cut}, {num}, {var}")
                        
                    outFile.Close()
                    if check==False: #if nothing was written i don't want the file saved at all
                        os.remove(output)



