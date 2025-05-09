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
DIRECTORY = "/ceph/sgiappic/HiggsCP/CPReco/final_explicit_new/"

#list of cuts you want to plot
CUT = [
    "selReco_CMS",
    "selReco_ILC20chi",
]

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

            "n_GenTau",
            "GenTau_e",
            "GenTau_p",
            "GenTau_pt",
            "GenTau_px",
            "GenTau_py",
            "GenTau_pz",
            "GenTau_y",
            "GenTau_eta",
            "GenTau_theta",
            "GenTau_phi",
            "GenTau_charge",
            "GenTau_mass",
            "GenTau_parentPDG",
            "GenTau_vertex_x",
            "GenTau_vertex_y",
            "GenTau_vertex_z",

            "GenNuP_e",
            "GenNuP_p",
            "GenNuP_pt",
            "GenNuP_px",
            "GenNuP_py",
            "GenNuP_pz",
            "GenNuP_y",
            "GenNuP_eta",
            "GenNuP_theta",
            "GenNuP_phi",
            "GenNuP_charge",
            "GenNuP_mass",
            "GenNuP_p4",

            "GenNuM_e",
            "GenNuM_p",
            "GenNuM_pt",
            "GenNuM_px",
            "GenNuM_py",
            "GenNuM_pz",
            "GenNuM_y",
            "GenNuM_eta",
            "GenNuM_theta",
            "GenNuM_phi",
            "GenNuM_charge",
            "GenNuM_mass",
            "GenNuM_p4",

            "GenPiP_e",
            "GenPiP_p",
            "GenPiP_pt",
            "GenPiP_px",
            "GenPiP_py",
            "GenPiP_pz",
            "GenPiP_y",
            "GenPiP_eta",
            "GenPiP_theta",
            "GenPiP_phi",
            "GenPiP_charge",
            "GenPiP_mass",
            "GenPiP_p4",
            "GenNuP_Impact_p4",

            "GenPiM_e",
            "GenPiM_p",
            "GenPiM_pt",
            "GenPiM_px",
            "GenPiM_py",
            "GenPiM_pz",
            "GenPiM_y",
            "GenPiM_eta",
            "GenPiM_theta",
            "GenPiM_phi",
            "GenPiM_charge",
            "GenPiM_mass",
            "GenPiM_p4",
            "GenNuM_Impact_p4",

            "GenPi0P1_e",
            "GenPi0P1_p",
            "GenPi0P1_pt",
            "GenPi0P1_px",
            "GenPi0P1_py",
            "GenPi0P1_pz",
            "GenPi0P1_y",
            "GenPi0P1_eta",
            "GenPi0P1_theta",
            "GenPi0P1_phi",
            "GenPi0P1_mass",
            "GenPi0P1_p4",

            "GenPi0P2_e",
            "GenPi0P2_p",
            "GenPi0P2_pt",
            "GenPi0P2_px",
            "GenPi0P2_py",
            "GenPi0P2_pz",
            "GenPi0P2_y",
            "GenPi0P2_eta",
            "GenPi0P2_theta",
            "GenPi0P2_phi",
            "GenPi0P2_mass",
            "GenPi0P2_p4",

            "GenRhoP_e",
            "GenRhoP_p",
            "GenRhoP_pt",
            "GenRhoP_px",
            "GenRhoP_py",
            "GenRhoP_pz",
            "GenRhoP_y",
            "GenRhoP_eta",
            "GenRhoP_theta",
            "GenRhoP_phi",
            "GenRhoP_mass",
            "GenRhoP_p4",

            "GenPi0M1_e",
            "GenPi0M1_p",
            "GenPi0M1_pt",
            "GenPi0M1_px",
            "GenPi0M1_py",
            "GenPi0M1_pz",
            "GenPi0M1_y",
            "GenPi0M1_eta",
            "GenPi0M1_theta",
            "GenPi0M1_phi",
            "GenPi0M1_mass",
            "GenPi0M1_p4",

            "GenPi0M2_e",
            "GenPi0M2_p",
            "GenPi0M2_pt",
            "GenPi0M2_px",
            "GenPi0M2_py",
            "GenPi0M2_pz",
            "GenPi0M2_y",
            "GenPi0M2_eta",
            "GenPi0M2_theta",
            "GenPi0M2_phi",
            "GenPi0M2_mass",
            "GenPi0M2_p4",

            "GenRhoM_e",
            "GenRhoM_p",
            "GenRhoM_pt",
            "GenRhoM_px",
            "GenRhoM_py",
            "GenRhoM_pz",
            "GenRhoM_y",
            "GenRhoM_eta",
            "GenRhoM_theta",
            "GenRhoM_phi",
            "GenRhoM_mass",
            "GenRhoM_p4",

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

            "n_GenTau_had",
            "HadGenTau_e",
            "HadGenTau_p",
            "HadGenTau_pt",
            "HadGenTau_px",
            "HadGenTau_py",
            "HadGenTau_pz",
            "HadGenTau_y",
            "HadGenTau_eta",
            "HadGenTau_theta",
            "HadGenTau_phi",
            "HadGenTau_charge",
            "HadGenTau_mass",
]

