"""
Plot Lower Tropospheric RMSE as a Function of UAS Number

shawn.s.murdzek@noaa.gov
"""

'''
To Do:

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
import metplus_OSSE_scripts.plotting.metplus_plots as mp


#---------------------------------------------------------------------------------------------------
# Input Parameters
#---------------------------------------------------------------------------------------------------

# YAML file with simulation and plotting info
yml_fname = 'verif_sim_info.yml'

# Valid times
valid_times = {'spring':[dt.datetime(2022, 4, 29, 21) + dt.timedelta(hours=i) for i in range(159)],
               'winter':[dt.datetime(2022, 2, 1, 9) + dt.timedelta(hours=i) for i in range(159)]}

# Initialization times to skip
itime_skip = {'winter':[dt.datetime(2022, 2, 4, 13),
                        dt.datetime(2022, 2, 4, 18),
                        dt.datetime(2022, 2, 4, 19),
                        dt.datetime(2022, 2, 4, 20)],
              'spring':[dt.datetime(2022, 5, 6, 5)]}

# Number of UAS for each simulation name
n_uas_dict = {'spring':{'ctrl':0, 'uas_300km':84, 'uas_150km':347, 'uas_100km':772, 'uas_75km':1381, 'uas_35km':6335},
              'winter':{'ctrl':0, 'uas_150km':347, 'uas_100km':772, 'uas_75km':1381, 'uas_35km':6335}}

# Output file name
out_fname = '../figs/RMSEvsUAS.pdf'


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

# Read in simulation and plotting information
with open(yml_fname, 'r') as fptr:
    param = yaml.safe_load(fptr)

input_sims = {}
for s in ['spring', 'winter']:
    input_sims[s] = param[f'sim_dict_{s}']
    for key in input_sims[s].keys():
        input_sims[s][key]['dir'] = input_sims[s][key]['dir'].format(typ='GridStat', subtyp='lower_atm_below_sfc_mask')

plot_dict = param['rmse_vs_uas']

# Create figure
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(7, 5), sharex=True, sharey='col')
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.98, top=0.95)
letters = ['a', 'b', 'c', 'd', 'e', 'f']
for i, s in enumerate(['winter', 'spring']):
    for j, v in enumerate(plot_dict.keys()):
        for fl, c in zip(plot_dict[v]['fcst_leads'], ['k', 'b', 'r']):
            print(f'\nCreating subplot for {s} {v} f{fl:02d}h')

            # Determine valid times
            valid_tmp = copy.deepcopy(valid_times[s])
            for itime in itime_skip[s]:
                valid_tmp.remove(itime + dt.timedelta(hours=fl))

            # Read in data
            print('Reading in data...')
            verif_df = {}
            for key in input_sims[s].keys():
                fnames = ['%s/%s_%02d0000L_%sV_%s.txt' %
                          (input_sims[s][key]['dir'], 
                           plot_dict[v]['file_prefix'], 
                           fl, 
                           t.strftime('%Y%m%d_%H%M%S'), 
                           plot_dict[v]['line_type']) for t in valid_tmp]
                tmp = mt.read_ascii(fnames, verbose=False)
                verif_df[key] = mt.subset_verif_df(tmp, plot_dict[v]['subset'])

            # Compute stats for the entire 1000-600 hPa layer for each output time and each simulation
            print('Computing stats...')
            stats = {}
            for key in verif_df.keys():
                stats[key] = mt.compute_stats_vert_avg(verif_df[key], vmin=600, vmax=1000,
                                                       line_type=plot_dict[v]['line_type'])
                #for t in np.unique(verif_df[key]['FCST_VALID_BEG'].values):
                #    subset_param_copy = copy.deepcopy(subset_param)
                #    subset_param_copy['FCST_VALID_BEG'] = t
                #    red_df = mt.subset_verif_df(verif_df[key], subset_param_copy)
                #    stats[key].append(mt.compute_stats_entire_df(red_df, agg=True))
                #stats[key] = pd.concat(stats[key])

            # Make plot
            print('Making plot...')
            ax = axes[i, j]
            _ = mp.plot_pct_diffs([stats[key] for key in n_uas_dict[s].keys()], 
                                  [n_uas_dict[s][key] for key in n_uas_dict[s].keys()],
                                  'number of UAS',
                                  plot_stat=plot_dict[v]['plot_stat'],
                                  ax=ax,
                                  ci=True,
                                  ci_lvl=0.95,
                                  ci_opt='bootstrap',
                                  ci_kw={'bootstrap_kw':{'paired':True, 'n_resamples':10000}},
                                  plot_pct_diff_kw={'lw':2, 'c':c, 'label':f'{fl}-hr fcst'},
                                  plot_ci_kw={'lw':0.75, 'c':c})
            if i == 0:
                ax.set_xlabel('')
            ax.set_title(f"{letters[3*i+j]}) {s} {plot_dict[v]['name']}", size=14)

axes[0, 0].legend()
plt.savefig(out_fname)
'''
# Compute percent diffs
n_uas = [0]
pct_diff = [0]
ci = [(0, 0)]
for key in n_uas_dict.keys():
    n_uas.append(n_uas_dict[key])
    pct_diff.append(mt.percent_diff(stats[key][plot_stat].values, stats['ctrl'][plot_stat].values))
    ci.append(mt.confidence_interval_pct_diff(stats[key][plot_stat].values, 
                                              stats['ctrl'][plot_stat].values, 
                                              level=0.95, 
                                              option='bootstrap', 
                                              ci_kw={'bootstrap_kw':{'paired':True, 'n_resamples':10000}}))

# Sort percent diffs
n_uas = np.array(n_uas)
pct_diff = np.array(pct_diff)
sort_idx = np.argsort(n_uas)
n_uas = n_uas[sort_idx]
pct_diff = pct_diff[sort_idx]
ci_sorted = []
for i in sort_idx:
    ci_sorted.append(ci[i])

# Make plot
print('Making plot...')
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))
ax.plot(n_uas, pct_diff, ls='-', lw=2)
for i, n in enumerate(n_uas):
    ax.plot([n, n], ci[i], linestyle='-', marker='_', lw=0.5)

ax.grid()
ax.set_xlabel('number of UAS', size=14)
ax.set_ylabel('RMSE % reduction', size=14)

plt.savefig(out_fname)
'''

"""
End lower_troposphere_rmse_vs_uas_number.py
"""
