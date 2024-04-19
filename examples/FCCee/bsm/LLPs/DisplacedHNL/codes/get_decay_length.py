import uproot
import os
import shutil
import numpy as np

replacement_words = [
    "HNL_4e-10_20gev",
    "HNL_4e-10_30gev",
    "HNL_4e-10_40gev",
    "HNL_4e-10_50gev",
    "HNL_4e-10_60gev",
    "HNL_4e-10_70gev",
    "HNL_4e-10_80gev",

    "HNL_1.33e-7_20gev",
    "HNL_1.33e-7_30gev",
    "HNL_1.33e-7_40gev",
    "HNL_1.33e-7_50gev",
    "HNL_1.33e-7_60gev",
    "HNL_1.33e-7_70gev",
    "HNL_1.33e-7_80gev",

    "HNL_2.86e-12_20gev",
    "HNL_2.86e-12_30gev",
    "HNL_2.86e-12_40gev",
    "HNL_2.86e-12_50gev",
    "HNL_2.86e-12_60gev",
    "HNL_2.86e-12_70gev",
    "HNL_2.86e-12_80gev",

    "HNL_5e-12_20gev",
    "HNL_5e-12_30gev",
    "HNL_5e-12_40gev",
    "HNL_5e-12_50gev",
    "HNL_5e-12_60gev",
    "HNL_5e-12_70gev",
    "HNL_5e-12_80gev",

    "HNL_6.67e-10_20gev",
    "HNL_6.67e-10_30gev",
    "HNL_6.67e-10_40gev",
    "HNL_6.67e-10_50gev",
    "HNL_6.67e-10_60gev",
    "HNL_6.67e-10_70gev",
    "HNL_6.67e-10_80gev",

    "HNL_2.86e-7_20gev",
    "HNL_2.86e-7_30gev",
    "HNL_2.86e-7_40gev",
    "HNL_2.86e-7_50gev",
    "HNL_2.86e-7_60gev",
    "HNL_2.86e-7_70gev",
    "HNL_2.86e-7_80gev",
]

replacement_bkgs = [
    "p8_ee_Zee_ecm91",
    "p8_ee_Zmumu_ecm91",
    "p8_ee_Ztautau_ecm91",
    "p8_ee_Zbb_ecm91",
    "p8_ee_Zcc_ecm91",
    #"p8_ee_Zud_ecm91",
    "p8_ee_Zss_ecm91",
    "emununu",
    "tatanunu"
]

replacement_words_flight = [
    "flight_4e-10_20gev",
    "flight_4e-10_30gev",
    "flight_4e-10_40gev",
    "flight_4e-10_50gev",
    "flight_4e-10_60gev",
    "flight_4e-10_70gev",
    "flight_4e-10_80gev",
]

# Define the tree name
tree_name = "events"

# Select the leaf you want to analyze
# automatic checks also prompt variable to get more accurate values
leaf_names = [
    "Reco_Lxyz",
    "FSGen_Lxyz",
]

# Print the results
output_file = "/eos/user/s/sgiappic/2HNL_ana/decay_lenght_histo.txt"

# Write the content of the selected row to the output CSV file
with open(output_file, "a") as file:
    file.write("# file, Reco L, Gen L, n. total (scaled to 180 ab-1) (with bsc)\n")

# Loop through each replacement word
for replacement_word in replacement_words:
 
    # Define the ROOT file path
    #root_file_path = "/eos/user/s/sgiappic/2HNL_bsc/final/{}_sel2RecoDF_vetoes_15-80M_39p_10ME43_cos.root".format(replacement_word)
    #histo_file_path = "/eos/user/s/sgiappic/2HNL_ana/signals_final/{}_sel2RecoDF_vetoes_15-80M_39p_10ME43_cos_histo.root".format(replacement_word)

    #root_file_path = "/eos/user/s/sgiappic/2HNL_bsc/final/{}_sel2RecoSF_vetoes_15-80M_42p_10ME_cos_MEt.root".format(replacement_word)
    #histo_file_path = "/eos/user/s/sgiappic/2HNL_bsc/final/{}_sel2RecoSF_vetoes_15-80M_42p_10ME_cos_MEt_histo.root".format(replacement_word)
    histo_file_path = "/eos/user/s/sgiappic/2HNL_bsc/final/{}_sel2RecoSF_vetoes_histo.root".format(replacement_word)

    #root_file_path = "/eos/user/s/sgiappic/2HNL_ana/final/{}_sel2RecoDF_vetoes_15-80M_39p_10ME43_cos.root".format(replacement_bkg)
    #histo_file_path = "/eos/user/s/sgiappic/2HNL_ana/final/{}_sel2RecoDF_vetoes_15-80M_39p_10ME43_cos_histo.root".format(replacement_bkg)

    #root_file_path = "/eos/user/s/sgiappic/2HNL_ana/final/{}_sel2RecoSF_vetoes_15-80M_42p_10ME_cos_MEt.root".format(replacement_bkg)
    #histo_file_path = "/eos/user/s/sgiappic/2HNL_ana/final/{}_sel2RecoSF_vetoes_15-80M_42p_10ME_cos_MEt_histo.root".format(replacement_bkg)

    # Open the ROOT file
    #root_file = uproot.open(root_file_path)

    # Get the tree from the ROOT file
    #tree = root_file[tree_name]

    # Get the array of values
    #array_1 = tree[leaf_name_1].array()
    #array_2 = tree[leaf_name_2].array()

    # Get the selected leaf from the tree
    histo_file = uproot.open(histo_file_path)

    with open(output_file, "a") as file:
            file.write("{}, ".format(replacement_word))

    for left_name in leaf_names:

        selected_leaf = histo_file[left_name]
        selected_leaf_prompt = histo_file[left_name+"_prompt"]

        # Get scaled number of events from histograms
        y_values = selected_leaf.values()
        y_values_prompt = selected_leaf_prompt.values()
        total_entries = sum(y_values)

        # Get bin edges in arrays
        bin_edges = selected_leaf.axis().edges()
        bin_edges_prompt = selected_leaf_prompt.axis().edges()

        array_1 = []
        array_2 = []

        # get associated value of variable from the bin and store the high edge (low edge of successive bin)
        for i in range(len(bin_edges)-1): #exclude one of the edges as bins have both 0. and max but the content is n-1
            if y_values[i]>0:
                array_1.append(bin_edges[i+1])

        for i in range(len(bin_edges_prompt)-1):
            if y_values_prompt[i]>0:
                array_2.append(bin_edges_prompt[i+1])

        if len(array_1) == 0:
            x_1 = 0 
        else:
            x_1 = np.max(array_1)

        if len(array_2) == 0:
            x_2 = 0 
        else:
            x_2 = np.max(array_2)

        #store the correct value depending on range
        if x_1 > 20.0:
            x = x_1
        else:
            x = x_2

        #print(x)

        # Write the content of the selected row to the output CSV file
        with open(output_file, "a") as file:
            file.write("{}, ".format(x))
    
    with open(output_file, "a") as file:
            file.write("\n")

    print("Content from {} has been written to {}".format(replacement_word, output_file))

