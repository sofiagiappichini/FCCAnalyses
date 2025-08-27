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
        os.system("cp /eos/user/s/sgiappic/www/index.php {}".format(directory)) #copy index to show plots in web page automatically
        #print(f"Directory created successfully.")
    #else:
        #print(f"Directory already exists.")

def file_exists(file_path):
    return os.path.isfile(file_path)

DIRECTORY = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/CP/final_250530/ktN-explicit/"

DIR_PLOTS = '/eos/user/s/sgiappic/www/Higgs_CP/ecm240/pythia/' 

SUB = [
    #'LL',
    'LH',
    'HH',
]
#category to plot
CAT = [
    "QQ",
    #"LL",
]

CUT = [
    "selReco",
    "selReco_100Coll150",
    "selReco_100Coll150_115Rec160",
    "selReco_100Coll150_115Rec160_2DR",
    "selReco_100Coll150_115Rec160_2DR_cos0.6",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_jets",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_jets_10EM",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_jets_10EM_40Zp55",
     
]

CUT_LLLL = [
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_20EM",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_20EM_HE110",
]

CUT_QQHH = [
    "selReco_100Coll150_115Rec160_2DR_0.98cos0.6_misscos0.98_80Z100_jets_10EM_40Zp55",
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_10EM",
    #"selReco_100Coll150_115Rec160_2DR3_cos0.6_misscos0.98_80Z100_10EM",
    #"selReco_100Coll150_115Rec160_2DR3_cos0.6_misscos0.98_80Z100_10EM95",
    #"selReco_100Coll150_115Rec160_2DR3_cos0.6_misscos0.98_80Z100_10EM95_40HE",
    
]

CUT_QQLH = [
    #"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_10EM",
    #"selReco_100Coll150_115Rec160_2DR3.2_cos0.6_misscos0.98_80Z100_10EM",
    #"selReco_100Coll150_115Rec160_2DR3.2_cos0.6_misscos0.98_80Z100_10EM_40Zp55",
]

CUT_QQLL = [
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_54EM",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_54EM_90HM",
]

LABELS = {
    "selReco": "No selection",
    "selReco_100Coll150": "100<M_{collinear}<150 GeV",
    "selReco_100Coll150_115Rec160": "115<M_{recoil}<160 GeV",
    "selReco_100Coll150_115Rec160_2DR": "#Delta R_{#tau}>2",
    "selReco_100Coll150_115Rec160_2DR_cos0.6": "cos#theta_{#tau}<-0.6",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98": "|cos#theta_{miss}|<0.98",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100": "80<M_{Z}<100 GeV",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_jets":"Charged quark jet constituents>0",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_jets_10EM":"E_{missing}>10 GeV",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_jets_10EM_40Zp55":"40<p_{Z}<55 GeV",
    "selReco_100Coll150_115Rec160_2DR_0.98cos0.6_misscos0.98_80Z100_jets_10EM_40Zp55":"cos#theta_{#tau}>-0.98",
    
    #cuts for NuNu
    "selReco_100Me": "E_{miss}>100 GeV",
    "selReco_100Me_TauDPhi3": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3",
    "selReco_100Me_TauDPhi3_2DR": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2",
    "selReco_100Me_TauDPhi3_2DR_cos0.4": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.98",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1": "E_{miss}>100 GeV, |#Delta#phi_{#tau}|<3, #Delta R_{#tau}>2, cos#theta_{#tau}<-0.4, |cos#theta_{miss}|<0.98, |y_{miss}|<1",

    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_20EM":"E_{missing}>20 GeV",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_20EM_HE110":"E_{H}>110 GeV",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_10EM":"E_{missing}>10 GeV",
    "selReco_100Coll150_115Rec160_2DR3.2_cos0.6_misscos0.98_80Z100_10EM":"#Delta R_{#tau}<3.2",
    "selReco_100Coll150_115Rec160_2DR3_cos0.6_misscos0.98_80Z100_10EM":"#Delta R_{#tau}<3",
    "selReco_100Coll150_115Rec160_2DR3.2_cos0.6_misscos0.98_80Z100_10EM_40Zp55":"40<p_{Z}>55 GeV",
    "selReco_100Coll150_115Rec160_2DR3.2_cos0.6_misscos0.98_80Z100_10EM":"E_{missing}>10 GeV",
    "selReco_100Coll150_115Rec160_2DR3_cos0.6_misscos0.98_80Z100_10EM95":"E_{missing}<95 GeV",
    "selReco_100Coll150_115Rec160_2DR3_cos0.6_misscos0.98_80Z100_10EM95_40HE":"E_{H}>40 GeV",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_54EM":"E_{missing}>54 GeV",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_54EM_90HM":"M_{H}<90 GeV",

 }

