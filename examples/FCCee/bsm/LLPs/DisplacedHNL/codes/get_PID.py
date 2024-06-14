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
    "p8_ee_Zee_ecm91",
    "p8_ee_Zmumu_ecm91",
    #"p8_ee_Ztautau_ecm91",
    #"p8_ee_Zbb_ecm91",
    #"p8_ee_Zcc_ecm91",
    #"p8_ee_Zud_ecm91",
    #"p8_ee_Zss_ecm91",
    #"emununu",
    #"tatanunu",
    #'HNL_2.86e-7_30gev',
    'HNL_2.86e-12_30gev',
    #'HNL_6.67e-10_30gev',
    'HNL_5e-12_60gev',
    'HNL_1.33e-7_40gev',
]

# Define the tree name
tree_name = "events"

# Select the leaf you want to analyze
# automatic checks also prompt variable to get more accurate values
leaf_names = [
    "FSGenParticles_PID",
    #"FSGen_Lxyz",
]

# Print the results
output_file = "/eos/user/s/sgiappic/2HNL_ana/problematic/GenPID_2.txt"

# Write the content of the selected row to the output CSV file
with open(output_file, "a") as file:
    file.write("# genPID, n. particles\n")

# Loop through each replacement word
for replacement_word in replacement_bkgs:
 
    # Define the ROOT file path
    #root_file_path = "/eos/user/s/sgiappic/2HNL_bsc/final/{}_sel2RecoDF_vetoes_15-80M_39p_10ME43_cos.root".format(replacement_word)
    histo_file_path = "/eos/user/s/sgiappic/2HNL_ana/problematic/{}_sel2Reco_vetoes_histo.root".format(replacement_word)

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
            file.write("{}: \n".format(replacement_word))

    for left_name in leaf_names:

        selected_leaf = histo_file[left_name]
        selected_leaf_prompt = histo_file["RecoMissingEnergy_e"]

        # Get scaled number of events from histograms
        y_values = selected_leaf.values()
        y_values_events = selected_leaf_prompt.values()
        total_entries = sum(y_values_events)

        # Get bin edges in arrays
        bin_edges = selected_leaf.axis().edges()
        #bin_edges_prompt = selected_leaf_prompt.axis().edges()

        # calculate the decay lenght by taking the weighted mean value across the populated bins
        with open(output_file, "a") as file:
            for i in range(len(bin_edges)-1):
                if (y_values[i]>0):
                    x_1=bin_edges[i]
                    x_2=y_values[i]
                    file.write("{}, {} \n".format(x_1, x_2))
                

        # Write the content of the selected row to the output CSV file
        with open(output_file, "a") as file:
            file.write("n. events: {}\n\n".format(total_entries))
    
    #with open(output_file, "a") as file:
            #file.write("{} \n".format(total_entries))

    print("Content from {} has been written to {}".format(replacement_word, output_file))

