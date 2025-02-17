"""
UeNsq_future.py - 31/03/2023

Summary: 
Code for plotting constraints on the mixing squared between
the electron neutrino and sterile neutrino |U_{eN}|^2 as 
a function of the sterile neutrino mass m_N

References for each individual constraint are compiled
on the 'Plots and Data' page of the website.

Here data with consistent log units are loaded and plotted.

Requires numpy, matplotlib, scipy and pandas.
"""

## from https://www.hep.ucl.ac.uk/~pbolton/plots.html

import numpy as np
from numpy import cos as Cos
from numpy import sin as Sin
from numpy import sqrt as Sqrt
from numpy import ma
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from matplotlib import ticker, cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import scipy.ndimage
from scipy.interpolate import griddata
import pandas as pd
from matplotlib.lines import Line2D

fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))

#my data
## displaced
data = np.genfromtxt("/eos/user/s/sgiappic/combine/nevents_7aug2.csv", delimiter=',')
#data = np.genfromtxt("/eos/user/s/sgiappic/combine/nevents_notaus.csv", delimiter=',')
#only take the points relative the point 6
data_point = data[280:]

log_coupling = np.log10(data_point[:, 0])
mass = data_point[:, 1]
significance = data_point[:, 2]*0.61 #scaling to 125ab-1

mass_grid, coupling_grid = np.meshgrid(np.linspace(min(mass), max(mass), 8),
                                                    np.linspace(min(log_coupling), max(log_coupling), 6))
significance_grid = griddata((mass, log_coupling), significance, (mass_grid, coupling_grid), method='linear')

contour_levels = [4]
contour_lines = plt.contour(mass_grid, coupling_grid, significance_grid, levels=contour_levels, colors='#8ab0ed', linewidths=5)

## prompt
data = np.genfromtxt("/eos/user/s/sgiappic/combine/output_250211_125ab.csv", delimiter=',')
#only take the points relative the point 6
data_point = data[280:]

log_coupling = np.log10(data_point[:, 0])
mass = data_point[:, 1]
significance = data_point[:, 2]

mass_grid, coupling_grid = np.meshgrid(np.linspace(min(mass), max(mass), 8),
                                                    np.linspace(min(log_coupling), max(log_coupling), 6))
significance_grid = griddata((mass, log_coupling), significance, (mass_grid, coupling_grid), method='linear')

contour_levels = [5]
contour_lines = plt.contour(mass_grid, coupling_grid, significance_grid, levels=contour_levels, colors='#8ab0ed', linestyles='--', linewidths=5)
plt.scatter(mass, log_coupling, marker='x', c='#8ab0ed')

### Labels ###

custom_lines = [Line2D([0], [0], color='#8ab0ed', lw=2),
                Line2D([0], [0], color='#8ab0ed', lw=2, linestyle='--')]

#axes.tick_params(axis='x', which='major', pad=7.5)

plt.xlabel(r'$M_N$ $[GeV]$', fontsize=18)
plt.ylabel(r'$log$ $U^2$', fontsize=18) 
plt.ylim([-12, -6])  # Corrected function call
plt.legend(custom_lines, [r'Event count from displaced selection', r'Significance from inclusive selection'], 
           title=r'$U^2_{e}/U^2:U^2_{\mu}/U^2:U^2_{\tau}/U^2$=0.9:0.1:0', title_fontsize=18, loc='lower right', fontsize=18 )
plt.title(r'$N_{1,2}\to\ell\ell\nu\; at\; FCC-ee,\; \sqrt{s}=91.2\; GeV,\; \mathcal{L}=125\; ab^{-1}$', fontsize=20, y=1.05)

plt.tick_params(direction='out', top=False, right=False, which='major', labelsize=16)
plt.tight_layout()
plt.savefig("/eos/user/s/sgiappic/www/paper/summary_plot_125ab.png", format='png', dpi=330)