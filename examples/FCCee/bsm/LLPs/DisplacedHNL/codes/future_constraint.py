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

### Load data frame for each data set ###

df_current_LNC = pd.read_csv("/eos/user/s/sgiappic/2HNL_samples/data/current_LNC_data.csv",header=None, sep=",", names = ["X", "Y"])
df_current_LNV = pd.read_csv("/eos/user/s/sgiappic/2HNL_samples/data/current_LNV_data.csv",header=None, sep=",", names = ["X","Y"])

df_SHiP = pd.read_csv("/eos/user/s/sgiappic/2HNL_samples/data/SHiP_data.csv",header=None, sep=",", names = ["X", "Y"])
df_DUNE_1 = pd.read_csv("/eos/user/s/sgiappic/2HNL_samples/data/DUNE_1_data.csv",header=None, sep=",", names = ["X", "Y"])
df_DUNE_2 = pd.read_csv("/eos/user/s/sgiappic/2HNL_samples/data/DUNE_2_data.csv",header=None, sep=",", names = ["X", "Y"])
#df_FCC_ee = pd.read_csv("/eos/user/s/sgiappic/2HNL_samples/data/FCC_ee_sn.csv",header=None, sep=",", names = ["X", "Y"])
df_FCC_ee = pd.read_csv("/eos/user/s/sgiappic/2HNL_samples/data/FCC_ee_2_data.csv",header=None, sep=",", names = ["X", "Y"])
df_MATHUSLA_disp = pd.read_csv("/eos/user/s/sgiappic/2HNL_samples/data/MATHUSLA_disp_data.csv",header=None, sep=",", names = ["X", "Y"])
df_FASER_disp = pd.read_csv("/eos/user/s/sgiappic/2HNL_samples/data/FASER_disp_data.csv",header=None, sep=",", names = ["X", "Y"])
df_AL3X_disp = pd.read_csv("/eos/user/s/sgiappic/2HNL_samples/data/AL3X_disp_data.csv",header=None, sep=",", names = ["X", "Y"])
df_CMB = pd.read_csv("/eos/user/s/sgiappic/2HNL_samples/data/CMB_data.csv",header=None, sep=",", names = ["X", "Y"])
df_CMB_Linear = pd.read_csv("/eos/user/s/sgiappic/2HNL_samples/data/CMB_Linear_data.csv",header=None, sep=",", names = ["X", "Y"])
df_ShiSigl_SN = pd.read_csv("/eos/user/s/sgiappic/2HNL_samples/data/ShiSigl_SN_data.csv",header=None, sep=",", names = ["X", "Y"])
df_CMB_BAO_H = pd.read_csv("/eos/user/s/sgiappic/2HNL_samples/data/CMB_BAO_H_data.csv",header=None, sep=",", names = ["X", "Y"])
df_CMB_H_only = pd.read_csv("/eos/user/s/sgiappic/2HNL_samples/data/CMB_H_only_data.csv",header=None, sep=",", names = ["X", "Y"])
df_BBN = pd.read_csv("/eos/user/s/sgiappic/2HNL_samples/data/BBN_data.csv",header=None, sep=",", names = ["X", "Y"])

#my own data
df_NO_prompt = pd.read_csv("/eos/user/s/sgiappic/combine/NO_prompt.csv",header=None, sep=",", names = ["X", "Y"])
df_NO_nevents = pd.read_csv("/eos/user/s/sgiappic/combine/NO_nevents.csv",header=None, sep=",", names = ["X", "Y"])
df_IO_prompt = pd.read_csv("/eos/user/s/sgiappic/combine/IO_prompt.csv",header=None, sep=",", names = ["X", "Y"])
df_IO_nevents = pd.read_csv("/eos/user/s/sgiappic/combine/IO_nevents.csv",header=None, sep=",", names = ["X", "Y"])


### Read to (x,y) = (m_N,|V_{eN}|^2)  ###

x_current_LNC, y_current_LNC = [], []
for i in range(len(df_current_LNC.index)):
    x_current_LNC.append(df_current_LNC.iloc[i]['X'])
    y_current_LNC.append(df_current_LNC.iloc[i]['Y'])

x_current_LNV, y_current_LNV = [], []
for i in range(len(df_current_LNV.index)):
    x_current_LNV.append(df_current_LNV.iloc[i]['X'])
    y_current_LNV.append(df_current_LNV.iloc[i]['Y'])

