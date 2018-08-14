import numpy as np
from HybridParticleReader import particle_data
from swap import single_spectrum_by_tag, bin_centers, bin_edges
import matplotlib.pyplot as plt
import argparse

cmd_line_parser = argparse.ArgumentParser()
cmd_line_parser.add_argument('--save', nargs='?', default=False, const='xz_context', 
        help='Set flag to save instead of displaying. Optionally provide a filename (or filepath).')
cmd_line_args = cmd_line_parser.parse_args()
savename = cmd_line_args.save

#para, x, v, mrat, beta, tags = particle_data('/home/nathan/data/2018-Mon-Apr-30/pluto-1/data', [0,1])
para, x, v, mrat, beta, tags = particle_data('/home/nathan/data/2018-Mon-Aug-13/pluto-13/data', range(-7,8))

volume = para['qx'].max() * para['qy'].max() * para['qzrange'].max()
Ni_tot = 1719996
Ni_used = 100000
reduced_volume = float(Ni_used)/float(Ni_tot)*volume

reduction = np.random.choice(len(x), size=Ni_used, replace=False)
v = v[reduction]
mrat = mrat[reduction]
beta = beta[reduction]
tags = tags[reduction]

cmat = np.array([[0,1,0],[1,0,0],[0,0,1]], dtype=np.float64)

spectra = single_spectrum_by_tag(v, mrat, beta, tags, cmat, volume=reduced_volume)

# Remove dummy particles
spectra_arr = np.array([v for k,v in spectra.items() if k != 0])

fig, ax = plt.subplots()

bin_widths = bin_edges[1:] - bin_edges[:-1]
multi_center = np.repeat(bin_centers[np.newaxis,:], len(spectra_arr), axis=0)

ax.hist([bin_centers,bin_centers, bin_centers], bins=bin_edges, weights=[spectra[3.0],spectra[2.0],spectra[1.0]], histtype='barstacked', stacked=True, log=True)
ax.set_xscale('log')

ax.set_title('Simulated Solar Wind\nSynthetic Energy Spectrum')
ax.set_xlabel('Energy/Q (eV/q)')
ax.set_ylabel('SCEM (Hz)')
ax.set_xlim(5e1,5e3)
ax.set_ylim(5e-3,3e4)
ax.annotate('IPUI',
        xy=(650,5e-2),
        size=12,
        bbox=dict(boxstyle='round', fc='w', ec='0.5', alpha=0.9))
ax.annotate('IPUI Energy Cutoff',
        xy=(3500,0.4),
        size=12,
        rotation=90,
        va='center', ha='center',
        bbox=dict(boxstyle='round', fc='w', ec='0.5', alpha=0.9))
ax.annotate('$\mathrm{H}^+$',
        xy=(470,9e3),
        size=12,
        va='center', ha='center',
        bbox=dict(boxstyle='round', fc='w', ec='0.5', alpha=0.9))
ax.annotate('$\mathrm{He}^{++}$',
        xy=(2100,1500),
        size=12,
        va='center', ha='center',
        bbox=dict(boxstyle='round', fc='w', ec='0.5', alpha=0.9))

if savename:
    plt.savefig(savename, bbox_inches='tight')
else:
    plt.show()
