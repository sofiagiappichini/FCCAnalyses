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
import uproot

# Set ROOT to batch mode so it doesn't open all the plots
ROOT.gROOT.SetBatch(True)

def check_nonzero(path, variable):
    if file_exists(path):
        histo_file = uproot.open(path)
        selected_leaf = histo_file[variable]
        y_values = selected_leaf.values()
        if (sum(y_values)!=0):
            return True
        else:
            return False

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
DIRECTORY = "/ceph/awiedl/FCCee/HiggsCP/"
TAG = [
    "R5-explicit",
    "R5-tag",
    "ktN-explicit",
    "ktN-tag",
]
SUBDIR = [
    'LL',
    'LH',
    'HH',
]
#category to plot
CAT = [
    "QQ",
    "LL",
    "NuNu",
]
CUTS = {
    #'LL':"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    #'QQ':"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    #'NuNu':"selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    'LL/HH':"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.96_80Z100_4Emiss_Zp54",
    'LL/LH':"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.88_84Z100_4Emiss_Zp54",
    'LL/LL':"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.9_80Z100_40Emiss_Zp54",
    'QQ/HH':"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.86_70Z100_8Emiss_Zp52",
    'QQ/LH':"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_36Emiss_Zp52",
    'QQ/LL':"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.92_70Z100_52Emiss_Zp52",
    'NuNu/HH':"selReco_112Me_TauDPhi3_2DR_cos0.4_misscos0.88_missy1",
    'NuNu/LH':"selReco_140Me_TauDPhi3_2DR_cos0.4_misscos0.94_missy1",
    'NuNu/LL':"selReco_152Me_TauDPhi3_2DR_cos0.4_misscos0.92_missy1",
}
VARIABLE = {
    'LL':"Recoil",
    'QQ':"Recoil",
    'NuNu':"Visible_mass",
    }

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

    "wzp6_ee_LLH_HQQ_ecm240",
    "wzp6_ee_LLH_Hgg_ecm240",
    "wzp6_ee_LLH_HVV_ecm240",

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

signals = [
    #'wzp6_ee_ZheavyH_Htautau_ecm240',
    #'wzp6_ee_ZlightH_Htautau_ecm240',
    'wzp6_ee_QQH_Htautau_ecm240',
    #'wzp6_ee_eeH_Htautau_ecm240',
    #'wzp6_ee_mumuH_Htautau_ecm240',
    'wzp6_ee_LLH_Htautau_ecm240',
    'wzp6_ee_nunuH_Htautau_ecm240',
]

for tag in TAG:
    for cat in CAT:
        for sub in SUBDIR:

            index = f"{cat}/{sub}"

            cut = CUTS[index]

            if "ktN-tag" in tag and "LL" in cat and "HH" in sub:
                cut = "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.96_86Z100_4Emiss_Zp54"
            if "tag" in tag and "QQ" in cat and "HH" in sub:
                cut = "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.86_75Z100_8Emiss_Zp52"

            variable = VARIABLE[cat]

            directory = DIRECTORY + tag + "/final_241202/" + cat + "/" + sub + "/"

            output = f"{directory}Combine_{variable}_{cut}_histo.root"
            outFile = ROOT.TFile.Open(output, "RECREATE")
        
            for proc in backgrounds_all:
                
                file = f"{directory}{proc}_{cut}_histo.root"
                check = False
                #print(file)
                if file_exists(file) and check_nonzero(file, variable):
                    check = True
                    hist_name = f"{proc}_{variable}"
                    #new_hist = ROOT.TH1F(hist_name, "", hist.GetNbinsX(), 0., 1.)
                    tf = ROOT.TFile.Open(file, "READ")
                    h = tf.Get(variable)
                    hh = h.Clone(hist_name)
                    #hh = copy.deepcopy(h)
                    hh.SetDirectory(0)
                    for b in range(hh.GetNbinsX()):
                        if (hh.GetBinContent(b)==0): #check if there are empty background bins
                            #print(i, asym_bins[i])
                            hh.SetBinContent(b, 1e-6)
                    tf.Close()
                    #write the histogram in the file   
                    outFile.cd()
                    hh.Write()

            for proc in signals:
                
                file = f"{directory}{proc}_{cut}_histo.root"
                check = False
                #print(file)
                if file_exists(file) and check_nonzero(file, variable):
                    check = True
                    hist_name = f"{proc}_{variable}"
                    #new_hist = ROOT.TH1F(hist_name, "", hist.GetNbinsX(), 0., 1.)
                    tf = ROOT.TFile.Open(file, "READ")
                    h = tf.Get(variable)
                    hh = h.Clone(hist_name)
                    #hh = copy.deepcopy(h)
                    hh.SetDirectory(0) 
                    outFile.cd()
                    hh.Write()
                    
            outFile.Close()
