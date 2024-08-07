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

# Set ROOT to batch mode
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
        print(f"Directory created successfully.")
    else:
        print(f"Directory already exists.")

# directory with final stage files
DIRECTORY = '/eos/user/s/sgiappic/2HNL_ana/final/' 
#directory where you want your plots to go
DIR_PLOTS = '/eos/user/s/sgiappic/www/paper/' 
#list of cuts you want to plot
CUTS = [
    "sel2Reco_vetoes",
    "sel2Reco_vetoes_notracks_nojets",
    "sel2Reco_vetoes_notracks_nojets_M80",
    "sel2Reco_vetoes_notracks_nojets_M80_10MEpt",
    "sel2Reco_vetoes_notracks_nojets_M80_10MEpt_0.8cos",
 ] 
#labels for the cuts in the plots
LABELS = {
    "sel2RecoSF_vetoes":"Two same flavor leptons, no photons",
    "sel2RecoSF_vetoes_notracks":"Two same flavor leptons, no photons, no other track",
    "sel2RecoSF_vetoes_notracks_nojets":"Two same flavor leptons, no photons, no other track, no jets",
    "sel2RecoSF_vetoes_notracks_nojets_M80":"Two same flavor leptons, no photons, no other track, no jets, M(l,l)<80 GeV",
    "sel2RecoSF_vetoes_notracks_nojets_M80_p40":"Two same flavor leptons, no photons, no other track, no jets, M(l,l)<80 GeV, p<40 GeV",
    "sel2RecoSF_vetoes_notracks_nojets_M80_p40_11.5MEpt":"Two same flavor leptons, no photons, no other track, no jets, M(l,l)<80 GeV, p<40 GeV, p_{T,miss}>11.5 GeV",
    "sel2RecoSF_vetoes_notracks_nojets_M80_11.5MEpt_p40_0.8cos":"Two same flavor leptons, no photons, no other track, no jets, M(l,l)<80 GeV, p<40 GeV, p_{T,miss}>11.5 GeV, cos\theta>-0.8",
    "sel2RecoSF_vetoes_notracks_nojets_M80_11.5MEpt_p40_0.8cos_chi_0.55d0":"Two same flavor leptons, no photons, no other track, no jets, M(l,l)<80 GeV, p<40 GeV, p_{T,miss}>11.5 GeV, cos\theta>-0.8, \chi^2<10, |d_0|>0.55 mm",

    "sel2RecoDF_vetoes":"Two different flavor leptons, no photons",
    "sel2RecoDF_vetoes_notracks":"Two different flavor leptons, no photons, no other tracks",
    "sel2RecoDF_vetoes_notracks_nojets":"Two different flavor leptons, no photons, no other tracks, no jets",
    "sel2RecoDF_vetoes_notracks_nojets_M80":"Two different flavor leptons, no photons, no other tracks, no jets, M(l,l)<80 GeV",
    "sel2RecoDF_vetoes_motracks_nojets_M80_7MEpt":"Two different flavor leptons, no photons, no other tracks, no jets, M(l,l)<80 GeV, p_{T,miss}>7 GeV",
    "sel2RecoDF_vetoes_notracks_nojets_M80_7MEpt_0.8cos":"Two different flavor leptons, no photons, no other tracks, no jets, M(l,l)<80 GeV, p_{T,miss}>11.5 GeV, cos\theta>-0.8",
    "sel2RecoDF_vetoes_notracks_nojets_M80_7MEpt_0.8cos_chi_0.5d0":"Two different flavor leptons, no photons, no other tracks, no jets, M(l,l)<80 GeV, p_{T,miss}>11.5 GeV, cos\theta>-0.8, \chi^2<10, |d_0|>0.55 mm",

    "sel2Reco_vetoes":"Two leptons, no photons",
    "sel2Gen_vetoes":"Two gen leptons, no photons",

    "selNone": "No selection",
    "sel2Reco_vetoes_notracks": "Two leptons, no photons, no other tracks",
    "sel2Reco_vetoes_notracks_nojets": "Two leptons, no photons, no other tracks, no antikt jets",
    "sel2Reco_vetoes_notracks_nojetsexcl": "Two leptons, no photons, no other tracks, no exclusive jets",

    "sel2Reco_vetoes":"Two leptons, no photons",
    "sel2Reco_vetoes_notracks":"Two leptons, no photons, no other tracks",
    "sel2Reco_vetoes_notracks_nojets":"Two leptons, no photons, no other tracks, no jets",
    "sel2Reco_vetoes_notracks_nojets_M80":"Two leptons, no photons, no other tracks, no jets, M(l,l)<80 GeV",
    "sel2Reco_vetoes_notracks_nojets_M80_10MEpt":"Two leptons, no photons, no other tracks, no jets, M(l,l)<80 GeV, p_{T,miss}>10 GeV",
    "sel2Reco_vetoes_notracks_nojets_M80_10MEpt_0.8cos":"Two leptons, no photons, no other tracks, no jets, M(l,l)<80 GeV, p_{T,miss}>10 GeV, cos#theta>-0.8",
    "sel2Reco_vetoes_notracks_nojets_M80_10MEpt_0.8cos_chi10_0.57d0":"Two leptons, no photons, no other tracks, no jets, M(l,l)<80 GeV, p_{T,miss}>10 GeV, cos#theta>-0.8, #chi^2<10, |d_{0}|>0.57 mm",
    
 }

