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
DIRECTORY = "/ceph/sgiappic/HiggsCP/CPReco/final_explicit_new/"

#directory where you want your plots to go
DIR_PLOTS = '/web/sgiappic/public_html/HiggsCP/Reco_explicit/' 
#list of cuts you want to plot
CUTS = [
    "selReco_ILC20chi",
    "selReco_CMS",
    #"selDPhi",
 ] 
#labels for the cuts in the plots
LABELS = {
    "selReco": "No additional selection",
    "selReco_ILC20chi": "p_{T,miss} (#chi^{2})<20 GeV",
    "selGen": "No additional selection",
    "selReco_CMS":"No additional selection",
    "selDPhi":"KinGen_hh_norm_DPhi<0.5",
 }

label = "_QQpinu_SM"
ana_tex        = "e^{+}e^{-} #rightarrow Z H, H #rightarrow #tau#tau (#pi#nu), SM"
energy         = 240
collider       = 'FCC-ee'
intLumi        = 10.8 #ab-1
LOGY = False


#list of signals, then legend and colors to be assigned to them
signals_old = [
    #'noISR_e+e-_noCuts_EWonly',
    #'noISR_e+e-_noCuts_cehre_m1',
    #'noISR_e+e-_noCuts_cehre_p1',
    #'noISR_e+e-_noCuts_cehim_m1',
    #'noISR_e+e-_noCuts_cehim_p1',

    #'EWonly_taudecay_2Pi2Nu',
    #'cehim_m1_taudecay_2Pi2Nu',
    #'cehim_p1_taudecay_2Pi2Nu',
    #'cehre_m1_taudecay_2Pi2Nu',
    #'cehre_p1_taudecay_2Pi2Nu',

    #'EWonly_taudecay_PiPi0Nu',
    #'cehim_m1_taudecay_PiPi0Nu',
    #'cehim_p1_taudecay_PiPi0Nu',
    #'cehre_m1_taudecay_PiPi0Nu',
    #'cehre_p1_taudecay_PiPi0Nu',

    #'cehim_m5_taudecay_2Pi2Nu',
    #'cehim_p5_taudecay_2Pi2Nu',
    #'cehre_m5_taudecay_2Pi2Nu',
    #'cehre_p5_taudecay_2Pi2Nu',

    #'cehim_m2_taudecay_2Pi2Nu',
    #'cehim_p2_taudecay_2Pi2Nu',
    #'cehre_m2_taudecay_2Pi2Nu',
    #'cehre_p2_taudecay_2Pi2Nu',

    #'cehim_p0p1_taudecay_2Pi2Nu',
    #'cehim_m0p1_taudecay_2Pi2Nu',
    #'cehre_m0p1_taudecay_2Pi2Nu',
    #'cehre_p0p1_taudecay_2Pi2Nu',

    #'cehim_p10_taudecay_2Pi2Nu',
    #'cehim_m10_taudecay_2Pi2Nu',

    #'cehim_p10_taudecay_2Pi2Nu',
    #'cehim_m10_taudecay_2Pi2Nu',

    #'wzp6_ee_eeH_Htautau_ecm240',
    "e+e-_qqH_H2Pi2Nu",
]

signals = [
    "sm",
    "sm_lin_quad_cehim_m1",
    "sm_lin_quad_cehim",
    "sm_lin_quad_cehre_m1",
    "sm_lin_quad_cehre_p1",
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

    'EWonly_taudecay_PiPi0Nu':"Z(ee)H(#tau#tau), SM",
    'cehim_m1_taudecay_PiPi0Nu':"Z(ee)H(#tau#tau), CPV -1",
    'cehim_p1_taudecay_PiPi0Nu':"Z(ee)H(#tau#tau), CPV +1",
    'cehre_m1_taudecay_PiPi0Nu':"Z(ee)H(#tau#tau), CPC -1",
    'cehre_p1_taudecay_PiPi0Nu':"Z(ee)H(#tau#tau), CPC +1",

    'sm':"Z(ee)H(#tau#tau), SM",
    'sm_lin_quad_cehim_m1':"Z(ee)H(#tau#tau), CPV -1",
    'sm_lin_quad_cehim':"Z(ee)H(#tau#tau), CPV +1",
    'sm_lin_quad_cehre_m1':"Z(ee)H(#tau#tau), CPC -1",
    'sm_lin_quad_cehre_p1':"Z(ee)H(#tau#tau), CPC +1",

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

    'EWonly_taudecay_PiPi0Nu':ROOT.kRed-9,
    'cehim_m1_taudecay_PiPi0Nu':ROOT.kBlue-9,
    'cehim_p1_taudecay_PiPi0Nu':ROOT.kBlue-7,
    'cehre_m1_taudecay_PiPi0Nu':ROOT.kGreen-8,
    'cehre_p1_taudecay_PiPi0Nu':ROOT.kGreen-6,

    'sm':ROOT.kRed-9,
    'sm_lin_quad_cehim_m1':ROOT.kBlue-9,
    'sm_lin_quad_cehim':ROOT.kBlue-7,
    'sm_lin_quad_cehre_m1':ROOT.kGreen-8,
    'sm_lin_quad_cehre_p1':ROOT.kGreen-6,

    'cehim_m5_taudecay_2Pi2Nu':ROOT.kBlue-9,
    'cehim_p5_taudecay_2Pi2Nu':ROOT.kBlue-7,
    'cehre_m5_taudecay_2Pi2Nu':ROOT.kGreen-8,
    'cehre_p5_taudecay_2Pi2Nu':ROOT.kGreen-6,

    'cehim_m2_taudecay_2Pi2Nu':ROOT.kBlue-9,
    'cehim_p2_taudecay_2Pi2Nu':ROOT.kBlue-7,
    'cehre_m2_taudecay_2Pi2Nu':ROOT.kGreen-8,
    'cehre_p2_taudecay_2Pi2Nu':ROOT.kGreen-6,

    'cehim_m0p1_taudecay_2Pi2Nu':ROOT.kBlue-9,
    'cehim_p0p1_taudecay_2Pi2Nu':ROOT.kBlue-7,
    'cehre_m0p1_taudecay_2Pi2Nu':ROOT.kGreen-8,
    'cehre_p0p1_taudecay_2Pi2Nu':ROOT.kGreen-6,

    'cehim_m10_taudecay_2Pi2Nu':ROOT.kBlue-9,
    'cehim_p10_taudecay_2Pi2Nu':ROOT.kBlue-7,
}

