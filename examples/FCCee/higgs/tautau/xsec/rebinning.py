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
DIRECTORY = {
    'LL':"/ceph/awiedl/FCCee/HiggsCP/final_v2/LL",
    'QQ':"/ceph/awiedl/FCCee/HiggsCP/final_v2_cut/QQ",
    'NuNu':"/ceph/awiedl/FCCee/HiggsCP/final_v2_cut/NuNu",
}
SUBDIR = [
    'LL',
    #'LH',
    #'HH',
]
#category to plot
CAT = [
    "QQ",
    #"LL",
    #"NuNu",
]
#list of CUTs you want to plot
CUTS_LL = [
    #"selReco",
    #"selReco_100Coll150",
    #"selReco_100Coll150_115Rec160",
    #"selReco_100Coll150_115Rec160_10Me",
    #"selReco_100Coll150_115Rec160_10Me_70Z100",
    #"selReco_100Coll150_115Rec160_2DR",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_10ME",
    #"selReco_100Coll150_115Rec160_10Me_70Z100_2DR_cos0.6_misscos0.98",
]

CUTS_QQ = [
    "selReco",
    "selReco_0.5BDT",
    #"selReco_0.6BDT",
    #"selReco_0.7BDT",
    #"selReco_100Coll150",
    #"selReco_100Coll150_115Rec160",
    #"selReco_100Coll150_115Rec160_10Me",
    #"selReco_100Coll150_115Rec160_10Me_80Z95",
    #"selReco_100Coll150_115Rec160_2DR",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_QTAU0.5",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_QTAU0.5_10ME",
    #"selReco_100Coll150_115Rec160_10Me_80Z95_2DR_cos0.6_misscos0.98",
]
    
CUTS_NuNu = [
    "selReco",
    "selReco_0.5BDT",
    #"selReco_0.6BDT",
    #"selReco_0.7BDT",
    #"selReco_100Me",
    #"selReco_100Me_TauDPhi3",
    #"selReco_100Me_TauDPhi3_2DR",
    #"selReco_100Me_TauDPhi3_2DR_cos0.4",
    #"selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98",
    #"selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
]

CUTS = {
    'LL':CUTS_LL,
    'QQ':CUTS_QQ,
    'NuNu':CUTS_NuNu,
}

#directory where you want your plots to go
DIR_PLOTS = '/web/sgiappic/public_html/Higgs_xsec/explicit/BDT' 

