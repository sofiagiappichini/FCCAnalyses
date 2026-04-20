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
DIRECTORY = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/CP/final_250530/ktN-explicit/"

#directory where you want your plots to go
DIR_PLOTS = '/eos/user/s/sgiappic/www/Higgs_CP/ecm240/EFT/' 
#list of cuts you want to plot
CUTS = [
    "selReco",
    #"selReco_3body",
    #"selReco_2body",
    #"selDM",
    #"selDiag",
    #"selOffDiag",
    #"selPi",
    #"selRho",

    #"selReco_ILC",
    #"selDiag_ILC",
    #"selOffDiag_ILC",
    #"selPi_ILC",
    #"selRho_ILC",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100",
    #"selReco_CMS",
    #"selDPhi",

    #"selReco_100Coll150",
    #"selReco_100Coll150_115Rec160",
    #"selReco_100Coll150_115Rec160_2DR",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_oneprong",
  
 ] 
#labels for the cuts in the plots
LABELS = {
    "selReco": "No additional selection",
    "selReco_ILC20chi": "p_{T,miss} (#chi^{2})<20 GeV",
    "selGen": "No additional selection",
    "selReco_ILC":"No additional selection",
    "selDPhi":"KinGen_hh_norm_DPhi<0.5",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100":"Full selection",
    "selDiag":"Both taus decay to pi or rho",
    "selOffDiag":"One tau decays to pi, the other rho",
    "selPi":"Both taus decay to pi",
    "selRho":"Both taus decay to rho",
    "selDiag_ILC":"Both taus decay to pi or rho",
    "selOffDiag_ILC":"One tau decays to pi, the other rho",
    "selPi_ILC":"Both taus decay to pi",
    "selRho_ILC":"Both taus decay to rho",
    "selDM":"Only valid tau DM",
    "selReco_3body":"three body",
    "selReco_2body":"two body",

    "selReco_100Coll150": "Collinear_mass>100 && Collinear_mass<150",
    "selReco_100Coll150_115Rec160": "Collinear_mass>100 && Collinear_mass<150 && Recoil_mass>115 && Recoil_mass<160",
    "selReco_100Coll150_115Rec160_2DR": "Collinear_mass>100 && Collinear_mass<150 && Recoil_mass>115 && Recoil_mass<160 && Tau_DR>2",
    "selReco_100Coll150_115Rec160_2DR_cos0.6": "Collinear_mass>100 && Collinear_mass<150 && Recoil_mass>115 && Recoil_mass<160 && Tau_DR>2 && Tau_cos<(-0.6)",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98": "Collinear_mass>100 && Collinear_mass<150 && Recoil_mass>115 && Recoil_mass<160 && Tau_DR>2 && Tau_cos<(-0.6) && RecoEmiss_costheta<0.98",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100": "Collinear_mass>100 && Collinear_mass<150 && Recoil_mass>115 && Recoil_mass<160 && Tau_DR>2 && Tau_cos<(-0.6) && RecoEmiss_costheta<0.98 && RecoZ_mass>80 && RecoZ_mass<100",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_oneprong": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 80<M_{Z}<100 GeV, one prong}",
    
 }

label = "_QQHH_ratio"
ana_tex        = "e^{+}e^{-} #rightarrow Z H, H #rightarrow #tau_{h}#tau_{h} one prong" #(#pi#pi^{0}#nu)
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
    "sm",
    "sm_lin_quad_cehim_m1",
    "sm_lin_quad_cehim",
    "sm_lin_quad_cehre_m1",
    "sm_lin_quad_cehre",
]

SINGLE = [
    "chb",
    "chwb",
    "chw",
]

