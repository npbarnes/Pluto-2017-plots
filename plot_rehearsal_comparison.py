import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.dates import HourLocator, MinuteLocator, DateFormatter
from matplotlib.ticker import MultipleLocator, FuncFormatter

import rehearsal_tools as rt
import spice_tools

def N_colorbars(fig, N, h_fraction=0.2, v_fraction=2./3., ax_pad=0.01, bar_pad=0.0, label_pad=0.1):
    """Adjust subplots, make axes for N colorbars, and return the axes objects.
    fig: The figure that will hold the colorbar axes
    N: How many colorbars to make
    h_fraction: What horizontal fraction of the figure to use up
    v_fraction: What vertical fraction of the figure to use up
    ax_pad: Amount of space between the subplot axes and the first colorbar axes
    bar_pad: Amount of space between each colorbar
    label_pad: Amount of space to save on the right for axis and tick labels
    """
    ax_right = 1-h_fraction
    bar_space = h_fraction-ax_pad-label_pad
    bar_width = (bar_space-(N-1)*bar_pad)/N
    centered_bar_bottom = (1-v_fraction)/2.

    fig.subplots_adjust(right=ax_right)

    first_cbar = fig.add_axes([ax_right+ax_pad, centered_bar_bottom, bar_width, v_fraction])

    cbars = [first_cbar]
    for i in range(1,N):
        prev_pos = cbars[i-1].get_position()
        cbars.append(fig.add_axes([prev_pos.xmax+bar_pad, centered_bar_bottom, bar_width, v_fraction]))

    return cbars

fig, (ax_NH, ax_sim) = plt.subplots(nrows=2, figsize=(7,5), 
        subplot_kw={'yscale':'log'},
        gridspec_kw={'left':0.09, 'top':0.85, 'bottom':0.11, 'hspace':0.08})

cbar = N_colorbars(fig, 1, h_fraction=0.2, v_fraction=1./2., ax_pad=0.06, label_pad=0.09)[0]
cbar.set_title('SCEM (Hz)', fontdict={'fontsize':12})

mappable = ax_NH.pcolormesh( rt.times, rt.energies, rt.scem, norm=LogNorm(), vmin=1, vmax=1e5)
ax_sim.pcolormesh(rt.sim_times, rt.sim_energies, rt.sim_scem, norm=LogNorm(), vmin=1, vmax=1e5)
print rt.scem.max(), rt.sim_scem.max(), rt.sim_scem.max()/rt.scem.max()

fig.colorbar(mappable, cax = cbar)

cbar.tick_params(which='y', left=True, right=True)

ax_NH.set_xlim([spice_tools.rehearsal_start_pydatetime, spice_tools.rehearsal_end_pydatetime])
ax_sim.set_xlim([spice_tools.rehearsal_start_pydatetime, spice_tools.rehearsal_end_pydatetime])

ax_sim.xaxis.set_major_locator(HourLocator())
ax_sim.xaxis.set_major_formatter(DateFormatter('%H:%M'))
ax_sim.xaxis.set_minor_locator(MinuteLocator(byminute=range(0,60,10)))
ax_sim.tick_params(which='both', top=True, bottom=True, left=True, right=True)
ax_sim.set_xlabel('Time (UTC)')
ax_sim.set_ylabel('Energy/Q (eV/q)')
ax_NH.xaxis.set_major_locator(HourLocator())
ax_NH.xaxis.set_major_formatter(DateFormatter('%H:%M'))
ax_NH.xaxis.set_minor_locator(MinuteLocator(byminute=range(0,60,10)))
ax_NH.tick_params(which='both', top=True, bottom=True, left=True, right=True)
ax_NH.set_ylabel('Energy/Q (eV/q)')

plt.setp(ax_NH.get_xticklabels(), visible=False)

ax_sim.text(1.0-0.017,0.07, 'Synthetic SWAP Spectrogram',
        ha='right',
        bbox=dict(fc='w', ec='0.05'),
        transform=ax_sim.transAxes,
        fontsize=12)
ax_NH.text(1.0-0.017,0.07, 'SWAP Spectrogram',
        ha='right',
        bbox=dict(fc='w', ec='0.05'),
        transform=ax_NH.transAxes,
        fontsize=12)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--save', nargs='?', const='synthetic_spectrograms.png')
args = parser.parse_args()
savename = args.save
if savename:
    plt.savefig(savename, bbox_inches='tight')
else:
    plt.show()
