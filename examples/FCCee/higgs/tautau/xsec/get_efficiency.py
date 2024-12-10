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
                return None, None

        except AttributeError:
            return None, None


    return events_processed, events_in_ttree

replacement_words = [
    'wzp6_ee_mumuH_Htautau_ecm240',
    'wzp6_ee_nunuH_Htautau_ecm240',
    'wzp6_ee_eeH_Htautau_ecm240',
    'wzp6_ee_qqH_Htautau_ecm240',
    'wzp6_ee_ssH_Htautau_ecm240',
    'wzp6_ee_ccH_Htautau_ecm240',
    'wzp6_ee_bbH_Htautau_ecm240',
]

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

DIRECTORY_EOS = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/"

TAG = [
    #"R5-explicit",
    #"R5-tag",
    "ktN-explicit",
    #"ktN-tag",
]

SUBDIR = [
    #'LL',
    'LH',
    #'HH',
]
#category to plot
CAT = [
    "QQ",
    #"LL",
    #"NuNu",
]

# Define the tree name
tree_name = "events"

tab = []
raw = {}

# Loop through each replacement word
row = []
row.append("Signal category & R5 explciit & & R5 PNet & & ktN explicit & & ktN PNet & ") #header
row.append(" & Signal & Background & Signal & Background & Signal & Background & Signal & Background ")
for cat in CAT:
    for sub in SUBDIR:

        row.append(f"{cat+sub} & ")
        
        for tag in TAG:

            process_events = 0
            events_ttree = 0
            eff = 0

            for replacement_word in replacement_words:

                #run over files with taus from function
                root_file_path = f"{DIRECTORY_EOS}/{tag}/stage2_241202/{cat}/{sub}/{replacement_word}"
                root_file_path_og = f"{DIRECTORY_EOS}/{replacement_word}"
                flist = glob.glob(root_file_path + '/*.root')
                flist_og = glob.glob(root_file_path_og + '/*.root')

                for filepath in flist:
                    chunk_process_events, chunk_events_ttree = get_entries(filepath)
                    if chunk_process_events is not None and chunk_events_ttree is not None:
                        #process_events += chunk_process_events #original number of events
                        events_ttree += chunk_events_ttree

                for filepath in flist_og:
                    chunk_process_events, chunk_events_ttree = get_entries(filepath)
                    if chunk_process_events is not None and chunk_events_ttree is not None:
                        process_events += chunk_process_events #original number of events
                        #events_ttree += chunk_events_ttree
                        
            process_events_b = 0
            events_ttree_b = 0
            eff_b = 0
                        
            for replacement_word in replacement_bkgs:

                #run over files with taus from function
                root_file_path = f"{DIRECTORY_EOS}/{tag}/stage2_241202/{cat}/{sub}/{replacement_word}"
                root_file_path_og = f"{DIRECTORY_EOS}/{replacement_word}"
                flist = glob.glob(root_file_path + '/*.root')
                flist_og = glob.glob(root_file_path_og + '/*.root')

                for filepath in flist:
                    chunk_process_events, chunk_events_ttree = get_entries(filepath)
                    if chunk_process_events is not None and chunk_events_ttree is not None:
                        #process_events += chunk_process_events #original number of events
                        events_ttree_b += chunk_events_ttree

                for filepath in flist_og:
                    chunk_process_events, chunk_events_ttree = get_entries(filepath)
                    if chunk_process_events is not None and chunk_events_ttree is not None:
                        process_events_b += chunk_process_events #original number of events
                        #events_ttree += chunk_events_ttree
                        
                    #print(f"{root_file_path}, {cat+sub}, {process_events}, {events_ttree}")
                
            if events_ttree!=0 :
                eff = events_ttree/process_events
            if events_ttree_b!=0 :
                eff_b = events_ttree_b/process_events_b

            row[-1] += f"{eff:.3f} & {eff_b:.3f} &"

            print(f"{eff:.3f} & {eff_b:.3f} &")

tab.append(row)

# Write the content of the selected row to the output CSV file
transposed_tab = list(zip(*tab))

output_file = DIRECTORY_EOS + "efficiency/cat_eff.txt"
 
#with open(output_file, "w", newline="") as file:
#    writer = csv.writer(file)
    # Write each row of the matrix
#    writer.writerows(transposed_tab)