x_SHiP, y_SHiP = [], []
for i in range(len(df_SHiP.index)):
    x_SHiP.append(df_SHiP.iloc[i]['X'])
    y_SHiP.append(df_SHiP.iloc[i]['Y'])

x_DUNE_1, y_DUNE_1 = [], []
for i in range(len(df_DUNE_1.index)):
    x_DUNE_1.append(df_DUNE_1.iloc[i]['X'])
    y_DUNE_1.append(df_DUNE_1.iloc[i]['Y'])

x_DUNE_2, y_DUNE_2 = [], []
for i in range(len(df_DUNE_2.index)):
    x_DUNE_2.append(df_DUNE_2.iloc[i]['X'])
    y_DUNE_2.append(df_DUNE_2.iloc[i]['Y'])

x_FCC_ee, y_FCC_ee = [], []
for i in range(len(df_FCC_ee.index)):
    x_FCC_ee.append(df_FCC_ee.iloc[i]['X'])
    y_FCC_ee.append(df_FCC_ee.iloc[i]['Y'])

x_NO_prompt, y_NO_prompt = [], []
for i in range(len(df_NO_prompt.index)):
    x_NO_prompt.append(df_NO_prompt.iloc[i]['X'])
    y_NO_prompt.append(df_NO_prompt.iloc[i]['Y'])

x_NO_nevents, y_NO_nevents = [], []
for i in range(len(df_NO_nevents.index)):
    x_NO_nevents.append(df_NO_nevents.iloc[i]['X'])
    y_NO_nevents.append(df_NO_nevents.iloc[i]['Y'])

x_IO_prompt, y_IO_prompt = [], []
for i in range(len(df_IO_prompt.index)):
    x_IO_prompt.append(df_IO_prompt.iloc[i]['X'])
    y_IO_prompt.append(df_IO_prompt.iloc[i]['Y'])

x_IO_nevents, y_IO_nevents = [], []
for i in range(len(df_IO_nevents.index)):
    x_IO_nevents.append(df_IO_nevents.iloc[i]['X'])
    y_IO_nevents.append(df_IO_nevents.iloc[i]['Y'])

x_MATHUSLA_disp, y_MATHUSLA_disp = [], []
for i in range(len(df_MATHUSLA_disp.index)):
    x_MATHUSLA_disp.append(df_MATHUSLA_disp.iloc[i]['X'])
    y_MATHUSLA_disp.append(df_MATHUSLA_disp.iloc[i]['Y'])

x_FASER_disp, y_FASER_disp = [], []
for i in range(len(df_FASER_disp.index)):
    x_FASER_disp.append(df_FASER_disp.iloc[i]['X'])
    y_FASER_disp.append(df_FASER_disp.iloc[i]['Y'])

x_AL3X_disp, y_AL3X_disp = [], []
for i in range(len(df_AL3X_disp.index)):
    x_AL3X_disp.append(df_AL3X_disp.iloc[i]['X'])
    y_AL3X_disp.append(df_AL3X_disp.iloc[i]['Y'])

x_CMB, y_CMB, z_CMB = [], [], []
for i in range(len(df_CMB.index)):
    x_CMB.append(df_CMB.iloc[i]['X'])
    y_CMB.append(df_CMB.iloc[i]['Y'])
    z_CMB.append(df_CMB.iloc[i]['Y']+0.7)

x_CMB_Linear, y_CMB_Linear, z_CMB_Linear = [], [], []
for i in range(len(df_CMB_Linear.index)):
    x_CMB_Linear.append(df_CMB_Linear.iloc[i]['X'])
    y_CMB_Linear.append(df_CMB_Linear.iloc[i]['Y'])
    z_CMB_Linear.append(df_CMB_Linear.iloc[i]['Y']+0.7)

x_CMB_BAO_H, y_CMB_BAO_H  = [], []
for i in range(len(df_CMB_BAO_H.index)):
    x_CMB_BAO_H.append(df_CMB_BAO_H.iloc[i]['X'])
    y_CMB_BAO_H.append(df_CMB_BAO_H.iloc[i]['Y'])

x_CMB_BAO_H_2, y_CMB_BAO_H_2  = [], []
for i in range(len(df_CMB_BAO_H.index)):
    x_CMB_BAO_H_2.append(df_CMB_BAO_H.iloc[i]['X'])
    y_CMB_BAO_H_2.append(df_CMB_BAO_H.iloc[i]['Y'])
for i in range(1,len(df_CMB_BAO_H.index)+1):
    x_CMB_BAO_H_2.append(df_CMB_BAO_H.iloc[-i]['X'] + 0.5)
    y_CMB_BAO_H_2.append(df_CMB_BAO_H.iloc[-i]['Y'] + 0.5)

