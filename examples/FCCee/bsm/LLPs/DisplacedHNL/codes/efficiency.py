import uproot
import os
import shutil
import numpy as np

replacement_bkgs = [
    "p8_ee_Zee_ecm91",
    "p8_ee_Zmumu_ecm91",
    "p8_ee_Ztautau_ecm91",
    "p8_ee_Zbb_ecm91",
    "p8_ee_Zcc_ecm91",
    "p8_ee_Zud_ecm91",
    "p8_ee_Zss_ecm91",
    "eenunu_m",
    "mumununu_m",
    "tatanunu_m",
    "llnunu_m",
]

# Select the leaf you want to analyze
# automatic checks also prompt variable to get more accurate values
#leaf_name = "n_noLeptonTracks"
#leaf_name = "n_NeutralHadrons"
leaf_name = "Reco_invMass"
#leaf_name = "Reco_cos"
#leaf_name = "Reco_DecayVertexLepton_chi2"
#leaf_name = "Reco_Lxy"
#leaf_name = "Reco_DecayVertexLepton_z"
#leaf_name = "RecoEmiss_e"
#leaf_name = "RecoEmiss_pt"
#leaf_name = "Reco_e_lead"

dir = "/eos/user/s/sgiappic/2HNL_ana/final_paper/"

cut = "selReco_gen"

# Print the results
output_file = "/eos/user/s/sgiappic/2HNL_ana/"+cut+"_efficiency.txt"

# Loop through each replacement word
for replacement_word in replacement_bkgs:

    # Define the ROOT file path
    histo_file_path = dir + "{}_".format(replacement_word) + cut + "_histo.root"

    # Get the selected leaf from the tree
    histo_file = uproot.open(histo_file_path)

    selected_leaf = histo_file[leaf_name]

    #some variables don't show all events in the range if the histo so taking ne that does
    additional_leaf = histo_file["Reco_DR"]

    # Get scaled number of events from histograms, array
    y_values = selected_leaf.values()
    total_entries = sum(additional_leaf.values())

    entries = sum(y_values[:81]) #values up to the bin number i want plus 1
    #print(len(y_values))
    #print(f"entries: {entries}")

    #to use in the case of a cut on a varibale that has all events in the histo or when the cut is up to a value
    efficiency = entries / total_entries

    #to use when the variable doesn't have all events in the histo and the cut is from a value 
    ########   BUT SUM THE ENTRIES UP TO THE CUT ANYWAY TO EXCLUDE THEM    #########
    #if (total_entries - entries)>0:
    #     efficiency = (total_entries - entries) / total_entries
    #else:
    #    efficiency = 0 # for some reason it gets an higher number of entries than the total number of events are lower so it gets a negative number
    #print(f"total - entries: {total_entries - entries}")

    with open(output_file, "a") as file:
        file.write("Relative efficiency of {} after cut on {}: {} \n".format(replacement_word, leaf_name, efficiency))

    print(output_file)