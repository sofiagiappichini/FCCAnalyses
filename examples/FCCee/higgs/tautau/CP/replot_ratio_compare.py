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
DIRECTORY = "/ceph/sgiappic/HiggsCP/CPReco_2Pi2Nu/final+gen/"

#directory where you want your plots to go
DIR_PLOTS = '/web/sgiappic/public_html/HiggsCP/Reco_2Pi2Nu/GenCompare_140225_onlyCP/' 
#list of cuts you want to plot
CUTS = [
    #"selReco",
    "selDPhi_low",
    "selDPhi_up",
 ] 
#labels for the cuts in the plots
LABELS = {
    "selReco": "No additional selection",
    "selGen": "No additional selection",
    "selDPhi_low":"KinGen_hh_norm_DPhi<1.5",
    "selDPhi_up":"KinGen_hh_norm_DPhi>1.5",
 }

ana_tex        = "e^{+}e^{-} #rightarrow Z H, H #rightarrow #tau#tau (#pi#nu)"
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

            "n_ChargedPar",
            "ChargedPar_e",
            "ChargedPar_p",
            "ChargedPar_pt",
            "ChargedPar_px",
            "ChargedPar_py",
            "ChargedPar_pz",
            "ChargedPar_eta",
            "ChargedPar_theta",
            "ChargedPar_phi",
            "ChargedPar_charge",
            "ChargedPar_mass",

            "n_NeutralSyst",
            "NeutralSyst_e",
            "NeutralSyst_p",
            "NeutralSyst_pt",
            "NeutralSyst_px",
            "NeutralSyst_py",
            "NeutralSyst_pz",
            "NeutralSyst_eta",
            "NeutralSyst_theta",
            "NeutralSyst_phi",
            "NeutralSyst_charge",
            "NeutralSyst_mass",
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
            "TauLead_type",
            
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
            "GenPiM_mass",

            "GenEmiss_px",
            "GenEmiss_py",
            "GenEmiss_pz",
            "GenEmiss_pt",
            "GenEmiss_p",
            "GenEmiss_e",
            "GenEmiss_eta",
            "GenEmiss_phi",
            "GenEmiss_theta",
            "GenEmiss_y",

            "Kin_TauP_Px", "Kin_TauP_Py", "Kin_TauP_Pz", "Kin_TauP_E",
            "Kin_TauP_M", "Kin_TauP_Eta", "Kin_TauP_Phi", "Kin_TauP_P", 
            "Kin_TauP_Pt", "Kin_TauP_Theta", "Kin_TauP_Rapidity",
            
            "Kin_TauM_Px", "Kin_TauM_Py", "Kin_TauM_Pz", "Kin_TauM_E",
            "Kin_TauM_M", "Kin_TauM_Eta", "Kin_TauM_Phi", "Kin_TauM_P", 
            "Kin_TauM_Pt", "Kin_TauM_Theta", "Kin_TauM_Rapidity",

            "Kin_NuP_Px", "Kin_NuP_Py", "Kin_NuP_Pz", "Kin_NuP_E",
            "Kin_NuP_M", "Kin_NuP_Eta", "Kin_NuP_Phi", "Kin_NuP_P", 
            "Kin_NuP_Pt", "Kin_NuP_Theta", "Kin_NuP_Rapidity",

            "Kin_NuM_Px", "Kin_NuM_Py", "Kin_NuM_Pz", "Kin_NuM_E",
            "Kin_NuM_M", "Kin_NuM_Eta", "Kin_NuM_Phi", "Kin_NuM_P", 
            "Kin_NuM_Pt", "Kin_NuM_Theta", "Kin_NuM_Rapidity",

            "TauPRF_KinPiP_Px", "TauPRF_KinPiP_Py", "TauPRF_KinPiP_Pz", "TauPRF_KinPiP_E",
            "TauPRF_KinPiP_M", "TauPRF_KinPiP_Eta", "TauPRF_KinPiP_Phi", "TauPRF_KinPiP_P", 
            "TauPRF_KinPiP_Pt", "TauPRF_KinPiP_Theta", "TauPRF_KinPiP_Rapidity",

            "TauPRF_KinNuP_Px", "TauPRF_KinNuP_Py", "TauPRF_KinNuP_Pz", "TauPRF_KinNuP_E",
            "TauPRF_KinNuP_M", "TauPRF_KinNuP_Eta", "TauPRF_KinNuP_Phi", "TauPRF_KinNuP_P", 
            "TauPRF_KinNuP_Pt", "TauPRF_KinNuP_Theta", "TauPRF_KinNuP_Rapidity",

            "TauMRF_KinPiM_Px", "TauMRF_KinPiM_Py", "TauMRF_KinPiM_Pz", "TauMRF_KinPiM_E",
            "TauMRF_KinPiM_M", "TauMRF_KinPiM_Eta", "TauMRF_KinPiM_Phi", "TauMRF_KinPiM_P", 
            "TauMRF_KinPiM_Pt", "TauMRF_KinPiM_Theta", "TauMRF_KinPiM_Rapidity",

            "TauMRF_KinNuM_Px", "TauMRF_KinNuM_Py", "TauMRF_KinNuM_Pz", "TauMRF_KinNuM_E",
            "TauMRF_KinNuM_M", "TauMRF_KinNuM_Eta", "TauMRF_KinNuM_Phi", "TauMRF_KinNuM_P", 
            "TauMRF_KinNuM_Pt", "TauMRF_KinNuM_Theta", "TauMRF_KinNuM_Rapidity",

            "RecoilKin_TauM_Px", "RecoilKin_TauM_Py", "RecoilKin_TauM_Pz", "RecoilKin_TauM_E",
            "RecoilKin_TauM_M", "RecoilKin_TauM_Eta", "RecoilKin_TauM_Phi", "RecoilKin_TauM_P", 
            "RecoilKin_TauM_Pt", "RecoilKin_TauM_Theta", "RecoilKin_TauM_Rapidity",

            "hPnormKin_Px", "hPnormKin_Py", "hPnormKin_Pz", "hPnormKin_Pt", "hPnormKin_P", "hPnormKin_Phi", "hPnormKin_Eta", "hPnormKin_Theta",
            "hMnormKin_Px", "hMnormKin_Py", "hMnormKin_Pz", "hMnormKin_Pt", "hMnormKin_P", "hMnormKin_Phi", "hMnormKin_Eta", "hMnormKin_Theta",
            "hh_normKin_Px", "hh_normKin_Py", "hh_normKin_Pz", "hh_normKin_Pt", "hh_normKin_P", "hh_normKin_Phi", "hh_normKin_Eta", "hh_normKin_Theta",

            "CosDeltaPhiKin",   
            "SinDeltaPhiKin",   
            "DeltaPhiKin",  
            "GenCosDeltaPhi",   
            "GenSinDeltaPhi",   
            "GenDeltaPhi",  
]

