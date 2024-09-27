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

DIRECTORY_EFF = "/ceph/awiedl/FCCee/HiggsCP/stage2_eff"

DIRECTORY = "/ceph/awiedl/FCCee/HiggsCP/stage2"

SUBDIR = [
    #'LL',
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

# Print the results
output_file = "/ceph/awiedl/FCCee/HiggsCP/stage2_eff/nevents_tree.txt"

tab = []
raw = {}

# Loop through each replacement word
row = []
row.append("Signal category & Efficiency of $\tau$ reconstruction \\ \hline") #header
for cat in CAT:
    for sub in SUBDIR:
        events_jets = 0
        events_tau = 0
        eff = 0
        for replacement_word in replacement_words:

            #run over files with taus from function
            root_file_path = f"{DIRECTORY_EFF}/{cat}/{sub}/{replacement_word}.root"
            process_events = 0
            events_ttree = 0

            chunk_process_events, chunk_events_ttree = get_entries(root_file_path)
            if chunk_process_events is not None and chunk_events_ttree is not None:
                process_events += chunk_process_events #original number of events
                events_ttree += chunk_events_ttree
            
            #sum all events for signals
            events_jets += events_ttree
            #print(f"{cat}, {sub}, {replacement_word}, {events_jets}")
            
            #now for jets instead of taus
            root_file_path1 = f"{DIRECTORY}/{cat}/{sub}/{replacement_word}"
            process_events1 = 0
            events_ttree1 = 0

            flist1 = glob.glob(root_file_path1 + '/chunk*.root')
            for filepath1 in flist1:
                chunk_process_events1, chunk_events_ttree1 = get_entries(filepath1)
                if chunk_process_events1 is not None and chunk_events_ttree1 is not None:
                    process_events1 += chunk_process_events1 #original number of events
                    events_ttree1 += chunk_events_ttree1
            
            #sum all events for signals
            events_tau += events_ttree1
            #print(f"{events_tau}")

        #get efficiency as tau events / jets events for each category
        if events_jets!=0:
            eff = events_tau / events_jets

        row.append(f"{cat+sub} & {eff*100:.1f}\%" + " \\ \hline")

tab.append(row)

# Write the content of the selected row to the output CSV file
transposed_tab = list(zip(*tab))
 
with open(output_file, "w", newline="") as file:
    writer = csv.writer(file)
    # Write each row of the matrix
    writer.writerows(transposed_tab)
