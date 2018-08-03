import os
import sys
sys.path.append(os.path.join(os.getcwd(),'swap'))
from swap import p, transmission
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import figaspect
plt.style.use('pluto-paper')

phi = np.linspace(-180,180, 1000)
plt.plot(phi, p(phi))
plt.title('Azimuth')
plt.xlabel('$\\phi$')
plt.ylabel('$p(\\phi)$')

fig = plt.gcf()
fig.savefig(os.path.expanduser('~/Dropbox/Pluto-2017/p_of_phi.png'))

plt.figure(figsize=figaspect(1/2.66))
theta = np.linspace(-90,90, 1000)

resp = np.empty((phi.shape[0], theta.shape[0]))
energy = 1000.0*np.ones_like(theta, dtype='f')
mrat = np.ones_like(theta, dtype='f')
l = np.empty((theta.shape[0], 2))
l[:,0] = theta
for i,p in enumerate(phi):
    l[:,1] = phi[i]
    resp[i,:] = transmission(energy, l)

plt.pcolormesh(phi, theta, resp.T, vmin=0, vmax=1, cmap='jet')
plt.xlim([-140,140])
plt.ylim([-4.75,4.25])
#plt.title('Synthetic SWAP Transmission\n1keV protons')
plt.xlabel('$\\phi$')
plt.ylabel('$\\theta$')
cb = plt.colorbar(shrink=0.6, aspect=10, fraction=0.1, pad=0.02)
cb.set_label('Transmission')
cb.set_ticks([0,0.25,0.5,0.75,1])
plt.minorticks_on()

fig = plt.gcf()
fig.savefig(os.path.expanduser('~/Dropbox/Pluto-2017/wp_1keV.png'))
plt.show()
