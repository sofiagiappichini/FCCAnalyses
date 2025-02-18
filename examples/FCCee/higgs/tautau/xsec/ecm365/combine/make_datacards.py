#!/usr/bin/env python

#### use python3 in cmssw with alma9

import sys
import os
import os.path
import ntpath
import importlib
import copy
import re
import logging
import ROOT
import array
import uproot

def file_exists(file_path):
    return os.path.isfile(file_path)

def check_nonzero(directory, CUTS, process, list, VARIABLE):
    path = f"{directory}{process}_{CUTS}_histo.root"
    if file_exists(path):
        histo_file = uproot.open(path)
        selected_leaf = histo_file[VARIABLE]
        y_values = selected_leaf.values()
        if (sum(y_values)!=0):
            list.append(process)
    return list

def get_procs(directory, cut, variable):
    path = f"{directory}Combine_{variable}_{cut}_histo.root"

    if file_exists(path):
        histo_file = uproot.open(path)
        all_keys = histo_file.keys()
        #print(all_keys)
        histo_list = [
            key.split(f"_{variable}")[0] for key in all_keys
        ]
        #print(histo_list)
        return histo_list

def get_combined_unc(name, procs, bkg_procs):
    line = f"unc_{name}      lnN     "
    for p in procs:
        if name in p and p in bkg_procs:
            line += f"{'1.20':{' '}{'<'}{lspace}}"
        else:
            line += f"{'-':{' '}{'<'}{lspace}}"
    line += "\n"
    return line

def get_combined_unc_v2(name, sub_proc, procs, bkg_procs):
    line = f"unc_{name}      lnN     "
    for p in procs:
        if p in sub_proc and p in bkg_procs:
            line += f"{'1.20':{' '}{'<'}{lspace}}"
        else:
            line += f"{'-':{' '}{'<'}{lspace}}"
    line += "\n"
    return line

os.system("source /cvmfs/cms.cern.ch/cmsset_default.sh")
os.system("cd /work/xzuo/combine_test/CMSSW_14_1_0_pre4/src/")
os.system("cmsenv")

outputDir = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/combine/"

DIRECTORY = "/ceph/awiedl/FCCee/HiggsCP/ecm365/"
TAG = [
    "R5-explicit",
    "R5-tag",
    "ktN-explicit",
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
    "LL",
    "NuNu",
]
CUTS = {
    'LL':"selReco_100Coll150_115Rec160_1DR_cos0.25_misscos0.98_70Z100",
    'QQ':"selReco_100Coll150_115Rec160_1DR_cos0.25_misscos0.98_70Z100",
    'NuNu':"selReco_180Me_TauDPhi3_1DR_cos0.25_misscos0.98_missy1",
}
VARIABLE = {
    'LL':"Recoil",
    'QQ':"Recoil",
    'NuNu':"Visible_mass",
    }

backgrounds_all = [
    "p8_ee_WW_ecm365",
    "p8_ee_ZQQ_ecm365",
    "p8_ee_ZZ_ecm365",
    'p8_ee_tt_ecm365',

    "wzp6_ee_LL_ecm365",
    "wzp6_ee_tautau_ecm365",

    "wzp6_ee_nuenueZ_ecm365",

    "wzp6_ee_egamma_eZ_ZLL_ecm365",
    
    "wzp6_ee_gaga_LL_60_ecm365",
    "wzp6_ee_gaga_tautau_60_ecm365",

    "wzp6_ee_tautauH_Htautau_ecm365",
    "wzp6_ee_tautauH_HQQ_ecm365",
    "wzp6_ee_tautauH_Hgg_ecm365",
    "wzp6_ee_tautauH_HVV_ecm365",

    #"wzp6_ee_nunuH_Htautau_ecm365",
    "wzp6_ee_VBFnunu_HQQ_ecm365",
    "wzp6_ee_VBFnunu_Hgg_ecm365",
    "wzp6_ee_VBFnunu_HVV_ecm365",

    "wzp6_ee_ZH_Znunu_HQQ_ecm365",
    "wzp6_ee_ZH_Znunu_Hgg_ecm365",
    "wzp6_ee_ZH_Znunu_HVV_ecm365",

    #"wzp6_ee_LLH_Htautau_ecm365",
    "wzp6_ee_LLH_HQQ_ecm365",
    "wzp6_ee_LLH_Hgg_ecm365",
    "wzp6_ee_LLH_HVV_ecm365",

    #"wzp6_ee_QQH_Htautau_ecm365",
    "wzp6_ee_QQH_HQQ_ecm365",
    "wzp6_ee_QQH_Hgg_ecm365",
    "wzp6_ee_QQH_HVV_ecm365",

    #"wzp6_ee_eeH_Htautau_ecm365",
    #"wzp6_ee_eeH_HQQ_ecm365",
    #"wzp6_ee_eeH_Hgg_ecm365",
    #"wzp6_ee_eeH_HVV_ecm365",

    #"wzp6_ee_mumuH_Htautau_ecm365",
    #"wzp6_ee_mumuH_HQQ_ecm365",
    #"wzp6_ee_mumuH_Hgg_ecm365",
    #"wzp6_ee_mumuH_HVV_ecm365",

    #"wzp6_ee_ZheavyH_Htautau_ecm365",
    #"wzp6_ee_ZheavyH_HQQ_ecm365",
    #"wzp6_ee_ZheavyH_Hgg_ecm365",
    #"wzp6_ee_ZheavyH_HVV_ecm365",

    #"wzp6_ee_ZlightH_Htautau_ecm365",
    #"wzp6_ee_ZlightH_HQQ_ecm365",
    #"wzp6_ee_ZlightH_Hgg_ecm365",
    #"wzp6_ee_ZlightH_HVV_ecm365",
]

