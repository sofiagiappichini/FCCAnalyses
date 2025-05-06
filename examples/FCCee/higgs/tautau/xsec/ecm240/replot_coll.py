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
DIRECTORY = "/ceph/awiedl/FCCee/HiggsCP/ecm240/"
TAG = [
    #"R5-explicit",
    #"R5-tag",
    #"ktN-explicit",
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
    #"LL",
    #"NuNu",
]

#list of cuts you want to plot
CUTS_LLHH = [
    #"selReco",
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

CUTS_LLLH = [
    #"selReco",
    #"selReco_100Coll150",
    #"selReco_100Coll150_115Rec160",
    #"selReco_100Coll150_115Rec160_2DR",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_4Emiss",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_84Z100_4Emiss", 
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_84Z100_4Emiss_Zp54",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.88_84Z100_4Emiss_Zp54",
]

CUTS_LLLL = [
    #"selReco",
    #"selReco_100Coll150",
    #"selReco_100Coll150_115Rec160",
    #"selReco_100Coll150_115Rec160_2DR",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_40Emiss",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_40Emiss", 
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_40Emiss_Zp54",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.9_80Z100_40Emiss_Zp54",
]

CUTS_QQHH = [
    "selReco",
    #"selReco_0.5BDT",
    #"selReco_100Coll150",
    #"selReco_100Coll150_115Rec160",
    #"selReco_100Coll150_115Rec160_2DR",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_8Emiss",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_8Emiss_Zp52",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.86_70Z100_8Emiss_Zp52",
]

CUTS_QQLH = [
    "selReco",
    #"selReco_100Coll150",
    #"selReco_100Coll150_115Rec160",
    #"selReco_100Coll150_115Rec160_2DR",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_36Emiss",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_36Emiss",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_36Emiss_Zp52",
]

CUTS_QQLL = [
    "selReco",
    #"selReco_100Coll150",
    #"selReco_100Coll150_115Rec160",
    #"selReco_100Coll150_115Rec160_2DR",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_52Emiss",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_52Emiss_Zp52",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.92_70Z100_52Emiss_Zp52",
]
    
CUTS_NuNuHH = [
    #"selReco",
    #"selReco_100Me",
    #"selReco_100Me_TauDPhi3",
    #"selReco_100Me_TauDPhi3_2DR",
    #"selReco_100Me_TauDPhi3_2DR_cos0.4",
    #"selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    #"selReco_112Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    #"selReco_112Me_TauDPhi3_2DR_cos0.4_misscos0.88_missy1",
]

CUTS_NuNuLH = [
    #"selReco",
    #"selReco_100Me",
    #"selReco_100Me_TauDPhi3",
    #"selReco_100Me_TauDPhi3_2DR",
    #"selReco_100Me_TauDPhi3_2DR_cos0.4",
    #"selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    #"selReco_140Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    #"selReco_140Me_TauDPhi3_2DR_cos0.4_misscos0.94_missy1",
]

CUTS_NuNuLL = [
    #"selReco",
    #"selReco_100Me",
    #"selReco_100Me_TauDPhi3",
    #"selReco_100Me_TauDPhi3_2DR",
    #"selReco_100Me_TauDPhi3_2DR_cos0.4",
    #"selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    #"selReco_152Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    #"selReco_152Me_TauDPhi3_2DR_cos0.4_misscos0.92_missy1",
]

CUTS = {
    'LLLL':CUTS_LLLL,
    'LLLH':CUTS_LLLH,
    'LLHH':CUTS_LLHH,
    'QQLL':CUTS_QQLL,
    'QQLH':CUTS_QQLH,
    'QQHH':CUTS_QQHH,
    'NuNuLL':CUTS_NuNuLL,
    'NuNuLH':CUTS_NuNuLH,
    'NuNuHH':CUTS_NuNuHH,
}

#now you can list all the histograms that you want to plot
VARIABLES_GEN = [
]

VARIABLES = [
    "Recoil",
    "Collinear_mass",
    "Collinear_mass_3d",
]

VARIABLES_TAG = [
]

VARIABLES_LL = [
 
]

VARIABLES_QQ = [
]

VARIABLES_NuNu = [
]

LIST_VAR = {
    "QQ": VARIABLES_QQ,
    "LL":VARIABLES_LL,
    "NuNu":VARIABLES_NuNu,
}

#directory where you want your plots to go
DIR_PLOTS = '/web/awiedl/public_html/HiggsCP/coll3d/' 

#labels for the cuts in the plots
LABELS = {
    "selReco": "No additional selection",
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
LOGY = False

#list of backgorunds, then legend and colors to be assigned to them
backgrounds_all = [
]

var_leg = {
     "Recoil":"Recoil mass",
     "Collinear_mass":"Coll mass xy",
     "Collinear_mass_3d":"Coll mass xyz"
}

var_leg_col = {
    "Recoil":ROOT.kBlue,
    "Collinear_mass": ROOT.kGreen,
    "Collinear_mass_3d": ROOT.kRed
}

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
    #'wzp6_ee_LLH_Htautau_ecm240',
    #'wzp6_ee_nunuH_Htautau_ecm240',
]

for tag in TAG:
    for cat in CAT:
        if "tag" in tag:
                variables = VARIABLES + VARIABLES_TAG +LIST_VAR[cat] #+ ["BDT_score"]
        else: 
            variables = VARIABLES + LIST_VAR[cat] #+["BDT_score"]
        #variables = ["RecoEmiss_e",]

        for sub in SUBDIR:
                    directory = DIRECTORY + tag + "/final/" + cat + "/" + sub + "/"

                    CUT = CUTS[cat+sub]

                    for cut in CUT:
                        
                        print(cut, directory)

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
                                for variable in variables:
                                    h = tf.Get(variable)
                                    hh = copy.deepcopy(h)
                                    hh.SetDirectory(0)
                                    histos.append(hh)
                                    colors.append(var_leg_col[variable])
                                    leg.AddEntry(histos[-1], var_leg[variable], "l")
                                    leg_bkg.append(0)
                        nsig=len(histos)


                        # add the signal histograms
                        for i in range(nsig):
                            h = histos[i]
                            h.SetLineWidth(3)
                            h.SetLineColor(colors[i])
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

                            dir = DIR_PLOTS + tag + "/" 
                            make_dir_if_not_exists(dir)

                            canvas.SaveAs(dir + "coll_" + cat + sub + ".png")
                            canvas.SaveAs(dir + "coll_" + cat + sub + ".pdf")
                        else:
                            canvas.SetTicks(1, 1)
                            canvas.SetLeftMargin(0.14)
                            canvas.SetRightMargin(0.08)
                            canvas.GetFrame().SetBorderSize(12)

                            canvas.RedrawAxis()
                            canvas.Modified()
                            canvas.Update()

                            dir = DIR_PLOTS + tag + "/" + cat + "/" + sub + "/lin/" + cut + "/"
                            make_dir_if_not_exists(dir)

                            canvas.SaveAs(dir + "coll_" + cat + sub + ".png")
                            canvas.SaveAs(dir + "coll_" + cat + sub + ".pdf")

                        for i in range(nsig):
                            h = histos[i]
                            gaussFit = ROOT.TF1("gaussfit","gaus",80.,160.) 
                            h.Fit(gaussFit, "EV")
                            mean = gaussFit.GetParameter(1)
                            sigma = gaussFit.GetParameter(2)
                            FWHM = sigma * 2.3548
                            with open('/work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/output_coll.txt', "a") as file:
                                file.write(f"{cat}\n")
                                file.write(f"{sub}\n")
                                file.write(f"{variables[i]}\n")
                                file.write(f"Mean: {mean}\n")
                                file.write(f"Sigma: {sigma}\n")
                                file.write(f"FWHM: {FWHM}\n\n")