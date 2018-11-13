import os
from matplotlib import rcParams
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.dates import HourLocator, MinuteLocator, DateFormatter
from matplotlib.ticker import MultipleLocator, FuncFormatter
from matplotlib.figure import figaspect
import numpy as np
import NH_tools
import spice_tools
from scipy.signal import convolve2d
from swap import find_fit_file
from espec import N_colorbars
from HybridHelper import build_format_coord
from pprint import pprint

from swap import bin_centers, bin_edges
bin_widths = bin_edges[1:] - bin_edges[:-1]

data = find_fit_file(spice_tools.rehearsal_start)
t = data['time_label_spect'].data
times = [spice_tools.et2pydatetime(tt) for tt in t['middle_et']]
positions = [spice_tools.pos_at_time(tt, mccomas=True)/1187. for tt in t['middle_et']]
energies = np.array(data['energy_label_spect'].data[0][2:])

# suppress error and poor statistics
s_raw = data['scem_spect_hz'].data
s_err = data['scem_error_bars_spect_hz'].data

sample_duration = (t['stop_et'] - t['start_et'])/len(energies)
s_sample = s_raw*sample_duration

mult = 0
samp = 3
s = np.where(np.logical_and(s_raw > mult*s_err, s_sample > samp), s_raw, 0)
s = np.ma.masked_where(s == 0, s)

interval = s_raw[:,655:711]
spectrum = np.mean(interval, axis=1)

print s.shape
print interval.shape
print spectrum.shape
print energies.shape

plt.hist(bin_centers, bins=bin_edges, weights=spectrum, log=True)
plt.xscale('log')
plt.show()
