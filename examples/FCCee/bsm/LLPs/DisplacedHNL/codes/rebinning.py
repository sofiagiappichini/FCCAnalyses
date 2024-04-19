# from https://github.com/mpresill/PlotsConfigurations/blob/matteo/Configurations/VBS_ZV/scripts/rebinning.py#L23-L66
# relevant lines for rebinning only: 23-66 
# https://root.cern/doc/master/classTH1.html#a9eef6f499230b88582648892e5e4e2ce on rebin 
# requires python3 from key4hep stack sourcing, not cmsenv

import os
import ROOT as R
import shutil
from matplotlib import pyplot as plt
import pandas as pd
import array

DIRECTORY = '/eos/user/s/sgiappic/2HNL_ana/final/' 
CUTS = [
    #'sel2RecoDF_vetoes_tracks_M80_5MEpt_0.8cos',
    'sel2RecoSF_vetoes_tracks_M80_5MEpt_p40_0.8cos',
 ] # cut to rebin
VARIABLE = "Reco_DR" # variable to rebin
FILES_B = [
    'p8_ee_Zee_ecm91',
    'p8_ee_Zmumu_ecm91',
    'p8_ee_Ztautau_ecm91',
    #'p8_ee_Zbb_ecm91',
    #'p8_ee_Zcc_ecm91',
    #'p8_ee_Zud_ecm91',
    #'p8_ee_Zss_ecm91',
    'emununu',
    'tatanunu'
]

FILES = [
    "HNL_4e-10_10gev",
    "HNL_4e-10_20gev",
    "HNL_4e-10_30gev",
    "HNL_4e-10_40gev",
    "HNL_4e-10_50gev",
    "HNL_4e-10_60gev",
    "HNL_4e-10_70gev",
    "HNL_4e-10_80gev",

    "HNL_1.33e-7_10gev",
    "HNL_1.33e-7_20gev",
    "HNL_1.33e-7_30gev",
    "HNL_1.33e-7_40gev",
    "HNL_1.33e-7_50gev",
    "HNL_1.33e-7_60gev",
    "HNL_1.33e-7_70gev",
    "HNL_1.33e-7_80gev",

    "HNL_2.86e-12_10gev",
    "HNL_2.86e-12_20gev",
    "HNL_2.86e-12_30gev",
    "HNL_2.86e-12_40gev",
    "HNL_2.86e-12_50gev",
    "HNL_2.86e-12_60gev",
    "HNL_2.86e-12_70gev",
    "HNL_2.86e-12_80gev",

    "HNL_5e-12_10gev",
    "HNL_5e-12_20gev",
    "HNL_5e-12_30gev",
    "HNL_5e-12_40gev",
    "HNL_5e-12_50gev",
    "HNL_5e-12_60gev",
    "HNL_5e-12_70gev",
    "HNL_5e-12_80gev",

    "HNL_6.67e-10_10gev",
    "HNL_6.67e-10_20gev",
    "HNL_6.67e-10_30gev",
    "HNL_6.67e-10_40gev",
    "HNL_6.67e-10_50gev",
    "HNL_6.67e-10_60gev",
    "HNL_6.67e-10_70gev",
    "HNL_6.67e-10_80gev",

    "HNL_2.86e-7_10gev",
    "HNL_2.86e-7_20gev",
    "HNL_2.86e-7_30gev",
    "HNL_2.86e-7_40gev",
    "HNL_2.86e-7_50gev",
    "HNL_2.86e-7_60gev",
    "HNL_2.86e-7_70gev",
    "HNL_2.86e-7_80gev"
]

#asym_bins = [-0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.35, 0.5, 0.8] #array of low bin edges wanted
#asym_bins = [0, 0.4, 0.6, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.6] #DF
asym_bins = [0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.6] #SF
nbins = len(asym_bins)-1
### note: The bin edges specified in xbins should correspond to bin edges in the original histogram. ###

for CUT in CUTS:
    NEWFILE='/eos/user/s/sgiappic/combine/' + VARIABLE + '_rebinned_' + CUT + '.root' # name of the rebinned file
    nf= R.TFile.Open(NEWFILE, "UPDATE") 

    #rebin FILES and save content in NEWFILE
    for file in FILES_B:

        FILE = DIRECTORY + file + '_' + CUT + '_histo.root'
        f= R.TFile.Open(FILE, "READ")
        hist=f.Get(VARIABLE)

        print("Rebinning variable {}, {} from {} bins to {} bins\n".format(VARIABLE, FILE, hist.GetNbinsX(), nbins))

        hist_name = file+"_"+VARIABLE
        new_hist = R.TH1F(hist_name, "Rebinned #Delta R", nbins, array.array('d', asym_bins))

        #for each bin in the original distribution, sum until one interval is reached
        i = 0
        bin_content = 0
        for b in range(hist.GetNbinsX()):
            bin_content += hist.GetBinContent(b)
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
