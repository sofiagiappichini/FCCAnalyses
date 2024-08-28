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

backgrounds = [
    "p8_ee_Zee_ecm91",
    "p8_ee_Ztautau_ecm91",
]

variables = [
    "RecoMissingEnergy_pt",
    "Reco_cos",
]

outFile = ROOT.TFile.Open(f"/eos/user/s/sgiappic/2HNL_ana/combined_histo.root", "RECREATE")
    #loop to merge different sources into one histograms for easier plotting
for var in variables:
    j = 0
    hh = None
    for b in backgrounds:
        tf = ROOT.TFile.Open(f"/eos/user/s/sgiappic/2HNL_ana/final/{b}_sel2Reco_vetoes_histo.root", "READ")
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
    outFile.cd()
    hh.Write()
    
outFile.Close()