slegend = {
    "mg_ee_eetata_pinu_smeft_cehim_m1_ecm240":"CPV -1, mass",
    "mg_ee_eetata_pinu_c_mass_smeft_cehim_m1_ecm240":"CPV -1, no mass",
    "mg_ee_eetata_pinu_ecm240":"SM",

    'noISR_e+e-_noCuts_EWonly':"Z(ee)H(#tau#tau), SM",
    'noISR_e+e-_noCuts_cehim_m1':"Z(ee)H(#tau#tau), CPV -1",
    'noISR_e+e-_noCuts_cehim_p1':"Z(ee)H(#tau#tau), CPV +1",
    'noISR_e+e-_noCuts_cehre_m1':"Z(ee)H(#tau#tau), CPC -1",
    'noISR_e+e-_noCuts_cehre_p1':"Z(ee)H(#tau#tau), CPC +1",
    'noISR':"Z(ee)H(#tau#tau), CPV +1, v.2",
    'taudecay':"Z(ee)H(#tau#tau), CPV +1, with #tau decay",
    'wzp6_ee_eeH_Htautau_ecm240':"Z(ee)H(#tau#tau), SM Whizard",
    "test_output":"new sample cpv",

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

    'sm':"ZH(#tau#tau), SM",
    'sm_lin_quad_cehim_m1':"ZH(#tau#tau), #it{Im}(#bf{O}_{eh}), #it{c}=-1",
    'sm_lin_quad_cehim':"ZH(#tau#tau), #it{Im}(#bf{O}_{eh}), #it{c}=+1",
    'sm_lin_quad_cehre_m1':"ZH(#tau#tau), #it{Re}(#bf{O}_{eh}), #it{c}=-1",
    'sm_lin_quad_cehre':"ZH(#tau#tau), #it{Re}(#bf{O}_{eh}), #it{c}=-1",

    "p8_ee_QQH_Htautau_CPeven":"Z(qq)H(#tau#tau), CP even",
    "p8_ee_QQH_Htautau_CPodd":"Z(qq)H(#tau#tau), CP odd",
    "p8_ee_LLH_Htautau_CPeven":"Z(ll)H(#tau#tau), CP even",
    "p8_ee_LLH_Htautau_CPodd":"Z(ll)H(#tau#tau), CP odd",

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

    "mg_ee_eetata_ecm240":"Z(ee)H(#tau#tau)",
    "mg_ee_eetata_smeft_cehim_m1_ecm240":"Z(ee)H(#tau#tau), CPV -1",
    "mg_ee_eetata_smeft_cehim_p1_ecm240":"Z(ee)H(#tau#tau), CPV +1",

    "mg_ee_eetata_mod1_ecm240":"Z(ee)H(#tau#tau)",                
    "mg_ee_eetata_mod1_smeft_cehim_m1_ecm240":"Z(ee)H(#tau#tau), CPV -1",
    "mg_ee_eetata_mod1_smeft_cehim_m1_ecm240_wMadspin":"Z(ee)H(#tau#tau), CPV -1, MadSpin",
    "mg_ee_eetata_mod1_smeft_cehim_p1_ecm240":"Z(ee)H(#tau#tau), CPV +1",

    "mg_ee_eetata_ecm240_NoTauDecay":"SM",
    "mg_ee_eetata_smeft_cehim_m1_ecm240_NoTauDecay":"CPV",
    "test-sm":"SM",
    "test-cehim-p1":"CPV",
    "test-sm-v2":"SM",
    "test-cehim-p10":"CPV +10",

    "p8_ee_eeH_Htautau_CPeven":"0",
    "p8_ee_eeH_Htautau_CPodd":"90",
    "p8_ee_eeH_Htautau_CPmix":"45",

    "llh-m1-2body":"m1",  
    "llh-m1-4body":"m1",
    "llh-p1-3body":"p1",
    "llh-sm-2body":"sm",
    "llh-sm-4body":"sm",
    "llh-m1-3body":"m1",
    "llh-p1-2body":"p1",
    "llh-p1-4body":"p1",
    "llh-sm-3body":"sm",
}