samples = [
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

    "wzp6_ee_nunuH_Htautau_ecm240",
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
    
    "p8_ee_QQH_Htautau_CPeven",
    "p8_ee_QQH_Htautau_CPodd",
    "p8_ee_LLH_Htautau_CPeven",
    "p8_ee_LLH_Htautau_CPodd",
]

def load_yield(sample, cut, dir):
    filename = f"{sample}_{cut}_histo.root"
    filepath = os.path.join(dir, filename)

    if not os.path.exists(filepath):
        return 0
    f = ROOT.TFile.Open(filepath)
    histo = f.Get("RecoEmiss_e")
    if not histo:
        return 0
    integral = histo.Integral()
    f.Close()
    return integral 

# Loop over each sample to make a cut flow
for cat in CAT:
    for sub in SUB:
        output_file = ROOT.TFile(DIRECTORY + cat + "/" + sub + "/cutflow_histos.root", "RECREATE")

        CUTS = ""
        if "LL" in cat:
            if "LL" in sub:
                CUTS = CUT + CUT_LLLL
            else:
                CUTS = CUT
        else:
            if "HH" in sub:
                CUTS = CUT +  CUT_QQHH
            elif "LH" in sub:
                CUTS = CUT + CUT_QQLH
            else:
                CUTS = CUT + CUT_QQLL
        
        print(len(CUTS))

        for sample in samples:
            cutflow = ROOT.TH1F(f"{sample}", f"Cutflow: {sample}", len(CUTS), 0, len(CUTS))
            cutflow.GetXaxis().SetLabelSize(0.05)
            
            for i, cut in enumerate(CUTS):
                yield_val = load_yield(sample, cut, DIRECTORY + cat + "/" + sub )
                cutflow.SetBinContent(i + 1, yield_val)
                cutflow.GetXaxis().SetBinLabel(i + 1, LABELS[cut])

            output_file.cd()
            cutflow.Write()

        output_file.Close()
        print(f"{cat}{sub} done")


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
LOGY = True

#list of backgorunds, then legend and colors to be assigned to them
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

    "wzp6_ee_nunuH_Htautau_ecm240",
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

    'sm':"ZH(#tau#tau), SM",
    'sm_lin_quad_cehim_m1':"ZH(#tau#tau), CPV -1",
    'sm_lin_quad_cehim':"ZH(#tau#tau), CPV +1",
    'sm_lin_quad_cehre_m1':"ZH(#tau#tau), CPC -1",
    'sm_lin_quad_cehre_p1':"ZH(#tau#tau), CPC +1",

    "p8_ee_QQH_Htautau_CPeven":"Z(qq)H(#tau#tau), CP even",
    "p8_ee_QQH_Htautau_CPodd":"Z(qq)H(#tau#tau), CP odd",
    "p8_ee_LLH_Htautau_CPeven":"Z(ll)H(#tau#tau), CP even",
    "p8_ee_LLH_Htautau_CPodd":"Z(ll)H(#tau#tau), CP odd",
}

