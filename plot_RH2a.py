import matplotlib.pyplot as plt
import grid_profiles as gp

fig, ax = plt.subplots()
prefix = '/home/nathan/data/2017-Mon-Nov-13/pluto-8/data'
gp.plot_profile(ax, gp.RH2a_profiler(prefix), labels=["Thing", "Plasma beta"], mccomas=True)

plt.show()
