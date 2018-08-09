#!/usr/bin/env python
import numpy as np
from HybridReader2 import HybridReader2 as hr
from HybridReader2 import NoSuchVariable
from HybridHelper import hybrid_parse, init_figures, direct_plot, beta_plot, bs_hi_plot, traj_plot
import matplotlib.pyplot as plt
from matplotlib import colors, rcParams
from os.path import expanduser
import argparse

plt.style.use('pluto-paper')

def var_sanity_check(isScalar, coord):
    if h.isScalar and args.variable.coordinate is not None:
        raise ValueError("Don't specify a coordinate for scalars.")
    if not h.isScalar and args.variable.coordinate is None:
        raise ValueError("Must specify a coordinate for vectors.")

cmd_line_parser = argparse.ArgumentParser()
cmd_line_parser.add_argument('--save', nargs='?', default=False, const='xz_context', 
        help='Set flag to save instead of displaying. Optionally provide a filename (or filepath).')
cmd_line_args = cmd_line_parser.parse_args()

args = hybrid_parse(['-p', expanduser('~/data/2017-Mon-Nov-13/pluto-7/data'),
                     '-v', 'np_CH4',
                     '--norm', 'log',
                     '--vmin', '1e13',
                     '--vmax', '1e16',
                     '--xlim', '-70', '110',
                     '--ylim', '-100', '200', 
                     '--mccomas', 
                     '--title', 'Heavy Ion Number Density\nIMF:0.3nT, With IPUIs',
                     '--units', '$\mathrm{km}^{-3}$',
                     '--titlesize', '15', 
                     '--labelsize', '13',
                     '--ticklabelsize', '12',
                     '--separate-figures'])

args.save = cmd_line_args.save


fig1, fig2, ax1, ax2 = init_figures(args)
plt.close() # Not using fig2, so we close it

h = hr(args.prefix,args.variable.name)
var_sanity_check(h.isScalar, args.variable.coordinate)

data = h.get_timestep(args.stepnum)[-1]
if not h.isScalar:
    data = data[:,:,:,args.variable.coordinate]
para = h.para

direct_plot(fig1, ax1, data, para, 'xz', cmap=args.colormap,
        norm=args.norm,
        vmin=args.vmin, vmax=args.vmax,
        mccomas=args.mccomas,
        titlesize=args.titlesize, 
        labelsize=args.labelsize, 
        ticklabelsize=args.ticklabelsize, 
        cbtitle=args.units)


if args.ylim is not None:
    ax1.set_ylim(*args.ylim)
if args.xlim is not None:
    ax1.set_xlim(*args.xlim)

ax1.set_title(args.title,  fontsize=args.titlesize)

ax1.annotate('',
        xy=(14,172), xycoords='data',
        xytext=(-48,21), textcoords='data',
        arrowprops=dict(arrowstyle='simple',
                        fc='0.6', ec='none',
                        connectionstyle='arc3,rad=-0.2'))
ax1.annotate('Gyromotion',
        xy=(-44,101), xycoords='data',
        size=8,
        bbox=dict(boxstyle='round', fc='w', ec='0.5', alpha=0.9),
        rotation=70, ha='center', va='center')

ax1.annotate('Bi-ion Waves',
        xy=(78,27), xycoords='data',
        size=8,
        bbox=dict(boxstyle='round', fc='w', ec='0.5', alpha=0.9),
        rotation=15, ha='center', va='center')

ax1.annotate('Tailward Flow',
        xy=(17,-23), xycoords='data',
        size=8,
        bbox=dict(boxstyle='round', fc='w', ec='0.5', alpha=0.9),
        ha='center', va='center')

ax1.annotate('',
        xy=(51,52), textcoords='data',
        xytext=(78,27), xycoords='data',
        arrowprops=dict(arrowstyle='simple',
                        fc='0.6', ec='none',
                        connectionstyle='arc3',
                        shrinkA=10))
ax1.annotate('',
        xy=(60,90), textcoords='data',
        xytext=(78,27), xycoords='data',
        arrowprops=dict(arrowstyle='simple',
                        fc='0.6', ec='none',
                        connectionstyle='arc3',
                        shrinkA=10))
ax1.annotate('',
        xy=(87,83), textcoords='data',
        xytext=(78,27), xycoords='data',
        arrowprops=dict(arrowstyle='simple',
                        fc='0.6', ec='none',
                        connectionstyle='arc3',
                        shrinkA=10))

ax1.annotate('',
        xy=(37,2), textcoords='data',
        xytext=(0,5), xycoords='data',
        arrowprops=dict(arrowstyle='simple',
                        fc='0.6', ec='none',
                        connectionstyle='arc3,rad=0.1',
                        shrinkA=0))

ax1.annotate('',
        xy=(37,-2), textcoords='data',
        xytext=(0,-5), xycoords='data',
        arrowprops=dict(arrowstyle='simple',
                        fc='0.6', ec='none',
                        connectionstyle='arc3,rad=-0.1',
                        shrinkA=0))




if args.save:
    fig1.savefig(args.save, bbox_inches='tight')
else:
    plt.show()
