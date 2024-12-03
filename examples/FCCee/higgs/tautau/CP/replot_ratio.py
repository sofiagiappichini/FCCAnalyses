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
DIRECTORY = "/ceph/sgiappic/HiggsCP/CPGen/final_pi+rho/"

#directory where you want your plots to go
DIR_PLOTS = '/web/sgiappic/public_html/HiggsCP/Gen/Pi+Rho/' 
#list of cuts you want to plot
CUTS = [
    #"selReco",
    "selGen",
 ] 
#labels for the cuts in the plots
LABELS = {
    "selReco": "No additional selection",
    "selGen": "No additional selection",
 }

ana_tex        = "e^{+}e^{-} #rightarrow Z H, H #rightarrow #tau#tau (#pi#nu + #pi#pi^{0}#nu)"
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
            "FSGenElectron_vertex_x",
            "FSGenElectron_vertex_y",
            "FSGenElectron_vertex_z",

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
            "HiggsGenTau_vertex_x",
            "HiggsGenTau_vertex_y",
            "HiggsGenTau_vertex_z",

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

            #"n_GenTau_had", 
            #"n_TauTag_R5_match",  
            #"n_TauTag_R5_mass_match",
            #"n_events_tag",  
            #"n_events_tag_mass",
            #"n_TauTag_R5_match5",  
            #"n_TauTag_R5_mass_match5",
            #"n_events_tag5",  
            #"n_events_tag5_mass",
            #"n_events_func",  

            "n_LeadingPi",
            "LeadingPi_e",
            "LeadingPi_p",
            "LeadingPi_pt",
            "LeadingPi_px",
            "LeadingPi_py",
            "LeadingPi_pz",
            "LeadingPi_eta",
            "LeadingPi_theta",
            "LeadingPi_phi",
            "LeadingPi_charge",
            "LeadingPi_mass",
]

VARIABLES_LL = [
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

            #"n_TauDaughter",
            #"TauDaughter_e",
            #"TauDaughter_p",
            #"TauDaughter_pt",
            #"TauDaughter_px",
            #"TauDaughter_py",
            #"TauDaughter_pz",
            #"TauDaughter_eta",
            #"TauDaughter_theta",
            #"TauDaughter_phi",
            #"TauDaughter_mass",

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
            "TauLead_type",
            "n_TauLead_constituents",
            "n_TauLead_charged_constituents",
            "n_TauLead_neutral_constituents",

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
            "TauSub_type",
            "n_TauSub_constituents",
            "n_TauSub_charged_constituents",
            "n_TauSub_neutral_constituents",

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
            "TauP_type",
            "n_TauP_constituents",
            "n_TauP_charged_constituents",
            "n_TauP_neutral_constituents",

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
            "TauM_type",
            "n_TauM_constituents",
            "n_TauM_charged_constituents",
            "n_TauM_neutral_constituents",

            "Recoil",
            "Collinear_mass", 
        
            "Tau_DR",
            "Tau_cos",
            "Tau_DEta", 
            "Tau_DPhi",
            "Tau_DEta_y", 
            "Tau_DPhi_y", 
            
            "RecoZDaughter_DR", 
            "RecoZDaughter_cos", 
            "RecoZDaughter_DEta", 
            "RecoZDaughter_DPhi", 
            "RecoZDaughter_DEta_y", 
            "RecoZDaughter_DPhi_y", 
]

