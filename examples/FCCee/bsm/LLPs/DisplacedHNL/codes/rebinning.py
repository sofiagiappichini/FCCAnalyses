# from https://github.com/mpresill/PlotsConfigurations/blob/matteo/Configurations/VBS_ZV/scripts/rebinning.py#L23-L66
# relevant lines for rebinning only: 23-66 
# https://root.cern/doc/master/classTH1.html#a9eef6f499230b88582648892e5e4e2ce on rebin 
# requires python3 from key4hep stack sourcing, not cmsenv

import os
import ROOT
import shutil
from matplotlib import pyplot as plt
import pandas as pd
import array
import sys
import os.path
import ntpath
import importlib
import copy
import re
import logging

def sorted_dict_values(dic: dict) -> list:
    ''''
    Sort values in the dictionary.
    '''
    keys = sorted(dic)
    return [dic[key] for key in keys]

def make_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory created successfully.")
    else:
        print(f"Directory already exists.")

ana_tex        = "e^{+}e^{-} #rightarrow N_{1,2} #nu, N_{1,2} #rightarrow ll#nu"
energy         = 91
collider       = 'FCC-ee'
intLumi        = 204 #ab-1

DIRECTORY = '/eos/user/s/sgiappic/2HNL_ana/final_final/' 

CUTS = [
    "selReco_gen_notracks_2eh_M80_10MET_0cos_45ME_e35_10gev_DF",
 ] # cut to rebin

VARIABLE = "Reco_DR" # variable to rebin