ana_tex        = "e^{+}e^{-} #rightarrow N_{1,2} #nu, N_{1,2} #rightarrow ll#nu"
energy         = 91
collider       = 'FCC-ee'
intLumi        = 10 #ab-1

LOGY = True
LOGX = False
#now you can list all the histograms that you want to plot
VARIABLES_ALL = [
    
    #gen variables
    "n_FSGenElectron",
    "n_FSGenMuon",
    "n_FSGenLepton",
    #"n_GenN",
    "n_FSGenPhoton",

    #"FSGenLepton_e",
    #"FSGenLepton_p",
    #"FSGenLepton_pt",
    #"FSGenLepton_pz",
    #"FSGenLepton_eta",
    #"FSGenLepton_theta",
    #"FSGenLepton_phi",

    #"FSGenLepton_vertex_x",
    #"FSGenLepton_vertex_z",
    #"FSGenLepton_vertex_x_prompt",
    #"FSGenLepton_vertex_y_prompt",
    #"FSGenLepton_vertex_z_prompt",
    #"FSGenLepton_time",   

    #"FSGen_Lxy",
    #"FSGen_Lxyz",
    #"FSGen_Lxyz_prompt",
    #"FSGen_Lxy_prompt",
    #"FSGen_invMass",

    #"GenN_mass",
    #"GenN_p",
    #"GenN_e",
    #"GenN_tau",
    #"GenN_Lxyz",
    #"GenN_Lxyz_prompt",

    #reco variables
    "n_RecoTracks",
    #"n_PrimaryTracks",
    #"n_SecondaryTracks",
    #"n_jets",
    #"n_jets_excl",
    "n_antikt_jets",
    #"n_antikt_jets10",
    "n_RecoPhotons",
    "n_RecoElectrons",
    "n_RecoMuons",
    "n_RecoLeptons",

    "Reco_e",
    "Reco_p",
    "Reco_pt",
    "Reco_px",
    "Reco_py",
    "Reco_pz",
    "Reco_eta",
    "Reco_theta",
    "Reco_phi",

    "RecoTrack_absD0_prompt",
    "RecoTrack_absZ0_prompt",
    "RecoTrack_absD0_med",
    "RecoTrack_absZ0_med",
    "RecoTrack_absD0",
    "RecoTrack_absZ0",
    "RecoTrack_absD0sig",
    "RecoTrack_absD0sig_med",
    "RecoTrack_absD0sig_prompt",
    "RecoTrack_absZ0sig",
    "RecoTrack_absZ0sig_med",
    "RecoTrack_absZ0sig_prompt",
    "RecoTrack_D0cov",
    "RecoTrack_Z0cov",

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
    
    "Reco_invMass",
    "Reco_cos",
    "Reco_DR",

    "RecoMissingEnergy_e",
    "RecoMissingEnergy_p",
    "RecoMissingEnergy_pt",
    "RecoMissingEnergy_px",
    "RecoMissingEnergy_py",
    "RecoMissingEnergy_pz",
    "RecoMissingEnergy_eta",
    "RecoMissingEnergy_theta",
    "RecoMissingEnergy_phi",

]
#list of backgorunds, then legend and colors to be assigned to them
backgrounds_old = [
    'p8_ee_Zee_ecm91',
    'p8_ee_Zmumu_ecm91',
    'p8_ee_Ztautau_ecm91',
    'p8_ee_Zbb_ecm91',
    'p8_ee_Zcc_ecm91',
    'p8_ee_Zud_ecm91',
    'p8_ee_Zss_ecm91',
    'emununu',
    'tatanunu',
]

