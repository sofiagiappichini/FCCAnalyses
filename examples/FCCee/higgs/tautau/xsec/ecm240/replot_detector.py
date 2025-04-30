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
directory = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/final/"
TAG = [
    "R5-explicit",
    "R5-tag",
    "ktN-explicit",
    "ktN-tag",
]


#list of cuts you want to plot
CUTS = [
    "selReco",
    #"selReco_100Coll150",
    #"selReco_100Coll150_115Rec160",
    #"selReco_100Coll150_115Rec160_2DR",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_4Emiss",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_4Emiss", 
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_4Emiss_Zp54",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.96_80Z100_4Emiss_Zp54",
]

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
    "Muon_p_res_0_20",
    "Muon_p_res_20_40",
    "Muon_p_res_40_60",
    "Muon_p_res_60_higher", 
    "Muon_p_res_total", 


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
]

#directory where you want your plots to go
DIR_PLOTS = '/web/awiedl/public_html/detector/mumu/' 

#labels for the cuts in the plots
LABELS = {
    "selReco": "No additional selection",
    "selReco_100Coll150": "100<M_{collinear}<150 GeV",
    "selReco_100Coll150_115Rec160": "100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV",
    "selReco_100Coll150_115Rec160_10Me": "100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV",

    "selReco_100Coll150_115Rec160_2DR": "100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2",
    "selReco_100Coll150_115Rec160_2DR_cos0.6": "100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_10ME": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>10 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_QTAU0.5": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_QTAU0.5_10ME": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>10 GeV}",

    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_4Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>4 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_4Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 80<M_{Z}<100 GeV, E_{miss}>4 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_4Emiss_Zp54": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 80<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<54 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.96_80Z100_4Emiss_Zp54": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.96, 80<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<54 GeV}",
    
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_84Z100_4Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 84<M_{Z}<100 GeV, E_{miss}>4 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_84Z100_4Emiss_Zp54": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 84<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<54 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.88_84Z100_4Emiss_Zp54": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.88, 84<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<54 GeV}",
    
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_40Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>40 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_40Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 80<M_{Z}<100 GeV, E_{miss}>40 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_40Emiss_Zp54": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 80<M_{Z}<100 GeV, E_{miss}>40 GeV, p_{Z}<54 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.9_80Z100_40Emiss_Zp54": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.9, 80<M_{Z}<100 GeV, E_{miss}>40 GeV, p_{Z}<54 GeV}",

    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_8Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>4 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_8Emiss_Zp52": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<52 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.86_70Z100_8Emiss_Zp52": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.86, 70<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<52 GeV}",

    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_8Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 75<M_{Z}<100 GeV, E_{miss}>4 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_8Emiss_Zp52": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 75<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<52 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.86_75Z100_8Emiss_Zp52": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.86, 75<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<52 GeV}",
    
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_36Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>36 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_36Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 75<M_{Z}<100 GeV, E_{miss}>36 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_36Emiss_Zp52": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 75<M_{Z}<100 GeV, E_{miss}>36 GeV, p_{Z}<52 GeV}",

    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_52Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>52 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_52Emiss_Zp52": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 70<M_{Z}<100 GeV, E_{miss}>52 GeV, p_{Z}<52 GeV}",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.92_70Z100_52Emiss_Zp52": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.92, 70<M_{Z}<100 GeV, E_{miss}>52 GeV, p_{Z}<52 GeV}",

    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_86Z100_4Emiss": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 86<M_{Z}<100 GeV, E_{miss}>4 GeV",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_86Z100_4Emiss_Zp54": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.98, 86<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<54 GeV",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.96_86Z100_4Emiss_Zp54": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6,}{|cos#theta_{miss}|<0.96, 86<M_{Z}<100 GeV, E_{miss}>4 GeV, p_{Z}<54 GeV",

    #cuts for LL
    "selReco_100Coll150_115Rec160_10Me_70Z100": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{70<M_{Z}<110 GeV}",
    "selReco_100Coll150_115Rec160_10Me_70Z100_2DR": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{70<M_{Z}<110 GeV, #Delta R_{#tau}>2}",
    "selReco_100Coll150_115Rec160_10Me_70Z100_2DR_cos0.6": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{70<M_{Z}<110 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6}",
    "selReco_100Coll150_115Rec160_10Me_70Z100_2DR_cos0.6_misscos0.98": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{70<M_{Z}<110 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6, |cos#theta_{miss}|<0.98}",

    #cuts for QQ
    "selReco_100Coll150_115Rec160_10Me_80Z95": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{80<M_{Z}<95 GeV}",
    "selReco_100Coll150_115Rec160_10Me_80Z95_2DR": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{80<M_{Z}<95 GeV, #Delta R_{#tau}>2}",
    "selReco_100Coll150_115Rec160_10Me_80Z95_2DR_cos0.6": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{80<M_{Z}<95 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6}",
    "selReco_100Coll150_115Rec160_10Me_80Z95_2DR_cos0.6_misscos0.98": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{80<M_{Z}<95 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6, |cos#theta_{miss}|<0.98}",
    
    "selReco_0.5BDT":"100<M_{collinear}<150 GeV, BDT score>0.5",
    "selReco_0.6BDT":"100<M_{collinear}<150 GeV, BDT score>0.6",
    "selReco_0.7BDT":"100<M_{collinear}<150 GeV, BDT score>0.7",

    #cuts for NuNu
    "selReco_100Me": "E_{miss}>100 GeV",
    "selReco_100Me_TauDPhi3": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3",
    "selReco_100Me_TauDPhi3_2DR": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2",
    "selReco_100Me_TauDPhi3_2DR_cos0.4": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.98",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.98, |y_{miss}|<1",

    "selReco_112Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1": "E_{miss}>112 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.98, |y_{miss}|<1",
    "selReco_112Me_TauDPhi3_2DR_cos0.4_misscos0.88_missy1": "E_{miss}>112 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.88, |y_{miss}|<1",
     
    "selReco_140Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1": "E_{miss}>112 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.98, |y_{miss}|<1",
    "selReco_140Me_TauDPhi3_2DR_cos0.4_misscos0.94_missy1": "E_{miss}>112 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.94, |y_{miss}|<1",

    "selReco_152Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1": "E_{miss}>112 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.98, |y_{miss}|<1",
    "selReco_152Me_TauDPhi3_2DR_cos0.4_misscos0.92_missy1": "E_{miss}>112 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.92, |y_{miss}|<1",

    #"selReco_0.5BDT":"E_{miss}>100 GeV, BDT score>0.5",
    #"selReco_0.6BDT":"E_{miss}>100 GeV, BDT score>0.6",
    #"selReco_0.7BDT":"E_{miss}>100 GeV, BDT score>0.7",

 }

ana_tex_cat = "e^{+}e^{-} #rightarrow Z H, Z #rightarrow #nu #nu, H #rightarrow #mu #mu "

energy         = 240
collider       = 'FCC-ee'
intLumi        = 10.8 #ab-1
LOGY = True

#list of backgorunds, then legend and colors to be assigned to them
backgrounds_all = [
]

legend = {
    'IDEA_events_050238459':'IDEA',
    'CMS_Phase2_events_050238459':'CMS Phase2',
    'CMS_Phase1_events_050238459':'CMS Phase1',
}

legcolors = {
    'IDEA_events_050238459':ROOT.kGreen,
    'CMS_Phase2_events_050238459':ROOT.kCyan,
    'CMS_Phase1_events_050238459':ROOT.kBlue,
}

#list of signals, then legend and colors to be assigned to them
signals = [
    'IDEA_events_050238459',
    'CMS_Phase2_events_050238459',
    'CMS_Phase1_events_050238459',
]

for cut in CUTS:
    for variable in VARIABLES:

        print(variable, cut, directory)

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
            #print(fin)
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

        text = '#bf{#it{' + ana_tex_cat + '}}'
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

            dir = DIR_PLOTS
            make_dir_if_not_exists(dir)

            canvas.SaveAs(dir + variable + ".png")
            canvas.SaveAs(dir + variable + ".pdf")
        else:
            canvas.SetTicks(1, 1)
            canvas.SetLeftMargin(0.14)
            canvas.SetRightMargin(0.08)
            canvas.GetFrame().SetBorderSize(12)

            canvas.RedrawAxis()
            canvas.Modified()
            canvas.Update()

            dir = DIR_PLOTS
            make_dir_if_not_exists(dir)

            canvas.SaveAs(dir + variable + ".png")
            canvas.SaveAs(dir + variable + ".pdf")