FILES = [
    "p8_ee_Zee_ecm91",
    "p8_ee_Zmumu_ecm91",
    "p8_ee_Ztautau_ecm91",
    "p8_ee_Zbb_ecm91",
    "p8_ee_Zcc_ecm91",
    "p8_ee_Zud_ecm91",
    "p8_ee_Zss_ecm91",
    "eenunu",
    "mumununu",
    "tatanunu",
    "llnunu",
    
    "HNL_1.33e-7_10gev",
    "HNL_1.33e-7_20gev",
    "HNL_1.33e-7_30gev",
    "HNL_1.33e-7_40gev",
    "HNL_1.33e-7_50gev",
    "HNL_1.33e-7_60gev",
    "HNL_1.33e-7_70gev",
    "HNL_1.33e-7_80gev",

    "HNL_2.78e-8_10gev",
    "HNL_2.78e-8_20gev",
    "HNL_2.78e-8_30gev",
    "HNL_2.78e-8_40gev",
    "HNL_2.78e-8_50gev",
    "HNL_2.78e-8_60gev",
    "HNL_2.78e-8_70gev",
    "HNL_2.78e-8_80gev",

    "HNL_6.05e-9_10gev",
    "HNL_6.05e-9_20gev",
    "HNL_6.05e-9_30gev",
    "HNL_6.05e-9_40gev",
    "HNL_6.05e-9_50gev",
    "HNL_6.05e-9_60gev",
    "HNL_6.05e-9_70gev",
    "HNL_6.05e-9_80gev",

    "HNL_1.33e-9_10gev",
    "HNL_1.33e-9_20gev",
    "HNL_1.33e-9_30gev",
    "HNL_1.33e-9_40gev",
    "HNL_1.33e-9_50gev",
    "HNL_1.33e-9_60gev",
    "HNL_1.33e-9_70gev",
    "HNL_1.33e-9_80gev",

    "HNL_2.90e-10_10gev",
    "HNL_2.90e-10_20gev",
    "HNL_2.90e-10_30gev",
    "HNL_2.90e-10_40gev",
    "HNL_2.90e-10_50gev",
    "HNL_2.90e-10_60gev",
    "HNL_2.90e-10_70gev",
    "HNL_2.90e-10_80gev",

    "HNL_6.34e-11_10gev",
    "HNL_6.34e-11_20gev",
    "HNL_6.34e-11_30gev",
    "HNL_6.34e-11_40gev",
    "HNL_6.34e-11_50gev",
    "HNL_6.34e-11_60gev",
    "HNL_6.34e-11_70gev",
    "HNL_6.34e-11_80gev",

    "HNL_1.33e-11_10gev",
    "HNL_1.33e-11_20gev",
    "HNL_1.33e-11_30gev",
    "HNL_1.33e-11_40gev",
    "HNL_1.33e-11_50gev",
    "HNL_1.33e-11_60gev",
    "HNL_1.33e-11_70gev",
    "HNL_1.33e-11_80gev",

    

    "HNL_4e-8_10gev",
    "HNL_4e-8_20gev",
    "HNL_4e-8_30gev",
    "HNL_4e-8_40gev",
    "HNL_4e-8_50gev",
    "HNL_4e-8_60gev",
    "HNL_4e-8_70gev",
    "HNL_4e-8_80gev",

    "HNL_8.35e-9_10gev",
    "HNL_8.35e-9_20gev",
    "HNL_8.35e-9_30gev",
    "HNL_8.35e-9_40gev",
    "HNL_8.35e-9_50gev",
    "HNL_8.35e-9_60gev",
    "HNL_8.35e-9_70gev",
    "HNL_8.35e-9_80gev",

    "HNL_1.81e-9_10gev",
    "HNL_1.81e-9_20gev",
    "HNL_1.81e-9_30gev",
    "HNL_1.81e-9_40gev",
    "HNL_1.81e-9_50gev",
    "HNL_1.81e-9_60gev",
    "HNL_1.81e-9_70gev",
    "HNL_1.81e-9_80gev",

    "HNL_4e-10_10gev",
    "HNL_4e-10_20gev",
    "HNL_4e-10_30gev",
    "HNL_4e-10_40gev",
    "HNL_4e-10_50gev",
    "HNL_4e-10_60gev",
    "HNL_4e-10_70gev",
    "HNL_4e-10_80gev",

    "HNL_8.69e-11_10gev",
    "HNL_8.69e-11_20gev",
    "HNL_8.69e-11_30gev",
    "HNL_8.69e-11_40gev",
    "HNL_8.69e-11_50gev",
    "HNL_8.69e-11_60gev",
    "HNL_8.69e-11_70gev",
    "HNL_8.69e-11_80gev",

    "HNL_1.90e-11_10gev",
    "HNL_1.90e-11_20gev",
    "HNL_1.90e-11_30gev",
    "HNL_1.90e-11_40gev",
    "HNL_1.90e-11_50gev",
    "HNL_1.90e-11_60gev",
    "HNL_1.90e-11_70gev",
    "HNL_1.90e-11_80gev",

    "HNL_4e-12_10gev",
    "HNL_4e-12_20gev",
    "HNL_4e-12_30gev",
    "HNL_4e-12_40gev",
    "HNL_4e-12_50gev",
    "HNL_4e-12_60gev",
    "HNL_4e-12_70gev",
    "HNL_4e-12_80gev",

    

    "HNL_2.86e-8_10gev",
    "HNL_2.86e-8_20gev",
    "HNL_2.86e-8_30gev",
    "HNL_2.86e-8_40gev",
    "HNL_2.86e-8_50gev",
    "HNL_2.86e-8_60gev",
    "HNL_2.86e-8_70gev",
    "HNL_2.86e-8_80gev",

    "HNL_5.97e-9_10gev",
    "HNL_5.97e-9_20gev",
    "HNL_5.97e-9_30gev",
    "HNL_5.97e-9_40gev",
    "HNL_5.97e-9_50gev",
    "HNL_5.97e-9_60gev",
    "HNL_5.97e-9_70gev",
    "HNL_5.97e-9_80gev",

    "HNL_1.30e-9_10gev",
    "HNL_1.30e-9_20gev",
    "HNL_1.30e-9_30gev",
    "HNL_1.30e-9_40gev",
    "HNL_1.30e-9_50gev",
    "HNL_1.30e-9_60gev",
    "HNL_1.30e-9_70gev",
    "HNL_1.30e-9_80gev",

    "HNL_2.86e-10_10gev",
    "HNL_2.86e-10_20gev",
    "HNL_2.86e-10_30gev",
    "HNL_2.86e-10_40gev",
    "HNL_2.86e-10_50gev",
    "HNL_2.86e-10_60gev",
    "HNL_2.86e-10_70gev",
    "HNL_2.86e-10_80gev",

    "HNL_6.20e-11_10gev",
    "HNL_6.20e-11_20gev",
    "HNL_6.20e-11_30gev",
    "HNL_6.20e-11_40gev",
    "HNL_6.20e-11_50gev",
    "HNL_6.20e-11_60gev",
    "HNL_6.20e-11_70gev",
    "HNL_6.20e-11_80gev",

    "HNL_1.36e-11_10gev",
    "HNL_1.36e-11_20gev",
    "HNL_1.36e-11_30gev",
    "HNL_1.36e-11_40gev",
    "HNL_1.36e-11_50gev",
    "HNL_1.36e-11_60gev",
    "HNL_1.36e-11_70gev",
    "HNL_1.36e-11_80gev",

    "HNL_2.86e-12_10gev",
    "HNL_2.86e-12_20gev",
    "HNL_2.86e-12_30gev",
    "HNL_2.86e-12_40gev",
    "HNL_2.86e-12_50gev",
    "HNL_2.86e-12_60gev",
    "HNL_2.86e-12_70gev",
    "HNL_2.86e-12_80gev",

    ##inverted

    "HNL_5e-8_10gev",
    "HNL_5e-8_20gev",
    "HNL_5e-8_30gev",
    "HNL_5e-8_40gev",
    "HNL_5e-8_50gev",
    "HNL_5e-8_60gev",
    "HNL_5e-8_70gev",
    "HNL_5e-8_80gev",

    "HNL_1.04e-8_10gev",
    "HNL_1.04e-8_20gev",
    "HNL_1.04e-8_30gev",
    "HNL_1.04e-8_40gev",
    "HNL_1.04e-8_50gev",
    "HNL_1.04e-8_60gev",
    "HNL_1.04e-8_70gev",
    "HNL_1.04e-8_80gev",

    "HNL_2.27e-9_10gev",
    "HNL_2.27e-9_20gev",
    "HNL_2.27e-9_30gev",
    "HNL_2.27e-9_40gev",
    "HNL_2.27e-9_50gev",
    "HNL_2.27e-9_60gev",
    "HNL_2.27e-9_70gev",
    "HNL_2.27e-9_80gev",

    "HNL_5e-10_10gev",
    "HNL_5e-10_20gev",
    "HNL_5e-10_30gev",
    "HNL_5e-10_40gev",
    "HNL_5e-10_50gev",
    "HNL_5e-10_60gev",
    "HNL_5e-10_70gev",
    "HNL_5e-10_80gev",

    "HNL_1.09e-10_10gev",
    "HNL_1.09e-10_20gev",
    "HNL_1.09e-10_30gev",
    "HNL_1.09e-10_40gev",
    "HNL_1.09e-10_50gev",
    "HNL_1.09e-10_60gev",
    "HNL_1.09e-10_70gev",
    "HNL_1.09e-10_80gev",

    "HNL_2.38e-11_10gev",
    "HNL_2.38e-11_20gev",
    "HNL_2.38e-11_30gev",
    "HNL_2.38e-11_40gev",
    "HNL_2.38e-11_50gev",
    "HNL_2.38e-11_60gev",
    "HNL_2.38e-11_70gev",
    "HNL_2.38e-11_80gev",

    "HNL_5e-12_10gev",
    "HNL_5e-12_20gev",
    "HNL_5e-12_30gev",
    "HNL_5e-12_40gev",
    "HNL_5e-12_50gev",
    "HNL_5e-12_60gev",
    "HNL_5e-12_70gev",
    "HNL_5e-12_80gev",

    

    "HNL_6.67e-8_10gev",
    "HNL_6.67e-8_20gev",
    "HNL_6.67e-8_30gev",
    "HNL_6.67e-8_40gev",
    "HNL_6.67e-8_50gev",
    "HNL_6.67e-8_60gev",
    "HNL_6.67e-8_70gev",
    "HNL_6.67e-8_80gev",

    "HNL_1.39e-8_10gev",
    "HNL_1.39e-8_20gev",
    "HNL_1.39e-8_30gev",
    "HNL_1.39e-8_40gev",
    "HNL_1.39e-8_50gev",
    "HNL_1.39e-8_60gev",
    "HNL_1.39e-8_70gev",
    "HNL_1.39e-8_80gev",

    "HNL_3.02e-9_10gev",
    "HNL_3.02e-9_20gev",
    "HNL_3.02e-9_30gev",
    "HNL_3.02e-9_40gev",
    "HNL_3.02e-9_50gev",
    "HNL_3.02e-9_60gev",
    "HNL_3.02e-9_70gev",
    "HNL_3.02e-9_80gev",

    "HNL_6.67e-10_10gev",
    "HNL_6.67e-10_20gev",
    "HNL_6.67e-10_30gev",
    "HNL_6.67e-10_40gev",
    "HNL_6.67e-10_50gev",
    "HNL_6.67e-10_60gev",
    "HNL_6.67e-10_70gev",
    "HNL_6.67e-10_80gev",

    "HNL_1.45e-10_10gev",
    "HNL_1.45e-10_20gev",
    "HNL_1.45e-10_30gev",
    "HNL_1.45e-10_40gev",
    "HNL_1.45e-10_50gev",
    "HNL_1.45e-10_60gev",
    "HNL_1.45e-10_70gev",
    "HNL_1.45e-10_80gev",

    "HNL_3.17e-11_10gev",
    "HNL_3.17e-11_20gev",
    "HNL_3.17e-11_30gev",
    "HNL_3.17e-11_40gev",
    "HNL_3.17e-11_50gev",
    "HNL_3.17e-11_60gev",
    "HNL_3.17e-11_70gev",
    "HNL_3.17e-11_80gev",

    "HNL_6.67e-12_10gev",
    "HNL_6.67e-12_20gev",
    "HNL_6.67e-12_30gev",
    "HNL_6.67e-12_40gev",
    "HNL_6.67e-12_50gev",
    "HNL_6.67e-12_60gev",
    "HNL_6.67e-12_70gev",
    "HNL_6.67e-12_80gev",

    

    "HNL_2.86e-7_10gev",
    "HNL_2.86e-7_20gev",
    "HNL_2.86e-7_30gev",
    "HNL_2.86e-7_40gev",
    "HNL_2.86e-7_50gev",
    "HNL_2.86e-7_60gev",
    "HNL_2.86e-7_70gev",
    "HNL_2.86e-7_80gev",

    "HNL_5.97e-8_10gev",
    "HNL_5.97e-8_20gev",
    "HNL_5.97e-8_30gev",
    "HNL_5.97e-8_40gev",
    "HNL_5.97e-8_50gev",
    "HNL_5.97e-8_60gev",
    "HNL_5.97e-8_70gev",
    "HNL_5.97e-8_80gev",

    "HNL_1.30e-8_10gev",
    "HNL_1.30e-8_20gev",
    "HNL_1.30e-8_30gev",
    "HNL_1.30e-8_40gev",
    "HNL_1.30e-8_50gev",
    "HNL_1.30e-8_60gev",
    "HNL_1.30e-8_70gev",
    "HNL_1.30e-8_80gev",

    "HNL_2.86e-9_10gev",
    "HNL_2.86e-9_20gev",
    "HNL_2.86e-9_30gev",
    "HNL_2.86e-9_40gev",
    "HNL_2.86e-9_50gev",
    "HNL_2.86e-9_60gev",
    "HNL_2.86e-9_70gev",
    "HNL_2.86e-9_80gev",

    "HNL_6.20e-10_10gev",
    "HNL_6.20e-10_20gev",
    "HNL_6.20e-10_30gev",
    "HNL_6.20e-10_40gev",
    "HNL_6.20e-10_50gev",
    "HNL_6.20e-10_60gev",
    "HNL_6.20e-10_70gev",
    "HNL_6.20e-10_80gev",

    "HNL_1.36e-10_10gev",
    "HNL_1.36e-10_20gev",
    "HNL_1.36e-10_30gev",
    "HNL_1.36e-10_40gev",
    "HNL_1.36e-10_50gev",
    "HNL_1.36e-10_60gev",
    "HNL_1.36e-10_70gev",
    "HNL_1.36e-10_80gev",

    "HNL_2.86e-11_10gev",
    "HNL_2.86e-11_20gev",
    "HNL_2.86e-11_30gev",
    "HNL_2.86e-11_40gev",
    "HNL_2.86e-11_50gev",
    "HNL_2.86e-11_60gev",
    "HNL_2.86e-11_70gev",
    "HNL_2.86e-11_80gev",
]