scolors = {
    "mg_ee_eetata_pinu_smeft_cehim_m1_ecm240":ROOT.kBlack,
    "mg_ee_eetata_pinu_c_mass_smeft_cehim_m1_ecm240":ROOT.kBlue,
    "mg_ee_eetata_pinu_ecm240":ROOT.kRed,

    'noISR_e+e-_noCuts_EWonly':ROOT.kRed-9,
    'noISR_e+e-_noCuts_cehim_m1':ROOT.kCyan-6,
    'noISR_e+e-_noCuts_cehim_p1':ROOT.kBlue-7,
    'noISR_e+e-_noCuts_cehre_m1':ROOT.kGreen-8,
    'noISR_e+e-_noCuts_cehre_p1':ROOT.kGreen-6,
    'noISR':ROOT.kCyan-6,
    'taudecay':ROOT.kMagenta-6,
    'wzp6_ee_eeH_Htautau_ecm240':ROOT.kGray+2,
    "test_output":ROOT.kRed,

    'EWonly_taudecay_2Pi2Nu':ROOT.kRed-9,
    'cehim_m1_taudecay_2Pi2Nu':ROOT.kCyan-6,
    'cehim_p1_taudecay_2Pi2Nu':ROOT.kBlue-7,
    'cehre_m1_taudecay_2Pi2Nu':ROOT.kGreen-8,
    'cehre_p1_taudecay_2Pi2Nu':ROOT.kGreen-6,

    'EWonly_taudecay_PiPi0Nu':ROOT.kRed-9,
    'cehim_m1_taudecay_PiPi0Nu':ROOT.kCyan-6,
    'cehim_p1_taudecay_PiPi0Nu':ROOT.kBlue-7,
    'cehre_m1_taudecay_PiPi0Nu':ROOT.kGreen-8,
    'cehre_p1_taudecay_PiPi0Nu':ROOT.kGreen-6,

    "mg_ee_eetata_ecm240":ROOT.kViolet-9,
    "mg_ee_eetata_smeft_cehim_m1_ecm240":ROOT.kAzure-6,
    "mg_ee_eetata_smeft_cehim_p1_ecm240":ROOT.kTeal-7,

    'sm':ROOT.kViolet-9,
    'sm_lin_quad_cehim_m1':ROOT.kTeal-7,
    'sm_lin_quad_cehim':ROOT.kSpring+2,
    'sm_lin_quad_cehre_m1':ROOT.kAzure-6,
    'sm_lin_quad_cehre':ROOT.kAzure-9, 
    "quad_cehim":ROOT.kTeal-7,

    "p8_ee_QQH_Htautau_CPeven":ROOT.kAzure-6,
    "p8_ee_QQH_Htautau_CPodd":ROOT.kTeal-7,
    "p8_ee_LLH_Htautau_CPeven":ROOT.kTeal+3,
    "p8_ee_LLH_Htautau_CPodd":ROOT.kSpring+2,

    'cehim_m5_taudecay_2Pi2Nu':ROOT.kCyan-6,
    'cehim_p5_taudecay_2Pi2Nu':ROOT.kBlue-7,
    'cehre_m5_taudecay_2Pi2Nu':ROOT.kGreen-8,
    'cehre_p5_taudecay_2Pi2Nu':ROOT.kGreen-6,

    'cehim_m2_taudecay_2Pi2Nu':ROOT.kCyan-6,
    'cehim_p2_taudecay_2Pi2Nu':ROOT.kBlue-7,
    'cehre_m2_taudecay_2Pi2Nu':ROOT.kGreen-8,
    'cehre_p2_taudecay_2Pi2Nu':ROOT.kGreen-6,

    'cehim_m0p1_taudecay_2Pi2Nu':ROOT.kCyan-6,
    'cehim_p0p1_taudecay_2Pi2Nu':ROOT.kBlue-7,
    'cehre_m0p1_taudecay_2Pi2Nu':ROOT.kGreen-8,
    'cehre_p0p1_taudecay_2Pi2Nu':ROOT.kGreen-6,

    'cehim_m10_taudecay_2Pi2Nu':ROOT.kCyan-6,
    'cehim_p10_taudecay_2Pi2Nu':ROOT.kBlue-7,

    "mg_ee_eetata_mod1_ecm240":ROOT.kViolet-9,            
    "mg_ee_eetata_mod1_smeft_cehim_m1_ecm240":ROOT.kAzure-6,
    "mg_ee_eetata_mod1_smeft_cehim_m1_ecm240_wMadspin":ROOT.kRed-4,
    "mg_ee_eetata_mod1_smeft_cehim_p1_ecm240":ROOT.kTeal-7, 

    "mg_ee_eetata_ecm240_NoTauDecay":ROOT.kRed-4,
    "mg_ee_eetata_smeft_cehim_m1_ecm240_NoTauDecay":ROOT.kBlue-4,

    "test-sm":ROOT.kRed-4,
    "test-cehim-p1":ROOT.kBlue-4,
    "test-sm-v2":ROOT.kRed-4,
    "test-cehim-p10":ROOT.kBlue-4,
    
    "p8_ee_eeH_Htautau_CPeven":ROOT.kRed,
    "p8_ee_eeH_Htautau_CPodd":ROOT.kBlue-7,
    "p8_ee_eeH_Htautau_CPmix":ROOT.kMagenta-6,

    "llh-m1-2body":ROOT.kCyan-6,  
    "llh-m1-4body":ROOT.kCyan-6,
    "llh-p1-3body":ROOT.kBlue-7,
    "llh-sm-2body":ROOT.kTeal-7,
    "llh-sm-4body":ROOT.kTeal-7,
    "llh-m1-3body":ROOT.kCyan-6,
    "llh-p1-2body":ROOT.kBlue-7,
    "llh-p1-4body":ROOT.kBlue-7,
    "llh-sm-3body":ROOT.kTeal-7,
}

