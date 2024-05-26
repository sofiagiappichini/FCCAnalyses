# adapted from jupyter notebook code

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
from matplotlib import ticker
from scipy.interpolate import griddata
from matplotlib.colors import LogNorm
from matplotlib.lines import Line2D

nrows_in = 1
ncol_in = 2
end_row = 72 # Last row to include in the first set, doesn't count commented lines
point1 = 8
color = ['#990202', '#D04747', '#FFABAC', '#03028D', '#4E6BD3', '#9FB5D7']
label = ['1.', '2.', '3.', '4.', '5.', '6.'] 

def split_into_three(arr):
    third = len(arr) // 3
    return arr[:third], arr[third:2*third], arr[2*third:]

data_files = [
    "/eos/user/s/sgiappic/combine/output_final_2.csv",
    ]

fig, axs = plt.subplots(nrows=nrows_in, ncols=ncol_in, figsize=(15, 7))

for i, data_file in enumerate(data_files): 
    # Read input data from the text file
    data = np.genfromtxt(data_file, delimiter=',')
    
    # The data are organised as normal hierarchy fisrt and then inverted hierarchy so the file needs to be splitted to make two plots
    data_part1 = data[0:end_row]
    data_part2 = data[end_row:]
    
    data_part1_splits = split_into_three(data_part1)
    data_part2_splits = split_into_three(data_part2)

    for j, data_splits in enumerate([data_part1_splits, data_part2_splits]):
        for k, data_point in enumerate(data_splits):

            # First column in file is the mixing angle, then mass, then significance
            #coupling = data_point[:, 0]
            log_coupling = np.log10(data_point[:, 0])
            mass = data_point[:, 1]
            significance = data_point[:, 2]

            #for k in range(len([coupling, log_coupling])):
                # Plot in the appropriate subplot
            #row = k % 2
            col = j % 2 #divide the plots by hierarchy
            #axs[row, col].set_aspect('equal') 

            '''if row == 0 :

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
                #axs[row, col].scatter(mass, coupling, marker='x', c='black')'''
                
            #else :

            # Now for the log scale, benefits from having less points
            mass_grid, coupling_grid = np.meshgrid(np.linspace(min(mass), max(mass), 8),
                                                    np.linspace(min(log_coupling), max(log_coupling), 20))
            significance_grid = griddata((mass, log_coupling), significance, (mass_grid, coupling_grid), method='linear')

            # Create the gradient plot using pcolormesh with logarithmic normalization
            #im = axs[row, col].pcolormesh(mass_grid, coupling_grid, significance_grid, cmap='coolwarm', norm=LogNorm(vmin=1e-4, vmax=10))
            #cbar = fig.colorbar(im, ax=axs[row, col])
            axs[col].set_xlabel(r'$M_N$ $[GeV]$', fontsize=16)
            axs[col].set_ylabel(r'$log$ $U^2$', fontsize=16) 
            #cbar.set_label(r'$Significance$', fontsize=16)

            # Add contour areas 
            contour_levels = [5]
            contour_lines = axs[col].contour(mass_grid, coupling_grid, significance_grid, levels=contour_levels, colors=color[k+3*j], linewidths=2)
            #axs[col].clabel(contour_lines, fmt=label[k+3*j], colors='black', fontsize=14)

            # Add scatter plot for points taken as reference
            axs[col].scatter(mass, log_coupling, marker='x', c=color[k+3*j])
            #axs[row, col].set_xscale('log')
            axs[col].set_ylim([-12, -6])

        axs[col].tick_params(direction='out', top=False, right=False)

legend_elements = [Line2D([0], [0], color=color[i], lw=2, label=label[i]) for i in range(0,3)]
axs[0].legend(handles=legend_elements, loc='lower right', fontsize=14)

legend_elements = [Line2D([0], [0], color=color[i], lw=2, label=label[i]) for i in range(3,6)]
axs[1].legend(handles=legend_elements, loc='lower right', fontsize=14)
    
# Set the title using the data file name
axs[0].set_title(r'$Significance - Normal\; Hierarchy$', fontsize=16, y=1.05)
axs[1].set_title(r'$Significance - Inverted\; Hierarchy$', fontsize=16, y=1.05)
#axs[1, 0].set_title(r'$Normal\;\; Hierarchy$', fontsize=16, y=1.05)
#axs[1, 1].set_title(r'$Inverted\; Hierarchy$', fontsize=16, y=1.05)

#plt.suptitle(r'$Significance\; from\; \Delta R - After\; Selection\; and\; Cuts$', fontsize=20, y=1.05)

# Show all the plots
plt.tight_layout()
plt.savefig('/eos/user/s/sgiappic/www/plots/significance_final_points.png', format='png', dpi=330)