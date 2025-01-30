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
DIRECTORY = '/ceph/sgiappic/HiggsCP/CPGen/final_pinu/'

#directory where you want your plots to go
DIR_PLOTS = '/web/sgiappic/public_html/Higgs_CP/' 

#labels for the CUTs in the plots
LABELS = {
    "selGen": "No additional selection",
 }

ana_tex = "e^{+}e^{-} #rightarrow Z H, Z #rightarrow LL, H #rightarrow #tau_{h}#tau_{h}"

energy         = 240
collider       = 'FCC-ee'
intLumi        = 10.8 #ab-1
LOGY = False
PLOT = False

VARIABLE = "GenPhi_decay" # VARIABLE to rebin
## "bin":63, "xmin":-3.14,"xmax":3.14

CUT = "selGen"

NEWFILE = DIRECTORY + VARIABLE + "_EFT_" + CUT + ".root"

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

    'p8_ee_ZZ_ecm240',
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

name = {
    'EWonly_taudecay_2Pi2Nu':"sm",
    'cehim_m1_taudecay_2Pi2Nu':"sm_lin_quad_cehim_m1",
    'cehim_p1_taudecay_2Pi2Nu':"sm_lin_quad_cehim",
    'cehre_m1_taudecay_2Pi2Nu':"sm_lin_quad_cehre_m1",
    'cehre_p1_taudecay_2Pi2Nu':"sm_lin_quad_cehre_p1",
    'p8_ee_ZZ_ecm240':"p8_ee_ZZ_ecm240",
}

#asym_bins = [-0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.35, 0.5, 0.8] #array of low bin edges wanted
#nbins = len(asym_bins)-1
### note: The bin edges specified in xbins should correspond to bin edges in the original histogram. ###

#nbins = 63
#rebin_factor = 20
#list = backgrounds_all + signals

## prepare the sm and lin+quad haistograms in the way the model wants:
## change name of the histoagrams accordingly to the process plus variable plotted

nf= ROOT.TFile.Open(NEWFILE, "RECREATE") 

for sample in signals:

    FILE = DIRECTORY + sample + '_' + CUT + '_histo.root'

    if file_exists(FILE):

        f= ROOT.TFile.Open(FILE, "READ")
        hist=f.Get(VARIABLE)

        new_hist = copy.deepcopy(hist)
        new_hist.SetDirectory(0)

        #change the name accordingly to the new histogram
        hist_name = name[sample]
        new_hist.SetName(hist_name + "_" + VARIABLE)

        print("VARIABLE {} to file {}\n".format(VARIABLE, NEWFILE))

        nf.cd()
        new_hist.Write()
        f.Close()

## now we need to "isolate" the quadratic contribution from the eft only from the sm and lin+quad
sm_file = ROOT.TFile.Open(DIRECTORY + "EWonly_taudecay_2Pi2Nu_selGen_histo.root", "READ")
cehim_m1_file = ROOT.TFile.Open(DIRECTORY + "cehim_m1_taudecay_2Pi2Nu_selGen_histo.root", "READ")
cehim_p1_file = ROOT.TFile.Open(DIRECTORY + "cehim_p1_taudecay_2Pi2Nu_selGen_histo.root", "READ")

sm_histo = sm_file.Get(VARIABLE)
cehim_m1_histo = cehim_m1_file.Get(VARIABLE)
cehim_p1_histo = cehim_p1_file.Get(VARIABLE)

# quad = cpv(+1) + cpv(-1) - 2*sm, in brackets the WC
quad_histo = copy.deepcopy(cehim_p1_histo)
quad_histo.SetDirectory(0)

quad_histo.Add(cehim_m1_histo)
quad_histo.Add(sm_histo, -2.)
quad_histo.SetName("quad_cehim_" + VARIABLE)

print("VARIABLE {} to file {}\n".format(VARIABLE, NEWFILE))

nf.cd()
quad_histo.Write()

nf.Close()

#plot the rebinned VARIABLE
if PLOT:
    canvas = ROOT.TCanvas("", "", 800, 800)

    nsig = len(signals)
    nbkg = 0#len(backgrounds_all) #put to zero if you only want to look at signals

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
        fin = NEWFILE
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

        dir = DIR_PLOTS 
        make_dir_if_not_exists(dir)

        canvas.SaveAs(dir + VARIABLE + ".png")
        canvas.SaveAs(dir + VARIABLE +  ".pdf")
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

        canvas.SaveAs(dir + VARIABLE + ".png")
        canvas.SaveAs(dir + VARIABLE + ".pdf")