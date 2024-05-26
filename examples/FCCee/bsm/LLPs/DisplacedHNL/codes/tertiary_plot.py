import matplotlib.pyplot as plt
import numpy as np
import ternary
import mpltern

# benchmark points

points_NOz = [0, 0.1, 0.1] #e
points_NOx = [0.5, 0.7, 0.15] #mu
points_NOy = [0.5, 0.2, 0.75] #tau
points_IOz = [0.1, 0.4, 0.93]
points_IOx = [0.4, 0.3, 0.07]
points_IOy = [0.5, 0.3, 0]

# nufit points

data_file = "/eos/user/s/sgiappic/2HNL_samples/nufit.csv"
data = np.genfromtxt(data_file, delimiter=',')

labels = [r'$NO 1 \sigma$', r'$NO 2 \sigma$', r'$NO 3 \sigma$', r'$IO 1 \sigma$', r'$IO 2 \sigma$', r'$IO 3 \sigma$']
colors = ['#B95C50', '#DE847B', '#DEB3AD', '#478C5C', '#94C973', '#B1D8B7']

    
ax = plt.subplot(projection="ternary", ternary_sum=1.0)

for i in range(0,6):
    #print(i)
    Ue = data[:, 0+i]
    Umu = data[:, 1+i]
    Utau = data[:, 2+i]

    #points = np.vstack((Ue, Umu, Utau)).T

    #ax.fill(Umu, Ue, Utau, alpha=1)
    ax.fill(Umu, Utau, Ue, facecolor=colors[i], alpha=0.9, label=labels[i])


ax.scatter(points_NOx, points_NOy, points_NOz, color='#900020', label='Normal hierarchy')
ax.scatter(points_IOx, points_IOy, points_IOz, color='#2F5233', label='Inverted hierarchy')

fontsize = 12
ax.set_tlabel(r'$U^2_\mu/U^2$', fontsize=fontsize)
ax.set_llabel(r'$U^2_\tau/U^2$', fontsize=fontsize)
ax.set_rlabel(r'$U^2_e/U^2$', fontsize=fontsize)

ax.grid()
#ax.legend()
#plt.show()
plt.savefig('/eos/user/s/sgiappic/www/plots/tertiary_plot.png', dpi=330, format='png')