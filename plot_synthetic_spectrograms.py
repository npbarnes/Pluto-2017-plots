import numpy as np
import argparse
import cPickle
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, MinuteLocator, DateFormatter
from matplotlib.figure import figaspect
from matplotlib.ticker import MultipleLocator
from espec import N_colorbars, color_coded_espec_pcolormesh
import itertools
import spice_tools

mpl.rcParams['text.latex.preamble']=[r'\usepackage[version=4]{mhchem}']
mpl.rc('text', usetex=True)
mpl.rc('axes', titlesize=15, labelsize=12)
mpl.rc('xtick', labelsize=12)
mpl.rc('ytick', labelsize=12)

def xlim2tlim(left,right):
    left_t  = spice_tools.et2pydatetime(spice_tools.time_at_pos(1187*left, mccomas=True))
    right_t = spice_tools.et2pydatetime(spice_tools.time_at_pos(1187*right, mccomas=True))

    return left_t, right_t

parser = argparse.ArgumentParser()
parser.add_argument('--save', nargs='?', const='synthetic_spectrograms.png')
savename = parser.parse_args().save

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

fig, (high_ax, medium_ax, low_ax) = plt.subplots(nrows=3, sharex=True, figsize=(7,5), 
        subplot_kw={'yscale':'log'},
        gridspec_kw={'left':0.09, 'top':0.85, 'bottom':0.11, 'hspace':0.1})
axs = (high_ax, medium_ax, low_ax)

cbars = N_colorbars(fig, 3, h_fraction=0.22, v_fraction=1./2., ax_pad=0.015, bar_pad=0.015, label_pad=0.06)
fig.text(np.average(cbars[0].get_position().intervalx), cbars[0].get_position().ymin-0.04, r'$\mathrm{H}^+$',
        va='bottom', ha='center', fontsize=10)
fig.text(cbars[1].get_position().xmin, cbars[1].get_position().ymin-0.04, r'$\mathrm{He}^{++}$',
        va='bottom', ha='left', fontsize=10)
fig.text(cbars[2].get_position().xmin, cbars[2].get_position().ymin-0.04, r'$\mathrm{CH}_4^+$',
        va='baseline', ha='left', fontsize=10)

#cbars[0].set_xlabel('$\ce{H^+}$', fontdict={'fontsize':10})
#cbars[1].set_xlabel('$\ce{He^{++}}$', fontdict={'fontsize':10})
#cbars[2].set_xlabel('$\ce{CH_4^+}$', fontdict={'fontsize':10})
cbars[1].set_title('SCEM (Hz)', fontdict={'fontsize':12})
for cbar in cbars:
    cbar.tick_params(labelsize=10)

with open('high_IMF_espec.pickle') as f:
    high_espec = cPickle.load(f)
with open('medium_IMF_espec.pickle') as f:
    medium_espec = cPickle.load(f)
with open('low_IMF_espec.pickle') as f:
    low_espec = cPickle.load(f)
especs = (high_espec, medium_espec, low_espec)

for espec in especs:
    assert np.allclose(espec['trajectory'], especs[0]['trajectory'])
# They all have the same trajectory so we only need to define the x axis once
X = -low_espec['trajectory'][:,0]/1187.

high_mappables   = color_coded_espec_pcolormesh(high_ax,   X, high_espec)
medium_mappables = color_coded_espec_pcolormesh(medium_ax, X, medium_espec)
low_mappables    = color_coded_espec_pcolormesh(low_ax,    X, low_espec)
for mappable in itertools.chain(high_mappables, medium_mappables, low_mappables):
    assert mappable.get_clim() == high_mappables[0].get_clim()
# They all have the same colorbar scales, so they call all share the same three colorbars
fig.colorbar(high_mappables[0], cax=cbars[0], format='')
fig.colorbar(high_mappables[1], cax=cbars[1], format='')
fig.colorbar(high_mappables[2], cax=cbars[2])

time_axs = []
for ax in axs:
    ax.xaxis.set_major_locator(MultipleLocator(50))
    ax.xaxis.set_minor_locator(MultipleLocator(10))
    ax.tick_params(which='both', bottom=True, left=True, right=True)
    ax.set_xlim([-20,105])
    time_axs.append(ax.twiny())
    time_axs[-1].set_xlim(xlim2tlim(*ax.get_xlim()))
    time_axs[-1].xaxis.set_major_locator(HourLocator())
    time_axs[-1].xaxis.set_major_formatter(DateFormatter('%H:%M'))
    time_axs[-1].xaxis.set_minor_locator(MinuteLocator(byminute=range(0,60,10)))
    plt.setp(time_axs[-1].get_xticklabels(), visible=False)

high_ax.set_title('Synthetic SWAP Spectrograms, with IPUI', pad=35)
low_ax.set_xlabel('X ($R_p$)')
medium_ax.set_ylabel('Energy/Q (eV/q)')
time_axs[0].set_xlabel('Time (UTC)')
plt.setp(time_axs[0].get_xticklabels(), visible=True)

for ax,imf in zip(axs,(0.3,0.19,0.08)):
    ax.text(0.017,0.1, 'IMF:{}nT'.format(imf),
            #bbox=dict(boxstyle='round', fc='w', ec='0.05', alpha=0.9),
            bbox=dict(fc='w', ec='0.05'),
            transform=ax.transAxes,
            fontsize=12)

#fig.text(0.95,0.95, 'With IPUI',
#        verticalalignment='top', horizontalalignment='right',
#        fontsize=12)

if savename:
    plt.savefig(savename)
else:
    plt.show()
