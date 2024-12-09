import uproot
import os
import shutil
import numpy as np
import csv
import ROOT
import glob

def file_exists(file_path):
    return os.path.isfile(file_path)

def get_entries(infilepath: str) -> tuple[int, int]:
    '''
    Get number of original entries and number of actual entries in the file
    '''
    events_processed = 0
    events_in_ttree = 0

    with ROOT.TFile(infilepath, 'READ') as infile:
        #try:
        #    events_processed = infile.Get('eventsProcessed').GetVal()
        #except AttributeError:
        #    LOGGER.warning('Input file is missing information about '
        #                   'original number of events!')

        #try:
        #    events_in_ttree = infile.Get("events").GetEntries()
        #except AttributeError:
        #    LOGGER.error('Input file is missing "events" TTree!\nAborting...')
        #    sys.exit(3)
        try:
            events_processed_obj = infile.Get('eventsProcessed')
            if events_processed_obj:
                events_processed = events_processed_obj.GetVal()
            events_ttree = infile.Get("events")
            if events_ttree:
                events_in_ttree = events_ttree.GetEntries()
            else:
                #print(f"Faulty {infilepath}")
                return None, None

        except AttributeError:
            return None, None


    return events_processed, events_in_ttree

replacement_words = [
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

    'wzp6_ee_nunuH_Htautau_ecm240',
    'wzp6_ee_nunuH_Hbb_ecm240',
    'wzp6_ee_nunuH_Hcc_ecm240',
    'wzp6_ee_nunuH_Hss_ecm240',
    'wzp6_ee_nunuH_Hgg_ecm240',
    'wzp6_ee_nunuH_HWW_ecm240',
    'wzp6_ee_nunuH_HZZ_ecm240',

    'wzp6_ee_eeH_Htautau_ecm240',
    'wzp6_ee_eeH_Hbb_ecm240',
    'wzp6_ee_eeH_Hcc_ecm240',
    'wzp6_ee_eeH_Hss_ecm240',
    'wzp6_ee_eeH_Hgg_ecm240',
    'wzp6_ee_eeH_HWW_ecm240',
    'wzp6_ee_eeH_HZZ_ecm240',

    'wzp6_ee_mumuH_Htautau_ecm240',
    'wzp6_ee_mumuH_Hbb_ecm240',
    'wzp6_ee_mumuH_Hcc_ecm240',
    'wzp6_ee_mumuH_Hss_ecm240',
    'wzp6_ee_mumuH_Hgg_ecm240',
    'wzp6_ee_mumuH_HWW_ecm240',
    'wzp6_ee_mumuH_HZZ_ecm240',

    'wzp6_ee_bbH_Htautau_ecm240',
    'wzp6_ee_bbH_Hbb_ecm240',
    'wzp6_ee_bbH_Hcc_ecm240',
    'wzp6_ee_bbH_Hss_ecm240',
    'wzp6_ee_bbH_Hgg_ecm240',
    'wzp6_ee_bbH_HWW_ecm240',
    'wzp6_ee_bbH_HZZ_ecm240',

    'wzp6_ee_ccH_Htautau_ecm240',
    'wzp6_ee_ccH_Hbb_ecm240',
    'wzp6_ee_ccH_Hcc_ecm240',
    'wzp6_ee_ccH_Hss_ecm240',
    'wzp6_ee_ccH_Hgg_ecm240',
    'wzp6_ee_ccH_HWW_ecm240',
    'wzp6_ee_ccH_HZZ_ecm240',

    'wzp6_ee_ssH_Htautau_ecm240',
    'wzp6_ee_ssH_Hbb_ecm240',
    'wzp6_ee_ssH_Hcc_ecm240',
    'wzp6_ee_ssH_Hss_ecm240',
    'wzp6_ee_ssH_Hgg_ecm240',
    'wzp6_ee_ssH_HWW_ecm240',
    'wzp6_ee_ssH_HZZ_ecm240',

    'wzp6_ee_qqH_Htautau_ecm240',
    'wzp6_ee_qqH_Hbb_ecm240',
    'wzp6_ee_qqH_Hcc_ecm240',
    'wzp6_ee_qqH_Hss_ecm240',
    'wzp6_ee_qqH_Hgg_ecm240',
    'wzp6_ee_qqH_HWW_ecm240',
    'wzp6_ee_qqH_HZZ_ecm240',
]

DIRECTORY = {
    'LL':"/ceph/awiedl/FCCee/HiggsCP/stage2/LL",
    'QQ':"/ceph/awiedl/FCCee/HiggsCP/stage2/QQ",
    'NuNu':"/ceph/awiedl/FCCee/HiggsCP/stage2/NuNu",
}

DIRECTORY_STAGE1 = "/ceph/awiedl/FCCee/HiggsCP/stage1/"

DIRECTORY_EOS = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/"

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

# Define the tree name
tree_name = "events"

tab = []
raw = {}

# Loop through each replacement word
row = []
#row.append(" & $N_{gen}$ & ") #header
'''for replacement_word in replacement_words:

    root_file_path = DIRECTORY_EOS + replacement_word
    process_events = 0
    events_ttree = 0

    flist = glob.glob(root_file_path + '/*.root')
    print(f"{replacement_word} & {len(flist)}")

for replacement_word in replacement_words:

    root_file_path = DIRECTORY_EOS + replacement_word
    process_events = 0
    events_ttree = 0

    flist = glob.glob(root_file_path + '/chunk*.root')
    for filepath in flist:
        chunk_process_events, chunk_events_ttree = get_entries(filepath)
        if chunk_process_events is not None and chunk_events_ttree is not None:
            process_events += chunk_process_events #original number of events
            events_ttree += chunk_events_ttree
    print((f"{replacement_word} & {process_events} & "))
    row.append(f"{replacement_word} & {process_events} & ")
    raw[replacement_word] = process_events
tab.append(row)

'''
for tag in TAG:
    tab = []
    for cat in CAT:
        for sub in SUBDIR:
            directory = DIRECTORY_EOS + tag + "/stage2_241202/" + cat + "/" + sub + "/"
            print(directory)
            newrow = []
            newrow.append(f"{cat+sub} & ") #header

            for replacement_word in replacement_words:
            
                root_file_path = directory + replacement_word
                process_events = 0
                events_ttree = 0

                flist = glob.glob(root_file_path + '/*.root')
                for filepath in flist:
                    chunk_process_events, chunk_events_ttree = get_entries(filepath)
                    if chunk_process_events is not None and chunk_events_ttree is not None:
                        process_events += chunk_process_events #original number of events
                        events_ttree += chunk_events_ttree #number of events after selection=

                newrow.append(f"{events_ttree} & ")

                #if process_events!=0 :
                #    newrow.append(f"{events_ttree/process_events:.2e} & ")
                #else:
                #    ratio = 1/raw[replacement_word]
                #    newrow.append(f"$\leq$ {ratio:.2e} & ") 

            tab.append(newrow)

    # Write the content of the selected row to the output CSV file
    transposed_tab = list(zip(*tab))

    output_file = DIRECTORY_EOS + tag + "/nevents.txt"
    
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        # Write each row of the matrix
        writer.writerows(transposed_tab)
