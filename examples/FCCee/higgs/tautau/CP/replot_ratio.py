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
DIRECTORY = "/ceph/sgiappic/HiggsCP/CPReco/final_explicit_v3/"

#directory where you want your plots to go
DIR_PLOTS = '/web/sgiappic/public_html/HiggsCP/Reco_explicit/' 
#list of cuts you want to plot
CUTS = [
    "selReco_20chi",
    #"selReco",
    #"selDPhi",
 ] 
#labels for the cuts in the plots
LABELS = {
    "selReco": "No additional selection",
    "selReco_20chi": "p_{T,miss} (#chi^{2})<20 GeV",
    "selGen": "No additional selection",
    "selDPhi":"KinGen_hh_norm_DPhi<0.5"
 }

label = ""
ana_tex        = "e^{+}e^{-} #rightarrow Z H, H #rightarrow #tau#tau (#pi#nu and #pi#pi^{0}#nu)"
energy         = 240
collider       = 'FCC-ee'
intLumi        = 10.8 #ab-1
LOGY = False

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

            ########## cp 
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
signals_old = [
    #'noISR_e+e-_noCuts_EWonly',
    #'noISR_e+e-_noCuts_cehre_m1',
    #'noISR_e+e-_noCuts_cehre_p1',
    #'noISR_e+e-_noCuts_cehim_m1',
    #'noISR_e+e-_noCuts_cehim_p1',

    #'EWonly_taudecay_2Pi2Nu',
    #'cehim_m1_taudecay_2Pi2Nu',
    #'cehim_p1_taudecay_2Pi2Nu',
    #'cehre_m1_taudecay_2Pi2Nu',
    #'cehre_p1_taudecay_2Pi2Nu',

    'EWonly_taudecay_PiPi0Nu',
    'cehim_m1_taudecay_PiPi0Nu',
    'cehim_p1_taudecay_PiPi0Nu',
    'cehre_m1_taudecay_PiPi0Nu',
    'cehre_p1_taudecay_PiPi0Nu',

    #'cehim_m5_taudecay_2Pi2Nu',
    #'cehim_p5_taudecay_2Pi2Nu',
    #'cehre_m5_taudecay_2Pi2Nu',
    #'cehre_p5_taudecay_2Pi2Nu',

    #'cehim_m2_taudecay_2Pi2Nu',
    #'cehim_p2_taudecay_2Pi2Nu',
    #'cehre_m2_taudecay_2Pi2Nu',
    #'cehre_p2_taudecay_2Pi2Nu',

    #'cehim_p0p1_taudecay_2Pi2Nu',
    #'cehim_m0p1_taudecay_2Pi2Nu',
    #'cehre_m0p1_taudecay_2Pi2Nu',
    #'cehre_p0p1_taudecay_2Pi2Nu',

    #'cehim_p10_taudecay_2Pi2Nu',
    #'cehim_m10_taudecay_2Pi2Nu',

    #'cehim_p10_taudecay_2Pi2Nu':{},
    #'cehim_m10_taudecay_2Pi2Nu':{},

    #'wzp6_ee_eeH_Htautau_ecm240',
]

signals = [
    "sm",
    "sm_lin_quad_cehim_m1",
    "sm_lin_quad_cehim",
    "sm_lin_quad_cehre_m1",
    "sm_lin_quad_cehre_p1",
]

slegend = {
    'noISR_e+e-_noCuts_EWonly':"Z(ee)H(#tau#tau), SM",
    'noISR_e+e-_noCuts_cehim_m1':"Z(ee)H(#tau#tau), CPV -1",
    'noISR_e+e-_noCuts_cehim_p1':"Z(ee)H(#tau#tau), CPV +1",
    'noISR_e+e-_noCuts_cehre_m1':"Z(ee)H(#tau#tau), CPC -1",
    'noISR_e+e-_noCuts_cehre_p1':"Z(ee)H(#tau#tau), CPC +1",
    'noISR':"Z(ee)H(#tau#tau), CPV +1, v.2",
    'taudecay':"Z(ee)H(#tau#tau), CPV +1, with #tau decay",
    'wzp6_ee_eeH_Htautau_ecm240':"Z(ee)H(#tau#tau), SM Whizard",

    'EWonly_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), SM",
    'cehim_m1_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPV -1",
    'cehim_p1_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPV +1",
    'cehre_m1_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPC -1",
    'cehre_p1_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPC +1",

    'EWonly_taudecay_PiPi0Nu':"Z(ee)H(#tau#tau), SM",
    'cehim_m1_taudecay_PiPi0Nu':"Z(ee)H(#tau#tau), CPV -1",
    'cehim_p1_taudecay_PiPi0Nu':"Z(ee)H(#tau#tau), CPV +1",
    'cehre_m1_taudecay_PiPi0Nu':"Z(ee)H(#tau#tau), CPC -1",
    'cehre_p1_taudecay_PiPi0Nu':"Z(ee)H(#tau#tau), CPC +1",

    'sm':"Z(ee)H(#tau#tau), SM",
    'sm_lin_quad_cehim_m1':"Z(ee)H(#tau#tau), CPV -1",
    'sm_lin_quad_cehim':"Z(ee)H(#tau#tau), CPV +1",
    'sm_lin_quad_cehre_m1':"Z(ee)H(#tau#tau), CPC -1",
    'sm_lin_quad_cehre_p1':"Z(ee)H(#tau#tau), CPC +1",

    'cehim_m5_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPV -5",
    'cehim_p5_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPV +5",
    'cehre_m5_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPC -5",
    'cehre_p5_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPC +5",

    'cehim_m2_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPV -2",
    'cehim_p2_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPV +2",
    'cehre_m2_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPC -2",
    'cehre_p2_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPC +2",

    'cehim_m0p1_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPV -0.1",
    'cehim_p0p1_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPV +0.1",
    'cehre_m0p1_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPC -0.1",
    'cehre_p0p1_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPC +0.1",

    'cehim_m10_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPV -10",
    'cehim_p10_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPV +10",
}