LABELS = {
    "sel2RecoSF_vetoes_tracks_M80_p40_11.5MEpt_0.8cos":"Same flavor, M(l,l)<80 GeV, p_{T,miss}>11.5 Gev, p<40 GeV, cos#theta>-0.8",
    "sel2RecoDF_vetoes_tracks_M80_7MEpt_0.8cos":"Different flavor, M(l,l)<80 GeV, p_{T,miss}>7 Gev, cos#theta>-0.8",
    "sel2Reco_vetoes":"Two leptons, no photons, no jets",
    "sel2RecoSF_vetoes":"Two same flavor leptons, no photons, no jets",
    "sel2RecoDF_vetoes":"Two different flavor leptons, no photons, no jets",
    "sel2Gen_vetoes":"Two gen leptons, no photons",
    "sel2Reco_vetoes_notracks_nojets_M80_10MEpt_0.8cos":"Two leptons, no photons, no other track, no jets, M(l,l)<80 GeV, p_{T,miss}>10 GeV, cos\theta>-0.8",
    
 }

backgrounds = [
    'p8_ee_Zee_ecm91',
    'p8_ee_Zmumu_ecm91',
    'p8_ee_Ztautau_ecm91',
    'p8_ee_Zbb_ecm91',
    'p8_ee_Zcc_ecm91',
    'p8_ee_Zud_ecm91',
    'p8_ee_Zss_ecm91',
    'eenunu',
    'mumununu'
    'tatanunu',
    'llnunu'
]

