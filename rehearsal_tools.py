import numpy as np
import cPickle
import spice_tools
from swap import find_fit_file, bin_centers

# New Horizons Data
data = find_fit_file(spice_tools.rehearsal_start)
_t = data['time_label_spect'].data

raw_scem = data['scem_spect_hz'].data
times = [spice_tools.et2pydatetime(tt) for tt in _t['middle_et']]
positions = [spice_tools.pos_at_time(tt, mccomas=True)/1187. for tt in _t['middle_et']]
energies = data['energy_label_spect'].data[0][2:]

_sample_duration = (_t['stop_et'] - _t['start_et'])/len(energies)
assert np.allclose(_sample_duration, _sample_duration[0])
sample_duration = _sample_duration[0]

# SCEM counts with bins that have less than 3 counts per sample zeroed
hz_threshold = 3.0/sample_duration
scem = np.where(raw_scem > hz_threshold, raw_scem, 0.)


# Simulation
with open('rehearsal_espec.pickle') as f:
    espec = cPickle.load(f)

sim_scem = (espec['H']+espec['He']).T
sim_times = [spice_tools.et2pydatetime(tt) for tt in espec['times']]
sim_positions = espec['trajectory']
sim_energies = bin_centers