scolors = {
    'noISR_e+e-_noCuts_EWonly':ROOT.kRed-9,
    'noISR_e+e-_noCuts_cehim_m1':ROOT.kBlue-9,
    'noISR_e+e-_noCuts_cehim_p1':ROOT.kBlue-7,
    'noISR_e+e-_noCuts_cehre_m1':ROOT.kGreen-8,
    'noISR_e+e-_noCuts_cehre_p1':ROOT.kGreen-6,
    'noISR':ROOT.kCyan-6,
    'taudecay':ROOT.kMagenta-6,
    'wzp6_ee_eeH_Htautau_ecm240':ROOT.kGray+2,

    'EWonly_taudecay_2Pi2Nu':ROOT.kRed-9,
    'cehim_m1_taudecay_2Pi2Nu':ROOT.kBlue-9,
    'cehim_p1_taudecay_2Pi2Nu':ROOT.kBlue-7,
    'cehre_m1_taudecay_2Pi2Nu':ROOT.kGreen-8,
    'cehre_p1_taudecay_2Pi2Nu':ROOT.kGreen-6,

    'EWonly_taudecay_PiPi0Nu':ROOT.kRed-9,
    'cehim_m1_taudecay_PiPi0Nu':ROOT.kBlue-9,
    'cehim_p1_taudecay_PiPi0Nu':ROOT.kBlue-7,
    'cehre_m1_taudecay_PiPi0Nu':ROOT.kGreen-8,
    'cehre_p1_taudecay_PiPi0Nu':ROOT.kGreen-6,

    'sm':ROOT.kRed-9,
    'sm_lin_quad_cehim_m1':ROOT.kBlue-9,
    'sm_lin_quad_cehim':ROOT.kBlue-7,
    'sm_lin_quad_cehre_m1':ROOT.kGreen-8,
    'sm_lin_quad_cehre_p1':ROOT.kGreen-6,

    'cehim_m5_taudecay_2Pi2Nu':ROOT.kBlue-9,
    'cehim_p5_taudecay_2Pi2Nu':ROOT.kBlue-7,
    'cehre_m5_taudecay_2Pi2Nu':ROOT.kGreen-8,
    'cehre_p5_taudecay_2Pi2Nu':ROOT.kGreen-6,

    'cehim_m2_taudecay_2Pi2Nu':ROOT.kBlue-9,
    'cehim_p2_taudecay_2Pi2Nu':ROOT.kBlue-7,
    'cehre_m2_taudecay_2Pi2Nu':ROOT.kGreen-8,
    'cehre_p2_taudecay_2Pi2Nu':ROOT.kGreen-6,

    'cehim_m0p1_taudecay_2Pi2Nu':ROOT.kBlue-9,
    'cehim_p0p1_taudecay_2Pi2Nu':ROOT.kBlue-7,
    'cehre_m0p1_taudecay_2Pi2Nu':ROOT.kGreen-8,
    'cehre_p0p1_taudecay_2Pi2Nu':ROOT.kGreen-6,

    'cehim_m10_taudecay_2Pi2Nu':ROOT.kBlue-9,
    'cehim_p10_taudecay_2Pi2Nu':ROOT.kBlue-7,
}

for cut in CUTS:
    #VARIABLES = VARIABLES_GEN + VARIABLES_CPGEN
    VARIABLES = VARIABLES_RECO + VARIABLES_CP 
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
                h = tf.Get(s + "_" + variable)
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
                #if h.Integral()>0:
                    #h.Scale(1./(h.Integral()))
                max_y = h.GetMaximum() 
                h.GetYaxis().SetRangeUser(0, max_y*2)
            else: 
                #if h.Integral()>0:
                    #h.Scale(1./(h.Integral()))
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
        #drawing error bar for SM sample centered at 1 (ratio with itself) but error from the full scale
        #dummy = histos[0].Clone("")
        #for i in range(dummy.GetNbinsX()):
        #    dummy.SetBinContent(i,1.0)
        dummy = histos[0].Clone("")
        dummy.Divide(histos[0])
        #for i in range(dummy.GetNbinsX()+1):
        #    dummy.SetBinContent(i,1.0)
        #    dummy.SetBinError(i, histos[0].GetBinError(i)/histos[0].GetBinContent(i))
        dummy.SetFillColor(ROOT.kGray)
        dummy.SetLineColor(0)
        #dummy.SetMarkerColor(0)
        dummy.SetLineWidth(0)
        #dummy.SetMarkerSize(0)

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
        dummy.Draw("e2")
            
        ratio_list = []
        for i in range(1,nsig):  
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

            canvas.SaveAs(dir + "log/" + variable + ".png")
            canvas.SaveAs(dir + "log/" + variable + ".pdf")

        else:

            canvas.SaveAs(dir + variable + label + ".png")
            canvas.SaveAs(dir+ variable + label + ".pdf")