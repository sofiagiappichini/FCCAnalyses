import uproot
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import uproot

def file_exists(file_path):
    return os.path.isfile(file_path)

signals = [
    'noISR_e+e-_noCuts_EWonly',
    'noISR_e+e-_noCuts_cehre_m1',
    'noISR_e+e-_noCuts_cehre_p1',
    'noISR_e+e-_noCuts_cehim_m1',
    'noISR_e+e-_noCuts_cehim_p1',
]

slegend = {
    'noISR_e+e-_noCuts_EWonly':"Z(ee)H(#tau#tau), SM",
    'noISR_e+e-_noCuts_cehim_m1':"Z(ee)H(#tau#tau), CPV -1",
    'noISR_e+e-_noCuts_cehim_p1':"Z(ee)H(#tau#tau), CPV +1",
    'noISR_e+e-_noCuts_cehre_m1':"Z(ee)H(#tau#tau), CPC -1",
    'noISR_e+e-_noCuts_cehre_p1':"Z(ee)H(#tau#tau), CPC +1",
}

scolors = {
    'noISR_e+e-_noCuts_EWonly':ROOT.kRed-9,
    'noISR_e+e-_noCuts_cehim_m1':ROOT.kBlue-9,
    'noISR_e+e-_noCuts_cehim_p1':ROOT.kBlue-7,
    'noISR_e+e-_noCuts_cehre_m1':ROOT.kGreen-8,
    'noISR_e+e-_noCuts_cehre_p1':ROOT.kGreen-6,
}

replacement_bkgs = [
    'p8_ee_WW_ecm240',
    'p8_ee_Zqq_ecm240',
    'p8_ee_ZZ_ecm240',
    
    'wzp6_ee_tautau_ecm240',
    'wzp6_ee_mumu_ecm240',
    'wzp6_ee_ee_Mee_30_150_ecm240',

    'wzp6_ee_tautauH_Htautau_ecm240',
    'wzp6_ee_tautauH_Hbb_ecm240',
    'wzp6_ee_tautauH_Hcc_ecm240',
    'wzp6_ee_tautauH_Hss_ecm240',
    'wzp6_ee_tautauH_Hgg_ecm240',
    'wzp6_ee_tautauH_HWW_ecm240',
    'wzp6_ee_tautauH_HZZ_ecm240',

    'wzp6_egamma_eZ_Zmumu_ecm240',
    'wzp6_egamma_eZ_Zee_ecm240',
    'wzp6_gammae_eZ_Zmumu_ecm240',
    'wzp6_gammae_eZ_Zee_ecm240',

    'wzp6_gaga_tautau_60_ecm240',
    'wzp6_gaga_mumu_60_ecm240',
    'wzp6_gaga_ee_60_ecm240',

    'wzp6_ee_nuenueZ_ecm240',

    'wzp6_ee_nunuH_Hbb_ecm240',
    'wzp6_ee_nunuH_Hcc_ecm240',
    'wzp6_ee_nunuH_Hss_ecm240',
    'wzp6_ee_nunuH_Hgg_ecm240',
    'wzp6_ee_nunuH_HWW_ecm240',
    'wzp6_ee_nunuH_HZZ_ecm240',

    'wzp6_ee_eeH_Hbb_ecm240',
    'wzp6_ee_eeH_Hcc_ecm240',
    'wzp6_ee_eeH_Hss_ecm240',
    'wzp6_ee_eeH_Hgg_ecm240',
    'wzp6_ee_eeH_HWW_ecm240',
    'wzp6_ee_eeH_HZZ_ecm240',

    'wzp6_ee_mumuH_Hbb_ecm240',
    'wzp6_ee_mumuH_Hcc_ecm240',
    'wzp6_ee_mumuH_Hss_ecm240',
    'wzp6_ee_mumuH_Hgg_ecm240',
    'wzp6_ee_mumuH_HWW_ecm240',
    'wzp6_ee_mumuH_HZZ_ecm240',

    'wzp6_ee_bbH_Hbb_ecm240',
    'wzp6_ee_bbH_Hcc_ecm240',
    'wzp6_ee_bbH_Hss_ecm240',
    'wzp6_ee_bbH_Hgg_ecm240',
    'wzp6_ee_bbH_HWW_ecm240',
    'wzp6_ee_bbH_HZZ_ecm240',

    'wzp6_ee_ccH_Hbb_ecm240',
    'wzp6_ee_ccH_Hcc_ecm240',
    'wzp6_ee_ccH_Hss_ecm240',
    'wzp6_ee_ccH_Hgg_ecm240',
    'wzp6_ee_ccH_HWW_ecm240',
    'wzp6_ee_ccH_HZZ_ecm240',

    'wzp6_ee_ssH_Hbb_ecm240',
    'wzp6_ee_ssH_Hcc_ecm240',
    'wzp6_ee_ssH_Hss_ecm240',
    'wzp6_ee_ssH_Hgg_ecm240',
    'wzp6_ee_ssH_HWW_ecm240',
    'wzp6_ee_ssH_HZZ_ecm240',

    'wzp6_ee_qqH_Hbb_ecm240',
    'wzp6_ee_qqH_Hcc_ecm240',
    'wzp6_ee_qqH_Hss_ecm240',
    'wzp6_ee_qqH_Hgg_ecm240',
    'wzp6_ee_qqH_HWW_ecm240',
    'wzp6_ee_qqH_HZZ_ecm240',

]

