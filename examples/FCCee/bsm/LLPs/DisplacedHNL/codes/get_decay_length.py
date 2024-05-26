import uproot
import os
import shutil
import numpy as np

replacement_words = [
        "HNL_1.33e-7_10gev",
    "HNL_1.33e-7_20gev",
    "HNL_1.33e-7_30gev",
    "HNL_1.33e-7_40gev",
    "HNL_1.33e-7_50gev",
    "HNL_1.33e-7_60gev",
    "HNL_1.33e-7_70gev",
    "HNL_1.33e-7_80gev",

    "HNL_2.86e-8_10gev",
    "HNL_2.86e-8_20gev",
    "HNL_2.86e-8_30gev",
    "HNL_2.86e-8_40gev",
    "HNL_2.86e-8_50gev",
    "HNL_2.86e-8_60gev",
    "HNL_2.86e-8_70gev",
    "HNL_2.86e-8_80gev",

    "HNL_1.33e-9_10gev",
    "HNL_1.33e-9_20gev",
    "HNL_1.33e-9_30gev",
    "HNL_1.33e-9_40gev",
    "HNL_1.33e-9_50gev",
    "HNL_1.33e-9_60gev",
    "HNL_1.33e-9_70gev",
    "HNL_1.33e-9_80gev",

    "HNL_4e-10_10gev",
    "HNL_4e-10_20gev",
    "HNL_4e-10_30gev",
    "HNL_4e-10_40gev",
    "HNL_4e-10_50gev",
    "HNL_4e-10_60gev",
    "HNL_4e-10_70gev",
    "HNL_4e-10_80gev",

    "HNL_1.33e-11_10gev",
    "HNL_1.33e-11_20gev",
    "HNL_1.33e-11_30gev",
    "HNL_1.33e-11_40gev",
    "HNL_1.33e-11_50gev",
    "HNL_1.33e-11_60gev",
    "HNL_1.33e-11_70gev",
    "HNL_1.33e-11_80gev",

    "HNL_2.86e-12_10gev",
    "HNL_2.86e-12_20gev",
    "HNL_2.86e-12_30gev",
    "HNL_2.86e-12_40gev",
    "HNL_2.86e-12_50gev",
    "HNL_2.86e-12_60gev",
    "HNL_2.86e-12_70gev",
    "HNL_2.86e-12_80gev",

    #inverted

    "HNL_2.86e-7_10gev",
    "HNL_2.86e-7_20gev",
    "HNL_2.86e-7_30gev",
    "HNL_2.86e-7_40gev",
    "HNL_2.86e-7_50gev",
    "HNL_2.86e-7_60gev",
    "HNL_2.86e-7_70gev",
    "HNL_2.86e-7_80gev",

    "HNL_5e-8_10gev",
    "HNL_5e-8_20gev",
    "HNL_5e-8_30gev",
    "HNL_5e-8_40gev",
    "HNL_5e-8_50gev",
    "HNL_5e-8_60gev",
    "HNL_5e-8_70gev",
    "HNL_5e-8_80gev",

    "HNL_2.86e-9_10gev",
    "HNL_2.86e-9_20gev",
    "HNL_2.86e-9_30gev",
    "HNL_2.86e-9_40gev",
    "HNL_2.86e-9_50gev",
    "HNL_2.86e-9_60gev",
    "HNL_2.86e-9_70gev",
    "HNL_2.86e-9_80gev",

    "HNL_6.67e-10_10gev",
    "HNL_6.67e-10_20gev",
    "HNL_6.67e-10_30gev",
    "HNL_6.67e-10_40gev",
    "HNL_6.67e-10_50gev",
    "HNL_6.67e-10_60gev",
    "HNL_6.67e-10_70gev",
    "HNL_6.67e-10_80gev",

    "HNL_2.86e-11_10gev",
    "HNL_2.86e-11_20gev",
    "HNL_2.86e-11_30gev",
    "HNL_2.86e-11_40gev",
    "HNL_2.86e-11_50gev",
    "HNL_2.86e-11_60gev",
    "HNL_2.86e-11_70gev",
    "HNL_2.86e-11_80gev",

    "HNL_5e-12_10gev",
    "HNL_5e-12_20gev",
    "HNL_5e-12_30gev",
    "HNL_5e-12_40gev",
    "HNL_5e-12_50gev",
    "HNL_5e-12_60gev",
    "HNL_5e-12_70gev",
    "HNL_5e-12_80gev",
]

replacement_bkgs = [
    #"p8_ee_Zee_ecm91",
    #"p8_ee_Zmumu_ecm91",
    #"p8_ee_Ztautau_ecm91",
    #"p8_ee_Zbb_ecm91",
    #"p8_ee_Zcc_ecm91",
    #"p8_ee_Zud_ecm91",
    #"p8_ee_Zss_ecm91",
    #"emununu",
    #"tatanunu"
]

replacement_words_flight = [
    'HNL_4e-8_10gev',
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

# Define the tree name
tree_name = "events"

# Select the leaf you want to analyze
# automatic checks also prompt variable to get more accurate values
leaf_names = [
    "Reco_Lxyz",
    #"FSGen_Lxyz",
]

# Print the results
output_file = "/eos/user/s/sgiappic/2HNL_ana/decay_lenght_mean.txt"

# Write the content of the selected row to the output CSV file
with open(output_file, "a") as file:
    file.write("# file, Reco L, n. total (scaled to 180 ab-1) \n")

# Loop through each replacement word
for replacement_word in replacement_words:
 
    # Define the ROOT file path
    #root_file_path = "/eos/user/s/sgiappic/2HNL_bsc/final/{}_sel2RecoDF_vetoes_15-80M_39p_10ME43_cos.root".format(replacement_word)
    histo_file_path = "/eos/user/s/sgiappic/2HNL_ana/final_final/{}_sel2RecoSF_vetoes_tracks_M80_p40_11.5MEpt_0.8cos_chi_0.55d0_histo.root".format(replacement_word)

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
        #total_entries = sum(y_values)

        # Get bin edges in arrays
        bin_edges = selected_leaf.axis().edges()
        bin_edges_prompt = selected_leaf_prompt.axis().edges()

        x_1 = []
        x_2 = []
        L = []
        # calculate the decay lenght by taking the weighted mean value across the populated bins
        for i in range(len(bin_edges)-1):
            x_1.append(bin_edges[i] * y_values[i])
        L_1 = sum(x_1) / sum(y_values)

        for i in range(len(bin_edges_prompt)-1):
            x_2.append(bin_edges_prompt[i] * y_values_prompt[i])
            if y_values_prompt[i]!=0 :
                L.append(bin_edges_prompt[i])
        L_2 = sum(x_2) / sum(y_values_prompt)

        if len(L) > 0:
            L_min = np.min(L)
        else:
            L_min = 10

        #store the correct value depending on range
        if L_1>20.:
            x = L_1
        else:
            x = L_2

        #print(x)

        # Write the content of the selected row to the output CSV file
        with open(output_file, "a") as file:
            file.write("{}, {} \n".format(x, L_min))
    
    #with open(output_file, "a") as file:
            #file.write("{} \n".format(total_entries))

    print("Content from {} has been written to {}".format(replacement_word, output_file))

