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

DIRECTORY = '/eos/user/s/sgiappic/2HNL_ana/final/' 
CUTS = [
    "sel2RecoSF_vetoes_tracks_M80_p40_11.5MEpt_0.8cos",
    "sel2RecoDF_vetoes_tracks_M80_7MEpt_0.8cos",
    #'sel2RecoSF_vetoes_tracks',
    #'sel2RecoDF_vetoes_tracks',
 ] # cut to rebin
VARIABLES = [
    "n_RecoTracks",
    "n_RecoPhotons",
    "n_RecoElectrons",
    "n_RecoMuons",

    "RecoElectron_e",
    "RecoElectron_p",
    "RecoElectron_pt",
    "RecoElectron_px",
    "RecoElectron_py",
    "RecoElectron_pz",
    "RecoElectron_eta",
    "RecoElectron_theta",
    "RecoElectron_phi",

    "RecoElectronTrack_absD0",
    "RecoElectronTrack_absD0_prompt",
    "RecoElectronTrack_absZ0",
    "RecoElectronTrack_absZ0_prompt",
    "RecoElectronTrack_absD0sig",
    "RecoElectronTrack_absD0sig_med",
    "RecoElectronTrack_absD0sig_prompt",
    "RecoElectronTrack_absZ0sig",
    "RecoElectronTrack_absZ0sig_prompt",
    "RecoElectronTrack_D0cov",
    "RecoElectronTrack_Z0cov",

    "RecoMuon_e",
    "RecoMuon_p",
    "RecoMuon_pt",
    "RecoMuon_px",
    "RecoMuon_py",
    "RecoMuon_pz",
    "RecoMuon_eta",
    "RecoMuon_theta",
    "RecoMuon_phi",

    "RecoMuonTrack_absD0",
    "RecoMuonTrack_absD0_prompt",
    "RecoMuonTrack_absZ0",
    "RecoMuonTrack_absZ0_prompt",
    "RecoMuonTrack_absD0sig",
    "RecoMuonTrack_absD0sig_prompt",
    "RecoMuonTrack_absZ0sig",
    "RecoMuonTrack_absZ0sig_prompt",
    "RecoMuonTrack_D0cov",
    "RecoMuonTrack_Z0cov",

    "Reco_DecayVertexLepton_x",       
    "Reco_DecayVertexLepton_y",          
    "Reco_DecayVertexLepton_z",          
    "Reco_DecayVertexLepton_x_prompt",   
    "Reco_DecayVertexLepton_y_prompt",    
    "Reco_DecayVertexLepton_z_prompt",    
    "Reco_DecayVertexLepton_chi2",    
    "Reco_DecayVertexLepton_probability", 

    "Reco_Lxy",
    "Reco_Lxy_prompt",
    "Reco_Lxyz",
    "Reco_Lxyz_prompt",

    "RecoMissingEnergy_e",
    "RecoMissingEnergy_p",
    "RecoMissingEnergy_pt",
    "RecoMissingEnergy_px",
    "RecoMissingEnergy_py",
    "RecoMissingEnergy_pz",
    "RecoMissingEnergy_eta",
    "RecoMissingEnergy_theta",
    "RecoMissingEnergy_phi",

    "Reco_e",
    "Reco_p",
    "Reco_pt",
    "Reco_px",
    "Reco_py",
    "Reco_pz",
    "Reco_eta",
    "Reco_theta",
    "Reco_phi",

    "Reco_absD0_prompt",
    "Reco_absZ0_prompt",
    "Reco_absD0_med",
    "Reco_absZ0_med",
    "Reco_absD0",
    "Reco_absZ0",
    "Reco_absD0sig",
    "Reco_absD0sig_med",
    "Reco_absD0sig_prompt",
    "Reco_absZ0sig",
    "Reco_absZ0sig_med",
    "Reco_absZ0sig_prompt",
    "Reco_D0cov",
    "Reco_Z0cov",

    "Reco_invMass",
    "Reco_cos",
    "Reco_DR",
    
 ] # variable to replot
DIR_PLOTS = '/eos/user/s/sgiappic/www/' 

ana_tex        = "e^{+}e^{-} #rightarrow N_{1,2} #nu, N_{1,2} #rightarrow ll#nu"
energy         = 91
collider       = 'FCC-ee'
intLumi        = 180

backgrounds = [
    'p8_ee_Zee_ecm91',
    'p8_ee_Zmumu_ecm91',
    'p8_ee_Ztautau_ecm91',
    #'p8_ee_Zbb_ecm91',
    #'p8_ee_Zcc_ecm91',
    #'p8_ee_Zud_ecm91',
    #'p8_ee_Zss_ecm91',
    'emununu',
    'tatanunu',
]