x_CMB_H_only, y_CMB_H_only  = [], []
for i in range(len(df_CMB_H_only.index)):
    x_CMB_H_only.append(df_CMB_H_only.iloc[i]['X'])
    y_CMB_H_only.append(df_CMB_H_only.iloc[i]['Y'])

x_BBN, y_BBN  = [], []
for i in range(len(df_BBN.index)):
    x_BBN.append(df_BBN.iloc[i]['X'])
    y_BBN.append(df_BBN.iloc[i]['Y'])
x_BBN.append(6.84-9)
y_BBN.append(0.1)

x_BBN_2, y_BBN_2  = [], []
x_BBN_2.append(6.84 - 0.5-9)
y_BBN_2.append(0.1)
for i in range(1,len(df_BBN.index)+1):
    x_BBN_2.append(df_BBN.iloc[-i]['X'] - 0.5)
    y_BBN_2.append(df_BBN.iloc[-i]['Y'] - 0.5)
for i in range(len(df_BBN.index)):
    x_BBN_2.append(df_BBN.iloc[i]['X'])
    y_BBN_2.append(df_BBN.iloc[i]['Y'])
x_BBN_2.append(6.84-9)
y_BBN_2.append(0.1)

x_ShiSigl_SN, y_ShiSigl_SN = [], []
for i in range(len(df_ShiSigl_SN.index)):
    x_ShiSigl_SN.append(df_ShiSigl_SN.iloc[i]['X'])
    y_ShiSigl_SN.append(df_ShiSigl_SN.iloc[i]['Y'])

fig, axes = plt.subplots(nrows=1, ncols=1)

spacing=0.2
m = np.arange(-12,6+spacing, spacing)
age_bound = np.log10(1.1 * 10**(-7) * ((50 * 10**(3))/10**(m))**5)
bbn_bound = np.log10(5.55007 * 10**(35) * (1/10**(m))**5)
seesaw_bound = np.log10(0.05*10**(-9)/10**(m))

### Current Constraints ###

axes.plot(m,seesaw_bound,linewidth=2,linestyle='-.',color='red') # Seesaw line
axes.plot(x_current_LNC,y_current_LNC,linewidth=0.5,linestyle='-.',color='black')
axes.plot(x_current_LNV,y_current_LNV,linewidth=0.5,linestyle='-.',color='black') 

### Future Constraints ###
axes.plot(x_MATHUSLA_disp,y_MATHUSLA_disp,linewidth=1.5,linestyle='-',color='gold') # MATHUSLA
axes.plot(x_FASER_disp,y_FASER_disp,linewidth=1.5,linestyle='--',color='c') # FASER
axes.plot(x_SHiP,y_SHiP,linewidth=1.5,linestyle='-',color='purple') # SHiP
axes.plot(x_AL3X_disp,y_AL3X_disp,linewidth=1.5,linestyle='--',color='indianred') # AL3X
# axes.plot(x_DUNE_1,y_DUNE_1,linewidth=1.5,linestyle='-',color='black') # DUNE ND
axes.plot(x_DUNE_2,y_DUNE_2,linewidth=1.5,linestyle='-',color='navy') # DUNE ND
axes.plot(x_FCC_ee,y_FCC_ee,linewidth=1.5,linestyle='-',color='darkgreen') # FCC-ee
axes.plot(x_NO_prompt,y_NO_prompt,linewidth=1.5,linestyle='-',color='#CC3333') # FCC-ee
axes.plot(x_NO_nevents,y_NO_nevents,linewidth=1.5,linestyle='--',color='#CC3333') # FCC-ee
axes.plot(x_IO_prompt,y_IO_prompt,linewidth=1.5,linestyle='-',color='#3366CC') # FCC-ee
axes.plot(x_IO_nevents,y_IO_nevents,linewidth=1.5,linestyle='--',color='#3366CC') # FCC-ee

#exclusion areas
axes.plot(x_CMB,y_CMB,linewidth=1,linestyle='-.',color='dimgrey') # Evans data
axes.plot(x_CMB_Linear,y_CMB_Linear,linewidth=1,linestyle='-.',color='dimgrey') # Linear CMB
axes.plot(x_CMB_BAO_H,y_CMB_BAO_H,linewidth=0.5,linestyle='-',color='grey') # # Decay after BBN constraints
# axes.plot(x_CMB_H_only,y_CMB_H_only,linewidth=1.5,linestyle='--',color='red') # Decay after BBN, Hubble only
axes.plot(x_BBN,y_BBN,linewidth=0.5,linestyle='-',color='grey') # Decay before BBN constraints
axes.plot(x_ShiSigl_SN,y_ShiSigl_SN,linewidth=1.5,linestyle=':',color='darkslateblue',alpha=0.4) # Shi and Sigl Supernova constraints