### main

canvas = ROOT.TCanvas("", "", 1000, 1000)
#canvas.SetTicks(1, 1)
canvas.cd()

nsig = 4

#legend coordinates and style
legsize = 0.04*nsig
leg = ROOT.TLegend(0.16, 0.70 - legsize, 0.45, 0.70)
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
style = []

#loop over files for signals and backgrounds and assign corresponding colors and titles
for s in signals_old:
    fin = f"{DIRECTORY}{s}_{CUTS[0]}_histo.root"
    with ROOT.TFile(fin) as tf:
        h = tf.Get("RecoH_mass")#s + "_" + variable
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(ROOT.kBlack)
    style.append(1)
    leg.AddEntry(histos[-1], "Reconstructed", "l")

for s in signals_old:
    fin = f"{DIRECTORY}{s}_{CUTS[1]}_histo.root"
    with ROOT.TFile(fin) as tf:
        h = tf.Get("Higgs_mass")#s + "_" + variable
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(ROOT.kRed)
    style.append(3)
    leg.AddEntry(histos[-1], "Visible", "l")

for s in signals_old:
    fin = f"{DIRECTORY}{s}_{CUTS[1]}_histo.root"
    with ROOT.TFile(fin) as tf:
        h = tf.Get("Collinear_mass")#s + "_" + variable
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(ROOT.kBlue)
    style.append(4)
    leg.AddEntry(histos[-1], "Collinear", "l")

for s in signals_old:
    fin = f"{DIRECTORY}{s}_{CUTS[1]}_histo.root"
    with ROOT.TFile(fin) as tf:
        h = tf.Get("Recoil")#s + "_" + variable
        hh = copy.deepcopy(h)
        hh.SetDirectory(0)
    histos.append(hh)
    colors.append(ROOT.kGreen)
    style.append(2)
    leg.AddEntry(histos[-1], "Recoil", "l")

# add the signal histograms
max = 0
for i in range(nsig):
    h = histos[i]
    if h.GetMaximum()>max:
        max = h.GetMaximum()

for i in range(nsig):
    h = histos[i]
    h.SetLineWidth(3)
    h.SetLineColor(colors[i])
    h.SetLineStyle(style[i])  # 1 = solid, 2 = dashed, 3 = dotted, etc.
    if i == 0:
        h.Draw("HIST")
        h.GetYaxis().SetTitle("Events (normalised)")
        h.GetXaxis().SetTitle("M_{H} [GeV]")
        h.GetYaxis().SetTitleOffset(1.2)
        if h.Integral()>0:
            h.Scale(1./(h.Integral()))
        max = h.GetMaximum()
        h.GetYaxis().SetRangeUser(0, max*2)
        #h.GetXaxis().SetLimits(20, 200)
    else: 
        if h.Integral()>0:
            h.Scale(1./(h.Integral()))
        h.Draw("HIST SAME")

extralab = "No additional selection"

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

text = '#bf{#it{' + extralab + '}}'
latex.SetTextSize(0.02)
latex.DrawLatex(0.18, 0.74, text)

leg.Draw()

latex.SetTextAlign(31)
text = '#it{' + leftText + '}'
latex.SetTextSize(0.03)

dir = DIR_PLOTS + "/"
make_dir_if_not_exists(dir)

if (LOGY == True):

    canvas.SaveAs(dir + "log/" + variable + ".png")
    canvas.SaveAs(dir + "log/" + variable + ".pdf")

else:

    canvas.SaveAs(dir + "Masses" + label + ".png")
    canvas.SaveAs(dir+ "Masses" + label + ".pdf")