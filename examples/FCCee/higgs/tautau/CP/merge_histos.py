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
DIRECTORY = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/CP/final_250530/ktN-explicit/"
CAT = [
    "QQ",
    "LL",
]

SUB = [
    #"LL",
    #"LH",
    "HH",
]

#set which samples to merge
eft = True
bkg = False
pythia = False

#list of cuts you want to plot
CUT = [
    "selReco",
    "selReco_100Coll150",
    "selReco_100Coll150_115Rec160",
    "selReco_100Coll150_115Rec160_2DR",
    "selReco_100Coll150_115Rec160_2DR_cos0.6",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100",
]

CUT_LLLL = [
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_20EM",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_20EM_HE110",
]

CUT_LLHH = [
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_oneprong"
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_notoneprong"
]

CUT_QQHH = [
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_jets",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_jets_10EM",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_jets_10EM_40Zp55",
    "selReco_100Coll150_115Rec160_2DR_0.98cos0.6_misscos0.98_80Z100_jets_10EM_40Zp55",
    "selReco_100Coll150_115Rec160_2DR_0.98cos0.6_misscos0.98_80Z100_jets_10EM_40Zp55_oneprong", 
    #"selReco_100Coll150_115Rec160_2DR_0.98cos0.6_misscos0.98_80Z100_jets_10EM_40Zp55_notoneprong", 
]

CUT_QQLH = [
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_jets",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_jets_10EM",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_jets_10EM_40Zp55",
]