legcolors = {
    'p8_ee_WW_ecm240':ROOT.kSpring+2,
    'p8_ee_Zqq_ecm240':ROOT.kPink+1,
    'p8_ee_ZZ_ecm240':ROOT.kSpring+3,

    'wzp6_ee_LL_ecm240':ROOT.kAzure-4,
    'wzp6_ee_tautau_ecm240':ROOT.kAzure-5,

    "wzp6_ee_nuenueZ_ecm240":ROOT.kAzure-1,

    "wzp6_ee_egamma_eZ_ZLL_ecm240":ROOT.kOrange-4,
    
    "wzp6_ee_gaga_LL_60_ecm240":ROOT.kOrange-9,
    "wzp6_ee_gaga_tautau_60_ecm240":ROOT.kOrange+6,

    "wzp6_ee_tautauH_Htautau_ecm240":ROOT.kViolet+6,
    "wzp6_ee_tautauH_HQQ_ecm240":ROOT.kViolet+5,
    "wzp6_ee_tautauH_Hgg_ecm240":ROOT.kViolet-4,
    "wzp6_ee_tautauH_HVV_ecm240":ROOT.kViolet+1,

    'wzp6_ee_nunuH_Htautau_ecm240':ROOT.kTeal-9,
    "wzp6_ee_nunuH_HQQ_ecm240":ROOT.kGreen-5,
    "wzp6_ee_nunuH_Hgg_ecm240":ROOT.kGreen-8,
    "wzp6_ee_nunuH_HVV_ecm240":ROOT.kGreen-10,

    'wzp6_ee_LLH_Htautau_ecm240':ROOT.kAzure-9,
    "wzp6_ee_LLH_HQQ_ecm240":ROOT.kCyan-5,
    "wzp6_ee_LLH_Hgg_ecm240":ROOT.kCyan-8,
    "wzp6_ee_LLH_HVV_ecm240":ROOT.kCyan-10,

    'wzp6_ee_QQH_Htautau_ecm240':ROOT.kViolet-9,
    "wzp6_ee_QQH_HQQ_ecm240":ROOT.kMagenta-5,
    "wzp6_ee_QQH_Hgg_ecm240":ROOT.kMagenta-8,
    "wzp6_ee_QQH_HVV_ecm240":ROOT.kMagenta-10,

    'sm':ROOT.kViolet-9,
    'sm_lin_quad_cehim_m1':ROOT.kAzure-6,
    'sm_lin_quad_cehim':ROOT.kTeal-7,
    'sm_lin_quad_cehre_m1':ROOT.kTeal+3,
    'sm_lin_quad_cehre_p1':ROOT.kSpring+2,

    "p8_ee_QQH_Htautau_CPeven":ROOT.kRed-10,
    "p8_ee_QQH_Htautau_CPodd":ROOT.kPink+3,
    "p8_ee_LLH_Htautau_CPeven":ROOT.kAzure-9,
    "p8_ee_LLH_Htautau_CPodd":ROOT.kAzure-6,

}

#list of signals, then legend and colors to be assigned to them
signals = [
    #"sm",
    #"sm_lin_quad_cehim_m1",
    #"sm_lin_quad_cehim",
    #"sm_lin_quad_cehre_m1",
    #"sm_lin_quad_cehre_p1",
    "p8_ee_QQH_Htautau_CPeven",
    "p8_ee_QQH_Htautau_CPodd",
    "p8_ee_LLH_Htautau_CPeven",
    "p8_ee_LLH_Htautau_CPodd",
]

