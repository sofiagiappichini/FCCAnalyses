import uproot
import os
import shutil
import numpy as np
import pylhe
import pandas as pd
from matplotlib import pyplot as plt
from tqdm import tqdm
import re
import math
from scipy.interpolate import griddata
from matplotlib.lines import Line2D

def calculate_weights(cross_section, num_events, luminosity=204e6):
    return cross_section * luminosity / num_events

def split_into_three(arr):
    third = len(arr) // 3
    return arr[:third], arr[third:2*third], arr[2*third:]

def extract_event_data(events, cross_section, num_events, width):
    event_data = []
    weight = calculate_weights(cross_section, num_events)

    for event in events:
        final_state_particles = []
        for particle in event.particles:
            if particle.id in [9900012, 9900014]:
                dl = get_decay_length(particle.e, particle.px, particle.py, particle.pz, width)
                event_data.append({
                    'particle_id': particle.id,  # Particle ID
                    'px': particle.px,
                    'py': particle.py,
                    'pz': particle.pz,
                    'energy': particle.e,
                    'width': width,
                    'decay_length':dl,
                    'weight':weight,
                })

    df = pd.DataFrame(event_data)
    return df

def read_lhe_file(filepath):
    cross_section = 0.
    num_events = 0.
    width = 0.

    with open(filepath, 'r') as file:
        for line in file:
            if "#  Integrated weight (pb)  :" in line:     
                cross_section = float(line[28:])
            if "#  Number of Events        :" in line:
                num_events = float(line[28:])

    if (cross_section == 0. or num_events == 0.):
        print(f"Failed to extract cross-section or number of events from {filepath}")

    events = pylhe.read_lhe(filepath)

    width = get_width(filepath)
    return cross_section, num_events, width, events

def get_width(filepath):
    with open(filepath, "r") as file:
        read = False
        for line in file:
            if "DECAY  9900012" in line: #N2 width is very similar, no need to get that value too
                content_of_row=float(line[15:])
                read=True
        if read == False:
            for line in file:
                if "DECAY 9900012" in line: #N2 width is very similar, no need to get that value too
                    content_of_row=float(line[14:])
    return content_of_row

conv = 1.52e24 

def get_decay_length(E, px, py, pz, width):
    #using c=1
    p = math.sqrt(px**2 + py**2 + pz**2)
    mass = math.sqrt(E**2 - p**2)
    gamma = E / mass
    beta = p / E
    length = gamma * beta * 3e8 / (conv * width)  # width in GeV to s-1
    #print(length)
    return length

def extract_name(process):
    mass = 0.
    coupling = 0.
    # Search for the pattern in the file name
    match = re.search(pattern, process)
    if match:
        coupling = float(match.group(1))  # First captured group is the coupling
        mass = float(match.group(2))       # Second captured group is the mass

    return mass, coupling

#### beginning of code #####
processList = {
    "HNL_1.33e-7_10gev",
    "HNL_1.33e-7_20gev",
    "HNL_1.33e-7_30gev",
    "HNL_1.33e-7_40gev",
    "HNL_1.33e-7_50gev",
    "HNL_1.33e-7_60gev",
    "HNL_1.33e-7_70gev",
    "HNL_1.33e-7_80gev",

    "HNL_2.78e-8_10gev",
    "HNL_2.78e-8_20gev",
    "HNL_2.78e-8_30gev",
    "HNL_2.78e-8_40gev",
    "HNL_2.78e-8_50gev",
    "HNL_2.78e-8_60gev",
    "HNL_2.78e-8_70gev",
    "HNL_2.78e-8_80gev",

    "HNL_6.05e-9_10gev",
    "HNL_6.05e-9_20gev",
    "HNL_6.05e-9_30gev",
    "HNL_6.05e-9_40gev",
    "HNL_6.05e-9_50gev",
    "HNL_6.05e-9_60gev",
    "HNL_6.05e-9_70gev",
    "HNL_6.05e-9_80gev",

    "HNL_1.33e-9_10gev",
    "HNL_1.33e-9_20gev",
    "HNL_1.33e-9_30gev",
    "HNL_1.33e-9_40gev",
    "HNL_1.33e-9_50gev",
    "HNL_1.33e-9_60gev",
    "HNL_1.33e-9_70gev",
    "HNL_1.33e-9_80gev",

    "HNL_2.90e-10_10gev",
    "HNL_2.90e-10_20gev",
    "HNL_2.90e-10_30gev",
    "HNL_2.90e-10_40gev",
    "HNL_2.90e-10_50gev",
    "HNL_2.90e-10_60gev",
    "HNL_2.90e-10_70gev",
    "HNL_2.90e-10_80gev",

    "HNL_6.34e-11_10gev",
    "HNL_6.34e-11_20gev",
    "HNL_6.34e-11_30gev",
    "HNL_6.34e-11_40gev",
    "HNL_6.34e-11_50gev",
    "HNL_6.34e-11_60gev",
    "HNL_6.34e-11_70gev",
    "HNL_6.34e-11_80gev",

    "HNL_1.33e-11_10gev",
    "HNL_1.33e-11_20gev",
    "HNL_1.33e-11_30gev",
    "HNL_1.33e-11_40gev",
    "HNL_1.33e-11_50gev",
    "HNL_1.33e-11_60gev",
    "HNL_1.33e-11_70gev",
    "HNL_1.33e-11_80gev",
}