#labels for the CUTs in the plots
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

    #CUTs for LL
    "selReco_100Coll150_115Rec160_10Me_70Z100": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{70<M_{Z}<110 GeV}",
    "selReco_100Coll150_115Rec160_10Me_70Z100_2DR": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{70<M_{Z}<110 GeV, #Delta R_{#tau}>2}",
    "selReco_100Coll150_115Rec160_10Me_70Z100_2DR_cos0.6": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{70<M_{Z}<110 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6}",
    "selReco_100Coll150_115Rec160_10Me_70Z100_2DR_cos0.6_misscos0.98": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{70<M_{Z}<110 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6, |cos#theta_{miss}|<0.98}",

    #CUTs for QQ
    "selReco_100Coll150_115Rec160_10Me_80Z95": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{80<M_{Z}<95 GeV}",
    "selReco_100Coll150_115Rec160_10Me_80Z95_2DR": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{80<M_{Z}<95 GeV, #Delta R_{#tau}>2}",
    "selReco_100Coll150_115Rec160_10Me_80Z95_2DR_cos0.6": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{80<M_{Z}<95 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6}",
    "selReco_100Coll150_115Rec160_10Me_80Z95_2DR_cos0.6_misscos0.98": "#splitline{100<M_{collinear}<150 GeV, 115<M_{recoil}<160 GeV, E_{miss}>10 GeV,}{80<M_{Z}<95 GeV, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.6, |cos#theta_{miss}|<0.98}",
    
    #"selReco_0.5BDT":"100<M_{collinear}<150 GeV, BDT score>0.5",
    #"selReco_0.6BDT":"100<M_{collinear}<150 GeV, BDT score>0.6",
    #"selReco_0.7BDT":"100<M_{collinear}<150 GeV, BDT score>0.7",

    #CUTs for NuNu
    "selReco_100Me": "E_{miss}>100 GeV",
    "selReco_100Me_TauDPhi3": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3",
    "selReco_100Me_TauDPhi3_2DR": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2",
    "selReco_100Me_TauDPhi3_2DR_cos0.4": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.98",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.98, |y_{miss}|<1",

    "selReco_0.5BDT":"E_{miss}>100 GeV, BDT score>0.5",
    "selReco_0.6BDT":"E_{miss}>100 GeV, BDT score>0.6",
    "selReco_0.7BDT":"E_{miss}>100 GeV, BDT score>0.7",

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
LOGY = True
PLOT = True

VARIABLE = "BDT_score" # VARIABLE to rebin

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

    #"wzp6_ee_nunuH_Htautau_ecm240",
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

    #"wzp6_ee_eeH_Htautau_ecm240",
    #"wzp6_ee_eeH_HQQ_ecm240",
    #"wzp6_ee_eeH_Hgg_ecm240",
    #"wzp6_ee_eeH_HVV_ecm240",

    #"wzp6_ee_mumuH_Htautau_ecm240",
    #"wzp6_ee_mumuH_HQQ_ecm240",
    #"wzp6_ee_mumuH_Hgg_ecm240",
    #"wzp6_ee_mumuH_HVV_ecm240",

    #"wzp6_ee_ZheavyH_Htautau_ecm240",
    #"wzp6_ee_ZheavyH_HQQ_ecm240",
    #"wzp6_ee_ZheavyH_Hgg_ecm240",
    #"wzp6_ee_ZheavyH_HVV_ecm240",

    #"wzp6_ee_ZlightH_Htautau_ecm240",
    #"wzp6_ee_ZlightH_HQQ_ecm240",
    #"wzp6_ee_ZlightH_Hgg_ecm240",
    #"wzp6_ee_ZlightH_HVV_ecm240",
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
}

legcolors = {
    'p8_ee_WW_ecm240':ROOT.kSpring+2,
    'p8_ee_Zqq_ecm240':ROOT.kMagenta-8,
    'p8_ee_ZZ_ecm240':ROOT.kSpring+3,

    'wzp6_ee_LL_ecm240':ROOT.kMagenta-6,
    'wzp6_ee_tautau_ecm240':ROOT.kPink+1,

    "wzp6_ee_nuenueZ_ecm240":ROOT.kPink-4,

    "wzp6_ee_egamma_eZ_ZLL_ecm240":ROOT.kOrange-4,
    
    "wzp6_ee_gaga_LL_60_ecm240":ROOT.kOrange-9,
    "wzp6_ee_gaga_tautau_60_ecm240":ROOT.kOrange+6,

    "wzp6_ee_tautauH_Htautau_ecm240":ROOT.kViolet+6,
    "wzp6_ee_tautauH_HQQ_ecm240":ROOT.kViolet+5,
    "wzp6_ee_tautauH_Hgg_ecm240":ROOT.kViolet-4,
    "wzp6_ee_tautauH_HVV_ecm240":ROOT.kViolet+1,

    'wzp6_ee_nunuH_Htautau_ecm240':ROOT.kGreen-3,
    "wzp6_ee_nunuH_HQQ_ecm240":ROOT.kGreen-5,
    "wzp6_ee_nunuH_Hgg_ecm240":ROOT.kGreen-8,
    "wzp6_ee_nunuH_HVV_ecm240":ROOT.kGreen-10,

    'wzp6_ee_eeH_Htautau_ecm240':ROOT.kBlue-9,
    "wzp6_ee_eeH_HQQ_ecm240":ROOT.kCyan-5,
    "wzp6_ee_eeH_Hgg_ecm240":ROOT.kCyan-8,
    "wzp6_ee_eeH_HVV_ecm240":ROOT.kCyan-10,

    'wzp6_ee_mumuH_Htautau_ecm240':ROOT.kBlue-3,
    "wzp6_ee_mumuH_HQQ_ecm240":ROOT.kBlue-5,
    "wzp6_ee_mumuH_Hgg_ecm240":ROOT.kBlue-8,
    "wzp6_ee_mumuH_HVV_ecm240":ROOT.kBlue-10,

    'wzp6_ee_ZheavyH_Htautau_ecm240':ROOT.kRed-3,
    "wzp6_ee_ZheavyH_HQQ_ecm240":ROOT.kRed-5,
    "wzp6_ee_ZheavyH_Hgg_ecm240":ROOT.kRed-8,
    "wzp6_ee_ZheavyH_HVV_ecm240":ROOT.kRed-10,

    'wzp6_ee_ZlightH_Htautau_ecm240':ROOT.kRed-9,
    "wzp6_ee_ZlightH_HQQ_ecm240":ROOT.kMagenta-5,
    "wzp6_ee_ZlightH_Hgg_ecm240":ROOT.kMagenta-8,
    "wzp6_ee_ZlightH_HVV_ecm240":ROOT.kMagenta-10,

    'wzp6_ee_LLH_Htautau_ecm240':ROOT.kBlue-9,
    "wzp6_ee_LLH_HQQ_ecm240":ROOT.kCyan-5,
    "wzp6_ee_LLH_Hgg_ecm240":ROOT.kCyan-8,
    "wzp6_ee_LLH_HVV_ecm240":ROOT.kCyan-10,

    'wzp6_ee_QQH_Htautau_ecm240':ROOT.kRed-9,
    "wzp6_ee_QQH_HQQ_ecm240":ROOT.kMagenta-5,
    "wzp6_ee_QQH_Hgg_ecm240":ROOT.kMagenta-8,
    "wzp6_ee_QQH_HVV_ecm240":ROOT.kMagenta-10,

}

#list of signals, then legend and colors to be assigned to them
signals = [
    #'wzp6_ee_ZheavyH_Htautau_ecm240',
    #'wzp6_ee_ZlightH_Htautau_ecm240',
    'wzp6_ee_QQH_Htautau_ecm240',
    #'wzp6_ee_eeH_Htautau_ecm240',
    #'wzp6_ee_mumuH_Htautau_ecm240',
    'wzp6_ee_LLH_Htautau_ecm240',
    'wzp6_ee_nunuH_Htautau_ecm240',
]

#asym_bins = [-0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.35, 0.5, 0.8] #array of low bin edges wanted
#asym_bins = [0, 0.4, 0.7, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.8, 4.6] 
#asym_bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5] 
#asym_bins = [0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6] 
#nbins = len(asym_bins)-1
### note: The bin edges specified in xbins should correspond to bin edges in the original histogram. ###

nbins = 100
rebin_factor = 20

for cat in CAT:
    for sub in SUBDIR:
        for CUT in CUTS[cat]:
            list = backgrounds_all + signals
            directory =  DIRECTORY[cat] + "/" + sub + "/" 

            for sample in list:

                FILE = directory + sample + '_' + CUT + '_histo.root'

                if file_exists(FILE):
            
                    NEWFILE = directory + sample + "_rebinned_BDTscore_" + CUT + ".root"
                    nf= ROOT.TFile.Open(NEWFILE, "RECREATE") 

                    f= ROOT.TFile.Open(FILE, "READ")
                    hist=f.Get(VARIABLE)

                    '''print("Rebinning VARIABLE {}, {} from {} bins to {} bins\n".format(VARIABLE, FILE, hist.GetNbinsX(), nbins))

                    hist_name = VARIABLE
                    new_hist = ROOT.TH1F(hist_name, "BDT score", hist.GetNbinsX(), 0., 1.)

                    new_edges = np.linspace(0., 1., nbins)

                    #for each bin in the original distribution, sum until one interval is reached
                    i = 0
                    bin_content = 0
                    for b in range(hist.GetNbinsX()):
                        bin_content += hist.GetBinContent(b) 
                        if (hist.GetBinLowEdge(b) >= new_edges[i]): #check if the interval edge has already been reached and if we are over it
                            #print(i, asym_bins[i])
                            new_hist.SetBinContent(i, bin_content)
                            i += 1
                            bin_content = 0
                            if (i > nbins):
                                break'''

                    new_hist = hist.Rebin(rebin_factor, VARIABLE) 
                    print("Rebinning VARIABLE {}, {} from {} bins to {} bins\n".format(VARIABLE, NEWFILE, hist.GetNbinsX(), hist.GetNbinsX()/rebin_factor))

                    nf.cd()
                    new_hist.Write()
                    f.Close()
                    nf.Close()

            #plot the rebinned VARIABLE
            if PLOT:
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
                    fin = f"{directory}{s}_rebinned_BDTscore_{CUT}.root"
                    if file_exists(fin): #might be an empty file after stage2 
                        tf = ROOT.TFile.Open(fin, 'READ')
                        h = tf.Get(VARIABLE)
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
                        fin = f"{directory}{b}_rebinned_BDTscore_{CUT}.root"
                        if file_exists(fin):
                            tf = ROOT.TFile.Open(fin, 'READ')
                            h = tf.Get(VARIABLE)
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
                            fin = f"{directory}{sub}{b}_{CUT}_histo.root"
                            if (i==0 and j==0):
                                with ROOT.TFile(fin) as tf:
                                    h = tf.Get(VARIABLE)
                                    hh = copy.deepcopy(h)
                                    hh.SetDirectory(0)
                            else:
                                with ROOT.TFile(fin) as tf:
                                    h = tf.Get(VARIABLE)
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
                        hStackBkg.SetMaximum(last*2)

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
                    #hStackBkg.GetXaxis().SetTitle("Reco visible mass [GeV]")
                    #hStackBkg.GetYaxis().SetTitleOffset(1.5)
                    hStackBkg.GetXaxis().SetTitleOffset(1.2)
                    #hStackBkg.GetXaxis().SetLimits(100, 150)

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
                            #h.GetXaxis().SetTitle("{}".format(VARIABLE))
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
                extralab = LABELS[CUT]

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

                    dir = DIR_PLOTS + "/" + cat + "/" + sub + "/log/" + CUT + "/"
                    make_dir_if_not_exists(dir)

                    canvas.SaveAs(dir + VARIABLE + "_" + cat + sub + ".png")
                    canvas.SaveAs(dir + VARIABLE + "_" + cat + sub + ".pdf")
                else:
                    canvas.SetTicks(1, 1)
                    canvas.SetLeftMargin(0.14)
                    canvas.SetRightMargin(0.08)
                    canvas.GetFrame().SetBorderSize(12)

                    canvas.RedrawAxis()
                    canvas.Modified()
                    canvas.Update()

                    dir = DIR_PLOTS + "/" + cat + "/" + sub + "/lin/" + CUT + "/"
                    make_dir_if_not_exists(dir)

                    canvas.SaveAs(dir + VARIABLE + "_" + cat + sub + ".png")
                    canvas.SaveAs(dir + VARIABLE + "_" + cat + sub + ".pdf")