for cat in CAT:
    for sub in SUB:
        directory = DIRECTORY  + cat + "/" + sub + "/"

        canvas = ROOT.TCanvas("", "", 800, 800)

        nsig = len(signals)
        nbkg = len(backgrounds_all) #put to zero if you only want to look at signals

        #legend coordinates and style
        legsize = 0.04*nsig
        legsize2 = 0.015*nbkg
        leg = ROOT.TLegend(0.16, 0.78 - legsize, 0.45, 0.78)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetLineColor(0)
        leg.SetShadowColor(0)
        leg.SetTextSize(0.025)
        leg.SetTextFont(42)

        leg2 = ROOT.TLegend(0.45, 0.78 - legsize2, 0.90, 0.78)
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
            fin = f"{directory}cutflow_histos.root"
            if file_exists(fin): #might be an empty file after stage2 
                tf = ROOT.TFile.Open(fin, 'READ')
                h = tf.Get(s)
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
                fin = f"{directory}cutflow_histos.root"
                if file_exists(fin):
                    tf = ROOT.TFile.Open(fin, 'READ')
                    h = tf.Get(b)
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
                    fin = f"{directory}{sub}{b}_{cut}_histo.root"
                    if (i==0 and j==0):
                        with ROOT.TFile(fin) as tf:
                            h = tf.Get(variable)
                            hh = copy.deepcopy(h)
                            hh.SetDirectory(0)
                    else:
                        with ROOT.TFile(fin) as tf:
                            h = tf.Get(variable)
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
                hStackBkg.SetMinimum(1e-3) #change the range to be plotted
                hStackBkg.SetMaximum(1e15) #leave some space on top for the legend
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
                if i == 0:
                    h.Draw("HIST")
                    h.GetYaxis().SetTitle("Events")
                    h.GetXaxis().SetTitle(histos[i].GetXaxis().GetTitle())
                    #h.GetYaxis().SetTitleOffset(1.5)
                    h.GetXaxis().SetTitleOffset(1.2)
                    #h.GetXaxis().SetLimits(1, 1000)
                    if LOGY==True :
                        h.GetYaxis().SetRangeUser(1e-3,1e8) #range to set if only working with signals
                    else:
                        max_y = h.GetMaximum() 
                        h.GetYaxis().SetRangeUser(0, max_y*1.5 )
                else: 
                    h.Draw("HIST SAME")

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

        latex.SetTextAlign(31)
        text = '#it{' + leftText + '}'
        latex.SetTextSize(0.03)
        latex.DrawLatex(0.92, 0.92, text)

        #fix legened height after having the correct number of processes
        legsize = 0.04*nsig
        legsize2 = 0.025*(len(histos)-nsig)/2
        leg.SetY1(0.78 - legsize)
        leg2.SetY1(0.78 - legsize2)
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

            dir = DIR_PLOTS + "/" + cat + "/" + sub + "/log/"
            make_dir_if_not_exists(DIR_PLOTS)
            make_dir_if_not_exists(DIR_PLOTS + "/" + cat)
            make_dir_if_not_exists(DIR_PLOTS + "/" + cat + "/" + sub)
            make_dir_if_not_exists(DIR_PLOTS + "/" + cat + "/" + sub + "/log/")
            make_dir_if_not_exists(dir)

            canvas.SaveAs(dir + "cutflow_" + cat + sub + ".png")
            canvas.SaveAs(dir + "cutflow_" + cat + sub + ".pdf")
        else:
            canvas.SetTicks(1, 1)
            canvas.SetLeftMargin(0.14)
            canvas.SetRightMargin(0.08)
            canvas.GetFrame().SetBorderSize(12)

            canvas.RedrawAxis()
            canvas.Modified()
            canvas.Update()

            dir = DIR_PLOTS + "/" + cat + "/" + sub + "/lin/"
            make_dir_if_not_exists(DIR_PLOTS )
            make_dir_if_not_exists(DIR_PLOTS + "/" + cat)
            make_dir_if_not_exists(DIR_PLOTS + "/" + cat + "/" + sub)
            make_dir_if_not_exists(DIR_PLOTS + "/" + cat + "/" + sub + "/lin/")
            make_dir_if_not_exists(dir)

            canvas.SaveAs(dir + "cutflow_" + cat + sub + ".png")
            canvas.SaveAs(dir + "cutflow_" + cat + sub + ".pdf")
