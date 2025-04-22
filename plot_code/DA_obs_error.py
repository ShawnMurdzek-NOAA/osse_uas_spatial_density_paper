"""
Plot Vertical Profiles of UAS Observation Error Standard Deviations Used in GSI

shawn.s.murdzek@noaa.gov
"""

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt

import pyDA_utils.gsi_fcts as gsi


#---------------------------------------------------------------------------------------------------
# Input Parameters
#---------------------------------------------------------------------------------------------------

errtable_fname = '../data/errtable.rrfs'

# Plotting parameters
param = {'Terr': {'TYP': 136,
                  'xlabel': 'temperature (K)',
                  'scale': 1},
         'RHerr': {'TYP': 136,
                   'xlabel': 'relative humidity (%)',
                   'scale': 10},
         'UVerr': {'TYP': 236,
                   'xlabel': 'wind (m s$^{-1}$)',
                   'scale': 1}}

out_fname = '../figs/DAerrUAS.pdf'


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

# Read in observation error variances used by GSI
errtable = gsi.read_errtable(errtable_fname)

# Create plot
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(3, 6), sharey=True)
plt.subplots_adjust(left=0.23, bottom=0.08, right=0.98, top=0.91, hspace=0.38)
letters = ['a', 'b', 'c']
for ax, err, l in zip(axes, list(param.keys()), letters):
    print(f'Making plot for {err}')
    typ = param[err]['TYP']
    ax.plot(errtable[typ][err] * param[err]['scale'], errtable[typ]['prs'], 'b-', lw=2)
    ax.set_ylim([1000, 100])
    ax.set_xlabel(param[err]['xlabel'], size=12)
    ax.set_ylabel('pressure (hPa)', size=12)
    ax.grid()
    ax.text(0.04, 0.86, f'{l})', size=10, weight='bold', transform=ax.transAxes,
            backgroundcolor='white')

plt.suptitle('UAS DA Observation Error\nStandard Deviations', size=14)
plt.savefig(out_fname)
plt.close()


"""
End DA_obs_error.py
"""