VARIABLES_RECO = [
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
            "RecoEmiss_e",
            "RecoEmiss_eta",
            "RecoEmiss_phi",
            "RecoEmiss_theta",
            "RecoEmiss_y",
            "RecoEmiss_costheta",

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

            "n_ChargedHadron",
            "ChargedHadron_e",
            "ChargedHadron_p",
            "ChargedHadron_pt",
            "ChargedHadron_px",
            "ChargedHadron_py",
            "ChargedHadron_pz",
            "ChargedHadron_eta",
            "ChargedHadron_theta",
            "ChargedHadron_phi",
            "ChargedHadron_charge",
            "ChargedHadron_mass",

            "n_NeutralHadron",
            "NeutralHadron_e",
            "NeutralHadron_p",
            "NeutralHadron_pt",
            "NeutralHadron_px",
            "NeutralHadron_py",
            "NeutralHadron_pz",
            "NeutralHadron_eta",
            "NeutralHadron_theta",
            "NeutralHadron_phi",
            "NeutralHadron_charge",
            "NeutralHadron_mass",

            "n_ChargedTau",
            "ChargedTau_e",
            "ChargedTau_p",
            "ChargedTau_pt",
            "ChargedTau_px",
            "ChargedTau_py",
            "ChargedTau_pz",
            "ChargedTau_eta",
            "ChargedTau_theta",
            "ChargedTau_phi",
            "ChargedTau_charge",
            "ChargedTau_mass",

            "n_NeutralTau",
            "NeutralTau_e",
            "NeutralTau_p",
            "NeutralTau_pt",
            "NeutralTau_px",
            "NeutralTau_py",
            "NeutralTau_pz",
            "NeutralTau_eta",
            "NeutralTau_theta",
            "NeutralTau_phi",
            "NeutralTau_charge",
            "NeutralTau_mass",

            "n_ChargedJet",
            "ChargedJet_e",
            "ChargedJet_p",
            "ChargedJet_pt",
            "ChargedJet_px",
            "ChargedJet_py",
            "ChargedJet_pz",
            "ChargedJet_eta",
            "ChargedJet_theta",
            "ChargedJet_phi",
            "ChargedJet_charge",
            "ChargedJet_mass",

            "n_NeutralJet",
            "NeutralJet_e",
            "NeutralJet_p",
            "NeutralJet_pt",
            "NeutralJet_px",
            "NeutralJet_py",
            "NeutralJet_pz",
            "NeutralJet_eta",
            "NeutralJet_theta",
            "NeutralJet_phi",
            "NeutralJet_charge",
            "NeutralJet_mass",
]