CUT_QQLL = [
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_jets",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_jets_10EM",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_jets_10EM_40Zp55",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_jets_10EM_40Zp55_HE95"
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

            "GenPhi_CP",
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
    #"BDT_score",
    #"Collinear_mass_3d",
    #"KinILC_H_mass",
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

CEHIM_M1 = ["mg_ee_fftata_ceHIm_m1_ecm240",]
CEHRE_M1 = ["mg_ee_fftata_ceHRe_m1_ecm240",]
SM = ["mg_ee_fftata_sm_ecm240",]
CEHIM_P1 = ["mg_ee_fftata_ceHIm_p1_ecm240",]
CEHRE_P1 = ["mg_ee_fftata_ceHRe_p1_ecm240",]
MIXED = ["mg_ee_fftata_ceHRe__ceHIm_p1_p1_ecm240",]

legend_sig = {
    1:"sm",
    2:"sm_lin_quad_cehim_m1",
    3:"sm_lin_quad_cehim",
    4:"sm_lin_quad_cehre_m1",
    5:"sm_lin_quad_cehre",
    6:"sm_lin_quad_mixed_cehim_cehre",
}

list_sig = {
    1:SM,
    2:CEHIM_M1,
    3:CEHIM_P1,
    4:CEHRE_M1,
    5:CEHRE_P1,
    6:MIXED,
}

################ signal #################
if eft:
    for cat in CAT:
        for sub in SUB:
            CUTS = ""
            if "LL" in cat:
                if "LL" in sub:
                    CUTS = CUT + CUT_LLLL
                elif "HH" in sub:
                    CUTS = CUT + CUT_LLHH
                else:
                    CUTS = CUT
            else:
                if "HH" in sub:
                    CUTS = CUT +  CUT_QQHH
                elif "LH" in sub:
                    CUTS = CUT + CUT_QQLH
                else:
                    CUTS = CUT + CUT_QQLL
            
            for cut in CUTS:

                variables = VARIABLES_RECO + VARIABLES_CP + VARIABLES_CMS

                dir = f"{DIRECTORY}/{cat}/{sub}/"
                #print(dir)

                for num in range(1,7):
                    outFile = ROOT.TFile.Open(dir + legend_sig[num] + "_" + cut + "_histo.root", "RECREATE")
                    for var in variables:
                        #loop to merge different sources into one histograms 
                        j = 0
                        hh = None
                        for b in list_sig[num]:
                            #print(b, var)
                            file = f"{dir}{b}_{cut}_histo.root"
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
                        #hist_name = legend_sig[num]
                        #hh.SetName(hist_name + "_" + var)
                        #write the histogram in the file   
                        outFile.cd()
                        hh.Write()
                        #print(f"{var}, {legend_sig[num]}")
                    outFile.Close()

                ## now we need to "isolate" the quadratic contribution from the eft only from the sm and lin+quad
                sm_file = ROOT.TFile.Open(dir + legend_sig[1] + "_" + cut + "_histo.root", "READ")
                cehim_m1_file = ROOT.TFile.Open(dir + legend_sig[2] + "_" + cut + "_histo.root", "READ")
                cehim_p1_file = ROOT.TFile.Open(dir + legend_sig[3] + "_" + cut + "_histo.root", "READ")
                quad_im_file = ROOT.TFile.Open(dir + "quad_cehim_" + cut + "_histo.root", "RECREATE")
                cehre_m1_file = ROOT.TFile.Open(dir + legend_sig[4] + "_" + cut + "_histo.root", "READ")
                cehre_p1_file = ROOT.TFile.Open(dir + legend_sig[5] + "_" + cut + "_histo.root", "READ")
                quad_re_file = ROOT.TFile.Open(dir + "quad_cehre_" + cut + "_histo.root", "RECREATE")

                for var in variables:
                    #sm_histo = sm_file.Get(legend_sig[1] + "_" + var)
                    #cehim_m1_histo = cehim_m1_file.Get(legend_sig[2] + "_" + var)
                    #cehim_p1_histo = cehim_p1_file.Get(legend_sig[3] + "_" + var)

                    sm_histo = sm_file.Get(var)
                    cehim_m1_histo = cehim_m1_file.Get(var)
                    cehim_p1_histo = cehim_p1_file.Get(var)

                    # quad = cpv(+1) + cpv(-1) - 2*sm, in brackets the WC
                    quad_im_histo = copy.deepcopy(cehim_p1_histo)
                    quad_im_histo.SetDirectory(0)

                    quad_im_histo.Add(cehim_m1_histo)
                    quad_im_histo.Add(sm_histo, -2.)
                    #quad_histo.SetName("quad_cehim_" + var)

                    quad_im_file.cd()
                    quad_im_histo.Write()

                    sm_histo = sm_file.Get(var)
                    cehre_m1_histo = cehre_m1_file.Get(var)
                    cehre_p1_histo = cehre_p1_file.Get(var)

                    # quad = cpv(+1) + cpv(-1) - 2*sm, in brackets the WC
                    quad_re_histo = copy.deepcopy(cehre_p1_histo)
                    quad_re_histo.SetDirectory(0)

                    quad_re_histo.Add(cehre_m1_histo)
                    quad_re_histo.Add(sm_histo, -2.)
                    #quad_histo.SetName("quad_cehim_" + var)

                    print("var {} to file {}\n".format(var, quad_re_file))

                    quad_re_file.cd()
                    quad_re_histo.Write()

                quad_re_file.Close()

                quad_im_file.Close()


############### backgrounds ##################

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
    'wzp6_ee_bbH_HWW_ecm240',
    'wzp6_ee_bbH_HZZ_ecm240',

    'wzp6_ee_ccH_HWW_ecm240',
    'wzp6_ee_ccH_HZZ_ecm240',

    'wzp6_ee_ssH_HWW_ecm240',
    'wzp6_ee_ssH_HZZ_ecm240',
    
    'wzp6_ee_qqH_HWW_ecm240',
    'wzp6_ee_qqH_HZZ_ecm240',
]
backgrounds_16 = [
    'wzp6_ee_bbH_Hgg_ecm240',
    'wzp6_ee_ccH_Hgg_ecm240',
    'wzp6_ee_ssH_Hgg_ecm240',
    'wzp6_ee_qqH_Hgg_ecm240',
]
backgrounds_17 = [
    'wzp6_ee_eeH_Hgg_ecm240',
    'wzp6_ee_mumuH_Hgg_ecm240',
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
    15:"wzp6_ee_QQH_HVV_ecm240",
    16:"wzp6_ee_QQH_Hgg_ecm240",

    17:"wzp6_ee_LLH_Hgg_ecm240",
    
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
}

