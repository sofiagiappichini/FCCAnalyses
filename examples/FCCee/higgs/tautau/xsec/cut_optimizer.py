import uproot
import os
import shutil
import numpy as np

replacement_sig = [
    'wzp6_ee_mumuH_Htautau_ecm240',
    'wzp6_ee_qqH_Htautau_ecm240',
    'wzp6_ee_ssH_Htautau_ecm240',
    'wzp6_ee_nunuH_Htautau_ecm240',
    'wzp6_ee_bbH_Htautau_ecm240',
    'wzp6_ee_ccH_Htautau_ecm240',
    'wzp6_ee_eeH_Htautau_ecm240'
]

replacement_bkgs = [
    'p8_ee_WW_ecm240',
    'p8_ee_Zqq_ecm240',
    'p8_ee_ZZ_ecm240',
    'wzp6_ee_tautau_ecm240',
    'wzp6_ee_mumu_ecm240',
    'wzp6_ee_ee_Mee_30_150_ecm240',
]

# Define the tree name
tree_name = "events"

# Select the leaf you want to analyze
# automatic checks also prompt variable to get more accurate values
leaf_name = "TauTag_isTAU"

DIRECTORY = {
    'LL':"/ceph/awiedl/FCCee/HiggsCP/final_tag/LL/",
    'QQ':"/ceph/awiedl/FCCee/HiggsCP/final_tag/QQ/",
    'NuNu':"/ceph/awiedl/FCCee/HiggsCP/final_tag/NuNu/",
}

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

CUT = [
    "selReco",
]

output_file = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/" +leaf_name+ "_optimization.txt"

for cut in CUT:
    for cat in CAT:
        for sub in SUBDIR:

            dir = DIRECTORY[cat] + sub + "/"

            # book array for background entries
            entries_bkg = []

            entries_sig = []

            # Loop through each replacement word
            for replacement_word in replacement_bkgs:
            
                # Define the ROOT file path
                histo_file_path = dir + "{}_".format(replacement_word) + cut + "_histo.root"

                # Get the selected leaf from the tree
                histo_file = uproot.open(histo_file_path)

                selected_leaf = histo_file[leaf_name]

                # Get scaled number of events from histograms, array
                y_values = selected_leaf.values()

                # Get bin edges in arrays
                bin_edges = selected_leaf.axis().edges()

                temp_bkg = []

                # get associated value of variable from the bin and store the high edge (low edge of successive bin)
                for i in range(0, len(bin_edges)-1, 1): #exclude one of the edges as bins have both 0. and max but the content is n-1
                #for i in range(len(bin_edges), len(bin_edges)-50, -1):
                    #entries.append(sum(y_values[:i]))
                    temp_bkg.append(sum(y_values[i:]))

                #add the entries for each background into the same array
                for i in range(len(temp_bkg)):
                    if len(entries_bkg) < len(temp_bkg):
                        entries_bkg.append(temp_bkg[i]) 
                    else:
                        entries_bkg[i] += temp_bkg[i]

            for replacement_word in replacement_sig:

                # Define the ROOT file path
                signal_file_path = dir + "{}_".format(replacement_word)+ cut + "_histo.root"

                # Get the selected leaf from the tree
                signal_file = uproot.open(signal_file_path)

                signal_leaf = signal_file[leaf_name]

                # Get scaled number of events from histograms, array
                y_values_signal = signal_leaf.values()

                # Get bin edges in arrays
                bin_edges_signal = selected_leaf.axis().edges()

                temp_sig = []

                # get associated value of variable from the bin and store the high edge (low edge of successive bin)
                for i in range(0, len(bin_edges)-1, 1): #exclude one of the edges as bins have both 0. and max but the content is n-1
                #for i in range(len(bin_edges), len(bin_edges)-50, -1):
                    #entries_signal.append(sum(y_values_signal[:i]))
                    temp_sig.append(sum(y_values_signal[i:]))

                #add the entries for each signal into the same array
                for i in range(len(temp_sig)):
                    if len(entries_sig) < len(temp_sig):
                        entries_sig.append(temp_sig[i]) 
                    else:
                        entries_sig[i] += temp_sig[i]

            # calculate significance for each bin 
            s = []

            for i in range(len(entries_bkg)):
                if entries_signal[i]>0:
                    s.append(entries_signal[i] / np.sqrt(entries_signal[i] + entries_bkg[i]))
                    
                    with open(output_file, "a") as file:
                        file.write("significance = {} for cut at TAU={} \n".format(s[i], i*(0.01)))
                
            s_max = np.max(s)
            index = s.index(s_max)*(0.01)

            with open(output_file, "a") as file:
                file.write("\n Max significance of {} = {} for cut at TAU={} \n\n".format(cat+sub, s_max, index))

            print("File written at {}".format(output_file))