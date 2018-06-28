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

data = find_fit_file(spice_tools.rehearsal_start)
t = data['time_label_spect'].data
times = [spice_tools.et2pydatetime(tt) for tt in t['middle_et']]
positions = [spice_tools.pos_at_time(tt, mccomas=True)/1187. for tt in t['middle_et']]
energies = data['energy_label_spect'].data[0][2:]

# suppress error and poor statistics
s_raw = data['scem_spect_hz'].data
s_err = data['scem_error_bars_spect_hz'].data

sample_duration = (t['stop_et'] - t['start_et'])/len(energies)
s_sample = s_raw*sample_duration

mult = 0
samp = 3
s = np.where(np.logical_and(s_raw > mult*s_err, s_sample > samp), s_raw, 0)
s = np.ma.masked_where(s == 0, s)

plt.style.use('pluto-paper')
rcParams['figure.autolayout'] = False # autolayout (default True in pluto-paper style) breaks these plots
fig, ax = plt.subplots(figsize=figaspect(0.3))

vmin = min(np.ma.min(s), 1)
mappable = ax.pcolormesh(times, energies, s, norm=LogNorm(), vmin=vmin)

cbars = N_colorbars(fig, ax, 1, fraction=0.1)
cb = fig.colorbar(mappable, cax=cbars[0])
cb.ax.set_title("SCEM (Hz)", fontsize=15)

ax.set_xlim([spice_tools.rehearsal_start_pydatetime, spice_tools.rehearsal_end_pydatetime])
ax.set_yscale('log')
ax.xaxis.set_major_locator(HourLocator())
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
ax.xaxis.set_minor_locator(MinuteLocator(byminute=range(0,60,10)))
ax.set_xlabel('Time (UTC)')
ax.set_ylabel('Energy/Q (eV/q)')
ax.set_title('SWAP Rehearsal Spectrogram')
ax.tick_params(axis='x', which='both', direction='out', top=True, bottom=True)

plt.savefig(os.path.expanduser('~/Dropbox/Pluto-2017/rehearsal_spectrogram.png'), bbox_inches='tight') 
#plt.show()
