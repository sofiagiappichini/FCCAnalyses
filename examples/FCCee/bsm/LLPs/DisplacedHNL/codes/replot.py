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

DIRECTORY = '/eos/user/s/sgiappic/2HNL_ana/final_july/' 
DIR_PLOTS = '/eos/user/s/sgiappic/www/paper/july/' 

CUTS = [
    #"sel2RecoSF_vetoes_tracks_M80_5MEpt_0.8cos_chi",
    #"sel2RecoDF_vetoes_tracks_M80_5MEpt_0.8cos_chi",
    #"sel2RecoSF_vetoes_tracks_M80_5MEpt_0.8cos",
    #"sel2RecoDF_vetoes_tracks_M80_5MEpt_0.8cos",

    #"sel2Reco_vetoes",
    #"sel2Gen_vetoes",

    #"sel2Reco_vetoes",
    #"sel2Reco_vetoes_notracks",
    #"sel2Reco_vetoes_notracks_nojets",
    #"sel2Reco_vetoes_notracks_nojets_M80",
    #"sel2Reco_vetoes_notracks_nojets_M80_10MEpt",
    #"sel2Reco_vetoes_notracks_nojets_M80_10MEpt_0.8cos",
    #"sel2Reco_vetoes_notracks_nojets_M80_10MEpt_0.8cos_chi10_0.57d0",

    #"selNone",
    #"selReco_gen",
    #"selReco_gen_notracks",
    #"selReco_gen_notrack_nojets",
    #"selReco_gen_notracks_nohad",
    #"selReco_gen_notracks_nohad_M80",
    #"selReco_gen_notracks_nohad_M80_0.8cos",
    #"selReco_gen_notracks_nohad_M80_0.8cos0.8",
    #"selReco_gen_notracks_nohad_SF",
    #"selReco_gen_notracks_nohad_DF",
    
    
    #"selReco_gen_notracks_nohad_M80_0.8cos0.8_8MET",
    #"selReco_gen_notracks_nohad_M80_0.7cos",
    #"selReco_gen_notracks_nohad_5M80_0.7cos",
    #"selReco_gen_notracks_nohad_M80_0.7cos_5pt",
    #"selReco_gen_notracks_nohad_M80_0.7cos_20MEpt",
    #"selReco_gen_notracks_nohad_5M80_0.7cos_5pt_20MEpt",
    #"selReco_gen_notracks_nojets_M80_0.8cos_10MEpt",
    "selReco_gen_notracks_2eh",
 ] 

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

    "sel2Gen_vetoes":"Two gen leptons, no photons",
    "sel2Reco_vetoes":"Two leptons, no photons",
    "sel2Reco_vetoes_notracks":"Two leptons, no photons, no other tracks",
    "sel2Reco_vetoes_notracks_nojets":"Two leptons, no photons, no other tracks, no jets",
    "sel2Reco_vetoes_notracks_nojets_M80":"Two leptons, no photons, no other tracks, no jets, M(l,l)<80 GeV",
    "sel2Reco_vetoes_notracks_nojets_M80_10MEpt":"Two leptons, no photons, no other tracks, no jets, M(l,l)<80 GeV, p_{T,miss}>10 GeV",
    "sel2Reco_vetoes_notracks_nojets_M80_10MEpt_0.8cos":"Two leptons, no photons, no other tracks, no jets, M(l,l)<80 GeV, p_{T,miss}>10 GeV, cos#theta>-0.8",
    "sel2Reco_vetoes_notracks_nojets_M80_10MEpt_0.8cos_chi10_0.57d0":"Two leptons, no photons, no other tracks, no jets, M(l,l)<80 GeV, p_{T,miss}>10 GeV, cos#theta>-0.8, #chi^2<10, |d_{0}|>0.57 mm",
    "sel2Reco_vetoes_notracks_nojets_pt10_2.5eta_0.4DR_M80_10MEpt_0.8cos":"Two leptons, no photons, no other tracks, no jets, M(l,l)<80 GeV, p_{T,miss}>10 GeV, cos#theta>-0.8, #chi^2<10, |d_{0}|>0.57 mm, MG cuts",
 
    "sel2Reco_vetoes_notracks_nojets_M80":"Two leptons, no photons, no other tracks, no jets, M(l,l)<80 GeV, MG cuts",
    "sel2Reco_vetoes_notracks_nojets_M80_5MEpt": "Two leptons, no photons, no other tracks, no jets, M(l,l)<80 GeV, p_{T,miss}>5 GeV, MG cuts",
    "sel2Reco_vetoes_notracks_nojets_M80_5MEpt_0.8cos":"Two leptons, no photons, no other tracks, no jets, M(l,l)<80 GeV, p_{T,miss}>5 GeV, cos#theta>-0.8, MG cuts",
 
    "selNone":"Two leptons, no photons",
    "selReco_gen": "Two leptons, no photons, p_{T}>1 GeV, p_{T, miss}>5 GeV",
    "selReco_gen_notracks": "Two leptons, no photons, no tracks, p_{T}>1 GeV, p_{T, miss}>5 GeV",
    "selReco_gen_notrack_nojets": "Two leptons, no photons, no tracks, no jets, p_{T}>1 GeV, p_{T, miss}>5 GeV",
    "selReco_gen_notracks_nohad": "Two leptons, no photons, no tracks, no neutral hadrons, p_{T}>1 GeV, p_{T, miss}>5 GeV",
    "selReco_gen_notracks_nohad_M80": "Two leptons, no photons, no tracks, no neutral hadrons, p_{T}>1 GeV, p_{T, miss}>5 GeV, M(l,l')<80 GeV",
    "selReco_gen_notracks_nohad_M80_0.8cos": "Two leptons, no photons, no tracks, no neutral hadrons, p_{T}>1 GeV, p_{T, miss}>5 GeV, M(l,l')<80 GeV, cos#theta>-0.8",
    "selReco_gen_notracks_nohad_M80_0.8cos0.8": "Two leptons, no photons, no tracks, no neutral hadrons, p_{T}>1 GeV, p_{T, miss}>5 GeV, M(l,l')<80 GeV, -0.8<cos#theta<0.8",
    "selReco_gen_notracks_nojets_M80_0.8cos_10MEpt": "Two leptons, no photons, no tracks, no jets, p_{T}>1 GeV, p_{T, miss}>10 GeV, M(l,l')<80 GeV",
    "selReco_gen_notracks_nojets_5M80_0.8cos_10MEpt": "Two leptons, no photons, no tracks, no jets, p_{T}>1 GeV, p_{T, miss}>10 GeV, 5<M(l,l')<80 GeV",
    
    "selReco_gen_notracks_nohad_SF": "Two leptons SF, no photons, no tracks, no neutral hadrons, p_{T}>1 GeV, p_{T, miss}>5 GeV",
    "selReco_gen_notracks_nohad_DF": "Two leptons DF, no photons, no tracks, no neutral hadrons, p_{T}>1 GeV, p_{T, miss}>5 GeV",

    "selReco_gen_notracks_2eh": "Two leptons, no photons, no neutral hadrons (E>2 GeV), no tracks, p_{T}>1 GeV, p_{T, miss}>5 GeV",

    "selReco_gen_notracks_nojets_M80_0.8cos_10MEpt": "Two leptons, no photons, no tracks, no jets, p_{T}>1 GeV, p_{T, miss}>10 GeV, M(l,l')<80 GeV, cos#theta>-0.8",
 
 }

