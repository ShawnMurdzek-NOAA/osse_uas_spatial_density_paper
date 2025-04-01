"""
Plot Lower Tropospheric RMSE as a Function of UAS Number

shawn.s.murdzek@noaa.gov
"""

'''
To Do:

- Come up with a way to compute confidence intervals (CIs). Can I use some kind of bivariate 
    bootstrap?
- Change code so I can iterate over each season, variable, and lead time
- Clean up code
'''

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import yaml
import datetime as dt
import pandas as pd
import numpy as np
import copy

import metplus_OSSE_scripts.plotting.metplus_tools as mt


#---------------------------------------------------------------------------------------------------
# Input Parameters
#---------------------------------------------------------------------------------------------------

# YAML file with simulation and plotting info
yml_fname = 'verif_sim_info.yml'

# Valid times
valid_times = [dt.datetime(2022, 4, 29, 21) + dt.timedelta(hours=i) for i in range(159)]

# Number of UAS for each simulation name
n_uas_dict = {'uas_300km':84, 'uas_150km':347, 'uas_100km':772, 'uas_75km':1381, 'uas_35km':6335}

# Output file name
out_fname = '../figs/RMSEvsUAS.png'


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

# Read in simulation and plotting information
with open(yml_fname, 'r') as fptr:
    param = yaml.safe_load(fptr)
input_sims = param['sim_dict_spring']
for key in input_sims.keys():
    input_sims[key]['dir'] = input_sims[key]['dir'].format(typ='GridStat', subtyp='lower_atm_below_sfc_mask')

'''
The following should be moved to a function
'''

file_prefix = 'grid_stat_FV3_TMP_vs_NR_TMP'
fcst_lead = 0
line_type = 'sl1l2'
verbose = True
subset_param = {'FCST_VAR': 'TMP', 'not_VX_MASK':'full'}
plot_stat = 'RMSE'

# Read in data
print('Reading in data...')
verif_df = {}
for key in input_sims.keys():
    fnames = ['%s/%s_%02d0000L_%sV_%s.txt' %
              (input_sims[key]['dir'], file_prefix, fcst_lead, t.strftime('%Y%m%d_%H%M%S'), line_type) for t in
              valid_times]
    verif_df[key] = mt.read_ascii(fnames, verbose=verbose)

# Compute stats for the entire 1000-600 hPa layer for each output time and each simulation
print('Computing stats...')
stats = {}
for key in verif_df.keys():
    stats[key] = []
    for t in np.unique(verif_df[key]['FCST_VALID_BEG'].values):
        subset_param_copy = copy.deepcopy(subset_param)
        subset_param_copy['FCST_VALID_BEG'] = t
        red_df = mt.subset_verif_df(verif_df[key], subset_param_copy)
        stats[key].append(mt.compute_stats_entire_df(red_df, agg=True))
    stats[key] = pd.concat(stats[key])

# Compute percent diffs
n_uas = [0]
pct_diff = [0]
for key in n_uas_dict.keys():
    n_uas.append(n_uas_dict[key])
    pct_diff.append(1e2 * (np.mean(stats[key][plot_stat].values) - 
                           np.mean(stats['ctrl'][plot_stat].values)) /
                           np.mean(stats['ctrl'][plot_stat].values))

# Sort percent diffs
n_uas = np.array(n_uas)
pct_diff = np.array(pct_diff)
sort_idx = np.argsort(n_uas)
n_uas = n_uas[sort_idx]
pct_diff = pct_diff[sort_idx]

'''
'''

# Make plot
print('Making plot...')
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))
ax.plot(n_uas, pct_diff, ls='-', marker='o', lw=2)

ax.grid()
ax.set_xlabel('number of UAS', size=14)
ax.set_ylabel('RMSE % reduction', size=14)

plt.savefig(out_fname)


"""
End lower_troposphere_rmse_vs_uas_number.py
"""
