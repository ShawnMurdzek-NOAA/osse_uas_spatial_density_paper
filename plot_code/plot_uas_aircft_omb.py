"""
Plot O-B Values for Commercial Aircraft and UAS

Used to create figure 17

shawn.s.murdzek@noaa.gov
"""

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import xarray as xr

import pyDA_utils.gsi_fcts as gsi


#---------------------------------------------------------------------------------------------------
# Parameters
#---------------------------------------------------------------------------------------------------

# Input file names
in_fnames = {}
for a in ['0.95', '0.985']:
    in_fnames[a] = {}
    for ob in ['uas', 'aircft']:
        in_fnames[a][ob] = f"../data/OMB/omb_t_{ob}_A{a}.nc"

# Output file
out_fname = '../figs/ombUASaircft.pdf'


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

fig, axes = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True, figsize=(6.5, 3.5))
plt.subplots_adjust(left=0.09, bottom=0.31, right=0.98, top=0.91, wspace=0.05)
bins = np.arange(-8, 8.1, 0.25)

for i, (key, ttl) in enumerate(zip(in_fnames, ['a) uas_35km_A0.95', 'b) uas_35km_A0.985'])):

    # Read in OmB
    omb_uas = xr.open_dataset(in_fnames[key]['uas'])
    omb_aircft = xr.open_dataset(in_fnames[key]['aircft'])

    # Plot histogram
    ax = axes[i]
    ax.hist(omb_uas['omb'], bins=bins, color='r', label=f"UAS (stdev = {np.std(omb_uas['omb']):.3f})", density=True, alpha=0.6)
    ax.hist(omb_aircft['omb'], bins=bins, color='b', label=f"aircraft (stdev = {np.std(omb_aircft['omb']):.3f})", density=True, alpha=0.6)

    ax.grid()
    ax.set_xlabel('O$-$B (K)', size=12)
    if i == 0:
        ax.set_ylabel('density', size=12)
    ax.set_title(ttl, size=14)
    ax.legend(fontsize=12, loc=(0.05, -0.48))
    ax.set_xlim([bins[0], bins[-1]])

plt.savefig(out_fname)
plt.close()


"""
End plot_uas_aircft_omb.py
"""