blegend = {
    'p8_ee_Zee_ecm91': 'Z #rightarrow ll',
    'p8_ee_Ztautau_ecm91': 'Z #rightarrow #tau#tau',
    'p8_ee_Zbb_ecm91': 'Z #rightarrow bb',
    'p8_ee_Zcc_ecm91': 'Z #rightarrow cc',
    'p8_ee_Zud_ecm91': 'Z #rightarrow uds',
    'eenunu': 'ee#nu#nu',
    'mumununu': '#mu#mu#nu#nu',
    'tatanunu': '#tau#tau#nu#nu',
    'llnunu': 'll#nu#nu',
}

bcolors = {
    'p8_ee_Zee_ecm91': 40,
    'p8_ee_Ztautau_ecm91': 36,
    'p8_ee_Zbb_ecm91': 48,
    'p8_ee_Zcc_ecm91': 44,
    'p8_ee_Zud_ecm91': 20,
    'eenunu': 30,
    'mumununu': 32,
    'tatanunu': 33,
    'llnunu': 38,
}

signals = [
    'HNL_2.86e-12_30gev',
    'HNL_6.67e-10_30gev',
    'HNL_5e-12_60gev',
    'HNL_1.33e-7_80gev',
]

slegend = {
    'HNL_2.86e-12_30gev':"U^{2}=2.86e-12, M_{N}=30 GeV",
    'HNL_6.67e-10_30gev':"U^{2}=6.67e-10, M_{N}=30 GeV",
    'HNL_5e-12_60gev':"U^{2}=5e-12, M_{N}=60 GeV",
    'HNL_1.33e-7_80gev':"U^{2}=1.33e-7, M_{N}=80 GeV",
}

