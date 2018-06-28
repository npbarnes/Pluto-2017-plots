import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['figure.autolayout'] = True

@np.vectorize
def atm(r):
    if r < 0:
        raise ValueError("Radius must be positive")

    if r > 30:
        return 0
    elif r >= 1.1 and r <= 30:
        return 1e15*(1e15*r**-25 + 5e9*r**-8)
    elif r < 1.1:
        return atm(1.1)

r = np.linspace(0, 35, 10000)
plt.plot(atm(r),r)
plt.title('Neutral Density Profile')
plt.ylabel('Radius ($R_p$)')
plt.xlabel('Neutral Density ($km^{-3}$)')
plt.xscale('log')

ax = plt.gca()

ax.title.set_fontsize(25)
ax.xaxis.label.set_fontsize(20)
ax.yaxis.label.set_fontsize(20)
for l in (ax.get_xticklabels() + ax.get_yticklabels()):
    l.set_fontsize(15)

import os
plt.savefig(os.path.expanduser('~/Dropbox/Pluto-2017/atmosphere-profile.png'))
