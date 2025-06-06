import uproot
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import uproot
import textwrap
import pickle

def file_exists(file_path):
    return os.path.isfile(file_path)

color_6 = ['#8C0303', '#D04747', '#FFABAC', '#03028D', '#4E6BD3', '#9FB5D7']
color = ['#8C0303', '#D04747', '#03028D', '#4E6BD3']
fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(25,25))

replacement_sig = [
    "mg_ee_eetata_ecm240",
    "mg_ee_mumutata_ecm240",
    "mg_ee_jjtata_ecm240",
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
leaf_name = "TauTag_R5_isTAU"

leaf_name_all = "RecoEmiss_costheta"

DIRECTORY = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/CP/final_250530/ktN-explicit/"

SUBDIR = [
    'LL',
    'LH',
    'HH',
]
#category to plot
CAT = [
    "QQ",
    "LL",
]

CUTS_LLHH = [
    "selReco",
    "selReco_100Coll150",
    "selReco_100Coll150_115Rec160",
    "selReco_100Coll150_115Rec160_2DR",
    "selReco_100Coll150_115Rec160_2DR_cos0.6",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_4Emiss",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_4Emiss", 
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_4Emiss_Zp54",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.96_80Z100_4Emiss_Zp54",
]

CUTS_LLLH = [
    "selReco",
    "selReco_100Coll150",
    "selReco_100Coll150_115Rec160",
    "selReco_100Coll150_115Rec160_2DR",
    "selReco_100Coll150_115Rec160_2DR_cos0.6",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_4Emiss",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_84Z100_4Emiss", 
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_84Z100_4Emiss_Zp54",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.88_84Z100_4Emiss_Zp54",
]

CUTS_LLLL = [
    "selReco",
    "selReco_100Coll150",
    "selReco_100Coll150_115Rec160",
    "selReco_100Coll150_115Rec160_2DR",
    "selReco_100Coll150_115Rec160_2DR_cos0.6",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_40Emiss",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_40Emiss", 
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_80Z100_40Emiss_Zp54",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.9_80Z100_40Emiss_Zp54",
]

CUTS_QQHH = [
    "selReco",
    "selReco_100Coll150",
    "selReco_100Coll150_115Rec160",
    "selReco_100Coll150_115Rec160_2DR",
    "selReco_100Coll150_115Rec160_2DR_cos0.6",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_8Emiss",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_8Emiss_Zp52",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.86_70Z100_8Emiss_Zp52",
]

CUTS_QQLH = [
    "selReco",
    "selReco_100Coll150",
    "selReco_100Coll150_115Rec160",
    "selReco_100Coll150_115Rec160_2DR",
    "selReco_100Coll150_115Rec160_2DR_cos0.6",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_36Emiss",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_36Emiss",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_36Emiss_Zp52",
]

CUTS_QQLL = [
    "selReco",
    "selReco_100Coll150",
    "selReco_100Coll150_115Rec160",
    "selReco_100Coll150_115Rec160_2DR",
    "selReco_100Coll150_115Rec160_2DR_cos0.6",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_52Emiss",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_52Emiss_Zp52",
    "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.92_70Z100_52Emiss_Zp52",
]
    
CUTS_NuNuHH = [
    "selReco",
    "selReco_100Me",
    "selReco_100Me_TauDPhi3",
    "selReco_100Me_TauDPhi3_2DR",
    "selReco_100Me_TauDPhi3_2DR_cos0.4",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    "selReco_112Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    "selReco_112Me_TauDPhi3_2DR_cos0.4_misscos0.88_missy1",
]

CUTS_NuNuLH = [
    "selReco",
    "selReco_100Me",
    "selReco_100Me_TauDPhi3",
    "selReco_100Me_TauDPhi3_2DR",
    "selReco_100Me_TauDPhi3_2DR_cos0.4",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    "selReco_140Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    "selReco_140Me_TauDPhi3_2DR_cos0.4_misscos0.94_missy1",
]

CUTS_NuNuLL = [
    "selReco",
    "selReco_100Me",
    "selReco_100Me_TauDPhi3",
    "selReco_100Me_TauDPhi3_2DR",
    "selReco_100Me_TauDPhi3_2DR_cos0.4",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98",
    "selReco_100Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    "selReco_152Me_TauDPhi3_2DR_cos0.4_misscos0.98_missy1",
    "selReco_152Me_TauDPhi3_2DR_cos0.4_misscos0.92_missy1",
]

CUTS = {
    'LLLL':CUTS_LLLL,
    'LLLH':CUTS_LLLH,
    'LLHH':CUTS_LLHH,
    'QQLL':CUTS_QQLL,
    'QQLH':CUTS_QQLH,
    'QQHH':CUTS_QQHH,
    'NuNuLL':CUTS_NuNuLL,
    'NuNuLH':CUTS_NuNuLH,
    'NuNuHH':CUTS_NuNuHH,
}

output_file = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/significance+purity_v2.txt"

results_file = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/results_v2.pkl"

s = []
p = []
results = {}

# Load results from a file if it exists
if os.path.exists(results_file):
    with open(results_file, "rb") as f:
        results = pickle.load(f)
        print(f"Results loaded from {results_file}")
else:
    print("Results file not found, running analysis.")

    for tag in TAG:
        
        for j, cat in enumerate(CAT):
            for k, sub in enumerate(SUBDIR):

                CUT = CUTS[cat+sub]

                if "ktN-tag" in tag and "LL" in cat and "HH" in sub:
                    CUT = [
                        "selReco",
                        "selReco_100Coll150",
                        "selReco_100Coll150_115Rec160",
                        "selReco_100Coll150_115Rec160_2DR",
                        "selReco_100Coll150_115Rec160_2DR_cos0.6",
                        "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
                        "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
                        "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_4Emiss",
                        "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_86Z100_4Emiss", 
                        "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_86Z100_4Emiss_Zp54",
                        "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.96_86Z100_4Emiss_Zp54",
                    ]

                if "tag" in tag and "QQ" in cat and "HH" in sub:
                    CUT = [
                        "selReco",
                        "selReco_100Coll150",
                        "selReco_100Coll150_115Rec160",
                        "selReco_100Coll150_115Rec160_2DR",
                        "selReco_100Coll150_115Rec160_2DR_cos0.6",
                        "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98",
                        "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100",
                        "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_70Z100_8Emiss",
                        "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_8Emiss",
                        "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.98_75Z100_8Emiss_Zp52",
                        "selReco_100Coll150_115Rec160_2DR_cos0.6_misscos0.86_75Z100_8Emiss_Zp52",
                    ]

                for cut in CUT:

                    dir_exc = DIRECTORY + tag + "/final_241202/" +  cat + "/" + sub + "/"

                    # book array for background entries
                    entries_bkg_tag = []

                    entries_sig_tag = []

                    entries_bkg_exc = 0

                    entries_sig_exc = 0

                    # Loop through each replacement word
                    for replacement_word in replacement_bkgs:

                        histo_path_excl= dir_exc + "{}_".format(replacement_word) + cut + "_histo.root"

                        if file_exists(histo_path_excl):

                            # Get the selected leaf from the tree
                            histo_exc = uproot.open(histo_path_excl)

                            selected_leaf_exc = histo_exc[leaf_name_all]

                            # Get scaled number of events from histograms, array
                            y_values_exc = selected_leaf_exc.values()

                            entries_bkg_exc += sum(y_values_exc)

                    for replacement_word in replacement_sig:

                        signal_path_excl= dir_exc + "{}_".format(replacement_word) + cut + "_histo.root"

                        if file_exists(signal_path_excl):

                            # Get the selected leaf from the tree
                            histo_exc = uproot.open(signal_path_excl)

                            selected_leaf_exc = histo_exc[leaf_name_all]

                            # Get scaled number of events from histograms, array
                            y_values_exc = selected_leaf_exc.values()

                            entries_sig_exc += sum(y_values_exc)

                    # calculate significance

                    if entries_sig_exc==0:
                        print(f"No signal files found {tag} {cat}{sub} {cut}")

                    significance = (entries_sig_exc / np.sqrt(entries_bkg_exc))
                    purity = ((entries_sig_exc / (entries_bkg_exc + entries_sig_exc)))

                    if tag not in results:
                        results[tag] = {}
                    if cat not in results[tag]:
                        results[tag][cat] = {}
                    if sub not in results[tag][cat]:
                        results[tag][cat][sub] = {'cuts': [], 'significance': [], 'purity': []}

                    results[tag][cat][sub]['cuts'].append(cut)
                    results[tag][cat][sub]['significance'].append(significance)
                    results[tag][cat][sub]['purity'].append(purity)

                    #print(results[tag][cat][sub]['significance'][-1])

                    #save results so you don't have to run it again to plot
                    with open(results_file, "wb") as f:
                        pickle.dump(results, f)
                        #print(f"Results saved to {results_file}")

                    #save values in a text file
                    #with open(output_file, "a") as file:

                    #    file.write("{}, {}, {} significance = {}\n".format(cut, tag, cat+sub, significance))
                    #    file.write("{}, {}, {} purity = {}\n\n".format(cut, tag, cat+sub, purity))

for i, tag in enumerate(TAG):
    for j, cat in enumerate(CAT):
        col = j % 3
        for k, sub in enumerate(SUBDIR):
            row = k % 3

            if tag in results and cat in results[tag] and sub in results[tag][cat]:
                data = results[tag][cat][sub]
                #data_norm = results[tag][cat][sub]
            else:
                print(cat,sub)

            x_indices = np.arange(len(data['cuts']))

            total_significance = sum(data['significance'])
            total_purity = sum(data['purity'])

            # Normalize the values
            #data_norm['significance'] = [s / total_significance for s in data['significance']]
            #data_norm['purity'] = [p / total_purity for p in data['purity']]

            # Plot significance and purity for this tag
            axs[row][col].plot(x_indices, data['significance'], label=f'{tag} - Significance', linestyle='-', color=color[i])
            axs[row][col].plot(x_indices, data['purity'], label=f'{tag} - Purity', linestyle='--', color=color[i])

            axs[row][col].set_xticks(x_indices)  # Set the position of the ticks
            axs[row][col].set_title(f"{cat}{sub}", fontsize=22)
            #axs[row][col].set_xlabel(r'cuts', fontsize=18)
            axs[row][col].set_ylabel(r'values', fontsize=18)

            axs[row][col].grid(True, which='both', linestyle='--', linewidth=0.5)

            #print(f"Plotting on subplot ({row}, {col}) for tag={tag}, cat={cat}, sub={sub}, significance={data['significance']}")

            #axs[row][col].set_yscale('log')

            #wrapped_cuts = [textwrap.fill(cut, width=25) for cut in data['cuts']]

        #axs[2][col].set_xticklabels(wrapped_cuts, rotation=45, fontsize=10)  # Set the cut labels on the x-axis with rotation only on the last row
    axs[0][2].legend(loc='lower right', fontsize=18) #common legend only in one plot is enough

plt.tight_layout()
plt.savefig(f'/web/sgiappic/public_html/Higgs_xsec/s+p.png', format='png', dpi=330)
