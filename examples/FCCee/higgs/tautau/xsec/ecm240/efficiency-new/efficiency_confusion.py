import uproot
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob

# GEN branches
gen_tauP_vars = [
    "n_TauPtoPiNu", "n_TauPtoRhoNu", "n_TauPto2Pi0Nu", "n_TauPto3Pi0Nu",
    "n_TauPto3PiNu", "n_TauPto3PiPi0Nu"
]
gen_tauM_vars = [
    "n_TauMtoPiNu", "n_TauMtoRhoNu", "n_TauMto2Pi0Nu", "n_TauMto3Pi0Nu",
    "n_TauMto3PiNu", "n_TauMto3PiPi0Nu"
]
gen_labels = [
    r"$\pi \nu$", r"$\pi \pi^0 \nu$", r"$\pi 2\pi^0 \nu$",
    r"$\pi 3\pi^0 \nu$", r"$3\pi \nu$", r"$3\pi \pi^0 \nu$"
]

# Reco variable names
reco_names = [
    ("TauP_kt2_type", "TauM_kt2_type"),
    ("TauP_R5_type", "TauM_R5_type"),
]

# Define the directories to explore
sample_dirs = {
    "p8_ee_Ztautau_ecm91": r"$Z\to\tau\tau,\; \sqrt{s}=91\;GeV$",
    "wzp6_ee_tautau_ecm240": r"$Z\to\tau\tau,\; \sqrt{s}=240\;GeV$",
    "wzp6_ee_tautau_ecm365": r"$Z\to\tau\tau,\; \sqrt{s}=365\;GeV$",
    "wzp6_ee_nunuH_Htautau_ecm240": r"$Z\to\nu\nu,\; H\to\tau\tau,\; \sqrt{s}=240\;GeV$",
}

def remap_tauID(tauid):
    # Skip 16-19 by shifting IDs after 19 down by 4
    if 0 <= tauid < 16:
        return tauid
    elif tauid > 19:
        return tauid - 4
    else:
        return -1  # invalid/irrelevant tauID 16 to 19

# Mapping tauID to labels (based on your logic)
def tauid_label(tauID):
    # Use a lookup table based on the mapping logic for all 36 tauID classes
    # Detailed labels for tauID 0 to 35
    label_map = {
        0: r"$\pi$",
        1: r"$\pi 1\gamma$",
        2: r"$\pi 2\gamma$",
        3: r"$\pi \pi^0$",
        4: r"$\pi 3\gamma$",
        5: r"$\pi \gamma \pi^0$",
        6: r"$\pi 4\gamma$",
        7: r"$\pi 2\gamma \pi^0$",
        8: r"$\pi 2\pi^0$",
        9: r"$\pi 5\gamma$",
        10: r"$\pi 3\gamma \pi^0$",
        11: r"$\pi 1\gamma 2\pi^0$",
        12: r"$\pi >5\gamma$",
        13: r"$\pi >5\gamma$ with $\pi^0$",
        14: r"$\pi >5\gamma$ with $2\pi^0$",
        15: r"$\pi >5\gamma$ with $>2\pi^0$",
        16: r"$3\pi$",
        17: r"$3\pi 1\gamma$",
        18: r"$3\pi 2\gamma$",
        19: r"$3\pi \pi^0$",
        20: r"$3\pi 3\gamma$",
        21: r"$3\pi 1\gamma \pi^0$",
        22: r"$3\pi 4\gamma$",
        23: r"$3\pi 2\gamma \pi^0$",
        24: r"$3\pi 2\pi^0$",
        25: r"$3\pi 5\gamma$",
        26: r"$3\pi 3\gamma \pi^0$",
        27: r"$3\pi 1\gamma 2\pi^0$",
        28: r"$3\pi >5\gamma$",
        29: r"$3\pi >5\gamma$ with $\pi^0$",
        30: r"$3\pi >5\gamma$ with $2\pi^0$",
        31: r"$3\pi >5\gamma$ with $>2\pi^0$",
    }
    return label_map.get(tauID, f"Unknown {tauID}")

