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
import numpy as np

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
directory = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/final_res/mumu/"
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
   
    #"n_FSGenElectron",
    #"FSGenElectron_e",
    #"FSGenElectron_p",
    #"FSGenElectron_pt",
    #"FSGenElectron_px",
    #"FSGenElectron_py",
    #"FSGenElectron_pz",
    #"FSGenElectron_y",
    #"FSGenElectron_eta",
    #"FSGenElectron_theta",
    #"FSGenElectron_phi",
    #"FSGenElectron_charge",
    #"FSGenElectron_mass",

    #"n_FSGenMuon",
    #"FSGenMuon_e",
    #"FSGenMuon_p",
    #"FSGenMuon_pt",
    #"FSGenMuon_px",
    #"FSGenMuon_py",
    #"FSGenMuon_pz",
    #"FSGenMuon_y",
    #"FSGenMuon_eta",
    #"FSGenMuon_theta",
    #"FSGenMuon_phi",
    #"FSGenMuon_charge",
    #"FSGenMuon_mass",

    #"n_FSGenPhoton",
    #"FSGenPhoton_e",
    #"FSGenPhoton_p",
    #"FSGenPhoton_pt",
    #"FSGenPhoton_px",
    #"FSGenPhoton_py",
    #"FSGenPhoton_pz",
    #"FSGenPhoton_y",
    #"FSGenPhoton_eta",
    #"FSGenPhoton_theta",
    #"FSGenPhoton_phi",
    #"FSGenPhoton_charge",

    #"n_RecoElectrons",
    #"RecoElectron_e",
    #"RecoElectron_p",
    #"RecoElectron_pt",
    #"RecoElectron_px",
    #"RecoElectron_py",
    #"RecoElectron_pz",
    #"RecoElectron_y",
    #"RecoElectron_eta",
    #"RecoElectron_theta",
    #"RecoElectron_phi",
    #"RecoElectron_charge",
    #"RecoElectron_mass",
    #"Electron_p_res_0_20",
    #"Electron_p_res_20_40",
    #"Electron_p_res_40_60",
    #"Electron_p_res_60_higher", 
    #"Electron_p_res_total",

    #"n_RecoMuons",
    #"RecoMuon_e",
    #"RecoMuon_p",
    #"RecoMuon_pt",
    #"RecoMuon_px",
    #"RecoMuon_py",
    #"RecoMuon_pz",
    #"RecoMuon_y",
    #"RecoMuon_eta",
    #"RecoMuon_theta",
    #"RecoMuon_phi",
    #"RecoMuon_charge",
    #"RecoMuon_mass",
    #"Muon_p_res_0_20",
    #"Muon_p_res_20_40",
    #"Muon_p_res_40_60",
    #"Muon_p_res_60_higher", 
    "Muon_p_res_total",

    #"n_RecoPhotons",
    #"RecoPhoton_e",
    #"RecoPhoton_p",
    #"RecoPhoton_pt",
    #"RecoPhoton_px",
    #"RecoPhoton_py",
    #"RecoPhoton_pz",
    #"RecoPhoton_y",
    #"RecoPhoton_eta",
    #"RecoPhoton_theta",
    #"RecoPhoton_phi",
    #"RecoPhoton_charge",
    #"RecoPhoton_mass",
    #"Photon_p_res_0_20",
    #"Photon_p_res_20_40",
    #"Photon_p_res_40_60",
    #"Photon_p_res_60_higher", 
    #"Photon_p_res_total",

    #"n_GenDown",
    #"GenDown_e",
    #"GenDown_p",
    #"GenDown_pt",
    #"GenDown_px",
    #"GenDown_py",
    #"GenDown_pz",
    #"GenDown_y",
    #"GenDown_eta",
    #"GenDown_theta",
    #"GenDown_phi",
    #"GenDown_charge",
    #"GenDown_mass",

    #"n_TagJet_kt2",
    #"TagJet_kt2_px", 
    #"TagJet_kt2_py",    
    #"TagJet_kt2_pz",      
    #"TagJet_kt2_p",  
    #"TagJet_kt2_pt",    
    #"TagJet_kt2_phi", 
    #"TagJet_kt2_eta",     
    #"TagJet_kt2_theta",          
    #"TagJet_kt2_e",     
    #"TagJet_kt2_mass",        
    #"TagJet_kt2_charge",  

    #####"n_genBottoms",
    #"genBottom_p",
    #"genBottom_e",
    #"genBottom_pt",
    #"genBottom_px",
    #"genBottom_py",
    #"genBottom_pz",
    #"genBottom_eta",
    #"genBottom_theta",
    #"genBottom_phi",
    #"genBottom_charge",
    #"genBottom_mass",

    #"n_FSGenChargedHadrons",
    #"FSGenChargedHadrons_p",
    #"FSGenChargedHadrons_eta",

    #"n_FSGenNeutralHadrons",
    #"FSGenNeutralHadrons_p",
    #"FSGenNeutralHadrons_eta",

    #"n_NeutralHadron", 
    #"NeutralHadron_p",
    #"NeutralHadron_eta",

    #"n_ChargedHadron",
    #"ChargedHadron_p",
    #"ChargedHadron_eta",

    #"n_NHadron_low_dR",  
    #"NHadron_low_dR_p",     
    #"NHadron_low_dR_e",
    #"NHadron_low_dR_pt",
    #"NHadron_low_dR_px",
    #"NHadron_low_dR_py",
    #"NHadron_low_dR_pz",
    #"NHadron_low_dR_eta",
    #"NHadron_low_dR_theta",
    #"NHadron_low_dR_phi",
    #"NHadron_low_dR_charge",
    #"NHadron_low_dR_mass",
    #"NHadron_low_dR_p_res_total",
    #"NHadron_low_dR_MCPDG_1",
    #"NHadron_low_dR_MCPDG_2",


    #"n_NHadron_high_dR",
    #"NHadron_high_dR_p",        
    #"NHadron_high_dR_e",
    #"NHadron_high_dR_pt",
    #"NHadron_high_dR_px",
    #"NHadron_high_dR_py",
    #"NHadron_high_dR_pz",
    #"NHadron_high_dR_eta",
    #"NHadron_high_dR_theta",
    #"NHadron_high_dR_phi",
    #"NHadron_high_dR_charge",
    #"NHadron_high_dR_mass",
    #"NHadron_high_dR_p_res_total", 
    #"NHadron_high_dR_MCPDG_1",
    #"NHadron_high_dR_MCPDG_2",

    #"n_TagJet_kt2",
    #"TagJet_kt2_eta",
    #"Dijet_mass",

    #"CHadron_dR",
    #"NHadron_dR",

    #"n_DeltaNeutralHadrons",

    #"NHadron_p_res_total",
    #"CHadron_p_res_total",
    #"NHadron_low_dR_p_res_total",
    #"NHadron_high_dR_p_res_total",
    #"jet_reso",
]

