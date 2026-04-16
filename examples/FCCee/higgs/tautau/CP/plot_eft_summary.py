import matplotlib.pyplot as plt
import numpy as np

# Operators
ops = ["cehre", "cehim", "chb", "chbtil", "chwb", "chwbtil", "chw", "chwtil"]

# 68% CL intervals: (low, high)

# Linear only
lin = {
    "cehim":   (-0.507,  0.506),
    "cehre":   (-0.156,  0.168),
    "chb":     (-1.231,  1.230),
    "chbtil":  (-1.424,  1.425),
    "chw":     (-1.510,  1.505),
    "chwb":    (-1.389,  1.397),
    "chwbtil": (-1.569,  1.570),
    "chwtil":  (-1.816,  1.820),
}

# Linear + quadratic
lin_quad = {
    "cehim":   (-0.490,  0.509),
    "cehre":   (-0.155,  0.170),
    "chb":     (-1.126,  1.367),
    "chbtil":  (-1.215,  1.774),
    "chw":     (-1.442,  1.317),
    "chwb":    (-1.237,  1.526),
    "chwbtil": (-1.426,  1.742),
    "chwtil":  (-1.762,  1.877),
}

# 95% CL — linear only
lin_95 = {
    "cehim":   (-1.176,  1.176),
    "cehre":   (-0.298,  0.340),
    "chb":     (-2.412,  2.408),
    "chbtil":  (-2.790,  2.795),
    "chw":     (-2.959,  2.938),
    "chwb":    (-2.715,  2.746),
    "chwbtil": (-3.075,  3.078),
    "chwtil":  (-3.555,  3.569),
}

# 95% CL — linear + quadratic
lin_quad_95 = {
    "cehim":   (-0.917,  0.977),
    "cehre":   (-0.293,  0.346),
    "chb":     (-2.047,  2.983),
    "chbtil":  (-2.143,  3.958),
    "chw":     (-2.475,  2.240),
    "chwb":    (-2.186,  2.990),
    "chwbtil": (-2.584,  3.698),
    "chwtil":  (-3.349,  3.783),
}


# Add new limits for lin profiled
lin_profiled = {
    "cehre":   (-0.157,  0.170),
    "cehim":   (-0.523,  0.522),
    "chb":     (-1.801,  1.801),
    "chbtil":  (-2.050,  2.051),
    "chw":     (-1.919,  1.917),
    "chwb":    (-2.032,  2.032),
    "chwbtil": (-2.240,  2.245),
    "chwtil":  (-2.372,  2.374),
}

lin_profiled_95 = {
    "cehre":   (-0.300,  0.344),
    "cehim":   (-1.014,  1.012),
    "chb":     (-3.509,  3.508),
    "chbtil":  (-4.018,  4.021),
    "chw":     (-3.762,  3.754),
    "chwb":    (-3.981,  3.981),
    "chwbtil": (-4.373,  4.393),
    "chwtil":  (-4.650,  4.655),
}


labels = {
    "cehre":   r"$Re(C_{eH})$",
    "cehim":   r"$Im(C_{eH})$",
    "chb":     r"$C_{HB}$",
    "chbtil":  r"$C_{H\tilde{B}}$",
    "chw":     r"$C_{HW}$",
    "chwb":    r"$C_{HWB}$",
    "chwbtil": r"$C_{HW\tilde{B}}$",
    "chwtil":  r"$C_{H\tilde{W}}$",
}


# Y positions
y = np.arange(len(ops))
offset = 0.15

def centers_and_errors(data):
    center = [(data[op][0] + data[op][1]) / 2 for op in ops]
    err_low = [center[i] - data[ops[i]][0] for i in range(len(ops))]
    err_high = [data[ops[i]][1] - center[i] for i in range(len(ops))]
    return center, [err_low, err_high]


# Compute errors, but set centers to zero
zeros = [0.0 for _ in ops]
_, e_lin = centers_and_errors(lin)
_, e_lq  = centers_and_errors(lin_quad)
_, e_lin95 = centers_and_errors(lin_95)
_, e_lq95  = centers_and_errors(lin_quad_95)
_, e_lin_profiled = centers_and_errors(lin_profiled)
_, e_lin_profiled_95 = centers_and_errors(lin_profiled_95)

# Plot 1: Only lin and lin profiled
plt.figure(figsize=(10, 6))
plt.errorbar(
    y - offset, zeros, yerr=e_lin95,
    fmt='o',
    label="Linear (95% CL)",
    ecolor='#5E2A84', 
    elinewidth=4,
    markerfacecolor='#5E2A84',
    markeredgecolor='#5E2A84',
)

plt.errorbar(
    y + offset, zeros, yerr=e_lin_profiled_95,
    fmt='o',
    label="Linear Profiled (95% CL)",
    ecolor='#1f77b4',
    elinewidth=4,
    markerfacecolor='#1f77b4',
    markeredgecolor='#1f77b4',
)

