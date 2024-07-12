import pylhe
import os
import pandas as pd
import numpy as np
#import seaborn as sns
from matplotlib import pyplot as plt
#from tqdm import tqdm
import matplotlib.colors as colors

DIRECTORY = "/eos/user/s/sgiappic/2HNL_prod/"

RUNS = [
    "run_01",
    "run_02",
    "run_03",
    "run_04",
    "run_05",
    "run_06"
]

SAMPLES = [
    "HNL_6.67e-8_mass_split",
    "HNL_6.67e-10_mass_split",
    "HNL_6.67e-12_mass_split"
]

SAMPLES_SCAN = [
    "HNL_6.67e-10_10mass_split",
    "HNL_6.67e-10_mass_split",
    "HNL_6.67e-10_70mass_split"
]

'''#needs to comment out the first plot to work properly on the second
arrxs = []
arrerr = []

for rep in SAMPLES:

    for run in RUNS:
        #read lhe file and store informations
        file = DIRECTORY + rep + "/Events/" + run + "/unweighted_events.lhe"
        #file_gz = DIRECTORY + rep + "/Events/" + run + "/unweighted_events.lhe.gz"
        os.system("gzip -d {}.gz".format(file))
        sample = pylhe.read_lhe_init(file)

        list = sample['procInfo']
        xs = list[0]['xSection']
        err = list[0]['error']

        arrxs.append(xs)
        arrerr.append(err)

        os.system("gzip {}".format(file))

datam = np.array([0.000000001, 0.0000001, 0.00001, 0.001, 0.1, 10])

xs1 = arrxs[0:6]
xs2 = arrxs[6:12]
xs3 = arrxs[12:18]

er1 = arrerr[0:6]
er2 = arrerr[6:12]
er3 = arrerr[12:18]

# plot dividing the arrays for each sample file
pl1 = plt.scatter(datam, np.array(xs1)/6.67e-8, label=r'$U^2=6.67\cdot 10^{-8}$', color="#CC3333")
pl1 = plt.errorbar(x=datam, y=np.array(xs1)/6.67e-8, yerr=np.array(er1)/6.67e-8, color="#CC3333")

pl1 = plt.scatter(datam, np.array(xs2)/6.67e-10, label=r'$U^2=6.67\cdot 10^{-10}$', color="grey")
pl1 = plt.errorbar(x=datam, y=np.array(xs2)/6.67e-10, yerr=np.array(er2)/6.67e-10, color="grey")

pl1 = plt.scatter(datam, np.array(xs3)/6.67e-12, label=r'$U^2=6.67\cdot 10^{-12}$', color="#3366CC")
pl1 = plt.errorbar(x=datam, y=np.array(xs3)/6.67e-12, yerr=np.array(er3)/6.67e-12, color="#3366CC")

pl1 = plt.title(r'$M_N=40$ GeV')
pl1 = plt.xlabel(r'$\Delta M$ [GeV]')
pl1 = plt.ylabel(r'$\sigma\; (pb)/U^2$')
#pl1 = plt.yscale('log')
pl1 = plt.xscale('log')
#pl1 = plt.xlim([0.0, 15])
pl1 = plt.xticks(datam)
pl1 = plt.legend()
pl1 = plt.grid()

pl1 = plt.savefig('/eos/user/s/sgiappic/www/paper/mass_scan_angles.png', format='png', dpi=300)'''

arrxs = []
arrerr = []

for rep in SAMPLES_SCAN:

    for run in RUNS:
        #read lhe file and store informations
        file = DIRECTORY + rep + "/Events/" + run + "/unweighted_events.lhe"
        #file_gz = DIRECTORY + rep + "/Events/" + run + "/unweighted_events.lhe.gz"
        os.system("gzip -d {}.gz".format(file))
        sample = pylhe.read_lhe_init(file)

        list = sample['procInfo']
        xs = list[0]['xSection']
        err = list[0]['error']

        arrxs.append(xs)
        arrerr.append(err)

        os.system("gzip {}".format(file))

datam = np.array([0.000000001, 0.0000001, 0.00001, 0.001, 0.1, 10])

xs1 = arrxs[0:6]
xs2 = arrxs[6:12]
xs3 = arrxs[12:18]

er1 = arrerr[0:6]
er2 = arrerr[6:12]
er3 = arrerr[12:18]
pl2 = plt.grid()
# plot dividing the arrays for each sample file
pl2 = plt.scatter(datam, np.array(xs1)/6.67e-10, label=r'$M_N=10\; GeV$', color="#CC3333")
pl2 = plt.errorbar(x=datam, y=np.array(xs1)/6.67e-10, yerr=np.array(er1)/6.67e-10, color="#CC3333")

pl2 = plt.scatter(datam, np.array(xs2)/6.67e-10, label=r'$M_N=40\; GeV$', color="grey")
pl2 = plt.errorbar(x=datam, y=np.array(xs2)/6.67e-10, yerr=np.array(er2)/6.67e-10, color="grey")

pl2 = plt.scatter(datam, np.array(xs3)/6.67e-10, label=r'$M_N=70\; GeV$', color="#3366CC")
pl2 = plt.errorbar(x=datam, y=np.array(xs3)/6.67e-10, yerr=np.array(er3)/6.67e-10, color="#3366CC")

pl2 = plt.title(r'$U^2=6.67\cdot 10^{-10}$')
pl2 = plt.xlabel(r'$\Delta M$ [GeV]')
pl2 = plt.ylabel(r'$\sigma\; (pb)/U^2$')
#pl2 = plt.yscale('log')
pl2 = plt.xscale('log')
#pl2 = plt.xlim([0.0, 15])
pl2 = plt.xticks([1e-9, 1e-7, 1e-5, 1e-3, 1e-1, 1e1])
pl2 = plt.legend()


pl2 = plt.savefig('/eos/user/s/sgiappic/www/paper/mass_scan_masses.png', format='png', dpi=300)