signals = [
    #'wzp6_ee_ZheavyH_Htautau_ecm365',
    #'wzp6_ee_ZlightH_Htautau_ecm365',
    'wzp6_ee_QQH_Htautau_ecm365',
    #'wzp6_ee_eeH_Htautau_ecm365',
    #'wzp6_ee_mumuH_Htautau_ecm365',
    'wzp6_ee_LLH_Htautau_ecm365',
    'wzp6_ee_VBFnunu_Htautau_ecm365',
    'wzp6_ee_ZH_Znunu_Htautau_ecm365',
]

make_card = True
rebinned = False
lspace = 35
# here i want to make separeate datacard for each final state so we can check each values independently, then combine them with combineCards.py
if make_card:
    for tag in TAG:
        for cat in CAT:
            for sub in SUBDIR:

                sig_procs = []
                bkg_procs = []

                ## datacard header, common
                dc = ""
                dc += f"# text2workspace.py datacard.txt -o ws.root\n"
                dc += f"# combine -M FitDiagnostics -t -1 --expectSignal=1 ws.root --rMin -2 \n"
                dc += f"imax    1 number of bins\n"
                dc += f"jmax    * number of processes minus 1\n"
                dc += f"kmax    * number of nuisance parameters\n"
                dc += f"--------------------------------------------------------------------------------\n"
                
                directory = DIRECTORY + tag + "/final_280125/" + cat  + "/" + sub + "/"

                cut = CUTS[cat]
                print(cut, tag, cat, sub)


                #add the processes in the respective lists
                if rebinned:
                    procs = get_procs(directory, cut, VARIABLE[cat])
                    for p in procs:
                        if p in signals:
                            sig_procs.append(p)
                        else:
                            bkg_procs.append(p)

                else:
                    for b in backgrounds_all:
                        if b not in signals:
                            check_nonzero(directory, cut, b, bkg_procs, VARIABLE[cat])
                        else:
                            check_nonzero(directory, cut, b, sig_procs, VARIABLE[cat])

                procs = sig_procs + bkg_procs
                #print(procs)
                nprocs = len(procs)
                #print(nprocs)

                procs_idx = list(range(-len(sig_procs)+1, len(bkg_procs)+1, 1)) # negative or 0 for signal, positive for bkg

                procs_str = " ".join(f"{proc:{' '}{'<'}{lspace}}" for proc in procs)
                cats_procs_str = " ".join([f"{VARIABLE[cat]:{' '}{'<'}{lspace}}"] * nprocs)
                proc_ind = " ".join(f"{proc:{' '}{'<'}{lspace}}" for proc in procs_idx)
                rates_procs = " ".join([f"{'-1':{' '}{'<'}{lspace}}"] * nprocs)
                
                if rebinned:
                    dc += f"shapes * * {directory}Combine_{VARIABLE[cat]}_{cut}_histo.root $PROCESS_$CHANNEL\n"
                    dc += f"shapes data_obs * {directory}Combine_{VARIABLE[cat]}_{cut}_histo.root {sig_procs[0]}_$CHANNEL\n"

                else:
                    for proc in procs:
                        dc += f"shapes {proc} * {directory}{proc}_{cut}_histo.root $CHANNEL\n"
                    dc += f"shapes data_obs * {directory}{procs[0]}_{cut}_histo.root $CHANNEL\n"

                dc += f"--------------------------------------------------------------------------------\n"
                dc += f"bin                        {VARIABLE[cat]}\n"
                dc += f"observation                -1\n"
                dc += f"--------------------------------------------------------------------------------\n"
                dc += f"bin                        {cats_procs_str}\n"
                dc += f"process                    {procs_str}\n"
                dc += f"process                    {proc_ind}\n"
                dc += f"rate                       {rates_procs}\n"
                dc += f"--------------------------------------------------------------------------------\n"

                ## systematic uncertainties
                '''systs = get_param(param, "systs")
                for systName, syst in systs.items():
                    syst_type = syst['type']
                    syst_val = str(syst['value'])
                    procs_to_apply = syst['procs']
                    dc_tmp = f"{systName:{' '}{'<'}{15}} {syst_type:{' '}{'<'}{10}} "
                    for cat in categories:
                        for proc in procs:
                            apply_proc = (isinstance(procs_to_apply, list) and proc in procs_to_apply) or (isinstance(procs_to_apply, str) and re.search(procs_to_apply, proc))
                            if apply_proc:
                                if syst_type == "shape":
                                    LOGGER.warning('Shape uncertainties not yet supported! Skipping')
                                    val = "-"
                                else:
                                    val = str(syst_val)
                            else:
                                val = "-"
                            dc_tmp += f"{val:{' '}{'<'}{lspace}}"
                    dc += f"{dc_tmp}\n"'''

                ## freely floating processes and statistical uncertainty
                '''for proc in bkg_procs:
                    if "nunuH" in proc:
                        dc += f"unc_nunuH rateParam {VARIABLE[cat]} {proc} 1.0 [0,2]\n"
                    elif "LLH" in proc:
                        dc += f"unc_LLH rateParam {VARIABLE[cat]} {proc} 1.0 [0,2]\n"
                    elif "tautauH" in proc:
                        dc += f"unc_tautauH rateParam {VARIABLE[cat]} {proc} 1.0 [0,2]\n"
                    elif "QQH" in proc:
                        dc += f"unc_QQH rateParam {VARIABLE[cat]} {proc} 1.0 [0,2]\n"
                    else:
                        dc += f"unc_{proc} rateParam {VARIABLE[cat]} {proc} 1.0 [0,2]\n"
                    
                dc += f"unc rateParam {VARIABLE[cat]} * 1.0\n"
                '''
                ## log normal uncertainties
                '''for proc in bkg_procs:
                    dc += f"unc_{proc}      lnN     "
                    for p in procs:
                        if p == proc:
                            dc += f"{'1.20':{' '}{'<'}{lspace}}"
                        else:
                            dc += f"{'-':{' '}{'<'}{lspace}}"
                    dc += "\n"
                dc += "\n\n"'''


                #combined uncertainties
                if any("H_H" in proc for proc in bkg_procs):
                    dc += get_combined_unc("H_H", procs, bkg_procs)

                Z_proc = []
                for proc in bkg_procs:
                    if proc in ["wzp6_ee_LL_ecm240", "wzp6_ee_tautau_ecm240","p8_ee_Zqq_ecm240"]:
                        Z_proc.append(proc)
                        print(proc)
                dc += get_combined_unc_v2("Z", Z_proc, procs, bkg_procs)        

                #individual uncertainties
                for proc in bkg_procs:
                    if all(substring not in proc for substring in ["nunuH", "LLH", "QQH", "tautauH", "_ee_tautau_", "_ee_LL_", "_ee_Zqq_"]):
                        dc += f"unc_{proc}      lnN     "
                        for p in procs:
                            if p == proc and ('p8_ee_ZZ_ecm240' in proc or 'p8_ee_WW_ecm240' in proc):
                                dc += f"{'1.02':<{lspace}}"
                            elif p == proc:
                                dc += f"{'1.20':<{lspace}}"
                            else:
                                dc += f"{'-':<{lspace}}"
                        dc += "\n"

                dc += "\n\n" 


                dc += "* autoMCStats 1 1"

                # write cards
                if not os.path.exists(f"{outputDir}/{tag}/{cat}/{sub}"):
                    os.system(f"mkdir -p {outputDir}/{tag}/{cat}/{sub}")

                with open(f"{outputDir}/{tag}/{cat}/{sub}/datacard.txt", 'w') as f:
                    f.write(dc)

## now we can combine the cards made

for tag in TAG:
    for cat in CAT:
        string = " ".join([f"{cat}{sub}={outputDir}/{tag}/{cat}/{sub}/datacard.txt" for sub in SUBDIR])
        os.system(f"combineCards.py {string} > {outputDir}/{tag}/{cat}/datacard_{cat}.txt")

    string = " ".join([f"{cat}={outputDir}/{tag}/{cat}/datacard_{cat}.txt" for cat in CAT])
    os.system(f"combineCards.py {string} > {outputDir}/{tag}/datacard_combined.txt")