blegend = {
    'p8_ee_Zee_ecm91': 'Z #rightarrow ee',
    'p8_ee_Zmumu_ecm91': 'Z #rightarrow #mu#mu',
    'p8_ee_Ztautau_ecm91': 'Z #rightarrow #tau#tau',
    'p8_ee_Zbb_ecm91': 'Z #rightarrow bb',
    'p8_ee_Zcc_ecm91': 'Z #rightarrow cc',
    'p8_ee_Zud_ecm91': 'Z #rightarrow ud',
    'p8_ee_Zss_ecm91': 'Z #rightarrow ss',
    'emununu': 'e#mu#nu#nu',
    'tatanunu': '#tau#tau#nu#nu',
}

bcolors = {
    'p8_ee_Zee_ecm91': 29,
    'p8_ee_Zmumu_ecm91': 32,
    'p8_ee_Ztautau_ecm91': 34,
    'p8_ee_Zbb_ecm91': 48,
    'p8_ee_Zcc_ecm91': 44,
    'p8_ee_Zud_ecm91': 41,
    'p8_ee_Zss_ecm91': 20,
    'emununu': 40,
    'tatanunu': 38,
}

signals = [
    'HNL_2.86e-12_30gev',
    'HNL_2.86e-7_30gev',
    #'HNL_5e-12_50gev',
    #'HNL_4e-10_80gev',
    'HNL_4e-12_50gev',
    'HNL_2.86e-8_80gev',
]

slegend = {
    'HNL_2.86e-12_30gev': 'U^{2}=2.86e-12, M_{N}=30 GeV',
    'HNL_2.86e-7_30gev': 'U^{2}=2.86e-7, M_{N}=30 GeV',
    'HNL_4e-12_50gev': 'U^{2}=4e-12, M_{N}=50 GeV',
    'HNL_2.86e-8_80gev': 'U^{2}=2.86e-8, M_{N}=80 GeV',
    'HNL_5e-12_50gev': 'U^{2}=5e-12, M_{N}=50 GeV',
    'HNL_4e-10_80gev': 'U^{2}=4e-10, M_{N}=80 GeV',
}

scolors = {
    'HNL_2.86e-12_30gev': ROOT.kAzure+6,
    'HNL_2.86e-7_30gev': ROOT.kOrange+1,
    'HNL_5e-12_50gev': ROOT.kRed-4,
    'HNL_4e-10_80gev': ROOT.kBlue-4,
    'HNL_4e-12_50gev': ROOT.kBlue-4,
    'HNL_2.86e-8_80gev': ROOT.kRed-4,
}

for cut in CUTS:

    for variable in VARIABLES:

        canvas = ROOT.TCanvas("", "", 800, 800)

        nsig = len(signals)
        nbkg = len(backgrounds)

        #legend coordinates and style
        legsize = 0.04*nsig
        legsize2 = 0.04*nbkg
        leg = ROOT.TLegend(0.16, 0.80 - legsize, 0.45, 0.78)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetLineColor(0)
        leg.SetShadowColor(0)
        leg.SetTextSize(0.025)
        leg.SetTextFont(42)

        leg2 = ROOT.TLegend(0.70, 0.80 - legsize2, 0.88, 0.78)
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
            fin = f"{DIRECTORY}{s}_{cut}_histo.root"
            with ROOT.TFile(fin) as tf:
                h = tf.Get(variable)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
            histos.append(hh)
            colors.append(scolors[s])
            leg.AddEntry(histos[-1], slegend[s], "l")

        for b in backgrounds:
            fin = f"{DIRECTORY}{b}_{cut}_histo.root"
            with ROOT.TFile(fin) as tf:
                h = tf.Get(variable)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
            histos.append(hh)
            colors.append(bcolors[b])
            leg2.AddEntry(histos[-1], blegend[b], "f")

        #drawing stack for backgrounds
        hStackBkg = ROOT.THStack("hStackBkg", "")
        hStackBkg.SetMinimum(1e-6)
        hStackBkg.SetMaximum(1e23)
        BgMCHistYieldsDic = {}
        for i in range(nsig, nsig+nbkg):
            h = histos[i]
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
            h.SetLineWidth(3)
            h.SetLineColor(colors[i])
            h.Draw("HIST SAME")

        hStackBkg.GetYaxis().SetTitle("Events")
        hStackBkg.GetXaxis().SetTitle("{}".format(variable))
        #hStackBkg.GetYaxis().SetTitleOffset(1.5)
        hStackBkg.GetXaxis().SetTitleOffset(1.2)
        #hStackBkg.GetXaxis().SetLimits(1, 1000)

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

        dir = DIR_PLOTS + "/" + cut + "/"
        make_dir_if_not_exists(dir)

        canvas.SaveAs(dir + variable + ".png")
        canvas.SaveAs(dir+ variable + ".pdf")