for op in SINGLE:
    label = f"_{op}_"
    for cut in CUTS:
        #VARIABLES = VARIABLES_GEN + VARIABLES_CPGEN
        #VARIABLES = VARIABLES_RECO + VARIABLES_CP + VARIABLES_CMS #+ VARIABLES_ILC
        VARIABLES = ["PhiCP_CMS",]
        for variable in VARIABLES:

            canvas = ROOT.TCanvas("", "", 800, 800)
            canvas.SetLeftMargin(0.14)
            canvas.SetRightMargin(0.08)
            canvas.GetFrame().SetBorderSize(12)

            pad = ROOT.TPad("", "", 0.0, 0.3, 1.0, 1.0)
            
            pad2 = ROOT.TPad("", "", 0.0, 0.0, 1.0, 0.35)

            pad.Draw()
            pad2.Draw()
            canvas.cd()
            pad.cd()

            nsig = len(signals)

            #legend coordinates and style
            legsize = 0.04*nsig
            leg = ROOT.TLegend(0.16, 0.78 - legsize, 0.45, 0.74)
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
            fin_ll = f"{DIRECTORY}/LL/HH/sm_{cut}_histo.root"
            fin_qq = f"{DIRECTORY}/QQ/HH/sm_{cut}_histo.root"
            tf_ll = ROOT.TFile.Open(fin_ll, 'READ')
            h = tf_ll.Get(variable)
            hh = copy.deepcopy(h)
            hh.SetDirectory(0)
            tf_qq = ROOT.TFile.Open(fin_qq, 'READ')
            h3 = tf_qq.Get(variable)
            hh.Add(h3)
            histos.append(hh)
            colors.append(scolors["sm"])
            leg.AddEntry(histos[-1], "sm", "l")

            fin_ll = f"{DIRECTORY}/LL/HH/sm_lin_quad_{op}til_{cut}_histo.root"
            fin_qq = f"{DIRECTORY}/QQ/HH/sm_lin_quad_{op}til_{cut}_histo.root"
            tf_ll = ROOT.TFile.Open(fin_ll, 'READ')
            h = tf_ll.Get(variable)
            hh = copy.deepcopy(h)
            hh.SetDirectory(0)
            tf_qq = ROOT.TFile.Open(fin_qq, 'READ')
            h3 = tf_qq.Get(variable)
            hh.Add(h3)
            histos.append(hh)
            colors.append(scolors["sm_lin_quad_cehre"])
            leg.AddEntry(histos[-1], f"{op}til", "l")

            fin_ll = f"{DIRECTORY}/LL/HH/sm_lin_quad_{op}_{cut}_histo.root"
            fin_qq = f"{DIRECTORY}/QQ/HH/sm_lin_quad_{op}_{cut}_histo.root"
            tf_ll = ROOT.TFile.Open(fin_ll, 'READ')
            h = tf_ll.Get(variable)
            hh = copy.deepcopy(h)
            hh.SetDirectory(0)
            tf_qq = ROOT.TFile.Open(fin_qq, 'READ')
            h3 = tf_qq.Get(variable)
            hh.Add(h3)
            histos.append(hh)
            colors.append(scolors["sm_lin_quad_cehim"])
            leg.AddEntry(histos[-1], f"{op}", "l")
                
                
            '''

            for s in signals:
                fin_ll = f"{DIRECTORY}/QQ/HH/{s}_{cut}_histo.root"
                tf_ll = ROOT.TFile.Open(fin_ll, 'READ')
                h = tf_ll.Get(variable)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
                histos.append(hh)
                colors.append(scolors[s])
                leg.AddEntry(histos[-1], slegend[s], "l")'''
            
            #for s in signals:
            #    fin = f"{DIRECTORY}/{s}_{cut}_histo.root"
            #    with ROOT.TFile(fin) as tf:
            #        h = tf.Get(variable) #s + "_" + variable
            #        hh = h.Clone()
            #        hh.SetDirectory(0)
            #    histos.append(hh)
            #    colors.append(ROOT.kBlue)
            #    leg.AddEntry(histos[-1], "no jet tagger", "l")

            nsig = len(histos)

            # add the signal histograms
            for i in range(nsig):
                h = histos[i]
                max = 0 
                if h.GetMaximum() > max :
                    max = h.GetMaximum() 
            for i in range(nsig):
                h = histos[i]
                h.SetLineWidth(3)
                h.SetLineColor(colors[i])
                #h.Rebin(2)
                if i == 0:
                    h.Draw("HIST")
                    h.GetYaxis().SetTitle("Events")
                    h.GetYaxis().SetTitleSize(0.05)
                    h.GetYaxis().SetLabelSize(0.048)
                    h.GetYaxis().SetTitleOffset(1.2)
                    h.GetXaxis().SetTitle(histos[0].GetXaxis().GetTitle())
                    if variable == "PhiCP_CMS":
                        h.GetXaxis().SetTitle("#phi_{CP} (rad)")
                    #h.GetXaxis().SetTitleOffset(1.2)
                    #if h.Integral()>0:
                    #    h.Scale(1./(h.Integral()))
                    h.GetYaxis().SetRangeUser(420, max*2)
                else: 
                    #if h.Integral()>0:
                    #    h.Scale(1./(h.Integral()))
                    #    h.Scale(0.5)
                    h.Draw("HIST SAME")
            
            

            #leg.Draw()

            pad.SetLeftMargin(0.14)
            pad.SetRightMargin(0.08)
            pad.GetFrame().SetBorderSize(12)
            pad.SetBottomMargin(0)
            pad.SetTopMargin(0.148)
            pad.SetTicks(1, 1)

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

            dummy.GetYaxis().SetTitle("Ratio with SM")
            dummy.GetYaxis().SetTitleSize(0.093)
            dummy.GetYaxis().CenterTitle()
            #adjust the range for the ratio here
            dummy.GetYaxis().SetRangeUser(0.95,1.05)
            dummy.GetYaxis().SetLabelSize(0.095)
            dummy.GetYaxis().SetNdivisions(5)
            dummy.GetYaxis().SetTitleOffset(0.6)

            dummy.GetXaxis().SetTitle(histos[0].GetXaxis().GetTitle())
            dummy.GetXaxis().SetTitleSize(0.1)
            dummy.GetXaxis().SetLabelSize(0.095)
            dummy.GetXaxis().SetTitleOffset(1.1)
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
            pad2.SetTopMargin(0.145)
            pad2.SetBottomMargin(0.28)
            pad2.SetFillColor(0)
            pad2.SetFillStyle(4000)
            #pad2.SetLogy()

            # Draw leftText on the main pad before saving
            canvas.cd()
            leg.Draw()
            extralab = LABELS[cut]

            #labels around the plot
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
            latex.DrawLatex(0.18, 0.76, text)

            if 'ee' in collider:
                leftText = 'FCCAnalyses: FCC-ee Simulation (Delphes)'
                latex.SetTextAlign(31)
                latex.SetTextSize(0.03)
                latex.DrawLatex(0.92, 0.92, '#it{' + leftText + '}')

            canvas.RedrawAxis()
            canvas.Modified()
            canvas.Update()

            dir = DIR_PLOTS + "/"
            make_dir_if_not_exists(dir)

            if (LOGY == True):
                canvas.SaveAs(dir + "log/" + variable + cut + ".png")
                canvas.SaveAs(dir + "log/" + variable + cut + ".pdf")
            else:
                canvas.SaveAs(dir + variable + label + ".png")
                canvas.SaveAs(dir + variable + label + ".pdf")