VARIABLES_CP = [

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

            "Higgs_px",
            "Higgs_py",
            "Higgs_pz",
            "Higgs_p",
            "Higgs_pt",
            "Higgs_e",
            "Higgs_eta",
            "Higgs_phi",
            "Higgs_theta",
            "Higgs_y",
            "Higgs_mass",

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


            "TauP_px", 
            "TauP_py",   
            "TauP_pz",   
            "TauP_p",    
            "TauP_pt",   
            "TauP_e",    
            "TauP_eta",    
            "TauP_phi",    
            "TauP_theta",   
            "TauP_y",     
            "TauP_mass",   

            "TauM_px",    
            "TauM_py",   
            "TauM_pz",   
            "TauM_p",   
            "TauM_pt",  
            "TauM_e",     
            "TauM_eta",   
            "TauM_phi",   
            "TauM_theta",    
            "TauM_y",    
            "TauM_mass", 

            "Recoil_mass",
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

VARIABLES_CMS = [
    "Phi_ZMF",
    "O_ZMF",
    "y_tau",
    "PhiCP_CMS",
]

VARIABLES_ILC = [
            "CosDeltaPhiILC", 
            "SinDeltaPhiILC", 
            "DeltaPhiILC",
            "KinILC_chi2",
            
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

            "RecoTauLead_px",    
            "RecoTauLead_py",   
            "RecoTauLead_pz",   
            "RecoTauLead_p",   
            "RecoTauLead_pt",   
            "RecoTauLead_e",    
            "RecoTauLead_eta",    
            "RecoTauLead_phi",    
            "RecoTauLead_theta",    
            "RecoTauLead_y",    
            "RecoTauLead_mass",

            "RecoTauSub_px",    
            "RecoTauSub_py",   
            "RecoTauSub_pz",   
            "RecoTauSub_p",   
            "RecoTauSub_pt",   
            "RecoTauSub_e",    
            "RecoTauSub_eta",    
            "RecoTauSub_phi",    
            "RecoTauSub_theta",    
            "RecoTauSub_y",    
            "RecoTauSub_mass",

            "RecoTauP_px", 
            "RecoTauP_py",   
            "RecoTauP_pz",   
            "RecoTauP_p",    
            "RecoTauP_pt",   
            "RecoTauP_e",    
            "RecoTauP_eta",    
            "RecoTauP_phi",    
            "RecoTauP_theta",   
            "RecoTauP_y",     
            "RecoTauP_mass",   

            "RecoTauM_px",    
            "RecoTauM_py",   
            "RecoTauM_pz",   
            "RecoTauM_p",   
            "RecoTauM_pt",  
            "RecoTauM_e",     
            "RecoTauM_eta",   
            "RecoTauM_phi",   
            "RecoTauM_theta",    
            "RecoTauM_y",    
            "RecoTauM_mass", 

            "RecoTau_DR",
            "RecoTau_cos",
            "RecoTau_DEta", 
            "RecoTau_DPhi",
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

SM = [
    'EWonly_taudecay_2Pi2Nu',
    'EWonly_taudecay_PiPi0Nu',
    ]

CEHIM_M1 = [
    'cehim_m1_taudecay_2Pi2Nu',
    'cehim_m1_taudecay_PiPi0Nu',
    ]

CEHIM_P1 = [
    'cehim_p1_taudecay_2Pi2Nu',
    'cehim_p1_taudecay_PiPi0Nu',
    ]

CEHRE_M1 = [
    'cehre_m1_taudecay_2Pi2Nu',
    'cehre_m1_taudecay_PiPi0Nu',
    ]

CEHRE_P1 = [
    'cehre_p1_taudecay_2Pi2Nu',
    'cehre_p1_taudecay_PiPi0Nu',
    ]

legend = {
    1:"sm",
    2:"sm_lin_quad_cehim_m1",
    3:"sm_lin_quad_cehim",
    4:"sm_lin_quad_cehre_m1",
    5:"sm_lin_quad_cehre_p1",

}

list = {
    1:SM,
    2:CEHIM_M1,
    3:CEHIM_P1,
    4:CEHRE_M1,
    5:CEHRE_P1,
}

'''for cut in CUT:

    variables = VARIABLES_RECO + VARIABLES_CP + VARIABLES_CMS + VARIABLES_ILC

    for num in range(1,6):
        outFile = ROOT.TFile.Open(DIRECTORY + legend[num] + "_" + cut + "_histo.root", "RECREATE")
        for var in variables:
            #loop to merge different sources into one histograms 
            j = 0
            hh = None
            for b in list[num]:
                file = f"{DIRECTORY}{b}_{cut}_histo.root"
                if file_exists(file):
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
            #change the name accordingly to the new histogram for EFT combine
            hist_name = legend[num]
            hh.SetName(hist_name + "_" + var)
            #write the histogram in the file   
            outFile.cd()
            hh.Write()
            print(f"{var}, {legend[num]}")
        outFile.Close()

    ## now we need to "isolate" the quadratic contribution from the eft only from the sm and lin+quad
    sm_file = ROOT.TFile.Open(DIRECTORY + legend[1] + "_" + cut + "_histo.root", "READ")
    cehim_m1_file = ROOT.TFile.Open(DIRECTORY + legend[2] + "_" + cut + "_histo.root", "READ")
    cehim_p1_file = ROOT.TFile.Open(DIRECTORY + legend[3] + "_" + cut + "_histo.root", "READ")
    quad_file = ROOT.TFile.Open(DIRECTORY + "quad_cehim_" + cut + "_histo.root", "RECREATE")

    for var in variables:
        sm_histo = sm_file.Get(legend[1] + "_" + var)
        cehim_m1_histo = cehim_m1_file.Get(legend[2] + "_" + var)
        cehim_p1_histo = cehim_p1_file.Get(legend[3] + "_" + var)

        # quad = cpv(+1) + cpv(-1) - 2*sm, in brackets the WC
        quad_histo = copy.deepcopy(cehim_p1_histo)
        quad_histo.SetDirectory(0)

        quad_histo.Add(cehim_m1_histo)
        quad_histo.Add(sm_histo, -2.)
        quad_histo.SetName("quad_cehim_" + var)

        print("var {} to file {}\n".format(var, quad_file))

        quad_file.cd()
        quad_histo.Write()

    quad_file.Close()'''

for cut in CUT:

    variables = VARIABLES_RECO + VARIABLES_CP + VARIABLES_CMS + VARIABLES_ILC
    outFile = ROOT.TFile.Open(DIRECTORY+'MG_P8_diff' + "_" + cut + "_histo.root", "RECREATE")
    for var in variables:
        #loop to merge different sources into one histograms 
        j = 0
        hh = None
        for b in ['EWonly_taudecay_2Pi2Nu', "p8_ee_llH_Hpinu_even"]:
            file = f"{DIRECTORY}{b}_{cut}_histo.root"
            if file_exists(file):
                tf = ROOT.TFile.Open(file, "READ")
                print(j)
                if (j==0):
                    h = tf.Get(var)
                    hh = copy.deepcopy(h)
                    hh.SetDirectory(0)
                else:
                    h = tf.Get(var)
                    hh1 = copy.deepcopy(h)
                    hh1.SetDirectory(0)
                    hh.Add(hh1, -1.)
                j += 1
                tf.Close()
        #write the histogram in the file   
        outFile.cd()
        hh.Write()
        print(f"{var}")
    outFile.Close()