pattern = r'HNL_([0-9]*\.?[0-9]+[eE]?-?[0-9]*)_([0-9]+)gev'

path = "/eos/user/s/sgiappic/2HNL_samples/lhe/"

grid_list = []

for process in processList:
    filepath = path + process + ".lhe"

    os.system(f"gzip -d {filepath}.gz")

    mass, coupling = extract_name(process) 
    print(process, mass, coupling)

    cross_section, num_events, width, events = read_lhe_file(filepath)

    df = extract_event_data(events, cross_section, num_events, width) 

    df_filtered = df[(df['decay_length'] > 0.0006) & (df['decay_length'] < 2.0)]  

    grid_list.append({
        'mass': mass,
        'coupling': np.log10(coupling),
        'events': float(len(df_filtered)) * cross_section * 204e6 / float(len(df)),
    })

    os.system(f"gzip {filepath}")

grid = pd.DataFrame(grid_list) 

mass_grid, coupling_grid = np.meshgrid(
        np.linspace(min(grid['mass']), max(grid['mass']), 8),
        np.linspace(min(grid['coupling']), max(grid['coupling']), 7))
    
significance_grid = griddata((grid['mass'], grid['coupling']), grid['events'], (mass_grid, coupling_grid), method='linear')
contour_levels = [4]
plt.contour(mass_grid, coupling_grid, significance_grid, levels=contour_levels, colors='red', linewidths=2)

plt.scatter(grid['mass'], grid['coupling'], marker='x', c='red')

nrows_in = 1
ncol_in = 2
end_row = 168 # Last row to include in the first set, doesn't count commented lines

data_files = ["/eos/user/s/sgiappic/combine/nevents_7aug2.csv",]

for i, data_file in enumerate(data_files): 
    # Read input data from the text file
    data = np.genfromtxt(data_file, delimiter=',')
    
    # The data are organised as normal hierarchy fisrt and then inverted hierarchy so the file needs to be splitted to make two plots
    data_part1 = data[0:end_row]
    data_part2 = data[end_row:]
    
    data_part1_splits = split_into_three(data_part1)
    data_part2_splits = split_into_three(data_part2)

    data_point = data_part1_splits[0]

    # First column in file is the mixing angle, then mass, then significance
    #coupling = data_point[:, 0]
    log_coupling = np.log10(data_point[:, 0])
    mass = data_point[:, 1]
    significance = data_point[:, 2]
    
    mass_grid, coupling_grid = np.meshgrid(np.linspace(min(mass), max(mass), 8),
                                            np.linspace(min(log_coupling), max(log_coupling), 6))
    significance_grid = griddata((mass, log_coupling), significance, (mass_grid, coupling_grid), method='linear')

    # Add contour areas 
    contour_levels = [4]
    contour_lines = plt.contour(mass_grid, coupling_grid, significance_grid, levels=contour_levels, colors='blue', linewidths=2)

    plt.scatter(mass, log_coupling, marker='x', c="blue")


plt.xlabel(r'$M_N$ $[GeV]$', fontsize=18)
plt.ylabel(r'$log$ $U^2$', fontsize=18) 

plt.ylim([-12, -6])  # Corrected function call
plt.legend(["LHE", "Delphes"], loc='upper right', fontsize=18)

plt.tick_params(direction='out', top=False, right=False, which='major', labelsize=16)

# Save the figure
output_path = '/eos/user/s/sgiappic/www/paper/'
plt.savefig(output_path + 'lhe_decaylenght_contour.png', bbox_inches='tight')