if bkg:
    for cat in CAT:
        for sub in SUB:
            CUTS = ""
            if "LL" in cat:
                if "LL" in sub:
                    CUTS = CUT + CUT_LLLL
                elif "HH" in sub:
                    CUTS = CUT + CUT_LLHH
                else:
                    CUTS = CUT
            else:
                if "HH" in sub:
                    CUTS = CUT +  CUT_QQHH
                elif "LH" in sub:
                    CUTS = CUT + CUT_QQLH
                else:
                    CUTS = CUT + CUT_QQLL
            for cut in CUTS:

                variables = VARIABLES_RECO + VARIABLES_CP + VARIABLES_CMS

                directory = f"{DIRECTORY}/{cat}/{sub}/"
            
                for num in range(1,18):
                    output = f"{directory}{legend[num]}_{cut}_histo.root"
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
                            #change the name accordingly to the new histogram for EFT combine
                            #hist_name = legend[num]
                            #hh.SetName(hist_name + "_" + var)
                            outFile.cd()
                            hh.Write()
                        #print(f"{cat}, {sub}, {cut}, {num}, {var}")
                        
                    outFile.Close()
                    if check==False: #if nothing was written i don't want the file saved at all
                        os.remove(output) 

################### pythia signals ###################

ll = [
    "p8_ee_eeH_Htautau",
    "p8_ee_mumuH_Htautau",
]

qq = [
    "p8_ee_bbH_Htautau",
    "p8_ee_ccH_Htautau",
    "p8_ee_ssH_Htautau",
    "p8_ee_qqH_Htautau",
]

samples_dict = {
    "ll": ll,
    "qq": qq,
}

legend_p8 = {
    "ll":"p8_ee_LLH_Htautau",
    "qq":"p8_ee_QQH_Htautau",
}

if pythia:
    for cat in CAT:
        for sub in SUB:
            CUTS = ""
            if "LL" in cat:
                if "LL" in sub:
                    CUTS = CUT + CUT_LLLL
                elif "HH" in sub:
                    CUTS = CUT + CUT_LLHH
                else:
                    CUTS = CUT
            else:
                if "HH" in sub:
                    CUTS = CUT +  CUT_QQHH
                elif "LH" in sub:
                    CUTS = CUT + CUT_QQLH
                else:
                    CUTS = CUT + CUT_QQLL
            for cut in CUTS:

                variables = VARIABLES_RECO + VARIABLES_CP + VARIABLES_CMS

                directory = f"{DIRECTORY}/{cat}/{sub}/"
            
                for dir in samples_dict:
                    for cp in ["even", "odd", "mix"]:
                        output = f"{directory}{legend_p8[dir]}_CP{cp}_{cut}_histo.root"
                        outFile = ROOT.TFile.Open(output, "RECREATE")
                        check = False
                        for var in variables:
                            #loop to merge different sources into one histograms for easier plotting
                            j = 0
                            hh = None
                            for b in samples_dict[dir]:
                                #print(var)
                                file = f"{directory}{b}_CP{cp}_{cut}_histo.root"
                                #print(file)
                                if file_exists(file):
                                    check = True
                                    #print("check")
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
                                #change the name accordingly to the new histogram for EFT combine
                                #hist_name = legend_p8[dir]
                                #hh.SetName(hist_name + "_" + var)
                                outFile.cd()
                                hh.Write()
                            #print(f"{cat}, {sub}, {cut}, {var}")
                            
                        outFile.Close()
                        if check==False: #if nothing was written i don't want the file saved at all
                            os.remove(output)
                        