VARIABLES_PI = [
            "PiLead_px",    
            "PiLead_py",   
            "PiLead_pz",   
            "PiLead_p",   
            "PiLead_pt",   
            "PiLead_e",    
            "PiLead_eta",    
            "PiLead_phi",    
            "PiLead_theta",    
            "PiLead_y",    
            "PiLead_mass",

            "PiSub_px",    
            "PiSub_py",   
            "PiSub_pz",   
            "PiSub_p",   
            "PiSub_pt",   
            "PiSub_e",    
            "PiSub_eta",    
            "PiSub_phi",    
            "PiSub_theta",    
            "PiSub_y",    
            "PiSub_mass",

            "PiP_px",    
            "PiP_py",   
            "PiP_pz",   
            "PiP_p",   
            "PiP_pt",   
            "PiP_e",    
            "PiP_eta",    
            "PiP_phi",    
            "PiP_theta",    
            "PiP_y",    
            "PiP_mass",

            "PiM_px",    
            "PiM_py",   
            "PiM_pz",   
            "PiM_p",   
            "PiM_pt",   
            "PiM_e",    
            "PiM_eta",    
            "PiM_phi",    
            "PiM_theta",    
            "PiM_y",    
            "PiM_mass",

            "Pi_DR",
            "Pi_cos",
            "Pi_DEta", 
            "Pi_DPhi",
            "Pi_DEta_y", 
            "Pi_DPhi_y", 

            "TauPiLead_DR",
            "TauPiLead_cos",
            "TauPiLead_DEta", 
            "TauPiLead_DPhi",
            "TauPiLead_DEta_y", 
            "TauPiLead_DPhi_y", 

            "TauPiSub_DR",
            "TauPiSub_cos",
            "TauPiSub_DEta", 
            "TauPiSub_DPhi",
            "TauPiSub_DEta_y", 
            "TauPiSub_DPhi_y", 

            "TauPiP_DR",
            "TauPiP_cos",
            "TauPiP_DEta", 
            "TauPiP_DPhi",
            "TauPiP_DEta_y", 
            "TauPiP_DPhi_y", 

            "TauPiM_DR",
            "TauPiM_cos",
            "TauPiM_DEta", 
            "TauPiM_DPhi",
            "TauPiM_DEta_y", 
            "TauPiM_DPhi_y", 

            "HRF_PiLead_px",  
            "HRF_PiLead_py",  
            "HRF_PiLead_pz", 
            "HRF_PiLead_p", 
            "HRF_PiLead_pt",  
            "HRF_PiLead_e",   
            "HRF_PiLead_eta", 
            "HRF_PiLead_phi",  
            "HRF_PiLead_theta",    
            "HRF_PiLead_y", 

            "HRF_PiSub_px",  
            "HRF_PiSub_py",  
            "HRF_PiSub_pz", 
            "HRF_PiSub_p", 
            "HRF_PiSub_pt",  
            "HRF_PiSub_e",   
            "HRF_PiSub_eta", 
            "HRF_PiSub_phi",  
            "HRF_PiSub_theta",    
            "HRF_PiSub_y", 

            "HRF_PiP_px",  
            "HRF_PiP_py",  
            "HRF_PiP_pz", 
            "HRF_PiP_p", 
            "HRF_PiP_pt",  
            "HRF_PiP_e",   
            "HRF_PiP_eta", 
            "HRF_PiP_phi",  
            "HRF_PiP_theta",    
            "HRF_PiP_y", 

            "HRF_PiM_px",  
            "HRF_PiM_py",  
            "HRF_PiM_pz", 
            "HRF_PiM_p", 
            "HRF_PiM_pt",  
            "HRF_PiM_e",   
            "HRF_PiM_eta", 
            "HRF_PiM_phi",  
            "HRF_PiM_theta",    
            "HRF_PiM_y", 

            "HRF_Pi_DEta", 
            "HRF_Pi_DPhi",
            "HRF_Pi_DEta_y", 
            "HRF_Pi_DPhi_y", 

            "HRF_TauPiLead_DEta", 
            "HRF_TauPiLead_DPhi",
            "HRF_TauPiLead_DEta_y", 
            "HRF_TauPiLead_DPhi_y",

            "HRF_TauPiSub_DEta", 
            "HRF_TauPiSub_DPhi",
            "HRF_TauPiSub_DEta_y", 
            "HRF_TauPiSub_DPhi_y",

            "HRF_TauPiP_DEta", 
            "HRF_TauPiP_DPhi",
            "HRF_TauPiP_DEta_y", 
            "HRF_TauPiP_DPhi_y",

            "HRF_TauPiM_DEta", 
            "HRF_TauPiM_DPhi",
            "HRF_TauPiM_DEta_y", 
            "HRF_TauPiM_DPhi_y",

            "TauLeadRF_PiLead_px",    
            "TauLeadRF_PiLead_py",   
            "TauLeadRF_PiLead_pz",   
            "TauLeadRF_PiLead_p",   
            "TauLeadRF_PiLead_pt",   
            "TauLeadRF_PiLead_e",    
            "TauLeadRF_PiLead_eta",    
            "TauLeadRF_PiLead_phi",    
            "TauLeadRF_PiLead_theta",    
            "TauLeadRF_PiLead_y",    

            "TauSubRF_PiSub_px",    
            "TauSubRF_PiSub_py",   
            "TauSubRF_PiSub_pz",   
            "TauSubRF_PiSub_p",   
            "TauSubRF_PiSub_pt",   
            "TauSubRF_PiSub_e",    
            "TauSubRF_PiSub_eta",    
            "TauSubRF_PiSub_phi",    
            "TauSubRF_PiSub_theta",    
            "TauSubRF_PiSub_y",    

            "TauPRF_PiP_px",    
            "TauPRF_PiP_py",   
            "TauPRF_PiP_pz",   
            "TauPRF_PiP_p",   
            "TauPRF_PiP_pt",   
            "TauPRF_PiP_e",    
            "TauPRF_PiP_eta",    
            "TauPRF_PiP_phi",    
            "TauPRF_PiP_theta",    
            "TauPRF_PiP_y",    

            "TauMRF_PiM_px",    
            "TauMRF_PiM_py",   
            "TauMRF_PiM_pz",   
            "TauMRF_PiM_p",   
            "TauMRF_PiM_pt",   
            "TauMRF_PiM_e",    
            "TauMRF_PiM_eta",    
            "TauMRF_PiM_phi",    
            "TauMRF_PiM_theta",    
            "TauMRF_PiM_y",   

            "TauRF_Pi_DEta", 
            "TauRF_Pi_DPhi",
            "TauRF_Pi_DEta_y", 
            "TauRF_Pi_DPhi_y",  

            "Boosted_PiP_px",    
            "Boosted_PiP_py",   
            "Boosted_PiP_pz",   
            "Boosted_PiP_p",   
            "Boosted_PiP_pt",   
            "Boosted_PiP_e",    
            "Boosted_PiP_eta",    
            "Boosted_PiP_phi",    
            "Boosted_PiP_theta",    
            "Boosted_PiP_y",    

            "Boosted_PiM_px",    
            "Boosted_PiM_py",   
            "Boosted_PiM_pz",   
            "Boosted_PiM_p",   
            "Boosted_PiM_pt",   
            "Boosted_PiM_e",    
            "Boosted_PiM_eta",    
            "Boosted_PiM_phi",    
            "Boosted_PiM_theta",    
            "Boosted_PiM_y",    

            "Boosted_Pi0P_px",    
            "Boosted_Pi0P_py",   
            "Boosted_Pi0P_pz",   
            "Boosted_Pi0P_p",   
            "Boosted_Pi0P_pt",   
            "Boosted_Pi0P_e",    
            "Boosted_Pi0P_eta",    
            "Boosted_Pi0P_phi",    
            "Boosted_Pi0P_theta",    
            "Boosted_Pi0P_y",    

            "Boosted_Pi0M_px",    
            "Boosted_Pi0M_py",   
            "Boosted_Pi0M_pz",   
            "Boosted_Pi0M_p",   
            "Boosted_Pi0M_pt",   
            "Boosted_Pi0M_e",    
            "Boosted_Pi0M_eta",    
            "Boosted_Pi0M_phi",    
            "Boosted_Pi0M_theta",    
            "Boosted_Pi0M_y",    

            "RecoPhiCP",
            "RecoPhiCP_cos",
]

