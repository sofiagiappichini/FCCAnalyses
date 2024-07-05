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

def inv(weight, s, n, events):
    mass = []
    for event in events:
        final_state_particles = []
        for particle in event.particles:
            if particle.status == 1 and particle.id in [11, -11, 13, -13, 15, -15]:
                final_state_particles.append(particle)
        if len(final_state_particles) == 2:
            inv_mass = get_invariant_mass(final_state_particles)
            mass.append(inv_mass)
            weight.append(s*204e6/n)
    return mass

def get_particle_pt(particle):
    px = particle.px
    py = particle.py
    return (px**2 + py**2)**0.5

def pt(weight, s, n, events):
    p = []
    for event in events:
        for particle in event.particles:
            if particle.status == 1 and particle.id in [11, -11, 13, -13, 15, -15]:
                pt = get_particle_pt(particle)
                p.append(pt)
                weight.append(s*204e6/n)
    return p

def e(weight, s, n, events):
    en = []
    for event in events:
        for particle in event.particles:
            if particle.status == 1 and particle.id in [11, -11, 13, -13, 15, -15]:
                en.append(particle.e)
                weight.append(s*204e6/n)
    return en


replacement_words = [
    "HNL_6.67e-10_40gev",
    "HNL_6.67e-10_40gev_isr",
    "HNL_6.67e-10_40gev_isrbm",
]

fig, ax = plt.subplots(ncols=3, figsize=(24,6))
xsec = []

# Loop through each replacement word
for replacement_word in replacement_words:

    #os.system("gzip -d /eos/user/s/sgiappic/2HNL_samples/lhe/{}.lhe.gz".format(replacement_word))

    input_file = '/eos/user/s/sgiappic/2HNL_samples/lhe/{}.lhe'.format(replacement_word)

    #get widht from lhe and check lifetime that way
    with open(input_file, "r") as file:
        read = False
        for line in file:
            if "#  Integrated weight (pb)  :" in line:
                xsec.append(float(line[30:]))
                read=True
        if read == False:
            content_of_row='error'

print(xsec)

invMass =[]
invMass_isr =[]
invMass_isrbm =[]
invMass_w =[]
invMass_isr_w =[]
invMass_isrbm_w =[]

Pt =[]
Pt_isr =[]
Pt_isrbm =[]
Pt_w =[]
Pt_isr_w =[]
Pt_isrbm_w =[]

En =[]
En_isr =[]
En_isrbm =[]
En_w =[]
En_isr_w =[]
En_isrbm_w =[]

event = pylhe.read_lhe('/eos/user/s/sgiappic/2HNL_samples/lhe/HNL_6.67e-10_40gev.lhe')
event_isr = pylhe.read_lhe('/eos/user/s/sgiappic/2HNL_samples/lhe/HNL_6.67e-10_40gev_isr.lhe')
event_isrbm = pylhe.read_lhe('/eos/user/s/sgiappic/2HNL_samples/lhe/HNL_6.67e-10_40gev_isrbm.lhe')

invMass = inv(invMass_w, xsec[0], 50000, event)
invMass_isr = inv(invMass_isr_w, xsec[1], 10000, event_isr)
invMass_isrbm = inv(invMass_isrbm_w, xsec[2], 10000, event_isrbm)

event = pylhe.read_lhe('/eos/user/s/sgiappic/2HNL_samples/lhe/HNL_6.67e-10_40gev.lhe')
event_isr = pylhe.read_lhe('/eos/user/s/sgiappic/2HNL_samples/lhe/HNL_6.67e-10_40gev_isr.lhe')
event_isrbm = pylhe.read_lhe('/eos/user/s/sgiappic/2HNL_samples/lhe/HNL_6.67e-10_40gev_isrbm.lhe')

Pt = pt(Pt_w, xsec[0], 50000, event)
Pt_isr = pt(Pt_isr_w, xsec[1], 10000, event_isr)
Pt_isrbm = pt(Pt_isrbm_w, xsec[2], 10000, event_isrbm)

event = pylhe.read_lhe('/eos/user/s/sgiappic/2HNL_samples/lhe/HNL_6.67e-10_40gev.lhe')
event_isr = pylhe.read_lhe('/eos/user/s/sgiappic/2HNL_samples/lhe/HNL_6.67e-10_40gev_isr.lhe')
event_isrbm = pylhe.read_lhe('/eos/user/s/sgiappic/2HNL_samples/lhe/HNL_6.67e-10_40gev_isrbm.lhe')

En = e(En_w, xsec[0], 50000, event)
En_isr = e(En_isr_w, xsec[1], 10000, event_isr)
En_isrbm = e(En_isrbm_w, xsec[2], 10000, event_isrbm)


ax[0].hist([Pt, Pt_isr, Pt_isrbm], 50, weights=[Pt_w, Pt_isr_w, Pt_isrbm_w], stacked=False, histtype='step',color=['blue', 'green', 'red'])

ax[0].set_title(r'$U^2=6.67e-10, \; M=40$ GeV, L=204ab$-1$')
ax[0].set_xlabel(r'$p_T$')
ax[0].set_ylabel(r'events')
ax[0].set_yscale('log')

ax[1].hist([invMass, invMass_isr, invMass_isrbm], 100, weights=[invMass_w, invMass_isr_w, invMass_isrbm_w], stacked=False, histtype='step', color=['blue', 'green', 'red'])

ax[1].set_title(r'$U^2=6.67e-10, \; M=40$ GeV, L=204ab$-1$')
ax[1].set_xlabel(r'$M(l,l)$')
ax[1].set_ylabel(r'events')
ax[1].set_yscale('log')

ax[2].hist([En, En_isr, En_isrbm], 100, weights=[En_w, En_isr_w, En_isrbm_w], stacked=False, histtype='step', label=['no isr', 'isr', 'isr+bm'], color=['blue', 'green', 'red'])

ax[2].set_title(r'$U^2=6.67e-10, \; M=40$ GeV, L=204ab$-1$')
ax[2].set_xlabel(r'$E$')
ax[2].set_ylabel(r'events')
ax[2].set_yscale('log')
ax[2].legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.savefig('/eos/user/s/sgiappic/www/paper/lhe_isr.png')

#for replacement_word in replacement_words:
    
    #os.system("gzip /eos/user/s/sgiappic/2HNL_samples/lhe/{}.lhe".format(replacement_word))

