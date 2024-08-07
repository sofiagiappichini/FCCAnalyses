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

    "HNL_2.78e-8_10gev",
    "HNL_2.78e-8_20gev",
    "HNL_2.78e-8_30gev",
    "HNL_2.78e-8_40gev",
    "HNL_2.78e-8_50gev",
    "HNL_2.78e-8_60gev",
    "HNL_2.78e-8_70gev",
    "HNL_2.78e-8_80gev",

    "HNL_6.05e-9_10gev",
    "HNL_6.05e-9_20gev",
    "HNL_6.05e-9_30gev",
    "HNL_6.05e-9_40gev",
    "HNL_6.05e-9_50gev",
    "HNL_6.05e-9_60gev",
    "HNL_6.05e-9_70gev",
    "HNL_6.05e-9_80gev",

    "HNL_1.33e-9_10gev",
    "HNL_1.33e-9_20gev",
    "HNL_1.33e-9_30gev",
    "HNL_1.33e-9_40gev",
    "HNL_1.33e-9_50gev",
    "HNL_1.33e-9_60gev",
    "HNL_1.33e-9_70gev",
    "HNL_1.33e-9_80gev",

    "HNL_2.90e-10_10gev",
    "HNL_2.90e-10_20gev",
    "HNL_2.90e-10_30gev",
    "HNL_2.90e-10_40gev",
    "HNL_2.90e-10_50gev",
    "HNL_2.90e-10_60gev",
    "HNL_2.90e-10_70gev",
    "HNL_2.90e-10_80gev",

    "HNL_6.34e-11_10gev",
    "HNL_6.34e-11_20gev",
    "HNL_6.34e-11_30gev",
    "HNL_6.34e-11_40gev",
    "HNL_6.34e-11_50gev",
    "HNL_6.34e-11_60gev",
    "HNL_6.34e-11_70gev",
    "HNL_6.34e-11_80gev",

    "HNL_1.33e-11_10gev",
    "HNL_1.33e-11_20gev",
    "HNL_1.33e-11_30gev",
    "HNL_1.33e-11_40gev",
    "HNL_1.33e-11_50gev",
    "HNL_1.33e-11_60gev",
    "HNL_1.33e-11_70gev",
    "HNL_1.33e-11_80gev",

    #######

    "HNL_4e-8_10gev",
    "HNL_4e-8_20gev",
    "HNL_4e-8_30gev",
    "HNL_4e-8_40gev",
    "HNL_4e-8_50gev",
    "HNL_4e-8_60gev",
    "HNL_4e-8_70gev",
    "HNL_4e-8_80gev",

    "HNL_8.35e-9_10gev",
    "HNL_8.35e-9_20gev",
    "HNL_8.35e-9_30gev",
    "HNL_8.35e-9_40gev",
    "HNL_8.35e-9_50gev",
    "HNL_8.35e-9_60gev",
    "HNL_8.35e-9_70gev",
    "HNL_8.35e-9_80gev",

    "HNL_1.81e-9_10gev",
    "HNL_1.81e-9_20gev",
    "HNL_1.81e-9_30gev",
    "HNL_1.81e-9_40gev",
    "HNL_1.81e-9_50gev",
    "HNL_1.81e-9_60gev",
    "HNL_1.81e-9_70gev",
    "HNL_1.81e-9_80gev",

    "HNL_4e-10_10gev",
    "HNL_4e-10_20gev",
    "HNL_4e-10_30gev",
    "HNL_4e-10_40gev",
    "HNL_4e-10_50gev",
    "HNL_4e-10_60gev",
    "HNL_4e-10_70gev",
    "HNL_4e-10_80gev",

    "HNL_8.69e-11_10gev",
    "HNL_8.69e-11_20gev",
    "HNL_8.69e-11_30gev",
    "HNL_8.69e-11_40gev",
    "HNL_8.69e-11_50gev",
    "HNL_8.69e-11_60gev",
    "HNL_8.69e-11_70gev",
    "HNL_8.69e-11_80gev",

    "HNL_1.90e-11_10gev",
    "HNL_1.90e-11_20gev",
    "HNL_1.90e-11_30gev",
    "HNL_1.90e-11_40gev",
    "HNL_1.90e-11_50gev",
    "HNL_1.90e-11_60gev",
    "HNL_1.90e-11_70gev",
    "HNL_1.90e-11_80gev",

    "HNL_4e-12_10gev",
    "HNL_4e-12_20gev",
    "HNL_4e-12_30gev",
    "HNL_4e-12_40gev",
    "HNL_4e-12_50gev",
    "HNL_4e-12_60gev",
    "HNL_4e-12_70gev",
    "HNL_4e-12_80gev",

    #########

    "HNL_2.86e-8_10gev",
    "HNL_2.86e-8_20gev",
    "HNL_2.86e-8_30gev",
    "HNL_2.86e-8_40gev",
    "HNL_2.86e-8_50gev",
    "HNL_2.86e-8_60gev",
    "HNL_2.86e-8_70gev",
    "HNL_2.86e-8_80gev",

    "HNL_5.97e-9_10gev",
    "HNL_5.97e-9_20gev",
    "HNL_5.97e-9_30gev",
    "HNL_5.97e-9_40gev",
    "HNL_5.97e-9_50gev",
    "HNL_5.97e-9_60gev",
    "HNL_5.97e-9_70gev",
    "HNL_5.97e-9_80gev",

    "HNL_1.30e-9_10gev",
    "HNL_1.30e-9_20gev",
    "HNL_1.30e-9_30gev",
    "HNL_1.30e-9_40gev",
    "HNL_1.30e-9_50gev",
    "HNL_1.30e-9_60gev",
    "HNL_1.30e-9_70gev",
    "HNL_1.30e-9_80gev",

    "HNL_2.86e-10_10gev",
    "HNL_2.86e-10_20gev",
    "HNL_2.86e-10_30gev",
    "HNL_2.86e-10_40gev",
    "HNL_2.86e-10_50gev",
    "HNL_2.86e-10_60gev",
    "HNL_2.86e-10_70gev",
    "HNL_2.86e-10_80gev",

    "HNL_6.20e-11_10gev",
    "HNL_6.20e-11_20gev",
    "HNL_6.20e-11_30gev",
    "HNL_6.20e-11_40gev",
    "HNL_6.20e-11_50gev",
    "HNL_6.20e-11_60gev",
    "HNL_6.20e-11_70gev",
    "HNL_6.20e-11_80gev",

    "HNL_1.36e-11_10gev",
    "HNL_1.36e-11_20gev",
    "HNL_1.36e-11_30gev",
    "HNL_1.36e-11_40gev",
    "HNL_1.36e-11_50gev",
    "HNL_1.36e-11_60gev",
    "HNL_1.36e-11_70gev",
    "HNL_1.36e-11_80gev",

    "HNL_2.86e-12_10gev",
    "HNL_2.86e-12_20gev",
    "HNL_2.86e-12_30gev",
    "HNL_2.86e-12_40gev",
    "HNL_2.86e-12_50gev",
    "HNL_2.86e-12_60gev",
    "HNL_2.86e-12_70gev",
    "HNL_2.86e-12_80gev",

    #inverted

    "HNL_5e-8_10gev",
    "HNL_5e-8_20gev",
    "HNL_5e-8_30gev",
    "HNL_5e-8_40gev",
    "HNL_5e-8_50gev",
    "HNL_5e-8_60gev",
    "HNL_5e-8_70gev",
    "HNL_5e-8_80gev",

    "HNL_1.04e-8_10gev",
    "HNL_1.04e-8_20gev",
    "HNL_1.04e-8_30gev",
    "HNL_1.04e-8_40gev",
    "HNL_1.04e-8_50gev",
    "HNL_1.04e-8_60gev",
    "HNL_1.04e-8_70gev",
    "HNL_1.04e-8_80gev",

    "HNL_2.27e-9_10gev",
    "HNL_2.27e-9_20gev",
    "HNL_2.27e-9_30gev",
    "HNL_2.27e-9_40gev",
    "HNL_2.27e-9_50gev",
    "HNL_2.27e-9_60gev",
    "HNL_2.27e-9_70gev",
    "HNL_2.27e-9_80gev",

    "HNL_5e-10_10gev",
    "HNL_5e-10_20gev",
    "HNL_5e-10_30gev",
    "HNL_5e-10_40gev",
    "HNL_5e-10_50gev",
    "HNL_5e-10_60gev",
    "HNL_5e-10_70gev",
    "HNL_5e-10_80gev",

    "HNL_1.09e-10_10gev",
    "HNL_1.09e-10_20gev",
    "HNL_1.09e-10_30gev",
    "HNL_1.09e-10_40gev",
    "HNL_1.09e-10_50gev",
    "HNL_1.09e-10_60gev",
    "HNL_1.09e-10_70gev",
    "HNL_1.09e-10_80gev",

    "HNL_2.38e-11_10gev",
    "HNL_2.38e-11_20gev",
    "HNL_2.38e-11_30gev",
    "HNL_2.38e-11_40gev",
    "HNL_2.38e-11_50gev",
    "HNL_2.38e-11_60gev",
    "HNL_2.38e-11_70gev",
    "HNL_2.38e-11_80gev",

    "HNL_5e-12_10gev",
    "HNL_5e-12_20gev",
    "HNL_5e-12_30gev",
    "HNL_5e-12_40gev",
    "HNL_5e-12_50gev",
    "HNL_5e-12_60gev",
    "HNL_5e-12_70gev",
    "HNL_5e-12_80gev",

    #######

    "HNL_6.67e-8_10gev",
    "HNL_6.67e-8_20gev",
    "HNL_6.67e-8_30gev",
    "HNL_6.67e-8_40gev",
    "HNL_6.67e-8_50gev",
    "HNL_6.67e-8_60gev",
    "HNL_6.67e-8_70gev",
    "HNL_6.67e-8_80gev",

    "HNL_1.39e-8_10gev",
    "HNL_1.39e-8_20gev",
    "HNL_1.39e-8_30gev",
    "HNL_1.39e-8_40gev",
    "HNL_1.39e-8_50gev",
    "HNL_1.39e-8_60gev",
    "HNL_1.39e-8_70gev",
    "HNL_1.39e-8_80gev",

    "HNL_3.02e-9_10gev",
    "HNL_3.02e-9_20gev",
    "HNL_3.02e-9_30gev",
    "HNL_3.02e-9_40gev",
    "HNL_3.02e-9_50gev",
    "HNL_3.02e-9_60gev",
    "HNL_3.02e-9_70gev",
    "HNL_3.02e-9_80gev",

    "HNL_6.67e-10_10gev",
    "HNL_6.67e-10_20gev",
    "HNL_6.67e-10_30gev",
    "HNL_6.67e-10_40gev",
    "HNL_6.67e-10_50gev",
    "HNL_6.67e-10_60gev",
    "HNL_6.67e-10_70gev",
    "HNL_6.67e-10_80gev",

    "HNL_1.45e-10_10gev",
    "HNL_1.45e-10_20gev",
    "HNL_1.45e-10_30gev",
    "HNL_1.45e-10_40gev",
    "HNL_1.45e-10_50gev",
    "HNL_1.45e-10_60gev",
    "HNL_1.45e-10_70gev",
    "HNL_1.45e-10_80gev",

    "HNL_3.17e-11_10gev",
    "HNL_3.17e-11_20gev",
    "HNL_3.17e-11_30gev",
    "HNL_3.17e-11_40gev",
    "HNL_3.17e-11_50gev",
    "HNL_3.17e-11_60gev",
    "HNL_3.17e-11_70gev",
    "HNL_3.17e-11_80gev",

    "HNL_6.67e-12_10gev",
    "HNL_6.67e-12_20gev",
    "HNL_6.67e-12_30gev",
    "HNL_6.67e-12_40gev",
    "HNL_6.67e-12_50gev",
    "HNL_6.67e-12_60gev",
    "HNL_6.67e-12_70gev",
    "HNL_6.67e-12_80gev",

    ########

    "HNL_2.86e-7_10gev",
    "HNL_2.86e-7_20gev",
    "HNL_2.86e-7_30gev",
    "HNL_2.86e-7_40gev",
    "HNL_2.86e-7_50gev",
    "HNL_2.86e-7_60gev",
    "HNL_2.86e-7_70gev",
    "HNL_2.86e-7_80gev",

    "HNL_5.97e-8_10gev",
    "HNL_5.97e-8_20gev",
    "HNL_5.97e-8_30gev",
    "HNL_5.97e-8_40gev",
    "HNL_5.97e-8_50gev",
    "HNL_5.97e-8_60gev",
    "HNL_5.97e-8_70gev",
    "HNL_5.97e-8_80gev",

    "HNL_1.30e-8_10gev",
    "HNL_1.30e-8_20gev",
    "HNL_1.30e-8_30gev",
    "HNL_1.30e-8_40gev",
    "HNL_1.30e-8_50gev",
    "HNL_1.30e-8_60gev",
    "HNL_1.30e-8_70gev",
    "HNL_1.30e-8_80gev",

    "HNL_2.86e-9_10gev",
    "HNL_2.86e-9_20gev",
    "HNL_2.86e-9_30gev",
    "HNL_2.86e-9_40gev",
    "HNL_2.86e-9_50gev",
    "HNL_2.86e-9_60gev",
    "HNL_2.86e-9_70gev",
    "HNL_2.86e-9_80gev",

    "HNL_6.20e-10_10gev",
    "HNL_6.20e-10_20gev",
    "HNL_6.20e-10_30gev",
    "HNL_6.20e-10_40gev",
    "HNL_6.20e-10_50gev",
    "HNL_6.20e-10_60gev",
    "HNL_6.20e-10_70gev",
    "HNL_6.20e-10_80gev",

    "HNL_1.36e-10_10gev",
    "HNL_1.36e-10_20gev",
    "HNL_1.36e-10_30gev",
    "HNL_1.36e-10_40gev",
    "HNL_1.36e-10_50gev",
    "HNL_1.36e-10_60gev",
    "HNL_1.36e-10_70gev",
    "HNL_1.36e-10_80gev",

    "HNL_2.86e-11_10gev",
    "HNL_2.86e-11_20gev",
    "HNL_2.86e-11_30gev",
    "HNL_2.86e-11_40gev",
    "HNL_2.86e-11_50gev",
    "HNL_2.86e-11_60gev",
    "HNL_2.86e-11_70gev",
    "HNL_2.86e-11_80gev",
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

# Define the tree name
tree_name = "events"

# Print the results
output_file = "/eos/user/s/sgiappic/2HNL_ana/tau/final/nevents_tree.txt"

# Write the content of the selected row to the output CSV file
with open(output_file, "a") as file:
    file.write("# file, n. total \n")

# Loop through each replacement word
for replacement_word in replacement_words:
 
    # Define the ROOT file path
    root_file_path = "/eos/user/s/sgiappic/2HNL_ana/tau/stage1/{}.root".format(replacement_word)
    
    # Open the ROOT file
    root_file = uproot.open(root_file_path)

    # Get the tree from the ROOT file
    tree = root_file[tree_name]

    x = tree.num_entries 

    # Write the content of the selected row to the output CSV file
    with open(output_file, "a") as file:
        file.write("{}, {} \n".format(replacement_word, x))

    print("Content from {} has been written to {}".format(replacement_word, output_file))