#directory where you want your plots to go
DIR_PLOTS = '/web/awiedl/public_html/detector_res/mumu/' 

#labels for the cuts in the plots
LABELS = {
    "selReco": "No additional selection",
 }

ana_tex_cat = "e^{+}e^{-} #rightarrow Z H, Z #rightarrow #nu #nu, H #rightarrow #mu #mu "

energy         = 240
collider       = 'FCC-ee'
intLumi        = 10.8 #ab-1
LOGY = False

#list of backgorunds, then legend and colors to be assigned to them
backgrounds_all = [
]

legend = {
    'IDEA_events_050238459':'IDEA',
    'CMS_Phase2_events_050238459':'CMS Phase2',
    'CMS_Phase1_events_050238459':'CMS Phase1',
    'IDEA_CMS2':'IDEA sf=~3.56310',
    'IDEA_CMS1':'IDEA sf=~6.63972',
}

legcolors = {
    'IDEA_events_050238459':ROOT.kGreen,
    'CMS_Phase2_events_050238459':ROOT.kCyan,
    'CMS_Phase1_events_050238459':ROOT.kBlue,
    'IDEA_CMS2':ROOT.kOrange,
    'IDEA_CMS1':ROOT.kBlack,
}

#list of signals, then legend and colors to be assigned to them
signals = [
    'IDEA_events_050238459',
    'IDEA_CMS2',
    'IDEA_CMS1',
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
                if('res' in variable):
                    bin1 = h.FindFirstBinAbove(h.GetMaximum()/2)
                    bin2 = h.FindLastBinAbove(h.GetMaximum()/2)
                    FWHM = h.GetBinCenter(bin2) - h.GetBinCenter(bin1)
                    maxi = h.GetMaximum()
                    maxi_bin = h.GetMaximumBin()
                    HM = h.Integral(maxi_bin-5, maxi_bin+5)/2.
                    left_bin = -1000
                    for k in range(1990):
                        if(h.Integral(k, k+10) >= HM and left_bin == -1000):
                            left_bin = k + 5
                            print(left_bin)
                        if(k > maxi_bin and h.Integral(k, k+10) <= HM):
                            right_bin = k + 5
                            print(right_bin)
                            break
                    FWHM_scan = h.GetBinCenter(right_bin) - h.GetBinCenter(left_bin)

                    #gaussFit = ROOT.TF1("gaussfit","gaus") 
                    #h.Fit(gaussFit, "E")
                    #mean = gaussFit.GetParameter(1)
                    #sigma = gaussFit.GetParameter(2)
                    #with open('/work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/output.txt', "a") as file:
                    #    file.write(f"{variable}\n")
                    #    file.write(f"{signals[i]}\n")
                    #    file.write(f"Mean: {mean}\n")
                    #    file.write(f"Sigma: {sigma}\n")
                    #    file.write(f"2Sigma: {sigma*2}\n")
                    #    file.write(f"FWHM: {FWHM}\n")
                    #    file.write(f"FWHM scan: {FWHM_scan}\n\n")
                    leg.AddEntry(histos[-1], legend[s] + ', FWHM: ' + str(round(FWHM_scan,5)), "l") #
                else:
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
                #if('Dijet' in variable):
                #    bin1 = h.FindFirstBinAbove(h.GetMaximum()/2)
                #    bin2 = h.FindLastBinAbove(h.GetMaximum()/2)
                #    FWHM = h.GetBinCenter(bin2) - h.GetBinCenter(bin1)
                #    maxi = h.GetMaximum()
                #    maxi_bin = h.GetMaximumBin()
                #    print(maxi)
                #    print(maxi_bin)
                #    HM = h.Integral(maxi_bin-5, maxi_bin+5)/2.
                #    #bins = np.linspace(-0.5, 0.5, 1990, True)
                #    left_bin = -1000
                #    for k in range(1990):
                #        if(h.Integral(k, k+10) >= HM and left_bin == -1000):
                #            left_bin = k + 5
                #            print(left_bin)
                #        if(k > maxi_bin and h.Integral(k, k+10) <= HM):
                #            right_bin = k + 5
                #            print(right_bin)
                #            break
                #    FWHM_scan = h.GetBinCenter(right_bin) - h.GetBinCenter(left_bin)

                    #gaussFit = ROOT.TF1("gaussfit","gaus") 
                    #h.Fit(gaussFit, "E")
                    #mean = gaussFit.GetParameter(1)
                    #sigma = gaussFit.GetParameter(2)
                #    with open('/work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/output.txt', "a") as file:
                #        file.write(f"{variable}\n")
                #        file.write(f"{signals[i]}\n")
                    #    file.write(f"Mean: {mean}\n")
                    #    file.write(f"Sigma: {sigma}\n")
                    #    file.write(f"2Sigma: {sigma*2}\n")
                    #    file.write(f"FWHM: {FWHM}\n")
                #        file.write(f"FWHM scan: {FWHM_scan}\n\n")
                
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

        # fitting resolution
        #if('res' in variable):
        #    for i in range(nsig):
        #        h = histos[i]
         #       gaussFit = ROOT.TF1("gaussfit","gaus",-0.05,0.05) 
        #        h.Fit(gaussFit, "EV")
        #        mean = gaussFit.GetParameter(1)
        #        sigma = gaussFit.GetParameter(2)
        #        FWHM = sigma * 2.3548
        #        with open('/work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/output.txt', "a") as file:
        #            file.write(f"{variable}\n")
        #            file.write(f"{signals[i]}\n")
        #            file.write(f"Mean: {mean}\n")
        #            file.write(f"Sigma: {sigma}\n")
        #            file.write(f"FWHM: {FWHM}\n\n")