import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
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
fig, axs = gp.figure_setup(len(profilers), 1/3.75, scale=3)
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

u.set_ylabel('Normalized\nVelocity')
nh.set_ylabel(r'$n_{H^+}$')
nch4.set_ylabel(r'$n_{CH_4^+}$')

u.get_yaxis().set_major_locator(MultipleLocator(0.1))
nh.set_yscale('log')
nch4.set_yscale('log')

u.set_ylim(0,1.09)
nh.set_ylim(0.000105,.2)
nch4.set_ylim(0.0001,1)
nch4.set_xlim(-30,80)

if args.sims == shell:
    u.set_title('Simulation Flyby Profiles\nWith IPUIs')
elif args.sims == noshell:
    u.set_title('Simulation Flyby Profiles\nWithout IPUIs')

if args.save:
    plt.savefig(args.save, bbox_inches='tight')
else:
    plt.show()
