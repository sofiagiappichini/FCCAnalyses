## I want to look at the CP angle and find the best cuts on kinematics that make the amplitude bigger (to distinguish form background)
## and eventually even to make the difference between cp odd and even more pronounced but this may not work since it's the same in gen level

import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# -------------------------
# Sine fit for modulation
# -------------------------
def sine_fit(phi, a, b, delta):
    return a + b * np.sin(phi + delta)

def get_modulation_amplitude(phi_values, bins=20):
    counts, edges = np.histogram(phi_values, bins=bins, range=(-np.pi, np.pi))
    centers = 0.5 * (edges[1:] + edges[:-1])

    # Initial guess for fit parameters
    a_init = np.mean(counts)  # Offset (mean of the histogram)
    b_init = (np.max(counts) - np.min(counts)) / 2  # Amplitude (half the range of the histogram)
    delta_init = 0  # Phase shift (initial guess, can be refined)

    try:
        popt, _ = curve_fit(sine_fit, centers, counts, p0=[a_init, b_init, delta_init])
        a, b, delta = popt
        amp = abs(b / a) if a != 0 else 0
        return amp, delta, centers, counts, popt
    except Exception as e:
        print(f"Fit failed: {e}")
        return 0, 0, centers, counts, None

# -------------------------
# Load ROOT TTree into DataFrame
# -------------------------
def load_root_data(file_path, branch_list, label, tree_name="events"):
    tree = uproot.open(file_path)[tree_name]
    df = tree.arrays(expressions=branch_list, library="pd")
    df["label"] = label
    return df

def count_events(file_path, tree_name="events"):
    with uproot.open(file_path) as f:
        tree = f[tree_name]
        return tree.num_entries

# -------------------------
# Apply a dictionary of cuts
# -------------------------
def apply_cuts(df, cut_dict):
    for var, val in cut_dict.items():
        df = df[df[var] > val]
    return df

# -------------------------
# Greedy optimization of cuts
# -------------------------
def greedy_optimize_cuts(df_even, df_odd, cut_ranges, factor_even=1.0, factor_odd=1.0, penalty_weight=2.0):
    remaining_vars = list(cut_ranges.keys())
    selected_cuts = {}
    best_score = -np.inf

    n_total_even = len(df_even)
    n_total_odd = len(df_odd)

    while remaining_vars:
        best_var = None
        best_val = None
        best_local_score = -np.inf

        for var in remaining_vars:
            for cut_val in cut_ranges[var]:
                trial_cuts = selected_cuts.copy()
                trial_cuts[var] = cut_val

                df_e_cut = apply_cuts(df_even, trial_cuts)
                df_o_cut = apply_cuts(df_odd, trial_cuts)

                n_e_cut = len(df_e_cut)
                n_o_cut = len(df_o_cut)

                if n_e_cut < 100 or n_o_cut < 100:
                    continue

                amp_e, delta_e, _, _, _ = get_modulation_amplitude(df_e_cut["PhiCP_CMS"])
                amp_o, delta_o, _, _, _ = get_modulation_amplitude(df_o_cut["PhiCP_CMS"])

                amp_diff = abs(amp_e - amp_o)
                delta_diff = abs((delta_e - delta_o + np.pi) % (2 * np.pi) - np.pi)

                # Scaled yield retention (fraction of weighted events retained)
                rel_yield_e = (n_e_cut * factor_even) / (n_total_even * factor_even)
                rel_yield_o = (n_o_cut * factor_odd) / (n_total_odd * factor_odd)
                min_retention = min(rel_yield_e, rel_yield_o)

                # Final score: balance between separation and retention
                combined_score = amp_diff + delta_diff - penalty_weight * (1 - min_retention)

                if combined_score > best_local_score:
                    best_local_score = combined_score
                    best_var = var
                    best_val = cut_val

        if best_local_score > best_score:
            selected_cuts[best_var] = best_val
            remaining_vars.remove(best_var)
            best_score = best_local_score
        else:
            break

    return selected_cuts, best_score


