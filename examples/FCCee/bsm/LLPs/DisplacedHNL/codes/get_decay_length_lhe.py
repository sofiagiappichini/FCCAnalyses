import uproot
import os
import shutil
import numpy as np
import pylhe
import pandas as pd
from tqdm import tqdm

replacement_words = [
    "HNL_4e-10_20gev",
    "HNL_4e-10_30gev",
    "HNL_4e-10_40gev",
    "HNL_4e-10_50gev",
    "HNL_4e-10_60gev",
    "HNL_4e-10_70gev",
    "HNL_4e-10_80gev",

    "HNL_1.33e-7_20gev",
    "HNL_1.33e-7_30gev",
    "HNL_1.33e-7_40gev",
    "HNL_1.33e-7_50gev",
    "HNL_1.33e-7_60gev",
    "HNL_1.33e-7_70gev",
    "HNL_1.33e-7_80gev",

    "HNL_2.86e-12_20gev",
    "HNL_2.86e-12_30gev",
    "HNL_2.86e-12_40gev",
    "HNL_2.86e-12_50gev",
    "HNL_2.86e-12_60gev",
    "HNL_2.86e-12_70gev",
    "HNL_2.86e-12_80gev",

    "HNL_5e-12_20gev",
    "HNL_5e-12_30gev",
    "HNL_5e-12_40gev",
    "HNL_5e-12_50gev",
    "HNL_5e-12_60gev",
    "HNL_5e-12_70gev",
    "HNL_5e-12_80gev",

    "HNL_6.67e-10_20gev",
    "HNL_6.67e-10_30gev",
    "HNL_6.67e-10_40gev",
    "HNL_6.67e-10_50gev",
    "HNL_6.67e-10_60gev",
    "HNL_6.67e-10_70gev",
    "HNL_6.67e-10_80gev",

    "HNL_2.86e-7_20gev",
    "HNL_2.86e-7_30gev",
    "HNL_2.86e-7_40gev",
    "HNL_2.86e-7_50gev",
    "HNL_2.86e-7_60gev",
    "HNL_2.86e-7_70gev",
    "HNL_2.86e-7_80gev",
]

replacement_words_flight = [
    "flight_4e-10_20gev",
    "flight_4e-10_30gev",
    "flight_4e-10_40gev",
    "flight_4e-10_50gev",
    "flight_4e-10_60gev",
    "flight_4e-10_70gev",
    "flight_4e-10_80gev",
]

# Print the results
output_file = "/eos/user/s/sgiappic/2HNL_ana/decay_length_lhe.txt"

# Write the content of the selected row to the output CSV file
with open(output_file, "a") as file:
    file.write("# file, Gen L\n")

# Loop through each replacement word
for replacement_word in replacement_words:

    input_file = '/eos/user/s/sgiappic/2HNL_samples/lhe/{}.lhe'.format(replacement_word)

    #get widht from lhe and check lifetime that way
    with open(input_file, "r") as file:
        read = False
        for line in file:
            if "DECAY  9900012" in line:
                content_of_row=float(line[15:])
                ctau = 6.5e-25 * 3e+8 * 1e3 / content_of_row #converted from m to mm
                read=True
        if read == False:
            ctau='error'

    # get info from lhe
    event = pylhe.read_lhe_with_attributes(input_file)
 
    data = {'event': [],
            'id': [],
            'px': [],
            'py': [],
            'pz': [],
            'lf':[],
            'm':[],
           }

    for n, event in tqdm(enumerate(event), unit='event(s)'):
        for particle in event.particles:
            data['event'].append(n)
            data['id'].append(particle.id)
            data['px'].append(particle.px)
            data['py'].append(particle.py)
            data['pz'].append(particle.pz)
            data['lf'].append(particle.lifetime)
            data['m'].append(particle.m)
            
    df = pd.DataFrame(data)

    # calculate decay lenght from momentum * lifetime /mass of HNLs (id == 9900012 for N_1, id == 9900014 for N_2)
    # in our model with almost degenate HNLs and same mixing angles the decay lenghts should be basically identical (width is, from lhe)
    px = df.query('id == 9900012')['px'].values
    py = df.query('id == 9900012')['py'].values
    pz = df.query('id == 9900012')['pz'].values

    p = np.sqrt(px**2+py**2+pz**2)

    lf = df.query('id == 9900012')['lf'].values

    m = df.query('id == 9900012')['m'].values

    dl = p * lf * 3e-1 / m #factor coming from converting ps into mm

    decay_length = np.max(dl)

    with open(output_file, "a") as file:
            file.write("{}, {}, {}\n".format(replacement_word, decay_length, ctau))

    print("Content from {} has been written to {}".format(replacement_word, output_file))