# adapted from jupyter notebook code

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
from matplotlib import ticker
from scipy.interpolate import griddata
from matplotlib.colors import LogNorm

nrows_in = 2
ncol_in = 2
end_row = 24 # Last row to include in the first set, doesn't count commented lines

data_files = [
    "output_tracks_asymDR_combined.csv",
    ]

fig, axs = plt.subplots(nrows=nrows_in, ncols=ncol_in, figsize=(14, 12))

for i, data_file in enumerate(data_files): 
    # Read input data from the text file
    data = np.genfromtxt(data_file, delimiter=',')
    
    # The data are organised as normal hierarchy fisrt and then inverted hierarchy so the file needs to be splitted to make two plots
    data_part1 = data[0:end_row]
    data_part2 = data[end_row:]
    
    for j, data_part in enumerate([data_part1, data_part2]):

        # First column in file is the mixing angle, then mass, then significance
        coupling = data_part[:, 0]
        log_coupling = np.log10(data_part[:, 0])
        mass = data_part[:, 1]
        significance = data_part[:, 2]

        for k in range(len([coupling, log_coupling])):
            # Plot in the appropriate subplot
            row = k % 2
            col = j % 2
            #axs[row, col].set_aspect('equal') 

            if row == 0 :

                # Create fluid grid for non-log coupling
                mass_grid, coupling_grid = np.meshgrid(np.linspace(min(mass), max(mass), 100), 
                                                            np.linspace(min(coupling), max(coupling), 100))
                significance_grid = griddata((mass, coupling), significance, (mass_grid, coupling_grid), method='linear')

                # Create the gradient plot using imshow with custom limits
                im = axs[row, col].imshow(significance_grid, extent=[min(mass), max(mass), min(coupling), max(coupling)],
                                        origin='lower', aspect='auto', cmap='coolwarm', vmin=0, vmax=5)  
                cbar = fig.colorbar(im, ax=axs[row, col])
                axs[row, col].set_xlabel(r'$M_N$ $[GeV]$', fontsize=16)
                axs[row, col].set_ylabel(r'$U^2$', fontsize=16)  
                cbar.set_label(r'$Significance$', fontsize=16)

                # Add contour lines at significance levels 2 and 5
                contour_levels = [3, 5]
                contour_lines = axs[row, col].contour(mass_grid, coupling_grid, significance_grid, levels=contour_levels, colors='white', linewidths=1.5)
                axs[row, col].clabel(contour_lines, fmt='%1.1f', colors='white', fontsize=12)
                
                # Add scatter plot for points taken as reference
                axs[row, col].scatter(mass, coupling, marker='x', c='black')
                #axs[row, col].set_xlim([min(mass), max(mass)])
                #axs[row, col].set_ylim([min(coupling), max(coupling)])
                
            else :

                # Now for the log scale, benefits from having less points
                mass_grid, coupling_grid = np.meshgrid(np.linspace(min(mass), max(mass), 8),
                                                        np.linspace(min(log_coupling), max(log_coupling), 10))
                significance_grid = griddata((mass, log_coupling), significance, (mass_grid, coupling_grid), method='linear')

                # Create the gradient plot using pcolormesh with logarithmic normalization
                im = axs[row, col].pcolormesh(mass_grid, coupling_grid, significance_grid, cmap='coolwarm', norm=LogNorm(vmin=1e-4, vmax=10))
                cbar = fig.colorbar(im, ax=axs[row, col])
                axs[row, col].set_xlabel(r'$M_N$ $[GeV]$', fontsize=16)
                axs[row, col].set_ylabel(r'$log$ $U^2$', fontsize=16) 
                cbar.set_label(r'$Significance$', fontsize=16)

                # Add contour lines at significance levels 2 and 5
                contour_levels = [3, 5]
                contour_lines = axs[row, col].contour(mass_grid, coupling_grid, significance_grid, levels=contour_levels, colors='white', linewidths=1.5)
                axs[row, col].clabel(contour_lines, fmt='%1.1f', colors='white', fontsize=12)

                # Add scatter plot for points taken as reference
                axs[row, col].scatter(mass, log_coupling, marker='x', c='black')
                #axs[row, col].set_xlim([min(mass), max(mass)])
                #axs[row, col].set_ylim([min(log_coupling), max(log_coupling)])

        axs[row, col].tick_params(direction='out', top=False, right=False)
    
# Set the title using the data file name
axs[0, 0].set_title(r'$Normal\; Hierarchy$', fontsize=16, y=1.05)
axs[0, 1].set_title(r'$Inverted\; Hierarchy$', fontsize=16, y=1.05)
axs[1, 0].set_title(r'$Normal\;\; Hierarchy$', fontsize=16, y=1.05)
axs[1, 1].set_title(r'$Inverted\; Hierarchy$', fontsize=16, y=1.05)

#plt.suptitle(r'$Significance\; from\; \Delta R - After\; Selection\; and\; Cuts$', fontsize=20, y=1.05)

# Show all the plots
plt.tight_layout()
plt.savefig('/eos/user/s/sgiappic/combine/significance_final.png', format='png', dpi=330)