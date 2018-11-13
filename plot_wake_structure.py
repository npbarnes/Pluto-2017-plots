import numpy as np
import argparse
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import grid_profiles as gp
from HybridReader2 import HybridReader2 as hr
from HybridReader2 import NoSuchVariable
from HybridHelper import bs_hi_plot, traj_plot

plt.style.use('pluto-paper')
parser = argparse.ArgumentParser()
parser.add_argument('--save', nargs='?', const='wake_structure.png')
savename = parser.parse_args().save

w = 7.6
fig, axs = plt.subplots(nrows=3, ncols=2, sharex=True, sharey=True, figsize=(w, 7), 
        gridspec_kw={'left':0.15125*8/w, 'right':0.6735*8/w, 'top':0.9, 'bottom':0.11, 'hspace':0.085, 'wspace':0.08})

[[high_with_ax, high_without_ax],[medium_with_ax,medium_without_ax],[low_with_ax,low_without_ax]] = axs
paths = np.array([gp.shell_prefixes,gp.no_shell_prefixes]).transpose()

fig.suptitle('Wake Structure', x=np.average((high_with_ax.get_position().xmax,high_without_ax.get_position().xmin)))

high_with_ax.set_title('With IPUI')
high_without_ax.set_title('Without IPUI')

low_with_ax.set_xlabel('$X$ ($R_p$)')
low_without_ax.set_xlabel('$X$ ($R_p$)')
low_with_ax.xaxis.set_major_locator(MultipleLocator(base=20))
low_without_ax.xaxis.set_major_locator(MultipleLocator(base=20))
for left_ax, imf in zip(axs[:,0], ('0.3nT', '0.19nT', '0.08nT')):
    left_ax.set_ylabel('Transverse ($R_p$)')
    row_center = np.average(left_ax.get_position().intervaly)
    fig.text(0,row_center, 'IMF\n{}'.format(imf),
            ha='left', va='center', multialignment='center',
            fontsize=12)

legend_proxies = []
for ax_row, path_row in zip(axs, paths):
    for ax, path in zip(ax_row, path_row):
        ax.set_aspect('equal')
        hup = hr(path,'up')
        try:
            hn_tot = hr(path,'np_tot')
        except NoSuchVariable:
            hn_tot = hr(path,'np')
        hn_h = hr(path,'np_H')
        hn_ch4 = hr(path,'np_CH4')

        ux = hup.get_timestep(-1)[-1]
        n_tot = hn_tot.get_timestep(-1)[-1]
        n_h = hn_h.get_timestep(-1)[-1]
        n_ch4 = hn_ch4.get_timestep(-1)[-1]

        ux = ux[:,:,:,0]
        para = hup.para

        contours = bs_hi_plot(fig, ax, n_tot, n_h, n_ch4, ux, 401, 2.7e13, para, 'xy', mccomas=True, skip_labeling=True)
        legend_proxies.extend( [plt.Rectangle((0,0),1,1,fc=pc.get_facecolor()[0]) for c in contours for pc in c.collections] )

        traj_plot(fig, ax, 'xy', mccomas=True)

high_with_ax.set_xlim([-20,60])
high_with_ax.set_ylim([-40,40])

high_without_ax.legend(legend_proxies, [r'20\% solar wind slowing', r'70\% solar wind exclusion', r'Heavy ions $> 5 \times 10^{-3} \mathrm{cm^{-3}}$'],
    loc='upper left', bbox_to_anchor=(1,1))
if savename:
    plt.savefig(savename)
else:
    plt.show()