VARIABLES_CPGEN = [
    "GenZ_px",
            "GenZ_py",
            "GenZ_pz",
            "GenZ_p",
            "GenZ_pt",
            "GenZ_e",
            "GenZ_eta",
            "GenZ_phi",
            "GenZ_theta",
            "GenZ_y",
            "GenZ_mass",

            "FSGenZLead_px", 
            "FSGenZLead_py",   
            "FSGenZLead_pz",   
            "FSGenZLead_p",    
            "FSGenZLead_pt",   
            "FSGenZLead_e",    
            "FSGenZLead_eta",    
            "FSGenZLead_phi",    
            "FSGenZLead_theta",   
            "FSGenZLead_y",     
            "FSGenZLead_mass",   

            "FSGenZSub_px",    
            "FSGenZSub_py",   
            "FSGenZSub_pz",   
            "FSGenZSub_p",   
            "FSGenZSub_pt",  
            "FSGenZSub_e",     
            "FSGenZSub_eta",   
            "FSGenZSub_phi",   
            "FSGenZSub_theta",    
            "FSGenZSub_y",    
            "FSGenZSub_mass",   

            "FSGenZP_px", 
            "FSGenZP_py",   
            "FSGenZP_pz",   
            "FSGenZP_p",    
            "FSGenZP_pt",   
            "FSGenZP_e",    
            "FSGenZP_eta",    
            "FSGenZP_phi",    
            "FSGenZP_theta",   
            "FSGenZP_y",     
            "FSGenZP_mass",   

            "FSGenZM_px",    
            "FSGenZM_py",   
            "FSGenZM_pz",   
            "FSGenZM_p",   
            "FSGenZM_pt",  
            "FSGenZM_e",     
            "FSGenZM_eta",   
            "FSGenZM_phi",   
            "FSGenZM_theta",    
            "FSGenZM_y",    
            "FSGenZM_mass", 

            "GenTauLead_px",    
            "GenTauLead_py",   
            "GenTauLead_pz",   
            "GenTauLead_p",   
            "GenTauLead_pt",   
            "GenTauLead_e",    
            "GenTauLead_eta",    
            "GenTauLead_phi",    
            "GenTauLead_theta",    
            "GenTauLead_y",    
            "GenTauLead_mass",

            "GenTauSub_px",    
            "GenTauSub_py",   
            "GenTauSub_pz",   
            "GenTauSub_p",   
            "GenTauSub_pt",   
            "GenTauSub_e",    
            "GenTauSub_eta",    
            "GenTauSub_phi",    
            "GenTauSub_theta",    
            "GenTauSub_y",    
            "GenTauSub_mass",

            "GenTauP_px",    
            "GenTauP_py",   
            "GenTauP_pz",   
            "GenTauP_p",   
            "GenTauP_pt",   
            "GenTauP_e",    
            "GenTauP_eta",    
            "GenTauP_phi",    
            "GenTauP_theta",    
            "GenTauP_y",    
            "GenTauP_mass",

            "GenTauM_px",    
            "GenTauM_py",   
            "GenTauM_pz",   
            "GenTauM_p",   
            "GenTauM_pt",   
            "GenTauM_e",    
            "GenTauM_eta",    
            "GenTauM_phi",    
            "GenTauM_theta",    
            "GenTauM_y",    
            "GenTauM_mass",
        
            "HiggsGenTau_DR",
            "HiggsGenTau_cos",
            "HiggsGenTau_DEta", 
            "HiggsGenTau_DPhi",
            
            "FSGenZDaughter_DR", 
            "FSGenZDaughter_cos", 
            "FSGenZDaughter_DEta", 
            "FSGenZDaughter_DPhi", 

            "HiggsGenTau_DEta_y", 
            "HiggsGenTau_DPhi_y", 
            
            "FSGenZDaughter_DEta_y", 
            "FSGenZDaughter_DPhi_y", 

            #"ytau", 
            #"GenPhiCP_pre",   
            #"GenPhiCP",   

            "HRF_GenTauLead_px",  
            "HRF_GenTauLead_py",  
            "HRF_GenTauLead_pz", 
            "HRF_GenTauLead_p", 
            "HRF_GenTauLead_pt",  
            "HRF_GenTauLead_e",   
            "HRF_GenTauLead_eta", 
            "HRF_GenTauLead_phi",  
            "HRF_GenTauLead_theta",    
            "HRF_GenTauLead_y", 

            "HRF_GenTauSub_px",  
            "HRF_GenTauSub_py",  
            "HRF_GenTauSub_pz", 
            "HRF_GenTauSub_p", 
            "HRF_GenTauSub_pt",  
            "HRF_GenTauSub_e",   
            "HRF_GenTauSub_eta", 
            "HRF_GenTauSub_phi",  
            "HRF_GenTauSub_theta",    
            "HRF_GenTauSub_y", 

            "HRF_GenTauP_px",  
            "HRF_GenTauP_py",  
            "HRF_GenTauP_pz", 
            "HRF_GenTauP_p", 
            "HRF_GenTauP_pt",  
            "HRF_GenTauP_e",   
            "HRF_GenTauP_eta", 
            "HRF_GenTauP_phi",  
            "HRF_GenTauP_theta",    
            "HRF_GenTauP_y", 

            "HRF_GenTauM_px",  
            "HRF_GenTauM_py",  
            "HRF_GenTauM_pz", 
            "HRF_GenTauM_p", 
            "HRF_GenTauM_pt",  
            "HRF_GenTauM_e",   
            "HRF_GenTauM_eta", 
            "HRF_GenTauM_phi",  
            "HRF_GenTauM_theta",    
            "HRF_GenTauM_y", 

            #"HRF_GenTau_DEta", 
            #"HRF_GenTau_DPhi",
            #"HRF_GenTau_DEta_y", 
            #"HRF_GenTau_DPhi_y", 

            "GenTheta2",
            "GenTheta2_cos",

            "GenRecoil",

            "CosDeltaPhi",  
            "SinDeltaPhi",    
            "GenDeltaPhi",

            "CosPhi",  
            "SinPhi",    
            "GenPhi_decay",
]