# directory with final stage files
DIRECTORY = "/ceph/sgiappic/HiggsCP/CP/final_tag/"

#directory where you want your plots to go
DIR_PLOTS = '/web/sgiappic/public_html/HiggsCP/Oneprong_tag/' 
#list of cuts you want to plot
CUTS = [
    "selReco",
    #"selGen",
 ] 
#labels for the cuts in the plots
LABELS = {
    "selReco": "No additional selection",
    "selGen": "No additional selection",
 }

ana_tex        = "e^{+}e^{-} #rightarrow Z H, H #rightarrow #tau#tau (one prong)"# (#pi#pi^{0}#nu)"
energy         = 240
collider       = 'FCC-ee'
intLumi        = 10.8 #ab-1
LOGY = False

# Define the tree name
tree_name = "events"

# Select the leaf you want to analyze
# automatic checks also prompt variable to get more accurate values
leaf_name = [
    "Pi_DEta_y",
    "Pi_DPhi_y",

]

CUT = [
    "selReco",
]

for cut in CUT:
    for leaf in leaf_name:

        asymmetry = []

            # Loop through each replacement word
            for replacement_word in signals:

                neg_events = []
                pos_events = []
            
                # Define the ROOT file path
                histo_file_path = DIRECTORY + "{}_".format(replacement_word) + cut + "_histo.root"

                output_file = DIRECTORY + "{}_asymmetries".format(replacement_word) + cut + "_histo.root""

                if file_exists(histo_file_path):

                    # Get the selected leaf from the tree
                    histo_file = uproot.open(histo_file_path)

                    selected_leaf = histo_file[leaf]

                    # Get scaled number of events from histograms, array
                    y_values = selected_leaf.values()

                    # Get bin edges in arrays
                    bin_edges = selected_leaf.axis().edges()

                    temp_bkg = []

                    # get associated value of variable from the bin and store the high edge (low edge of successive bin)
                    for i in range(0, len(bin_edges)-1, 1): #exclude one of the edges as bins have both 0. and max but the content is n-1
                        if bin_edges[i]<0:
                            neg_events.append((y_values[i]))
                        else:
                            pos_events.append((y_values[i]))

                    asymmetry.append((sum(pos_events) - sum(neg_events)) / (sum(pos_events) + sum(neg_events)))

        # plot in ROOT (same as replot_ratio.py)

        canvas = ROOT.TCanvas("", "", 1000, 1000)
        #canvas.SetTicks(1, 1)

        pad = ROOT.TPad("", "", 0.0, 0.3, 1.0, 1.0)
        
        pad2 = ROOT.TPad("", "", 0.0, 0.0, 1.0, 0.3)

        pad.Draw()
        pad2.Draw()
        canvas.cd()
        pad.cd()

        nsig = len(signals)

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

        # add the signal histograms

        for i in range(nsig):
            h = histos[i]
            h.SetLineWidth(3)
            h.SetLineColor(colors[i])
            if i == 0:
                h.Draw("HIST")
                h.GetYaxis().SetTitle("Events")
                #h.GetXaxis().SetTitle(histos[0].GetXaxis().GetTitle())
                #h.GetXaxis().SetTitleOffset(1.2)
                #if h.Integral()>0:
                    #h.Scale(1./(h.Integral()))
                max_y = h.GetMaximum() 
                h.GetYaxis().SetRangeUser(0, max_y*2.5)
            else: 
                #if h.Integral()>0:
                    #h.Scale(1./(h.Integral()))
                h.Draw("HIST SAME")
        
        extralab = LABELS[cut]

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


        pad.SetLeftMargin(0.14)
        pad.SetRightMargin(0.08)
        pad.GetFrame().SetBorderSize(12)
        pad.SetBottomMargin(0)

        canvas.cd()
        
        #### ratio plot ####
        pad2.cd()
 
        legend2size = 0.1*(nsig-1)
        legend2 = ROOT.TLegend(0.16, 0.90 - legend2size, 0.45, 0.74)
        legend2.SetFillColor(0)
        legend2.SetFillStyle(0)
        legend2.SetLineColor(0)
        legend2.SetShadowColor(0)
        legend2.SetTextSize(0.04)
        legend2.SetTextFont(42)

        #dummy plot
        #drawing error bar for SM sample centered at 1 (ratio with itself) but error from the full scale
        #dummy = histos[0].Clone("")
        #for i in range(dummy.GetNbinsX()):
        #    dummy.SetBinContent(i,1.0)
        dummy = histos[0].Clone("")
        dummy.Divide(histos[0])
        #for i in range(dummy.GetNbinsX()+1):
        #    dummy.SetBinContent(i,1.0)
        #    dummy.SetBinError(i, histos[0].GetBinError(i)/histos[0].GetBinContent(i))
        dummy.SetFillColor(ROOT.kGray)
        dummy.SetLineColor(0)
        #dummy.SetMarkerColor(0)
        dummy.SetLineWidth(0)
        #dummy.SetMarkerSize(0)

        dummy.GetYaxis().SetTitle("Ratio")
        dummy.GetYaxis().SetTitleSize(0.08)
        dummy.GetYaxis().CenterTitle()
        #adjust the range for the ratio here
        dummy.GetYaxis().SetRangeUser(0.5,1.5)
        dummy.GetYaxis().SetLabelSize(0.08)
        dummy.GetYaxis().SetNdivisions(5)
        dummy.GetYaxis().SetTitleOffset(0.5)

        dummy.GetXaxis().SetTitle(histos[0].GetXaxis().GetTitle())
        dummy.GetXaxis().SetTitleSize(0.08)
        dummy.GetXaxis().SetLabelSize(0.08)
        dummy.GetXaxis().SetTitleOffset(1.2)
        dummy.Draw("e2")
            
        ratio_list = []
        for i in range(3,nsig):  
            ratio = histos[i].Clone("")
            ratio.Divide(histos[0])
            ratio.SetLineWidth(3)
            ratio.SetLineColor(colors[i])
            #print(f"{legend[i]}")
            ratio.Draw("hist same")
            ratio_list.append(ratio)
            #legend2.AddEntry(ratio, legend[i], "l")

        #legend2.Draw()
        
        pad2.SetLeftMargin(0.14)
        pad2.SetRightMargin(0.08)
        pad2.GetFrame().SetBorderSize(12)
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(0.3)
        #pad2.SetLogy()

        #canvas.cd()

        #canvas.RedrawAxis()
        #canvas.Modified()
        #canvas.Update()

        dir = DIR_PLOTS + "/" + cut + "/"
        make_dir_if_not_exists(dir)

        if (LOGY == True):

            canvas.SaveAs(dir + "log/" + variable + ".png")
            canvas.SaveAs(dir + "log/" + variable + ".pdf")

        else:

            canvas.SaveAs(dir + variable + ".png")
            canvas.SaveAs(dir+ variable + ".pdf")



            