ana_tex        = "e^{+}e^{-} #rightarrow N_{1,2} #nu, N_{1,2} #rightarrow ll#nu"
energy         = 91
collider       = 'FCC-ee'
intLumi        = 204 #ab-1

LOGY = True
LOGX = False

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

    "n_NeutralHadrons",
    "NeutralHadrons_e",
    "NeutralHadrons_p",
    "NeutralHadrons_pt",
    "NeutralHadrons_px",
    "NeutralHadrons_py",
    "NeutralHadrons_pz",
    "NeutralHadrons_eta",
    "NeutralHadrons_theta",
    "NeutralHadrons_phi",
    "NeutralHadrons_charge",
    "NeutralHadrons_mass",

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

    "Reco_e_led",
    "Reco_p_led",
    "Reco_pt_led",
    "Reco_px_led",
    "Reco_py_led",
    "Reco_pz_led",
    "Reco_eta_led",
    "Reco_theta_led",
    "Reco_phi_led",
    #"Reco_charge_led",
    "RecoTrack_absD0_led",
    "RecoTrack_absZ0_led",
    "RecoTrack_absD0sig_led",
    "RecoTrack_absZ0sig_led",
    "RecoTrack_D0cov_led",
    "RecoTrack_Z0cov_led",

    "Reco_e_sub",
    "Reco_p_sub",
    "Reco_pt_sub",
    "Reco_px_sub",
    "Reco_py_sub",
    "Reco_pz_sub",
    "Reco_eta_sub",
    "Reco_theta_sub",
    "Reco_phi_sub",
    #"Reco_charge_sub",
    "RecoTrack_absD0_sub",
    "RecoTrack_absZ0_sub",
    "RecoTrack_absD0sig_sub",
    "RecoTrack_absZ0sig_sub",
    "RecoTrack_D0cov_sub",
    "RecoTrack_Z0cov_sub",

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

    "RecoEmiss_px",
    "RecoEmiss_py",
    "RecoEmiss_pz",
    "RecoEmiss_pt",
    "RecoEmiss_e",

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

