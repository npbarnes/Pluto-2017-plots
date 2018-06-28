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

data = find_fit_file(spice_tools.flyby_start)
t = data['time_label_spect'].data
times = [spice_tools.et2pydatetime(tt) for tt in t['middle_et']]
positions = [spice_tools.pos_at_time(tt, mccomas=True)/1187. for tt in t['middle_et']]
energies = data['energy_label_spect'].data[0][2:]

# suppress error and poor statistics
s_raw = data['scem_spect_hz'].data
s_err = data['scem_error_bars_spect_hz'].data
p_raw = data['pcem_spect_hz'].data
p_err = data['pcem_error_bars_spect_hz'].data

sample_duration = (t['stop_et'] - t['start_et'])/len(energies)
p_sample = p_raw*sample_duration
s_sample = s_raw*sample_duration

mult = 0
samp = 3
s = np.where(np.logical_and(s_raw > mult*s_err, s_sample > samp), s_raw, 0)
p = np.where(np.logical_and(p_raw > mult*p_err, p_sample > samp), p_raw, 0)

# Find the smoothed S/P ratios
# Take a boxcar average
p_boxcar = convolve2d(p_raw, np.ones((3,3),dtype='f')/9., mode='same')
s_boxcar = convolve2d(s_raw, np.ones((3,3),dtype='f')/9., mode='same')
sp_ratio = np.divide(s_boxcar, p_boxcar, out=np.zeros_like(p_boxcar), where=(p_boxcar!=0))

# Use S/P ratios to identify bins and plot resulting identified spectrogram
cutoff = 3.5
light = np.ma.masked_where(np.logical_or(sp_ratio >= cutoff, s==0), s)
heavy = np.ma.masked_where(np.logical_or(sp_ratio <  cutoff, s==0), s)

plt.style.use('pluto-paper')
rcParams['figure.autolayout'] = False # autolayout (default True in pluto-paper style) breaks these plots
fig, ax = plt.subplots(figsize=figaspect(0.3))

vmin = min(np.ma.min(light),np.ma.min(heavy), 1)
vmax = max(np.ma.max(light),np.ma.max(heavy))

light_mappable = ax.pcolormesh(times, energies, light, norm=LogNorm(), cmap='Blues', vmin=vmin, vmax=vmax)
heavy_mappable = ax.pcolormesh(times, energies, heavy, norm=LogNorm(), cmap='Reds',  vmin=vmin, vmax=vmax)

cbars = N_colorbars(fig, ax, 2, fraction=0.2*2./3.)
fig.colorbar(light_mappable, cax=cbars[1])
cb = fig.colorbar(heavy_mappable, cax=cbars[0], format='')

cb_pos = cb.ax.get_position()
fig.text(cb_pos.x1, cb_pos.y1+0.01, "SCEM (Hz)", horizontalalignment='center', fontsize=15)

ax.set_xlim([spice_tools.flyby_start_pydatetime, spice_tools.flyby_end_pydatetime])
ax.set_yscale('log')
ax.xaxis.set_major_locator(HourLocator())
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
ax.xaxis.set_minor_locator(MinuteLocator(byminute=range(0,60,10)))
ax.set_xlabel('Time (UTC)')
ax.set_ylabel('Energy/Q (eV/q)')
ax.set_title('SWAP Flyby Spectrogram', pad=50)

pos_ax = ax.twiny()
pos_ax.set_xlim(ax.get_xlim())
pos_ax.set_xlabel('X ($R_p$)')

class PositionLocator(MultipleLocator):
    def __call__(self):
        vmin_mpldate, vmax_mpldate = self.axis.get_view_interval()
        vmin_x = spice_tools.pos_at_mpl_date(vmin_mpldate, mccomas=True)
        vmax_x = spice_tools.pos_at_mpl_date(vmax_mpldate, mccomas=True)
        ticks = self.tick_values(vmin_x/1187., vmax_x/1187.)
        return [spice_tools.mpl_date_at_pos(x*1187., beg_end=[spice_tools.flyby_lmargin, spice_tools.flyby_rmargin], mccomas=True) for x in ticks]

def mpldate2position_formatter(tick_val, tick_pos):
    string = '{0:.0f}'.format(spice_tools.pos_at_mpl_date(tick_val, mccomas=True)/1187.) # add zero to make -0 become 0
    if string == '-0':
        return '0'
    else:
        return string

pos_ax.xaxis.set_major_locator(PositionLocator(50))
pos_ax.xaxis.set_minor_locator(PositionLocator(10))
pos_ax.xaxis.set_major_formatter(FuncFormatter(mpldate2position_formatter))


ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')
pos_ax.xaxis.tick_bottom()
pos_ax.xaxis.set_label_position('bottom')

#plt.savefig(os.path.expanduser('~/Dropbox/Pluto-2017/red_blue_spectrogram.png'), bbox_inches='tight') 
plt.show()
