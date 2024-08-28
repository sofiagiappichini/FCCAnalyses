#!/usr/bin/env python

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

def check_nonzero(directory, cut, process, list, variable):
    path = f"{directory}{process}_{cut}_histo.root"
    histo_file = uproot.open(path)
    selected_leaf = histo_file[variable]
    y_values = selected_leaf.values()
    if (sum(y_values)!=0):
        list.append(process)
    return list

outputDir = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/CP/combine/"

DIRECTORY = {
    'LL':'/final/LL',
    'QQ':'/final/QQ',
    'NuNu':'/final/NuNu',
}
SUBDIR = [
    'LL',
    'LH',
    'HH',
]
cut = ""
VARIABLE = "Recoil_mass"

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

    "wzp6_ee_nunuH_HQQ_ecm240",
    "wzp6_ee_nunuH_Hgg_ecm240",
    "wzp6_ee_nunuH_HVV_ecm240",

    "wzp6_ee_eeH_HQQ_ecm240",
    "wzp6_ee_eeH_Hgg_ecm240",
    "wzp6_ee_eeH_HVV_ecm240",

    "wzp6_ee_mumuH_HQQ_ecm240",
    "wzp6_ee_mumuH_Hgg_ecm240",
    "wzp6_ee_mumuH_HVV_ecm240",

    "wzp6_ee_ZheavyH_HQQ_ecm240",
    "wzp6_ee_ZheavyH_Hgg_ecm240",
    "wzp6_ee_ZheavyH_HVV_ecm240",

    "wzp6_ee_ZlightH_HQQ_ecm240",
    "wzp6_ee_ZlightH_Hgg_ecm240",
    "wzp6_ee_ZlightH_HVV_ecm240",
]

signals_QQ = [
    'wzp6_ee_ZheavyH_Htautau_ecm240',
    'wzp6_ee_ZlightH_Htautau_ecm240',
]

signals_LL = [
    'wzp6_ee_eeH_Htautau_ecm240',
    'wzp6_ee_mumuH_Htautau_ecm240',
]

signals_NuNu= [
    'wzp6_ee_nunuH_Htautau_ecm240',
]

CAT = [
    "QQ",
    "LL",
    "NuNu",
]

LIST_S = {
    "QQ": signals_QQ,
    "LL":signals_LL,
    "NuNu":signals_NuNu,
}


lspace = 35
# here i want to make separeate datacard for each final state so we can check each values independently, then combine them with combineCards.py
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
        
        directory = DIRECTORY[cat] + "/" + sub + "/"

        #add the processes in the respective lists
        for s in LIST_S[cat]:
            check_nonzero(directory, cut, s, sig_procs, VARIABLE)
        for b in backgrounds_all:
            check_nonzero(directory, cut, b, bkg_procs, VARIABLE)

        procs = sig_procs + bkg_procs
        nprocs = len(procs)
        procs_idx = list(range(-len(sig_procs)+1, len(bkg_procs)+1, 1)) # negative or 0 for signal, positive for bkg

        procs_str = " ".join(f"{proc:{' '}{'<'}{lspace}}" for proc in procs)
        cats_procs_str = " ".join([f"{VARIABLE:{' '}{'<'}{lspace}}"] * nprocs)
        proc_ind = " ".join(f"{proc:{' '}{'<'}{lspace}}" for proc in procs_idx)
        rates_procs = " ".join([f"{'-1':{' '}{'<'}{lspace}}"] * nprocs)
        
        for proc in procs:
            dc += f"shapes {proc} * {directory}{proc}_{cut}_histo.root $PROCESS\n"
        dc += f"shapes data_obs * {directory}{procs[0]}_{cut}_histo.root {procs[0]}\n"
        dc += f"--------------------------------------------------------------------------------\n"
        dc += f"bin                        {VARIABLE}\n"
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

        ## auto MC stats
        dc += "* autoMCStats 1 1"

        # write cards
        if not os.path.exists(f"{outputDir}/{cat}/{sub}"):
            os.system(f"mkdir -p {outputDir}/{cat}/{sub}")

        with open(f"{outputDir}/{cat}/{sub}/datacard.txt", 'w') as f:
            f.write(dc)

## now we can combine the cards made
## need to work in centos7 : portal1-centos7.etp.kit.edu
os.system("source /cvmfs/cms.cern.ch/cmsset_default.sh")
os.system("cd /work/nfaltermann/cmssw/CMSSW_10_6_0/src/")
os.system("cmsenv")

for cat in CAT:
    string = "".join([f"{cat}{sub}={outputDir}/{cat}/{sub}/datacard.txt" for sub in SUBDIR])
    os.system(f"combineCards.py {string} > {outputDir}/{cat}/datacard_{cat}.txt")

string = "".join([f"{cat}{sub}={outputDir}/{cat}/{sub}/datacard.txt" for cat in CAT for sub in SUBDIR])
os.system(f"combineCards.py {string} > {outputDir}/datacard_combined.txt")