VARIBALES_JETS = [
    "n_noLeptonTracks",
    "noLep_e",
    "noLep_p",   
    "noLep_pt",   
    "noLep_px",   
    "noLep_py",   
    "noLep_pz",    
    "noLep_eta",   
    "noLep_{T}heta",
    "noLep_phi",  
    "noLep_charge",  
    "RecoTracknoLep_absD0", 
    "RecoTracknoLep_absZ0", 
    "RecoTracknoLep_absD0sig", 
    "RecoTracknoLep_absZ0sig", 
    "RecoTracknoLep_D0cov", 
    "RecoTracknoLep_Z0cov",

    "GenParticles_PID",
    "n_GenTaus",
    "n_GenPions",
    "n_GenKLs",
    "n_GenKpluss",

    "GenPion_e",
    "GenTau_e",
    "GenKL_e",
    "GenKplus_e",

    "GenPion_pt",
    "GenTau_pt",
    "GenKL_pt",
    "GenKplus_pt",

    "RecoMC_PID",
    "n_RecoTaus",
    "n_RecoPions",
    "n_RecoKLs",
    "n_RecoKpluss",

    "RecoPion_e",
    "RecoTau_e",
    "RecoKL_e",
    "RecoKplus_e",

    "RecoPion_pt",
    "RecoTau_pt",
    "RecoKL_pt",
    "RecoKplus_pt",

 ] 

VARIABLES_PID = [
    "GenParticles_PID",
    "FSGenParticles_PID",
    "n_GenTaus",
    "n_GenPions",
    "n_GenKLs",
    "n_GenKpluss",

    "GenPion_e",
    "GenTau_e",
    "GenKL_e",
    "GenKplus_e",

    "GenPion_pt",
    "GenTau_pt",
    "GenKL_pt",
    "GenKplus_pt",
]

backgrounds = [
    #'p8_ee_Zee_ecm91',
    #'p8_ee_Zmumu_ecm91',
    'p8_ee_Ztautau_ecm91',
    'p8_ee_Zbb_ecm91',
    'p8_ee_Zcc_ecm91',
    #'p8_ee_Zud_ecm91',
    #'p8_ee_Zss_ecm91',
    'eenunu_m',
    'mumununu_m',
    'tatanunu_m',
    'llnunu_m',
]

backgrounds_pairs = [
    'p8_ee_Zee_ecm91',
    'p8_ee_Zmumu_ecm91',
    'p8_ee_Zud_ecm91',
    'p8_ee_Zss_ecm91',
]

blegend = {
    'p8_ee_Zee_ecm91': 'Z #rightarrow ll',
    #'p8_ee_Zee_ecm91': 'Z #rightarrow ee',
    'p8_ee_Zmumu_ecm91': 'Z #rightarrow mumu',
    'p8_ee_Ztautau_ecm91': 'Z #rightarrow #tau#tau',
    'p8_ee_Zbb_ecm91': 'Z #rightarrow bb',
    'p8_ee_Zcc_ecm91': 'Z #rightarrow cc',
    'p8_ee_Zud_ecm91': 'Z #rightarrow uds',
    'p8_ee_Zss_ecm91': 'Z #rightarrow ss',
    'eenunu_m': 'ee#nu#nu',
    'mumununu_m': '#mu#mu#nu#nu',
    'tatanunu_m': '#tau#tau#nu#nu',
    'llnunu_m': 'll#nu#nu',
}