scolors = {
    'HNL_2.86e-12_30gev': ROOT.kBlue-9,
    'HNL_6.67e-10_30gev': ROOT.kRed-9,
    'HNL_5e-12_60gev': ROOT.kRed-3,
    'HNL_1.33e-7_80gev': ROOT.kBlue-3,
}

#asym_bins = [-0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.35, 0.5, 0.8] #array of low bin edges wanted
#asym_bins = [0, 0.4, 0.7, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.8, 4.6] 
asym_bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5] 
#asym_bins = [0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6] 
nbins = len(asym_bins)-1
### note: The bin edges specified in xbins should correspond to bin edges in the original histogram. ###

for CUT in CUTS:
    #NEWFILE='/eos/user/s/sgiappic/combine/' + VARIABLE + '_norebin_' + CUT + '.root' # name of the rebinned file
    NEWFILE = "/eos/user/s/sgiappic/2HNL_ana/final_final/HNL_6.67e-8_10gev_" + CUT + ".root"
    nf= ROOT.TFile.Open(NEWFILE, "UPDATE") 

    #rebin FILES and save content in NEWFILE
    for file in ["HNL_1.39e-8_10gev",]:# "p8_ee_Ztautau_ecm91", "llnunu_m", "eenunu_m", "mumununu_m"]:

        FILE = DIRECTORY + file + '_' + CUT + '_histo.root'
        f= ROOT.TFile.Open(FILE, "READ")
        hist=f.Get(VARIABLE)

        print("Rebinning variable {}, {} from {} bins to {} bins\n".format(VARIABLE, FILE, hist.GetNbinsX(), nbins))

        hist_name = file +"_"+VARIABLE
        new_hist = ROOT.TH1F(hist_name, "Rebinned #Delta R", nbins, array.array('d', asym_bins))

        #for each bin in the original distribution, sum until one interval is reached
        i = 0
        bin_content = 0
        for b in range(hist.GetNbinsX()):
            bin_content += hist.GetBinContent(b) * 4.7 # scale lumi from 180 to 204
            if (hist.GetBinLowEdge(b) >= asym_bins[i]): #check if the interval edge has already been reached and if we are over it
                 #print(i, asym_bins[i])
                new_hist.SetBinContent(i, bin_content)
                i += 1
                bin_content = 0
                if (i > nbins):
                    break

        nf.cd()
        new_hist.Write()
        f.Close()

    nf.Close()