VARIABLES_CPRECO = [
            "HRF_TauLead_px",  
            "HRF_TauLead_py",  
            "HRF_TauLead_pz", 
            "HRF_TauLead_p", 
            "HRF_TauLead_pt",  
            "HRF_TauLead_e",   
            "HRF_TauLead_eta", 
            "HRF_TauLead_phi",  
            "HRF_TauLead_theta",    
            "HRF_TauLead_y", 

            "HRF_TauSub_px",  
            "HRF_TauSub_py",  
            "HRF_TauSub_pz", 
            "HRF_TauSub_p", 
            "HRF_TauSub_pt",  
            "HRF_TauSub_e",   
            "HRF_TauSub_eta", 
            "HRF_TauSub_phi",  
            "HRF_TauSub_theta",    
            "HRF_TauSub_y", 

            "HRF_TauP_px",  
            "HRF_TauP_py",  
            "HRF_TauP_pz", 
            "HRF_TauP_p", 
            "HRF_TauP_pt",  
            "HRF_TauP_e",   
            "HRF_TauP_eta", 
            "HRF_TauP_phi",  
            "HRF_TauP_theta",    
            "HRF_TauP_y", 

            "HRF_TauM_px",  
            "HRF_TauM_py",  
            "HRF_TauM_pz", 
            "HRF_TauM_p", 
            "HRF_TauM_pt",  
            "HRF_TauM_e",   
            "HRF_TauM_eta", 
            "HRF_TauM_phi",  
            "HRF_TauM_theta",    
            "HRF_TauM_y", 

            "HRF_Tau_DEta", 
            "HRF_Tau_DPhi",
            "HRF_Tau_DEta_y", 
            "HRF_Tau_DPhi_y", 

            "ZRF_RecoZLead_px",  
            "ZRF_RecoZLead_py",  
            "ZRF_RecoZLead_pz", 
            "ZRF_RecoZLead_p", 
            "ZRF_RecoZLead_pt",  
            "ZRF_RecoZLead_e",   
            "ZRF_RecoZLead_eta", 
            "ZRF_RecoZLead_phi",  
            "ZRF_RecoZLead_theta",    
            "ZRF_RecoZLead_y", 

            "ZRF_RecoZSub_px",  
            "ZRF_RecoZSub_py",  
            "ZRF_RecoZSub_pz", 
            "ZRF_RecoZSub_p", 
            "ZRF_RecoZSub_pt",  
            "ZRF_RecoZSub_e",   
            "ZRF_RecoZSub_eta", 
            "ZRF_RecoZSub_phi",  
            "ZRF_RecoZSub_theta",    
            "ZRF_RecoZSub_y", 

            "ZRF_RecoZP_px",  
            "ZRF_RecoZP_py",  
            "ZRF_RecoZP_pz", 
            "ZRF_RecoZP_p", 
            "ZRF_RecoZP_pt",  
            "ZRF_RecoZP_e",   
            "ZRF_RecoZP_eta", 
            "ZRF_RecoZP_phi",  
            "ZRF_RecoZP_theta",    
            "ZRF_RecoZP_y", 

            "ZRF_RecoZM_px",  
            "ZRF_RecoZM_py",  
            "ZRF_RecoZM_pz", 
            "ZRF_RecoZM_p", 
            "ZRF_RecoZM_pt",  
            "ZRF_RecoZM_e",   
            "ZRF_RecoZM_eta", 
            "ZRF_RecoZM_phi",  
            "ZRF_RecoZM_theta",    
            "ZRF_RecoZM_y", 

            "ZRF_RecoZDaughter_DEta", 
            "ZRF_RecoZDaughter_DPhi",
            "ZRF_RecoZDaughter_DEta_y", 
            "ZRF_RecoZDaughter_DPhi_y", 

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
    'noISR_e+e-_noCuts_cehre_m1',
    'noISR_e+e-_noCuts_cehre_p1',
    'noISR_e+e-_noCuts_cehim_m1',
    'noISR_e+e-_noCuts_cehim_p1',

    #'EWonly_taudecay_2Pi2Nu',
    #'cehim_m1_taudecay_2Pi2Nu',
    #'cehim_p1_taudecay_2Pi2Nu',
    #'cehre_m1_taudecay_2Pi2Nu',
    #'cehre_p1_taudecay_2Pi2Nu',

    #'cehim_m5_taudecay_2Pi2Nu',
    #'cehim_p5_taudecay_2Pi2Nu',
    #'cehre_m5_taudecay_2Pi2Nu',
    #'cehre_p5_taudecay_2Pi2Nu',

    #'cehim_m2_taudecay_2Pi2Nu',
    #'cehim_p2_taudecay_2Pi2Nu',
    #'cehre_m2_taudecay_2Pi2Nu',
    #'cehre_p2_taudecay_2Pi2Nu',

    #'wzp6_ee_eeH_Htautau_ecm240',
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

    'cehim_m5_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPV -5",
    'cehim_p5_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPV +5",
    'cehre_m5_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPC -5",
    'cehre_p5_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPC +5",

    'cehim_m2_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPV -2",
    'cehim_p2_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPV +2",
    'cehre_m2_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPC -2",
    'cehre_p2_taudecay_2Pi2Nu':"Z(ee)H(#tau#tau), CPC +2",
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

    'cehim_m5_taudecay_2Pi2Nu':ROOT.kBlue-9,
    'cehim_p5_taudecay_2Pi2Nu':ROOT.kBlue-7,
    'cehre_m5_taudecay_2Pi2Nu':ROOT.kGreen-8,
    'cehre_p5_taudecay_2Pi2Nu':ROOT.kGreen-6,

    'cehim_m2_taudecay_2Pi2Nu':ROOT.kBlue-9,
    'cehim_p2_taudecay_2Pi2Nu':ROOT.kBlue-7,
    'cehre_m2_taudecay_2Pi2Nu':ROOT.kGreen-8,
    'cehre_p2_taudecay_2Pi2Nu':ROOT.kGreen-6,
}

for cut in CUTS:
    VARIABLES = VARIABLES_GEN + VARIABLES_CPGEN
    #VARIABLES = VARIABLES_RECO + VARIABLES_LL + VARIABLES_CPRECO + VARIABLES_PI
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

            canvas.SaveAs(dir + variable + ".png")
            canvas.SaveAs(dir+ variable + ".pdf")