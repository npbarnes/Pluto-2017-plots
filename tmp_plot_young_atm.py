import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

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

def cm3_atm(r):
    return atm(r)/1e15

def gph(r, ref=1187.0):
    return (r-ref)*(ref/r)

def r(gph, ref=1187.0):
    return ref**2/(ref-gph)

def actual(gph_p):
    return 1e8*np.exp(-gph_p/150.0)

r = np.linspace(1.0*1187.0, 35*1187.0, 10000)

plt.plot(cm3_atm(r/1187.0),r/1187.0)
plt.plot(actual(gph(r,869.0+1187.0)), r/1187.0)




plt.title('Neutral Density Profile')
plt.ylabel('geopotential height ($km$)')
plt.xlabel('Neutral Density ($\mathrm{cm}^{-3}$)')
plt.xscale('log')

ax = plt.gca()

plt.show()