# Reduced labels summing over different pi0 counts (just grouping by (count_piP+count_piM) and count_pho)
# We'll assign generic names for summed classes with tauID sums mapped into fewer bins:
def reduced_label(index):
    # Map tauID to reduced labels (0 to 15 roughly)
    # Summed labels grouping tauIDs by (count_piP+count_piM) and count_pho, ignoring count_pi0
    reduced_map = {
        0: r"$\pi$",
        1: r"$\pi 1\gamma$",
        2: r"$\pi 2\gamma$",
        3: r"$\pi 3\gamma$",
        4: r"$\pi 4\gamma$",
        5: r"$\pi 5\gamma$",
        6: r"$\pi >5\gamma$",
        7: r"$3\pi$",
        8: r"$3\pi 1\gamma$",
        9: r"$3\pi 2\gamma$",
        10: r"$3\pi 3\gamma$",
        11: r"$3\pi 4\gamma$",
        12: r"$3\pi 5\gamma$",
        13: r"$3\pi >5\gamma$",
    }
    return reduced_map.get(index, f"Reduced {index}")

# Build confusion matrix with tauID labels
def build_conf_matrix(gen_arrays, reco_array, max_reco_class=31):  # 35-4=31
    n_gen = len(gen_arrays)
    conf_matrix = np.zeros((n_gen, max_reco_class + 1), dtype=int)
    n_events = len(reco_array)
    for i in range(n_events):
        for gen_idx, gen_array in enumerate(gen_arrays):
            if gen_array[i] > 0:
                reco_val = remap_tauID(reco_array[i])
                if 0 <= reco_val <= max_reco_class:
                    conf_matrix[gen_idx, reco_val] += 1
                break
    return conf_matrix

# Build reduced confusion matrix summing over pi0 (tauID grouped)
def build_conf_matrix_reduced(gen_arrays, reco_array, max_reco_class=13):
    # The reduced reco classes are 0-13 or so (fewer bins)
    n_gen = len(gen_arrays)
    conf_matrix = np.zeros((n_gen, max_reco_class + 1), dtype=int)
    n_events = len(reco_array)
    # Mapping detailed tauID (0-35) to reduced class index (0-13)
    tauid_to_reduced = {}
    for tauid in range(32):
        # decode tauID logic: count_piP+count_piM and count_pho decide reduced class
        # 1pi groups (indices 0-15)
        if tauid <= 1: reduced_idx = tauid  # 0,1
        elif 2 <= tauid <= 3: reduced_idx = 2
        elif 4 <= tauid <= 5: reduced_idx = 3
        elif 6 <= tauid <= 8: reduced_idx = 4
        elif 9 <= tauid <= 11: reduced_idx = 5
        elif 12 <= tauid <= 15: reduced_idx = 6
        elif tauid == 16 : reduced_idx = 7
        elif tauid == 17 : reduced_idx = 8
        elif 18 <= tauid <= 19: reduced_idx = 9
        elif 20 <= tauid <= 21: reduced_idx = 10
        elif 22 <= tauid <= 24: reduced_idx = 11
        elif 25 <= tauid <= 27: reduced_idx = 12
        else: reduced_idx = 13
        tauid_to_reduced[tauid] = reduced_idx

    for i in range(n_events):
        for gen_idx, gen_array in enumerate(gen_arrays):
            if gen_array[i] > 0:
                reco_val = remap_tauID(reco_array[i]) 
                if 0 <= reco_val <= 31:
                    reduced_val = tauid_to_reduced.get(reco_val, max_reco_class)
                    conf_matrix[gen_idx, reduced_val] += 1
                break
    return conf_matrix


