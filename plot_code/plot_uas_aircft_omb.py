"""
Plot O-B Values for Commercial Aircraft and UAS

shawn.s.murdzek@noaa.gov
"""

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

import pyDA_utils.gsi_fcts as gsi


#---------------------------------------------------------------------------------------------------
# Parameters
#---------------------------------------------------------------------------------------------------

# Input file names
parent1 = '/work/noaa/wrfruc/murdzek/RRFS_OSSE/syn_data_rrfs-workflow_orion/spring_uas_35km_autocorr0.95/NCO_dirs/ptmp/prod'
parent2 = '/work/noaa/wrfruc/murdzek/RRFS_OSSE/syn_data_rrfs-workflow_orion/spring_uas_35km_autocorr0.985/NCO_dirs/ptmp/prod'
times = [dt.datetime(2022, 4, 29, 21) + dt.timedelta(hours=t) for t in range(159)]
#times = [dt.datetime(2022, 5, 1, 0)]
in_fnames = {"a) uas_35km_A0.95" : [f"{parent1}/rrfs.{t.strftime('%Y%m%d/%H/diag_conv_t_ges.%Y%m%d%H.nc4')}" for t in times],
             "b) uas_35km_A0.985" : [f"{parent2}/rrfs.{t.strftime('%Y%m%d/%H/diag_conv_t_ges.%Y%m%d%H.nc4')}" for t in times]}

# Pressure bounds (hPa)
pmin = 700
pmax = 1050

# Output file
out_fname = '../figs/ombUASaircft.pdf'


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

omb_uas = {}
omb_aircft = {}

fig, axes = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True, figsize=(6.5, 3.5))
plt.subplots_adjust(left=0.09, bottom=0.31, right=0.98, top=0.91, wspace=0.05)
bins = np.arange(-8, 8.1, 0.25)

for i, key in enumerate(in_fnames):

    # Read in GSI diag files
    diag_full = gsi.read_diag(in_fnames[key], ftype='netcdf')
    diag = diag_full.loc[np.logical_and(diag_full['Pressure'] >= pmin, diag_full['Pressure'] <= pmax), :]
    omb_uas[key] = diag.loc[diag['Observation_Type'] == 136, 'Obs_Minus_Forecast_adjusted'].values
    omb_aircft[key] = diag.loc[(diag['Observation_Type'] == 130) |
                               (diag['Observation_Type'] == 131) |
                               (diag['Observation_Type'] == 133) |
                               (diag['Observation_Type'] == 134) |
                               (diag['Observation_Type'] == 135), 'Obs_Minus_Forecast_adjusted'].values

    # Plot histogram
    ax = axes[i]
    ax.hist(omb_uas[key], bins=bins, color='r', label=f"UAS (stdev = {np.std(omb_uas[key]):.3f})", density=True, alpha=0.6)
    ax.hist(omb_aircft[key], bins=bins, color='b', label=f"aircraft (stdev = {np.std(omb_aircft[key]):.3f})", density=True, alpha=0.6)

    ax.grid()
    ax.set_xlabel('O$-$B (K)', size=12)
    if i == 0:
        ax.set_ylabel('density', size=12)
    ax.set_title(key, size=14)
    ax.legend(fontsize=12, loc=(0.05, -0.48))
    ax.set_xlim([bins[0], bins[-1]])

plt.savefig(out_fname)
plt.close()


"""
End plot_uas_aircft_omb.py
"""