# -------------------------
# Plot φ* with fit
# -------------------------
def plot_phi_star(phi_values, label, popt=None):
    plt.figure(figsize=(7, 5))
    counts, bins, _ = plt.hist(phi_values, bins=20, range=(-np.pi, np.pi),
                                density=True, alpha=0.6, label=f"{label}")
    centers = 0.5 * (bins[1:] + bins[:-1])

    if popt is not None:
        x_fit = np.linspace(-np.pi, np.pi, 100)
        y_fit = sine_fit(x_fit, *popt)
        plt.plot(x_fit, y_fit / np.trapz(y_fit, x_fit), 'k--', label="Sine Fit")

    plt.xlabel("φ* [rad]")
    plt.ylabel("Normalized Entries")
    plt.title(f"φ* Distribution: {label}")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_phi_star_combined(phi_even_raw, phi_even_cut, phi_odd_raw, phi_odd_cut,
                           popt_even=None, popt_odd=None, bins=20,
                           norm_factor_even=1.0, norm_factor_odd=1.0):
    plt.figure(figsize=(8, 6))

    range_phi = (-np.pi, np.pi)
    bins_edges = np.linspace(*range_phi, bins + 1)
    bin_centers = 0.5 * (bins_edges[:-1] + bins_edges[1:])

    # Raw distributions (using 'step' to plot lines)
    counts_even_raw, _ = np.histogram(phi_even_raw, bins=bins_edges)
    counts_odd_raw, _ = np.histogram(phi_odd_raw, bins=bins_edges)
    plt.step(bin_centers, counts_even_raw * norm_factor_even, 'b-', label="CP-even (raw)")
    plt.step(bin_centers, counts_odd_raw * norm_factor_odd, 'r-', label="CP-odd (raw)")

    # Cut distributions (using 'step' to plot lines)
    counts_even_cut, _ = np.histogram(phi_even_cut, bins=bins_edges)
    counts_odd_cut, _ = np.histogram(phi_odd_cut, bins=bins_edges)
    plt.step(bin_centers, counts_even_cut * norm_factor_even, 'b--', label="CP-even (cut)")
    plt.step(bin_centers, counts_odd_cut * norm_factor_odd, 'r--', label="CP-odd (cut)")

    # Sine fits after cuts
    '''x_fit = np.linspace(-np.pi, np.pi, 200)
    if popt_even is not None:
        y_fit_even = sine_fit(x_fit, *popt_even)
        # Normalize the fit to the total event count
        y_fit_even *= np.sum(counts_even_raw) / np.trapz(y_fit_even, x_fit)
        plt.plot(x_fit, y_fit_even, 'b-', lw=2, label="Fit (CP-even)")

    if popt_odd is not None:
        y_fit_odd = sine_fit(x_fit, *popt_odd)
        # Normalize the fit to the total event count
        y_fit_odd *= np.sum(counts_odd_raw) / np.trapz(y_fit_odd, x_fit)
        plt.plot(x_fit, y_fit_odd, 'r-', lw=2, label="Fit (CP-odd)")'''

    plt.xlabel("φ* [rad]")
    plt.ylabel("Scaled Entries")
    plt.title("CP-sensitive angle φ*: before vs after cuts")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    dir = "/ceph/sgiappic/HiggsCP/CPReco/stage2_explicit_new/"
    even_file = dir + "EWonly_taudecay_2Pi2Nu.root"
    odd_file = dir + "cehim_m1_taudecay_2Pi2Nu.root"

    lumi = 10.8e6
    n_gen =100000
    xsec_odd = 5.8024289951161206e-06
    xsec_even = 5.778120325123597e-06

    factor_odd = lumi * xsec_odd / n_gen
    factor_even = lumi * xsec_even / n_gen

    cut_def = {
        "TauP_p": (0, 10, 100),
        "TauM_p": (0, 10, 100),
        "TauP_e": (0, 10, 100),
        "TauM_e": (0, 10, 100),
        "RecoPiP_p": (0, 10, 100),
        "RecoPiM_p": (0, 10, 100),
        "RecoPiP_e": (0, 10, 100),
        "RecoPiM_e": (0, 10, 100),
        "RecoPiP_D0sig": (0, 50, 500),
        "RecoPiM_D0sig": (0, 50, 500),
        "RecoPiP_Z0sig": (0, 50, 500),
        "RecoPiM_Z0sig": (0, 50, 500),
        "RecoEmiss_e": (0, 10, 100)
    }

    cut_ranges = {k: np.linspace(*v) for k, v in cut_def.items()}
    branches = list(cut_ranges.keys()) + ["PhiCP_CMS"]

    df_even = load_root_data(even_file, branches, label=0)
    df_odd = load_root_data(odd_file, branches, label=1)

    print("Running greedy cut optimization...")
    best_cuts, score = greedy_optimize_cuts(df_even, df_odd, cut_ranges, factor_even, factor_odd, penalty_weight=5)

    print("\nBest cut strategy found:")
    for var, val in best_cuts.items():
        print(f"{var} > {val:.3f}")
    print(f"Combined modulation score: {score:.4f}")

    # Apply final cuts
    df_even_cut = apply_cuts(df_even, best_cuts)
    df_odd_cut = apply_cuts(df_odd, best_cuts)

    _, _, _, _, popt_even = get_modulation_amplitude(df_even_cut["PhiCP_CMS"])
    _, _, _, _, popt_odd = get_modulation_amplitude(df_odd_cut["PhiCP_CMS"])

    print(f"Fit CP-even: {'Success' if popt_even is not None else 'Failed'}")
    print(f"Fit CP-odd: {'Success' if popt_odd is not None else 'Failed'}")

    #plot_phi_star(df_even_cut["PhiCP_CMS"], label="CP-even", popt=popt_even)
    #plot_phi_star(df_odd_cut["PhiCP_CMS"], label="CP-odd", popt=popt_odd)

    plot_phi_star_combined(phi_even_raw=df_even["PhiCP_CMS"], phi_even_cut=df_even_cut["PhiCP_CMS"], phi_odd_raw=df_odd["PhiCP_CMS"],
                            phi_odd_cut=df_odd_cut["PhiCP_CMS"], popt_even=popt_even, popt_odd=popt_odd, norm_factor_even=factor_even ,norm_factor_odd=factor_odd)
