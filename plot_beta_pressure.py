import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import grid_profiles as gp
import argparse
from HybridReader2 import HybridReader2 as hr
from HybridReader2 import NoSuchVariable
from HybridHelper import beta_plot2, traj_plot
from scipy.constants import value, unit

def insert_beta_plot(fig, ax, prefix, cax):
    hn = hr(prefix, 'np')
    para = hn.para
    n = hn.get_timestep(-1)[-1]
    try:
        T = hr(prefix, 'temp_tot').get_timestep(-1)[-1]
    except NoSuchVariable:
        T = hr(prefix, 'temp_p').get_timestep(-1)[-1]

    B = hr(prefix, 'bt').get_timestep(-1)[-1]

    # Convert units
    n = n/(1000.0**3)                    # 1/km^3 -> 1/m^3
    T = 1.60218e-19 * T                  # eV -> J
    B = 1.6726219e-27/1.60217662e-19 * B # proton gyrofrequency -> T

    # Compute B \cdot B
    B2 = np.sum(B**2, axis=-1)

    # Compute plasma beta
    mu_0 = value('mag. constant')
    assert unit('mag. constant') == 'N A^-2'
    data = n*T/(B2/(2*mu_0))

    m, x, y, s = beta_plot2(ax, data, para, 'xy', mccomas=True)

    if cax != 'None':
        fig.colorbar(m, cax=cax, orientation='horizontal')


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('--shell', action='store_const', dest='prefixes', const=gp.shell_prefixes)
group.add_argument('--no-shell', action='store_const', dest='prefixes', const=gp.no_shell_prefixes)
parser.set_defaults(prefixes=gp.shell_prefixes)
parser.add_argument('--save', nargs='?', default=False, const='my_feyerabend6', 
        help='Set flag to save instead of displaying. Optionally provide a filename (or filepath).')
args = parser.parse_args()

plt.style.use('pluto-paper')

fig, axs = plt.subplots(nrows=3, ncols=2, sharex=True, figsize=(5.5, 7), 
        gridspec_kw={'left':0.22, 'right':0.98, 'top':0.85, 'bottom':0.08, 'hspace':0.08, 'wspace':0.4})
[[high_beta_ax, high_pres_ax],[medium_beta_ax,medium_pres_ax],[low_beta_ax,low_pres_ax]] = axs


high_beta_bbox = high_beta_ax.get_position()
high_pres_bbox = high_pres_ax.get_position()
colorbar_ax = fig.add_axes([high_beta_bbox.xmin,
                            high_beta_bbox.ymax+0.02,
                            high_beta_bbox.width,
                            0.02])

insert_beta_plot(fig, axs[0,0], args.prefixes[0], colorbar_ax)
for beta_ax, prefix in zip(axs[1:,0], args.prefixes[1:]):
    insert_beta_plot(fig, beta_ax, prefix, 'None')

for pres_ax, prefix in zip(axs[:,1], args.prefixes):
    gp.plot_profile(pres_ax, gp.pressure_profiler(prefix), labels=['Thermal Pressure', 'Magnetic Pressure'], mccomas=True)
    pres_ax.set_yscale('log')
    pres_ax.set_ylim([0.0008, 3])
high_pres_ax.legend(loc='lower center', bbox_to_anchor=(0.5,0.99))

colorbar_ax.tick_params(axis='x', bottom=False, top=True, labelbottom=False, labeltop=True, pad=-1.5)

# JGR Wants titles separate from the figure (put them in the LaTeX file as text).
#if args.prefixes == gp.shell_prefixes:
#    fig.suptitle('With IPUI', fontsize=15, x=np.average((high_beta_bbox.xmax,high_pres_bbox.xmin)), y=0.99)
#elif args.prefixes == gp.no_shell_prefixes:
#    fig.suptitle('Without IPUI', fontsize=15, x=np.average((high_beta_bbox.xmax,high_pres_bbox.xmin)), y=0.99)

high_beta_ax.set_title('Plasma Beta', pad=40)
high_pres_ax.set_title('Pressure Profiles', pad=40)

low_beta_ax.set_xlabel('$X$ ($R_p$)')
low_pres_ax.set_xlabel('$X$ ($R_p$)')
low_beta_ax.xaxis.set_major_locator(MultipleLocator(base=20))
low_pres_ax.xaxis.set_major_locator(MultipleLocator(base=20))

for left_ax, imf in zip(axs[:,0], ('0.3 nT', '0.19 nT', '0.08 nT')):
    left_ax.set_ylabel('Transverse ($R_p$)')
    row_center = np.average(left_ax.get_position().intervaly)
    fig.text(0,row_center, 'IMF\n{}'.format(imf),
            ha='left', va='center', multialignment='center',
            fontsize=12)
    left_ax.set_xlim([-20,100])
    left_ax.set_ylim([-40,40])
    traj_plot(fig, left_ax, 'xy', mccomas=True)

for right_ax in axs[:,1]:
    right_ax.set_ylabel('Pressure (pPa)')

if args.save:
    plt.savefig(args.save)
else:
    plt.show()