'''#plot the rebinned variable
NEWFILE_SF='/eos/user/s/sgiappic/combine/Reco_DR_norebin_selReco_gen_notracks_nohad_5M80_0.7cos_20MEpt.root' # name of the rebinned file
    
#extralab = LABELS[CUT]

canvas = ROOT.TCanvas("", "", 800, 800)

nsig = len(signals)
nbkg = 9 # change according to type of plots, 6 for grouped backgrounds

#legend coordinates and style
legsize = 0.06*nsig 
legsize2 = 0.04*nbkg
leg = ROOT.TLegend(0.16, 0.80 - legsize, 0.45, 0.74)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetLineColor(0)
leg.SetShadowColor(0)
leg.SetTextSize(0.025)
leg.SetTextFont(42)

leg2 = ROOT.TLegend(0.70, 0.80 - legsize2, 0.88, 0.74)
leg2.SetFillColor(0)
leg2.SetFillStyle(0)
leg2.SetLineColor(0)
leg2.SetShadowColor(0)
leg2.SetTextSize(0.025)
leg2.SetTextFont(42)

#global arrays for histos and colors
histos = []
colors = []

#loop over files for signals and backgrounds and assign corresponding colors and titles
for s in signals:
    fin_SF = NEWFILE_SF
    #fin_DF = NEWFILE_DF
    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get(s + "_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
   # with ROOT.TFile(fin_DF) as tf_DF:
    #    h1 = tf_DF.Get(s + "_" + VARIABLE)
    #    hh1 = copy.deepcopy(h1)
    #    hh1.SetDirectory(0)
    #hh.Add(hh1)
    histos.append(hh)
    colors.append(scolors[s])
    leg.AddEntry(histos[-1], slegend[s], "l")

#for b in backgrounds:
    #fin = f"{DIRECTORY}{b}_{cut}_histo.root"
    #with ROOT.TFile(fin) as tf:
        #h = tf.Get(variable)
        #hh = copy.deepcopy(h)
        #hh.SetDirectory(0)
    #histos.append(hh)
    #colors.append(bcolors[b])
    #leg2.AddEntry(histos[-1], blegend[b], "f")

if nbkg != 0:
    #add some backgrounds to the same histogram
    fin_SF = NEWFILE_SF
    #fin_DF = NEWFILE_DF
    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "eenunu_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(bcolors["eenunu"])
    leg2.AddEntry(histos[-1], blegend["eenunu"], "f")

    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "mumununu_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(bcolors["mumununu"])
    leg2.AddEntry(histos[-1], blegend["mumununu"], "f")

    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "tatanunu_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(bcolors["tatanunu"])
    leg2.AddEntry(histos[-1], blegend["tatanunu"], "f")

    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "llnunu_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(bcolors["llnunu"])
    leg2.AddEntry(histos[-1], blegend["llnunu"], "f")
    
    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "p8_ee_Zee_ecm91_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    with ROOT.TFile(fin_SF) as tf_SF:
        h1 = tf_SF.Get( "p8_ee_Zmumu_ecm91_" + VARIABLE)
        hh1 = copy.deepcopy(h1)
        hh1.SetDirectory(0)
    hh.Add(hh1)
    histos.append(hh)
    colors.append(bcolors["p8_ee_Zee_ecm91"])
    leg2.AddEntry(histos[-1], blegend["p8_ee_Zee_ecm91"], "f")

    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "p8_ee_Ztautau_ecm91_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(bcolors["p8_ee_Ztautau_ecm91"])
    leg2.AddEntry(histos[-1], blegend["p8_ee_Ztautau_ecm91"], "f")

    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "p8_ee_Zud_ecm91_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    with ROOT.TFile(fin_SF) as tf_SF:
        h1 = tf_SF.Get( "p8_ee_Zss_ecm91_" + VARIABLE)
        hh1 = copy.deepcopy(h1)
        hh1.SetDirectory(0)
    hh.Add(hh1)
    histos.append(hh)
    colors.append(bcolors["p8_ee_Zud_ecm91"])
    leg2.AddEntry(histos[-1], blegend["p8_ee_Zud_ecm91"], "f")

    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "p8_ee_Zcc_ecm91_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(bcolors["p8_ee_Zcc_ecm91"])
    leg2.AddEntry(histos[-1], blegend["p8_ee_Zcc_ecm91"], "f")

    with ROOT.TFile(fin_SF) as tf_SF:
        h = tf_SF.Get( "p8_ee_Zbb_ecm91_" + VARIABLE)
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(bcolors["p8_ee_Zbb_ecm91"])
    leg2.AddEntry(histos[-1], blegend["p8_ee_Zbb_ecm91"], "f")

    #drawing stack for backgrounds
    hStackBkg = ROOT.THStack("hStackBkg", "")
    hStackBkg.SetMinimum(1e-6)
    hStackBkg.SetMaximum(1e17)
    BgMCHistYieldsDic = {}
    for i in range(nsig, nsig+nbkg):
        h = histos[i]
        h.Scale(1.13) # scale lumi from 180 to 204
        h.SetLineWidth(1)
        h.SetLineColor(ROOT.kBlack)
        h.SetFillColor(colors[i])
        if h.Integral() > 0:
            BgMCHistYieldsDic[h.Integral()] = h
        else:
            BgMCHistYieldsDic[-1*nbkg] = h

    # sort stack by yields (smallest to largest)
    BgMCHistYieldsDic = sorted_dict_values(BgMCHistYieldsDic)
    for h in BgMCHistYieldsDic:
        hStackBkg.Add(h)

    #draw the histograms
    hStackBkg.Draw("HIST")

    # add the signal histograms
    for i in range(nsig):
        h = histos[i]
        h.Scale(1.13) # scale lumi from 180 to 204
        h.SetLineWidth(3)
        h.SetLineColor(colors[i])
        h.Draw("HIST SAME")

    hStackBkg.GetYaxis().SetTitle("Events")
    hStackBkg.GetXaxis().SetTitle("Reco #Delta R(l,l')")
    #hStackBkg.GetYaxis().SetTitleOffset(1.5)
    hStackBkg.GetXaxis().SetTitleOffset(1.2)
    #hStackBkg.GetXaxis().SetLimits(1, 1000)

else: 
        # add the signal histograms
    for i in range(nsig):
        h = histos[i]
        h.Scale(1.13) # scale lumi from 180 to 204
        h.SetLineWidth(3)
        h.SetLineColor(colors[i])
        if i == 0:
            h.Draw("HIST")
            h.GetYaxis().SetTitle("Events")
            h.GetXaxis().SetTitle(histos[i].GetXaxis().GetTitle())
            #h.GetXaxis().SetTitle("{}".format(variable))
            h.GetYaxis().SetRangeUser(1e-6,1e15)
            #h.GetYaxis().SetTitleOffset(1.5)
            h.GetXaxis().SetTitleOffset(1.2)
            #h.GetXaxis().SetLimits(1, 1000)
        else: 
            h.Draw("HIST SAME")

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

#text = '#bf{#it{' + extralab + '}}'
text = '#bf{#it{Two leptons, no photons, no other tracks, no neutral hadrons, 5<M(l,l)<80 GeV, p_{T,miss}>20 GeV, cos#theta>-0.7}}'
latex.SetTextSize(0.02)
latex.DrawLatex(0.18, 0.76, text)

leg.Draw()
leg2.Draw()

latex.SetTextAlign(31)
text = '#it{' + leftText + '}'
latex.SetTextSize(0.03)
latex.DrawLatex(0.92, 0.92, text)

# Set Logarithmic scales for both x and y axes
#canvas.SetLogx()
canvas.SetLogy()
canvas.SetTicks(1, 1)
canvas.SetLeftMargin(0.14)
canvas.SetRightMargin(0.08)
canvas.GetFrame().SetBorderSize(12)

canvas.RedrawAxis()
canvas.Modified()
canvas.Update()

#dir = "/eos/user/s/sgiappic/www/plots/" + CUT + "/"
#make_dir_if_not_exists(dir)

#canvas.SaveAs(dir + VARIABLE + "_rebinned.png")
#canvas.SaveAs(dir+ VARIABLE + "_rebinned.pdf")

canvas.SaveAs("/eos/user/s/sgiappic/www/paper/Reco_DR_rebinned_24july.png")
canvas.SaveAs("/eos/user/s/sgiappic/www/paper/Reco_DR_rebinned_24july.pdf")'''