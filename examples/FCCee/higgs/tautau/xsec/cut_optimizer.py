import uproot
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import uproot

def file_exists(file_path):
    return os.path.isfile(file_path)

color_6 = ['#8C0303', '#D04747', '#FFABAC', '#03028D', '#4E6BD3', '#9FB5D7']
color = ['#8C0303', '#D04747', '#03028D', '#4E6BD3']
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(25, 25))

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

# Define the tree name
tree_name = "events"

# Select the leaf you want to analyze
# automatic checks also prompt variable to get more accurate values
#leaf_name = "TauTag_R5_isTAU"

leaf_name = "RecoZ_p"

DIRECTORY = "/ceph/awiedl/FCCee/HiggsCP/"

TAG = [
    "R5-explicit",
    "R5-tag",
    "ktN-explicit",
    "ktN-tag",
]

SUBDIR = [
    'LL',
    'LH',
    'HH',
]
#category to plot
CAT = [
    "QQ",
    "LL",
    #"NuNu",
]

CUTS = {
    'LL':"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    'QQ':"selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    'NuNu':"selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
}

output_file = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/" +leaf_name+ "_optimization_lower.txt"

for a, tag in enumerate(TAG):
    for j, cat in enumerate(CAT):
        for k, sub in enumerate(SUBDIR):

            dir = DIRECTORY + tag + "/final_241202/" + cat + "/" + sub + "/"

            # book array for background entries
            entries_bkg_tag = []

            entries_sig_tag = []

            entries_bkg_exc = 0

            entries_sig_exc = 0

            # Loop through each replacement word
            for replacement_word in replacement_bkgs:
            
                # Define the ROOT file path
                histo_file_path = dir + "{}_".format(replacement_word) + CUTS[cat] + "_histo.root"

                if file_exists(histo_file_path):

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
                        temp_bkg.append(sum(y_values[i:]))

                    #add the entries for each background into the same array
                    for i in range(len(temp_bkg)):
                        if len(entries_bkg_tag) < len(temp_bkg):
                            entries_bkg_tag.append(temp_bkg[i]) 
                        else:
                            entries_bkg_tag[i] += temp_bkg[i]

                '''histo_path_excl= dir_exc + "{}_".format(replacement_word) + CUTS[cat] + "_histo.root"

                if file_exists(histo_path_excl):

                    # Get the selected leaf from the tree
                    histo_exc = uproot.open(histo_path_excl)

                    selected_leaf_exc = histo_exc[leaf_name_all]

                    # Get scaled number of events from histograms, array
                    y_values_exc = selected_leaf_exc.values()

                    entries_bkg_exc += sum(y_values_exc)'''

            for replacement_word in replacement_sig:

                # Define the ROOT file path
                signal_file_path = dir + "{}_".format(replacement_word)+ CUTS[cat] + "_histo.root"

                if file_exists(signal_file_path):

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
                        temp_sig.append(sum(y_values_signal[i:]))

                    #add the entries for each signal into the same array
                    for i in range(len(temp_sig)):
                        if len(entries_sig_tag) < len(temp_sig):
                            entries_sig_tag.append(temp_sig[i]) 
                        else:
                            entries_sig_tag[i] += temp_sig[i]

                '''signal_path_excl= dir_exc + "{}_".format(replacement_word) + cut + "_histo.root"

                if file_exists(signal_path_excl):

                    # Get the selected leaf from the tree
                    histo_exc = uproot.open(signal_path_excl)

                    selected_leaf_exc = histo_exc[leaf_name_all]

                    # Get scaled number of events from histograms, array
                    y_values_exc = selected_leaf_exc.values()

                    entries_sig_exc += sum(y_values_exc)'''

            # calculate significance for each bin 
            s = []
            p = []

            for i in range(len(entries_bkg_tag)):
                if (entries_bkg_tag[i]>0):
                    #if "HH" in sub:
                        #need to account for the fact that I have two jets in the same histogram so the number of event is half of that, approximately
                    #    s.append(entries_sig_tag[i] / (2 * np.sqrt(entries_bkg_tag[i] / 2))) 
                    #    p.append(entries_sig_tag[i] / (2 * (entries_sig_tag[i]/2 + entries_bkg_tag[i]/2)))
                    #else:
                        s.append(entries_sig_tag[i] / np.sqrt(entries_bkg_tag[i]))
                        p.append(entries_sig_tag[i] / (entries_sig_tag[i] + entries_bkg_tag[i]))
                    
                    #with open(output_file, "a") as file:
                    #    file.write("significance = {} for cut at TAU={} \n".format(s[i], i*(0.01)+0.5))
                    #    file.write("purity = {} for cut at TAU={} \n".format(p[i], i*(0.01)+0.5))
                    
                else:
                    s.append(0)
                    p.append(0)
                
            s_max = np.max(s)
            index = s.index(s_max)*(2)

            p_max = np.max(p)
            indexp = p.index(p_max)*(2)

            #significance = (entries_sig_exc / np.sqrt(entries_bkg_exc))
            #purity = ((entries_sig_exc / (entries_bkg_exc + entries_sig_exc)))

            with open(output_file, "a") as file:
                #file.write("\nTAGGER PERFORMANCE:\n")
                file.write(f"Class {tag}:\n\n")
                file.write("Max significance of {} = {} for cut at {}={} \n".format(cat+sub, s_max, leaf_name, index))
                file.write("Max purity of {} = {} for cut at {}={} \n\n".format(cat+sub, p_max, leaf_name, indexp))
                #file.write("\nEXPLICIT RECO PERFORMANCE:\n")
                #file.write("Significance of {} = {}\n".format(cat+sub, significance))
                #file.write("Purity of {} = {} \n\n".format(cat+sub, purity))

                #file.write("{} = {}\n".format(cat+sub, s[0]))
                #file.write("{} = {}\n\n".format(cat+sub, p[0]))

            #print("File written at {}".format(output_file))

            s_sum = sum(s)
            p_sum = sum(p)
            #normalise to 1 significance and purity for plotting
            #for i in range(len(s)):
            #    s[i] = s[i]/s_sum
            #    p[i] = p[i]/p_sum

            row = k % 3
            col = j % 2

            x = np.arange(0, 150, 2).tolist()

            axs[row][col].plot(x, s, linestyle='-', color=color[a], label=f"{tag} significance")
            #axs[row][col].plot(x, p, linestyle='--', color=color[a], label=f"{tag} purity")

            #axs[row][col].plot(x, [significance] * len(x), linestyle='-.', color=color[j+3*k], label="explicit significance")
            #axs[row][col].plot(x, [purity] * len(x), linestyle=':', color=color[j+3*k], label="explicit purity")

            axs[row][col].set_title(f"{cat}{sub}", fontsize=22)
            axs[row][col].set_xlabel(f'{leaf_name}', fontsize=18)
            axs[row][col].set_ylabel(r'values', fontsize=18)
            axs[row][col].legend(loc='lower right', fontsize=18)

            axs[row][col].grid(True, which='both', linestyle='--', linewidth=0.5)

            #axs[row][col].set_yscale('log')

plt.tight_layout()
plt.savefig(f'/web/sgiappic/public_html/Higgs_xsec/cut_optimizer_{leaf_name}_lower.png', format='png', dpi=330)