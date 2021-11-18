import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, LogLocator, NullFormatter
from matplotlib.figure import figaspect
import grid_profiles as gp
from FortranFile import NoMoreRecords
import argparse

shell = zip(gp.shell_prefixes,gp.generic_labels)
noshell = zip(gp.no_shell_prefixes,gp.generic_labels)

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('--shell', action='store_const', dest='sims', const=shell)
group.add_argument('--no-shell', action='store_const', dest='sims', const=noshell)
parser.set_defaults(sims=shell)
parser.add_argument('--save', nargs='?', default=False, const='my_feyerabend6', 
        help='Set flag to save instead of displaying. Optionally provide a filename (or filepath).')
args = parser.parse_args()

plt.style.use('pluto-paper')

profilers = [gp.vnorm_profiler, gp.light_profiler, gp.heavy_profiler]

plt.style.use('pluto-paper')
fig, axs = plt.subplots(nrows=3, sharex=True, gridspec_kw={'left':0.1, 'right':0.87, 'hspace':0}, figsize=(7,5))
u, nh, nch4 = axs

for ax, profiler in zip(axs, profilers):
    for h, line_label in args.sims:
        pro = profiler(h, step=-1)
        gp.plot_profile(ax, pro, labels=[line_label], mccomas=True)

u.plot([-12.7,3.8,8.8,13.1,18.9,158.7,175.2],np.array([400.,365.,324.,250.,140.,320.,400.])/401.0, marker='o', linestyle='None', label='Data')

nch4.set_xlabel('$X (R_p)$')
u.legend(loc='lower left')

u.yaxis.set_label_position('right')
nh.yaxis.set_label_position('right')
nch4.yaxis.set_label_position('right')

u.set_ylabel('Normalized\nVelocity\n$u/u_{sw}$', rotation=0, labelpad=30, va='center')
nh.set_ylabel('$n_{\mathrm{H}^+}$\n$(\mathrm{cm}^{-3})$', rotation=0, labelpad=30, va='center')
nch4.set_ylabel('$n_{\mathrm{CH}_4^+}$\n$(\mathrm{cm}^{-3})$', rotation=0, labelpad=30, va='center')

u.get_yaxis().set_major_locator(MultipleLocator(0.1))
nh.set_yscale('log')
nch4.set_yscale('log')


u.set_ylim(-0.09,1.09)
nh.set_ylim(0.000105,.2)
nch4.set_ylim(0.0001,1)
nch4.set_xlim(-30,80)

# Need a stupid workaround to make nch4 show minor ticks >:(
majloc = LogLocator(base=10.0, numticks=6)
nch4.yaxis.set_major_locator(majloc)
minloc = LogLocator(base=10.0, subs=(0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9), numticks=6)
nch4.yaxis.set_minor_locator(minloc)
nch4.yaxis.set_minor_formatter(NullFormatter())

if args.sims == shell:
    u.set_title('With IPUIs', pad=3, fontsize=12)
elif args.sims == noshell:
    u.set_title('Without IPUIs', pad=3, fontsize=12)

if args.save:
    plt.savefig(args.save)
else:
    plt.show()
