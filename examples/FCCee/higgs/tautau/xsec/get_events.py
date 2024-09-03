import uproot
import os
import shutil
import numpy as np
import csv

replacement_words = [
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

    "wzp6_ee_nunuH_Htautau_ecm240",
    "wzp6_ee_nunuH_HQQ_ecm240",
    "wzp6_ee_nunuH_Hgg_ecm240",
    "wzp6_ee_nunuH_HVV_ecm240",

    "wzp6_ee_eeH_Htautau_ecm240",
    "wzp6_ee_eeH_HQQ_ecm240",
    "wzp6_ee_eeH_Hgg_ecm240",
    "wzp6_ee_eeH_HVV_ecm240",

    "wzp6_ee_mumuH_Htautau_ecm240",
    "wzp6_ee_mumuH_HQQ_ecm240",
    "wzp6_ee_mumuH_Hgg_ecm240",
    "wzp6_ee_mumuH_HVV_ecm240",

    "wzp6_ee_ZheavyH_Htautau_ecm240",
    "wzp6_ee_ZheavyH_HQQ_ecm240",
    "wzp6_ee_ZheavyH_Hgg_ecm240",
    "wzp6_ee_ZheavyH_HVV_ecm240",

    "wzp6_ee_ZlightH_Htautau_ecm240",
    "wzp6_ee_ZlightH_HQQ_ecm240",
    "wzp6_ee_ZlightH_Hgg_ecm240",
    "wzp6_ee_ZlightH_HVV_ecm240",
]

DIRECTORY = {
    'LL':"/ceph/awiedl/FCCee/HiggsCP/stage2/LL",
    'QQ':"/ceph/awiedl/FCCee/HiggsCP/stage2/QQ",
    'NuNu':"/ceph/awiedl/FCCee/HiggsCP/stage2/NuNu",
}
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

# Print the results
output_file = "/ceph/awiedl/FCCee/HiggsCP/stage2/nevents_tree.txt"

tab = []
tab.append("empty")

# Loop through each replacement word
for replacement_word in replacement_words:
    tab.append(replacement_word) #header
for cat in CAT:
    variables = VARIABLES + LIST_VAR[cat] 
    for sub in SUBDIR:
        directory = DIRECTORY[cat] + "/" + sub + "/"
        newrow = []
        newrow.append(cat+sub) #header
        for replacement_word in replacement_words:
        
            # Define the ROOT file path
            root_file_path = directory + replacement_word
            
            # Open the ROOT file
            root_file = uproot.open(root_file_path)

            # Get the tree from the ROOT file
            tree = root_file[tree_name]

            x = tree.num_entries 

            newrow.append(x)

        tab.append(newrow)

# Write the content of the selected row to the output CSV file
 
with open(utput_file,, "w", newline="") as file:
    writer = csv.writer(file)
    # Write each row of the matrix
    writer.writerows(tab)