bcolors = {
    'p8_ee_Zee_ecm91': 40,
    #'p8_ee_Zee_ecm91': 48,
    #'p8_ee_Zmumu_ecm91': 44,
    'p8_ee_Ztautau_ecm91': 36,
    'p8_ee_Zbb_ecm91': 48,
    'p8_ee_Zcc_ecm91': 44,
    'p8_ee_Zud_ecm91': 20,
    'eenunu': 30,
    'mumununu': 32,
    'tatanunu': 38,
    'llnunu': 33,
}

signals = [
    'HNL_2.86e-12_30gev',
    'HNL_6.67e-10_30gev',
    'HNL_5e-12_60gev',
    'HNL_1.33e-7_80gev',
    
    
    #"HNL_6.67e-10_40gev",
    #"HNL_6.67e-10_40gev_isr",
    #"HNL_6.67e-10_40gev_isrbm",
]

slegend = {
    'HNL_6.67e-10_40gev':"U^{2}=6.67e-10, M_{N}=40 GeV",
    'HNL_6.67e-10_40gev_isr':"U^{2}=6.67e-10, M_{N}=40 GeV with ISR",
    'HNL_6.67e-10_40gev_isrbm':"U^{2}=6.67e-10, M_{N}=40 GeV with ISR+BS",
    'HNL_2.86e-12_30gev':"U^{2}=2.86e-12, M_{N}=30 GeV",
    'HNL_2.86e-7_30gev':"U^{2}=2.86e-7, M_{N}=30 GeV",
    'HNL_6.67e-10_30gev':"U^{2}=6.67e-10, M_{N}=30 GeV",
    'HNL_5e-12_60gev':"U^{2}=5e-12, M_{N}=60 GeV",
    'HNL_1.33e-7_80gev':"U^{2}=1.33e-7, M_{N}=80 GeV",
}

scolors = {
    'HNL_6.67e-10_40gev':ROOT.kBlue-8,
    'HNL_6.67e-10_40gev_isr':ROOT.kRed-8,
    'HNL_6.67e-10_40gev_isrbm':ROOT.kGreen-8,
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
        nbkg = 9 # change according to type of plots, 6 for grouped backgrounds, #len(backgrounds)

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
            #leg.AddEntry(histos[-1], blegend[s]+": "+str(histos[-1].Integral()), "l")
        
        if nbkg != 0:

            for b in backgrounds:
                fin = f"{DIRECTORY}{b}_{cut}_histo.root"
                with ROOT.TFile(fin) as tf:
                    h = tf.Get(variable)
                    hh = copy.deepcopy(h)
                    hh.SetDirectory(0)
                histos.append(hh)
                colors.append(bcolors[b])
                leg2.AddEntry(histos[-1], blegend[b], "f")

            for i in range(0, len(backgrounds_pairs), 2):
                p = backgrounds_pairs[i]
                p1 = backgrounds_pairs[i + 1]
                fin = f"{DIRECTORY}{p}_{cut}_histo.root"
                with ROOT.TFile(fin) as tf:
                    h = tf.Get(variable)
                    hh = copy.deepcopy(h)
                    hh.SetDirectory(0)
                fin1 = f"{DIRECTORY}{p1}_{cut}_histo.root"
                with ROOT.TFile(fin1) as tf1:
                    h1 = tf1.Get(variable)
                    hh1 = copy.deepcopy(h1)
                    hh1.SetDirectory(0)
                hh.Add(hh1)
                histos.append(hh)
                colors.append(bcolors.get(p))
                leg2.AddEntry(histos[-1], blegend.get(p), "f")

            #drawing stack for backgrounds
            hStackBkg = ROOT.THStack("hStackBkg", "")
            if LOGY==True :
                hStackBkg.SetMinimum(1e-5)
                hStackBkg.SetMaximum(1e25)
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
            hStackBkg.GetXaxis().SetTitle(histos[0].GetXaxis().GetTitle())
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
                    h.GetYaxis().SetRangeUser(1e-6,1e8)
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