blegend = {
    'p8_ee_Zee_ecm91': 'Z #rightarrow ll',
    'p8_ee_Ztautau_ecm91': 'Z #rightarrow #tau#tau',
    'p8_ee_Zbb_ecm91': 'Z #rightarrow bb',
    'p8_ee_Zcc_ecm91': 'Z #rightarrow cc',
    'p8_ee_Zud_ecm91': 'Z #rightarrow uds',
    'emununu': 'll#nu#nu',
}

bcolors = {
    'emununu': 33,
    'p8_ee_Zee_ecm91': 40,
    'p8_ee_Ztautau_ecm91': 36,
    'p8_ee_Zbb_ecm91': 48,
    'p8_ee_Zcc_ecm91': 44,
    'p8_ee_Zud_ecm91': 20,
}

#list of signals, then legend and colors to be assigned to them
signals = [
    #'HNL_2.86e-7_30gev',
    'HNL_2.86e-12_30gev',
    'HNL_6.67e-10_30gev',
    'HNL_5e-12_60gev',
    'HNL_1.33e-7_80gev',
]

slegend = {
    'HNL_2.86e-12_30gev':"U^{2}=2.86e-12, M_{N}=30 GeV",
    'HNL_2.86e-7_30gev':"U^{2}=2.86e-7, M_{N}=30 GeV",
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

for cut in CUTS:

    extralab = LABELS[cut]

    for variable in VARIABLES_ALL:

        canvas = ROOT.TCanvas("", "", 800, 800)

        nsig = len(signals)
        nbkg = len(backgrounds) # change according to type of plots, 6 for grouped backgrounds, #len(backgrounds)

        #legend coordinates and style
        
        legsize = 0.05*nsig
        legsize2 = 0.04*nbkg
        leg = ROOT.TLegend(0.16, 0.80 - legsize, 0.45, 0.74)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetLineColor(0)
        leg.SetShadowColor(0)
        leg.SetTextSize(0.025)
        leg.SetTextFont(42)

        leg2 = ROOT.TLegend(0.65, 0.80 - legsize2, 0.85, 0.74)
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

        for b in backgrounds_old:
            fin = f"{DIRECTORY}{b}_{cut}_histo.root"
            with ROOT.TFile(fin) as tf:
                h = tf.Get(variable)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
            histos.append(hh)
            colors.append(bcolors_old[b])
            leg2.AddEntry(histos[-1], blegend_old[b], "f")
        
        #use this as an example if you want to plot two or more backgrounds in the same histogram
        '''if nbkg != 0:
            #add some backgrounds to the same histogram
            fin = f"{DIRECTORY}emununu_{cut}_histo.root"
            with ROOT.TFile(fin) as tf:
                h = tf.Get(variable)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
            fin1 = f"{DIRECTORY}tatanunu_{cut}_histo.root"
            with ROOT.TFile(fin1) as tf1:
                h1 = tf1.Get(variable)
                hh1 = copy.deepcopy(h1)
                hh1.SetDirectory(0)
            hh.Add(hh1)
            histos.append(hh)
            colors.append(bcolors["emununu"])
            leg2.AddEntry(histos[-1], blegend["emununu"], "f")
            
            fin = f"{DIRECTORY}p8_ee_Zee_ecm91_{cut}_histo.root"
            with ROOT.TFile(fin) as tf:
                h = tf.Get(variable)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
            fin1 = f"{DIRECTORY}p8_ee_Zmumu_ecm91_{cut}_histo.root"
            with ROOT.TFile(fin1) as tf1:
                h1 = tf1.Get(variable)
                hh1 = copy.deepcopy(h1)
                hh1.SetDirectory(0)
            hh.Add(hh1)
            histos.append(hh)
            colors.append(bcolors["p8_ee_Zee_ecm91"])
            leg2.AddEntry(histos[-1], blegend["p8_ee_Zee_ecm91"], "f")

            fin = f"{DIRECTORY}p8_ee_Ztautau_ecm91_{cut}_histo.root"
            with ROOT.TFile(fin) as tf:
                h = tf.Get(variable)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
            histos.append(hh)
            colors.append(bcolors["p8_ee_Ztautau_ecm91"])
            leg2.AddEntry(histos[-1], blegend["p8_ee_Ztautau_ecm91"], "f")

            fin = f"{DIRECTORY}p8_ee_Zud_ecm91_{cut}_histo.root"
            with ROOT.TFile(fin) as tf:
                h = tf.Get(variable)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
            fin1 = f"{DIRECTORY}p8_ee_Zss_ecm91_{cut}_histo.root"
            with ROOT.TFile(fin1) as tf1:
                h1 = tf1.Get(variable)
                hh1 = copy.deepcopy(h1)
                hh1.SetDirectory(0)
            hh.Add(hh1)
            histos.append(hh)
            colors.append(bcolors["p8_ee_Zud_ecm91"])
            leg2.AddEntry(histos[-1], blegend["p8_ee_Zud_ecm91"], "f")

            fin = f"{DIRECTORY}p8_ee_Zcc_ecm91_{cut}_histo.root"
            with ROOT.TFile(fin) as tf:
                h = tf.Get(variable)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
            histos.append(hh)
            colors.append(bcolors["p8_ee_Zcc_ecm91"])
            leg2.AddEntry(histos[-1], blegend["p8_ee_Zcc_ecm91"], "f")

            fin = f"{DIRECTORY}p8_ee_Zbb_ecm91_{cut}_histo.root"
            with ROOT.TFile(fin) as tf:
                h = tf.Get(variable)
                hh = copy.deepcopy(h)
                hh.SetDirectory(0)
            histos.append(hh)
            colors.append(bcolors["p8_ee_Zbb_ecm91"])
            leg2.AddEntry(histos[-1], blegend["p8_ee_Zbb_ecm91"], "f")'''

            #drawing stack for backgrounds
            hStackBkg = ROOT.THStack("hStackBkg", "")
            if LOGY==True :
                hStackBkg.SetMinimum(1e-5) #change the range to be plotted
                hStackBkg.SetMaximum(1e25) #leave some space on top for the legend
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
            hStackBkg.GetXaxis().SetTitle(histos[0].GetXaxis().GetTitle()) #get x axis label from final stage
            #hStackBkg.GetYaxis().SetTitleOffset(1.5)
            hStackBkg.GetXaxis().SetTitleOffset(1.2)
            #hStackBkg.GetXaxis().SetLimits(1, 1000)

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
                    #h.GetXaxis().SetTitle("{}".format(variable))
                    h.GetYaxis().SetRangeUser(1e-6,1e8) #range to set if only working with signals
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

        text = '#bf{#it{' + extralab + '}}'
        latex.SetTextSize(0.02)
        latex.DrawLatex(0.18, 0.76, text)

        leg.Draw()
        leg2.Draw()

        latex.SetTextAlign(31)
        text = '#it{' + leftText + '}'
        latex.SetTextSize(0.03)
        latex.DrawLatex(0.92, 0.92, text)

        # Set Logarithmic scales for both x and y axes
        if LOGY == True:
            canvas.SetLogy()
            if LOGX == True:
                canvas.SetLogx()
            canvas.SetTicks(1, 1)
            canvas.SetLeftMargin(0.14)
            canvas.SetRightMargin(0.08)
            canvas.GetFrame().SetBorderSize(12)

            canvas.RedrawAxis()
            canvas.Modified()
            canvas.Update()

            dir = DIR_PLOTS + "/" + cut + "/"
            make_dir_if_not_exists(dir)

            canvas.SaveAs(dir + variable + "_log.png")
            canvas.SaveAs(dir+ variable + "_log.pdf")
        else:
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