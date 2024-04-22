import uproot
import os
import shutil
import numpy as np

replacement_words = [
    #'HNL_4e-8_10gev',
    'HNL_1.33e-9_20gev',
    'HNL_2.86e-12_30gev',
    'HNL_2.86e-7_30gev',
    'HNL_5e-12_40gev',
    'HNL_4e-12_50gev',
    'HNL_6.67e-8_60gev',
    'HNL_4e-8_60gev',
    'HNL_2.86e-9_70gev',
    'HNL_2.86e-8_80gev',
]

replacement_bkgs = [
    "p8_ee_Zee_ecm91",
    #"p8_ee_Zmumu_ecm91",
    #"p8_ee_Ztautau_ecm91",
    #"p8_ee_Zbb_ecm91",
    #"p8_ee_Zcc_ecm91",
    #"p8_ee_Zud_ecm91",
    #"p8_ee_Zss_ecm91",
    "emununu",
    #"tatanunu"
]

# Define the tree name
tree_name = "events"

# Select the leaf you want to analyze
# automatic checks also prompt variable to get more accurate values
leaf_name = "Reco_Lxy_prompt"

dir = "/eos/user/s/sgiappic/2HNL_ana/final/"

cuts = [
    
    "sel2RecoSF_vetoes_tracks_M80_p40_11.5MEpt_0.8cos",
    "sel2RecoDF_vetoes_tracks_M80_7MEpt_0.8cos",
]

for cut in cuts:

    # Print the results
    output_file = "/eos/user/s/sgiappic/2HNL_ana/" +leaf_name+ "_" +cut+"_optimization.txt"

    # book array for background entries
    entries_bkg = []

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

        entries = []

        # get associated value of variable from the bin and store the high edge (low edge of successive bin)
        for i in range(len(bin_edges)-60): #exclude one of the edges as bins have both 0. and max but the content is n-1
            #entries.append(sum(y_values[:i]))
            entries.append(sum(y_values[i:]))

        #add the entries for each background into the same array
        for i in range(len(entries)):
            if len(entries_bkg) < len(entries):
                entries_bkg.append(entries[i]) 
            else:
                entries_bkg[i] += entries[i]

    for replacement_word in replacement_words:

        # Define the ROOT file path
        signal_file_path = dir + "{}_".format(replacement_word)+ cut + "_histo.root"

        # Get the selected leaf from the tree
        signal_file = uproot.open(signal_file_path)

        signal_leaf = signal_file[leaf_name]

        # Get scaled number of events from histograms, array
        y_values_signal = signal_leaf.values()

        # Get bin edges in arrays
        bin_edges_signal = selected_leaf.axis().edges()

        entries_signal = []

        # get associated value of variable from the bin and store the high edge (low edge of successive bin)
        for i in range(len(bin_edges_signal)-60): #exclude one of the edges as bins have both 0. and max but the content is n-1
            #entries_signal.append(sum(y_values_signal[:i]))
            entries_signal.append(sum(y_values_signal[i:]))

        # calculate significance for each bin 
        s = []

        for i in range(len(entries_bkg)):
            if entries_signal[i]>0:
                s.append(entries_signal[i] / np.sqrt(entries_signal[i] + entries_bkg[i]))
                
                with open(output_file, "a") as file:
                    file.write("significance = {} for cut at cos={} Gev \n".format(s[i], i*(-0.02)))
            
        s_max = np.max(s)
        index = s.index(s_max)*(-0.02)

        with open(output_file, "a") as file:
            file.write("\n Max significance of {} = {} for cut at L_xy={} Gev \n\n".format(replacement_word, s_max, index))