### Shading ###

plt.fill_between(x_current_LNC,0.2,y_current_LNC, facecolor='k', alpha=0.075)
plt.fill_between(x_current_LNV,0.2,y_current_LNV, facecolor='grey', alpha=0.075)
plt.fill_between(x_CMB,y_CMB,z_CMB, facecolor='black', alpha=0.02,lw=0)
plt.fill_between(x_CMB_BAO_H_2,0.1,y_CMB_BAO_H_2, facecolor='black', alpha=0.02,lw=0)
plt.fill_between(x_BBN_2,0.1,y_BBN_2, facecolor='black', alpha=0.02,lw=0)
plt.fill_between(x_CMB_Linear,y_CMB_Linear,z_CMB_Linear,facecolor='black', alpha=0.02,lw=0)
plt.fill_between(x_ShiSigl_SN,-3.6,y_ShiSigl_SN,facecolor='darkslateblue', alpha=0.01,lw=0)

#my data

### Labels ###

plt.text(10.5-9, -6.4, r'$\mathrm{Theory\; FCC-ee} $',fontsize=16,rotation=0,color='darkgreen')
plt.text(10-9, -8.8, r'$\mathrm{NH\; HNLs} $',fontsize=16,rotation=0,color="#CC3333")
plt.text(10.8-9, -9.6, r'$\mathrm{NH\; displaced \; HNLs\;} $',fontsize=16,rotation=0,color="#CC3333")
plt.text(10.7-9, -7.6, r'$\mathrm{IH\; HNLs\;} $',fontsize=16,rotation=0,color="#3366CC")
plt.text(10.8-9, -10.2, r'$\mathrm{IH\; displaced \; HNLs\;} $',fontsize=16,rotation=0,color="#3366CC")
plt.text(9.1-9, -10.35, r'$\mathrm{SHiP} $',fontsize=16,rotation=0,color='purple')
plt.text(8.25-9, -10.2, r'$\mathrm{DUNE} $',fontsize=16,rotation=0,color='navy')
plt.text(9.3-9, -9, r'$\mathrm{MATHUSLA} $',fontsize=15,rotation=0,color='gold')
plt.text(8.25-9, -4.9, r'$\mathrm{FASER2} $',fontsize=15,rotation=0,color='c')
plt.text(8.2-9, -6.8, r'$\mathrm{AL3X} $',fontsize=15,rotation=0,color='indianred')
plt.text(10.7-9, -11.8, r'$\mathrm{Seesaw}$',fontsize=16,rotation=0,color='red')
plt.text(9.4-9, -11.7, r'$\mathrm{BBN}$',fontsize=16,rotation=0,color='grey')

axes.set_xticks([-1,0,1,2,3])
axes.xaxis.set_ticklabels([r'$10^{-1}$',r'$1$',r'$10^{1}$',r'$10^{2}$',r'$10^{3}$'],fontsize =26)
axes.set_yticks([-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3])
axes.yaxis.set_ticklabels([r'',r'$10^{-12}$',r'',r'$10^{-10}$',r'',r'$10^{-8}$',r'',r'$10^{-6}$',r'',r'$10^{-4}$',r''],fontsize =26)
axes.tick_params(axis='x', which='major', pad=7.5)

axes.set_ylabel(r'$|U|^2$',fontsize=30,rotation=90)
axes.set_xlabel(r'$M_N \, [\mathrm{GeV}]$',fontsize=30,rotation=0)

axes.xaxis.set_label_coords(0.52,-0.08)
axes.yaxis.set_label_coords(-0.09,0.5)
axes.set_xlim(-1.1,3.1)
axes.set_ylim(-12.1,-3.9)

### Set aspect ratio (golden ratio) ###

x0,x1 = axes.get_xlim()
y0,y1 = axes.get_ylim()
axes.set_aspect(2*(x1-x0)/(1+Sqrt(5))/(y1-y0))

fig.set_size_inches(15,15)

plt.legend(loc='lower right',fontsize=18,frameon=False)

plt.savefig("/eos/user/s/sgiappic/www/plots/future_constraints.png",bbox_inches='tight')