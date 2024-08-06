import uproot
import os
import shutil
import numpy as np
import pylhe
import pandas as pd
from matplotlib import pyplot as plt
from tqdm import tqdm

def get_invariant_mass(particles):
    px = sum(p.px for p in particles)
    py = sum(p.py for p in particles)
    pz = sum(p.pz for p in particles)
    energy = sum(p.e for p in particles)
    return (energy**2 - px**2 - py**2 - pz**2)**0.5

def get_particle_pt(particle):
    px = particle.px
    py = particle.py
    return (px**2 + py**2)**0.5

def get_particle_p(particle):
    px = particle.px
    py = particle.py
    pz = particle.pz
    return (px**2 + py**2 + pz**2)**0.5

def calculate_weights(cross_section, num_events, luminosity=204e6):
    return cross_section * luminosity / num_events

def extract_event_data(events, cross_section, num_events):
    invariant_masses = []
    transverse_momenta = []
    energies = []
    weight_list = []
    weight = calculate_weights(cross_section, num_events)

    for event in events:
        final_state_particles = []
        for particle in event.particles:
            if particle.status == 1 and particle.id in [11, -11, 13, -13, 15, -15]:
                final_state_particles.append(particle)
        if len(final_state_particles) == 2:
            invariant_masses.append(get_invariant_mass(final_state_particles))
            if (get_particle_p(final_state_particles[0]) > get_particle_p(final_state_particles[1])):
                transverse_momenta.append(get_particle_pt(final_state_particles[0]))
                energies.append(final_state_particles[0].e)
            else:
                transverse_momenta.append(get_particle_pt(final_state_particles[1]))
                energies.append(final_state_particles[1].e)
            weight_list.append(weight)

    return invariant_masses, transverse_momenta, energies, weight_list

def read_lhe_file(filepath):
    cross_section = 0.
    num_events = 0.

    with open(filepath, 'r') as file:
        for line in file:
            if "#  Integrated weight (pb)  :" in line:     
                cross_section = float(line[28:])
            if "#  Number of Events        :" in line:
                num_events = float(line[28:])

    if (cross_section == 0. or num_events == 0.):
        print(f"Failed to extract cross-section or number of events from {filepath}")

    events = pylhe.read_lhe(filepath)

    return cross_section, num_events, events

def process_files(filepaths):
    data = {'inv_mass': [], 'pt': [], 'energy': [], 'weights': []}
    for filepath in filepaths:
        #os.system(f"gzip -d {filepath}.gz")
        cross_section, num_events, events = read_lhe_file(filepath)
        print(cross_section, num_events)
        inv_mass, pt, energy, weight = extract_event_data(events, cross_section, num_events)
        data['inv_mass'].extend(inv_mass)
        data['pt'].extend(pt)
        data['energy'].extend(energy)
        data['weights'].extend(weight)
        #os.system(f"gzip {filepath}")
    return data

def process_file(filepath):
    data = {'inv_mass': [], 'pt': [], 'energy': [], 'weights': []}
    cross_section, num_events, events = read_lhe_file(filepath)
    cross_section = 0.002
    num_events = 1e6
    print(cross_section, num_events)
    inv_mass, pt, energy, weight = extract_event_data(events, cross_section, num_events)
    data['inv_mass'].extend(inv_mass)
    data['pt'].extend(pt)
    data['energy'].extend(energy)
    data['weights'].extend(weight)
    return data

#### beginning of code #####
filepaths = [
    '/eos/user/s/sgiappic/2HNL_samples/lhe/eenunu_m.lhe',
    '/eos/user/s/sgiappic/2HNL_samples/lhe/mumununu_m.lhe',
    '/eos/user/s/sgiappic/2HNL_samples/lhe/tatanunu_m.lhe',
    '/eos/user/s/sgiappic/2HNL_samples/lhe/llnunu_m.lhe',
]

data1 = process_files(filepaths)
data2 = process_file("/eos/user/s/sajmal/HNLBackgrounds/llnunu/llnunu.lhe")

fig, ax = plt.subplots(ncols=3, figsize=(24,6))

ax[0].hist([data1['pt'], data2['pt']], 100, weights=[data1['weights'], data2['weights']], stacked=False, histtype='step',color=['blue', 'green'])

#ax[0].set_title(r'$U^2=6.67e-10, \; M=40$ GeV, L=204ab$-1$')
ax[0].set_xlabel(r'$p_T$')
ax[0].set_ylabel(r'events')
ax[0].set_yscale('log')

ax[1].hist([data1['inv_mass'], data2['inv_mass']], 100, weights=[data1['weights'], data2['weights']], stacked=False, histtype='step', color=['blue', 'green'])

#ax[1].set_title(r'$U^2=6.67e-10, \; M=40$ GeV, L=204ab$-1$')
ax[1].set_xlabel(r'$M(l,l)$')
ax[1].set_ylabel(r'events')
ax[1].set_yscale('log')

ax[2].hist([data1['energy'], data2['energy']], 100, weights=[data1['weights'], data2['weights']], stacked=False, histtype='step', label=['llnunu pythia', 'llnunu madgraph'], color=['blue', 'green'])

#ax[2].set_title(r'$U^2=6.67e-10, \; M=40$ GeV, L=204ab$-1$')
ax[2].set_xlabel(r'$E$')
ax[2].set_ylabel(r'events')
ax[2].set_yscale('log')
ax[2].legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.savefig('/eos/user/s/sgiappic/www/paper/llnunu.png')