def plot_conf_matrix(conf_matrix, title, fig, labels, max_x_ticks=None):
    eff_matrix = np.divide(conf_matrix, conf_matrix.sum(axis=1, keepdims=True),
                           out=np.zeros_like(conf_matrix, dtype=float),
                           where=conf_matrix.sum(axis=1, keepdims=True) != 0) * 100

    if max_x_ticks>15:
        plt.figure(figsize=(22, 5))
    else:
        plt.figure(figsize=(12, 5))
    ax = sns.heatmap(
        eff_matrix, annot=True, fmt=".1f", cmap="BuPu_r",
        xticklabels=labels if max_x_ticks is None else labels[:max_x_ticks],
        yticklabels=gen_labels,
        cbar_kws={"label": "Event fraction [%]"}
    )
    ax.set_xlabel(r"Reco $\tau$ ID")
    ax.set_ylabel(r"Gen $\tau$ decay mode")
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(fig)
    plt.close()


# Main loop over sample directories and reco variables
for sample_dir in sample_dirs:
    print(f"Processing sample: {sample_dir}")
    all_files = glob.glob(f"/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/efficiencyZ-pi0_0.2theta/{sample_dir}/chunk_*.root")
    if not all_files:
        print(f"Warning: No files found for {sample_dir}")
        continue

    # Load all branches for this sample
    reco_vars = sum(reco_names, ())  # flatten list of tuples
    all_branches = gen_tauP_vars + gen_tauM_vars + list(reco_vars)

    arrays = uproot.concatenate(
        {f: "events" for f in all_files},
        expressions=all_branches,
        library="np"
    )
    print("Data loaded")

    for recoP_name, recoM_name in reco_names:
        recoP = arrays[recoP_name]
        recoM = arrays[recoM_name]
        genP_arrays = [arrays[var] for var in gen_tauP_vars]
        genM_arrays = [arrays[var] for var in gen_tauM_vars]

        # --- Full detailed tauID plots ---
        conf_matrix_P = build_conf_matrix(genP_arrays, recoP)
        conf_matrix_M = build_conf_matrix(genM_arrays, recoM)

        labels_full = [tauid_label(i) for i in range(32)]
        suffix = recoP_name.split('_')[1]  # e.g., 'kt2' or 'R5'

        plot_conf_matrix(
            conf_matrix_P,
            fr"$\tau^+$ with $\pi^0$ reconstruction ({suffix}) - {sample_dirs[sample_dir]}",
            f'/eos/user/s/sgiappic/www/Higgs_xsec/{sample_dir}_TauP_{suffix}_full_0.2.png',
            labels_full, max_x_ticks=32
        )
        plot_conf_matrix(
            conf_matrix_M,
            fr"$\tau^-$ with $\pi^0$ reconstruction ({suffix}) - {sample_dirs[sample_dir]}",
            f'/eos/user/s/sgiappic/www/Higgs_xsec/{sample_dir}_TauM_{suffix}_full_0.2.png',
            labels_full, max_x_ticks=32
        )

        # --- Reduced tauID plots (grouped by pi count and pho count) ---
        conf_matrix_P_red = build_conf_matrix_reduced(genP_arrays, recoP)
        conf_matrix_M_red = build_conf_matrix_reduced(genM_arrays, recoM)

        labels_reduced = [reduced_label(i) for i in range(14)]

        plot_conf_matrix(
            conf_matrix_P_red,
            fr"$\tau^+$ ({suffix}) - {sample_dirs[sample_dir]}",
            f'/eos/user/s/sgiappic/www/Higgs_xsec/{sample_dir}_TauP_{suffix}_reduced_0.2.png',
            labels_reduced, max_x_ticks=14
        )
        plot_conf_matrix(
            conf_matrix_M_red,
            fr"$\tau^-$ ({suffix}) - {sample_dirs[sample_dir]}",
            f'/eos/user/s/sgiappic/www/Higgs_xsec/{sample_dir}_TauM_{suffix}_reduced_0.2.png',
            labels_reduced, max_x_ticks=14
        )

print("All plots saved.")