VARIABLES_COMP = [ 
            "KinGenTauP_Px",
            "KinGenTauP_Py",
            "KinGenTauP_Pz",
            "KinGenTauP_Pt",
            "KinGenTauP_P",
            "KinGenTauP_E", 
            "KinGenTauP_M",   
            "KinGenTauP_DPhi",
            "KinGenTauP_DEta", 
            "KinGenTauP_DTheta", 

            "KinGenNuP_Px",
            "KinGenNuP_Py",
            "KinGenNuP_Pz",
            "KinGenNuP_Pt",
            "KinGenNuP_P",
            "KinGenNuP_E", 
            "KinGenNuP_M", 
            "KinGenNuP_DPhi",      
            "KinGenNuP_DEta",   
            "KinGenNuP_DTheta",      
 
            "TauPRF_KinGenNuP_Px",
            "TauPRF_KinGenNuP_Py",
            "TauPRF_KinGenNuP_Pz",
            "TauPRF_KinGenNuP_Pt",
            "TauPRF_KinGenNuP_P",
            "TauPRF_KinGenNuP_M",
            "TauPRF_KinGenNuP_E",      
            "TauPRF_KinGenNuP_DPhi",      
            "TauPRF_KinGenNuP_DEta",  
            "TauPRF_KinGenNuP_DTheta",       

            "TauPRF_KinGenPiP_Px",
            "TauPRF_KinGenPiP_Py",
            "TauPRF_KinGenPiP_Pz",
            "TauPRF_KinGenPiP_P",
            "TauPRF_KinGenPiP_Pt",
            "TauPRF_KinGenPiP_M",
            "TauPRF_KinGenPiP_E",      
            "TauPRF_KinGenPiP_DPhi",       
            "TauPRF_KinGenPiP_DEta",   
            "TauPRF_KinGenPiP_DTheta",

            "KinGen_hPnorm_Px",
            "KinGen_hPnorm_Py",
            "KinGen_hPnorm_Pz",
            "KinGen_hPnorm_P",         
            "KinGen_hPnorm_DPhi",     
            "KinGen_hPnorm_DEta", 
            "KinGen_hPnorm_DTheta",     

            "KinGenTauM_Px",
            "KinGenTauM_Py",
            "KinGenTauM_Pz",
            "KinGenTauM_P",
            "KinGenTauM_Pt",
            "KinGenTauM_E",
            "KinGenTauM_M",         
            "KinGenTauM_DPhi",
            "KinGenTauM_DEta", 
            "KinGenTauM_DTheta",

            "KinGenNuM_Px",
            "KinGenNuM_Py",
            "KinGenNuM_Pz",
            "KinGenNuM_P",
            "KinGenNuM_E",
            "KinGenNuM_M",
            "KinGenNuM_Pt",      
            "KinGenNuM_DPhi",      
            "KinGenNuM_DEta",     
            "KinGenNuM_DTheta", 
   
            "TauMRF_KinGenNuM_Px",
            "TauMRF_KinGenNuM_Py",
            "TauMRF_KinGenNuM_Pz",
            "TauMRF_KinGenNuM_P",
            "TauMRF_KinGenNuM_E",
            "TauMRF_KinGenNuM_M",
            "TauMRF_KinGenNuM_Pt",
            "TauMRF_KinGenNuM_DPhi",      
            "TauMRF_KinGenNuM_DEta",      
            "TauMRF_KinGenNuM_DTheta",

            "TauMRF_KinGenPiM_Px",
            "TauMRF_KinGenPiM_Py",
            "TauMRF_KinGenPiM_Pz",
            "TauMRF_KinGenPiM_P",
            "TauMRF_KinGenPiM_Pt",
            "TauMRF_KinGenPiM_E",
            "TauMRF_KinGenPiM_M",      
            "TauMRF_KinGenPiM_DPhi",       
            "TauMRF_KinGenPiM_DEta",    
            "TauMRF_KinGenPiM_DTheta",  

            "HRF_KinGenTauM_Px",
            "HRF_KinGenTauM_Py",
            "HRF_KinGenTauM_Pz",
            "HRF_KinGenTauM_Pt",
            "HRF_KinGenTauM_P",
            "HRF_KinGenTauM_E",
            "HRF_KinGenTauM_M",            
            "HRF_KinGenTauM_DPhi",       
            "HRF_KinGenTauM_DEta",   
            "HRF_KinGenTauM_DTheta",

            "KinGen_hMnorm_Px",
            "KinGen_hMnorm_Py",
            "KinGen_hMnorm_Pz",
            "KinGen_hMnorm_P",
            "KinGen_hMnorm_Pt",      
            "KinGen_hMnorm_DPhi",     
            "KinGen_hMnorm_DEta",   
            "KinGen_hMnorm_DTheta",

            "KinGen_hh_norm_Px",
            "KinGen_hh_norm_Py",
            "KinGen_hh_norm_Pz",
            "KinGen_hh_norm_P",
            "KinGen_hh_norm_Pt",                              
            "KinGen_hh_norm_DPhi",     
            "KinGen_hh_norm_DEta",    
            "KinGen_hh_norm_DTheta", 
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
    #'noISR_e+e-_noCuts_EWonly',
    #'noISR_e+e-_noCuts_cehre_m1',
    #'noISR_e+e-_noCuts_cehre_p1',
    #'noISR_e+e-_noCuts_cehim_m1',
    #'noISR_e+e-_noCuts_cehim_p1',

    'EWonly_taudecay_2Pi2Nu',
    'cehim_m1_taudecay_2Pi2Nu',
    'cehim_p1_taudecay_2Pi2Nu',
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

#for cut in CUTS:
for s in signals:
    #VARIABLES = VARIABLES_GEN + VARIABLES_CPGEN
    VARIABLES = VARIABLES_CPRECO + VARIABLES_COMP
    for variable in VARIABLES:

        canvas = ROOT.TCanvas("", "", 1000, 1000)
        #canvas.SetTicks(1, 1)

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
        for cut in CUTS:
            fin = f"{DIRECTORY}{s}_{cut}_histo.root"
            with ROOT.TFile(fin) as tf:
                h = tf.Get(variable)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
            histos.append(hh)
            colors.append(scolors[s])
            leg.AddEntry(histos[-1], slegend[s], "l")

        # add the signal histograms

        for i in range(len(CUTS)):
            h = histos[i]
            h.SetLineWidth(3)
            h.SetLineStyle(i+1)  # 1 = solid, 2 = dashed, 3 = dotted, etc.
            h.SetLineColor(colors[i])
            if i == 0:
                h.Draw("HIST")
                h.GetYaxis().SetTitle("Events")
                h.GetXaxis().SetTitle(histos[0].GetXaxis().GetTitle())
                h.GetXaxis().SetTitleOffset(1.2)
                #if h.Integral()>0:
                    #h.Scale(1./(h.Integral()))
                max_y = h.GetMaximum() 
                h.GetYaxis().SetRangeUser(0, max_y*2)
            else: 
                #if h.Integral()>0:
                    #h.Scale(1./(h.Integral()))
                h.Draw("HIST SAME")
        
        extralab = "solid #Delta#phi <1.5, dashed #Delta#phi >1.5"#LABELS[cut]

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

        canvas.SetTicks(1, 1)
        canvas.SetLeftMargin(0.14)
        canvas.SetRightMargin(0.08)
        canvas.GetFrame().SetBorderSize(12)
        #canvas.SetBottomMargin(0)

        canvas.cd()

        canvas.RedrawAxis()
        canvas.Modified()
        canvas.Update()

        dir = DIR_PLOTS + s + "/" #+ cut + "/"
        make_dir_if_not_exists(dir)

        if (LOGY == True):

            canvas.SaveAs(dir + "log/" + variable + ".png")
            canvas.SaveAs(dir + "log/" + variable + ".pdf")

        else:

            canvas.SaveAs(dir + variable + ".png")
            canvas.SaveAs(dir + variable + ".pdf")