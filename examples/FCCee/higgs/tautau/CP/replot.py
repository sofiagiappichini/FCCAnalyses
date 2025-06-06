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
        #print(f"Directory created successfully.")
    #else:
        #print(f"Directory already exists.")

def file_exists(file_path):
    return os.path.isfile(file_path)

# directory with final stage files
DIRECTORY = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/CP/final_250530/"

SUBDIR = [
    'LL',
    'LH',
    'HH',
]
#category to plot
CAT = [
    "QQ",
    "LL",
]

CUTS = [
    "selReco",
    "selReco_100Coll150",
    "selReco_100Coll150_115Rec160",
    "selReco_100Coll150_115Rec160_2DR",
    "selReco_100Coll150_115Rec160_2DR_cos0.6",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100",
     
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

VARIABLES_CMS = [
    "Phi_ZMF",
    "O_ZMF",
    "y_tau",
    "PhiCP_CMS",
]

LIST_VAR = {
    "QQ": VARIABLES_QQ,
    "LL":VARIABLES_LL,
    "NuNu":VARIABLES_NuNu,
}

#directory where you want your plots to go
DIR_PLOTS = '/eos/user/s/sgiappic/www/Higgs_CP/ecm240/' 

#labels for the cuts in the plots
LABELS = {
    "selReco": "No additional selection",
    "selReco_100Coll150": "100<M_{collinear}<150 GeV",
    "selReco_100Coll150_115Rec160": "100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV",
    "selReco_100Coll150_115Rec160_2DR": "100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2",
    "selReco_100Coll150_115Rec160_2DR_cos0.6": "100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 80<M_{Z}<100 GeV}",
    
    #cuts for NuNu
    "selReco_100Me": "E_{miss}>100 GeV",
    "selReco_100Me_TauDPhi3": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3",
    "selReco_100Me_TauDPhi3_2DR": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2",
    "selReco_100Me_TauDPhi3_2DR_cos0.4": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.98",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.98, |y_{miss}|<1",

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
LOGY = False

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

    "wzp6_ee_nunuH_Htautau_ecm240",
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

    'sm':"ZH(#tau#tau), SM",
    'sm_lin_quad_cehim_m1':"ZH(#tau#tau), CPV -1",
    'sm_lin_quad_cehim':"ZH(#tau#tau), CPV +1",
    'sm_lin_quad_cehre_m1':"ZH(#tau#tau), CPC -1",
    'sm_lin_quad_cehre_p1':"ZH(#tau#tau), CPC +1",

    "p8_ee_QQH_Htautau_CPeven":"Z(qq)H(#tau#tau), CP even",
    "p8_ee_QQH_Htautau_CPodd":"Z(qq)H(#tau#tau), CP odd",
    "p8_ee_LLH_Htautau_CPeven":"Z(ll)H(#tau#tau), CP even",
    "p8_ee_LLH_Htautau_CPodd":"Z(ll)H(#tau#tau), CP odd",
}

legcolors = {
    'p8_ee_WW_ecm240':ROOT.kSpring+2,
    'p8_ee_Zqq_ecm240':ROOT.kPink+1,
    'p8_ee_ZZ_ecm240':ROOT.kSpring+3,

    'wzp6_ee_LL_ecm240':ROOT.kAzure-4,
    'wzp6_ee_tautau_ecm240':ROOT.kAzure-5,

    "wzp6_ee_nuenueZ_ecm240":ROOT.kAzure-1,

    "wzp6_ee_egamma_eZ_ZLL_ecm240":ROOT.kOrange-4,
    
    "wzp6_ee_gaga_LL_60_ecm240":ROOT.kOrange-9,
    "wzp6_ee_gaga_tautau_60_ecm240":ROOT.kOrange+6,

    "wzp6_ee_tautauH_Htautau_ecm240":ROOT.kViolet+6,
    "wzp6_ee_tautauH_HQQ_ecm240":ROOT.kViolet+5,
    "wzp6_ee_tautauH_Hgg_ecm240":ROOT.kViolet-4,
    "wzp6_ee_tautauH_HVV_ecm240":ROOT.kViolet+1,

    'wzp6_ee_nunuH_Htautau_ecm240':ROOT.kTeal-9,
    "wzp6_ee_nunuH_HQQ_ecm240":ROOT.kGreen-5,
    "wzp6_ee_nunuH_Hgg_ecm240":ROOT.kGreen-8,
    "wzp6_ee_nunuH_HVV_ecm240":ROOT.kGreen-10,

    'wzp6_ee_LLH_Htautau_ecm240':ROOT.kAzure-9,
    "wzp6_ee_LLH_HQQ_ecm240":ROOT.kCyan-5,
    "wzp6_ee_LLH_Hgg_ecm240":ROOT.kCyan-8,
    "wzp6_ee_LLH_HVV_ecm240":ROOT.kCyan-10,

    'wzp6_ee_QQH_Htautau_ecm240':ROOT.kViolet-9,
    "wzp6_ee_QQH_HQQ_ecm240":ROOT.kMagenta-5,
    "wzp6_ee_QQH_Hgg_ecm240":ROOT.kMagenta-8,
    "wzp6_ee_QQH_HVV_ecm240":ROOT.kMagenta-10,

    'sm':ROOT.kViolet-9,
    'sm_lin_quad_cehim_m1':ROOT.kAzure-6,
    'sm_lin_quad_cehim':ROOT.kTeal-7,
    'sm_lin_quad_cehre_m1':ROOT.kTeal+3,
    'sm_lin_quad_cehre_p1':ROOT.kSpring+2,

    "p8_ee_QQH_Htautau_CPeven":ROOT.kAzure-6,
    "p8_ee_QQH_Htautau_CPodd":ROOT.kTeal-7,
    "p8_ee_LLH_Htautau_CPeven":ROOT.kTeal+3,
    "p8_ee_LLH_Htautau_CPodd":ROOT.kSpring+2,

}

#list of signals, then legend and colors to be assigned to them
signals = [
    "sm",
    "sm_lin_quad_cehim_m1",
    "sm_lin_quad_cehim",
    #"sm_lin_quad_cehre_m1",
    #"sm_lin_quad_cehre_p1",
    #"p8_ee_QQH_Htautau_CPeven",
    #"p8_ee_QQH_Htautau_CPodd",
    #"p8_ee_LLH_Htautau_CPeven",
    #"p8_ee_LLH_Htautau_CPodd",
]

for cat in CAT:
    variables = VARIABLES + LIST_VAR[cat] + VARIABLES_CMS

    for sub in SUBDIR:
        directory = DIRECTORY + "ktN-explicit/" + cat + "/" + sub + "/"

        for cut in CUTS:
            for variable in variables:

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

                    dir = DIR_PLOTS + "/" + cat + "/" + sub + "/log/" + cut + "/"
                    make_dir_if_not_exists(DIR_PLOTS)
                    make_dir_if_not_exists(DIR_PLOTS + "/" + cat)
                    make_dir_if_not_exists(DIR_PLOTS + "/" + cat + "/" + sub)
                    make_dir_if_not_exists(DIR_PLOTS + "/" + cat + "/" + sub + "/log/")
                    make_dir_if_not_exists(DIR_PLOTS + "/" + cat + "/" + sub + "/log/" + cut)
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

                    dir = DIR_PLOTS + "/" + cat + "/" + sub + "/lin/" + cut + "/"
                    make_dir_if_not_exists(DIR_PLOTS )
                    make_dir_if_not_exists(DIR_PLOTS + "/" + cat)
                    make_dir_if_not_exists(DIR_PLOTS + "/" + cat + "/" + sub)
                    make_dir_if_not_exists(DIR_PLOTS + "/" + cat + "/" + sub + "/lin/")
                    make_dir_if_not_exists(DIR_PLOTS + "/" + cat + "/" + sub + "/lin/" + cut)
                    make_dir_if_not_exists(dir)

                    canvas.SaveAs(dir + variable + "_" + cat + sub + ".png")
                    canvas.SaveAs(dir + variable + "_" + cat + sub + ".pdf")