plt.errorbar(
    y - offset, zeros, yerr=e_lin,
    fmt='o',
    label="Linear (68% CL)",
    ecolor='#c7bcdd',
    elinewidth=4,
    markerfacecolor='#c7bcdd',
    markeredgecolor='#c7bcdd',
)

plt.errorbar(
    y + offset, zeros, yerr=e_lin_profiled,
    fmt='o',
    label="Linear Profiled (68% CL)",
    ecolor='#aec7e8',
    elinewidth=4,
    markerfacecolor='#aec7e8',
    markeredgecolor='#aec7e8',
)

plt.xticks(y, [labels[op] for op in ops], rotation=90, ha='left', fontsize=12)
plt.ylabel(r"$C/\Lambda^2\; [TeV^{-2}]$")
plt.yticks(np.arange(-5, 6, 1))
plt.gca().set_yticks(np.arange(-5, 5.5, 0.5), minor=True)
plt.grid(axis='y', which='minor', linestyle='--', linewidth=0.5, alpha=0.5)
plt.grid(axis='y', which='major', linestyle='--', linewidth=0.5, alpha=0.5)
leg = plt.legend(loc='upper left', ncol=2, fontsize=10, columnspacing=0.2, frameon=True, framealpha=1)
leg.get_frame().set_edgecolor('none')
plt.axhline(0, linestyle='--', linewidth=1, color="black")
plt.ylim(-5, 5)
plt.subplots_adjust(top=0.92)
plt.gcf().text(0.9, 0.96, "FCC-ee Simulation (Delphes)", fontsize=13, va='top', ha='right', fontweight='bold', transform=plt.gcf().transFigure)
plt.savefig("/eos/user/s/sgiappic/www/Higgs_CP/ecm240/EFT/summary_lin_profiled.png", bbox_inches='tight')
plt.savefig("/eos/user/s/sgiappic/www/Higgs_CP/ecm240/EFT/summary_lin_profiled.pdf", bbox_inches='tight')

# Plot 2: All three (lin, lin profiled, lin_quad)
plt.figure(figsize=(10, 6))
plt.errorbar(
    y - offset, zeros, yerr=e_lin95,
    fmt='o',
    label="Linear (95% CL)",
    ecolor='#5E2A84', 
    elinewidth=4,
    markerfacecolor='#5E2A84',
    markeredgecolor='#5E2A84',
)

plt.errorbar(
    y, zeros, yerr=e_lin_profiled_95,
    fmt='o',
    label="Linear Profiled (95% CL)",
    ecolor='#1f77b4',
    elinewidth=4,
    markerfacecolor='#1f77b4',
    markeredgecolor='#1f77b4',
)

plt.errorbar(
    y + offset, zeros, yerr=e_lq95,
    fmt='o',
    label="Linear + quadratic (95% CL)",
    ecolor='#004d00',
    elinewidth=4,
    markerfacecolor='#004d00',
    markeredgecolor='#004d00',
)

plt.errorbar(
    y - offset, zeros, yerr=e_lin,
    fmt='o',
    label="Linear (68% CL)",
    ecolor='#c7bcdd',
    elinewidth=4,
    markerfacecolor='#c7bcdd',
    markeredgecolor='#c7bcdd',
)

plt.errorbar(
    y, zeros, yerr=e_lin_profiled,
    fmt='o',
    label="Linear Profiled (68% CL)",
    ecolor='#aec7e8',
    elinewidth=4,
    markerfacecolor='#aec7e8',
    markeredgecolor='#aec7e8',
)

plt.errorbar(
    y + offset, zeros, yerr=e_lq,
    fmt='o',
    label="Linear + quadratic (68% CL)",
    ecolor='#c4d7b5',
    elinewidth=4,
    markerfacecolor='#c4d7b5',
    markeredgecolor='#c4d7b5',
)

plt.xticks(y, [labels[op] for op in ops], rotation=90, ha='left', fontsize=12)
plt.ylabel(r"$C/\Lambda^2\; [TeV^{-2}]$")
plt.yticks(np.arange(-5, 6, 1))
plt.gca().set_yticks(np.arange(-5, 5.5, 0.5), minor=True)
plt.grid(axis='y', which='minor', linestyle='--', linewidth=0.5, alpha=0.5)
plt.grid(axis='y', which='major', linestyle='--', linewidth=0.5, alpha=0.5)
leg = plt.legend(loc='upper left', ncol=2, fontsize=10, columnspacing=0.2, frameon=True, framealpha=1)
leg.get_frame().set_edgecolor('none')
plt.axhline(0, linestyle='--', linewidth=1, color="black")
plt.ylim(-5, 6)
plt.subplots_adjust(top=0.92)
plt.gcf().text(0.9, 0.96, "FCC-ee Simulation (Delphes)", fontsize=13, va='top', ha='right', fontweight='bold', transform=plt.gcf().transFigure)
plt.savefig("/eos/user/s/sgiappic/www/Higgs_CP/ecm240/EFT/summary_all.png", bbox_inches='tight')
plt.savefig("/eos/user/s/sgiappic/www/Higgs_CP/ecm240/EFT/summary_all.pdf", bbox_inches='tight')
