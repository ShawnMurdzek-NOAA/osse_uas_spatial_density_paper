"""
Plot Lower Tropospheric RMSE as a Function of UAS Number

shawn.s.murdzek@noaa.gov
"""

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
#out_fname = '../figs/RMSEvsUAS.png'


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

# Read in simulation and plotting information
with open(yml_fname, 'r') as fptr:
    param = yaml.safe_load(fptr)

plot_dict = param['rmse_vs_uas']

# Create figure
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(7, 5), sharex=True, sharey=True)
plt.subplots_adjust(left=0.1, bottom=0.17, right=0.98, top=0.94, hspace=0.22, wspace=0.1)
letters = ['a', 'b', 'c', 'd', 'e', 'f']
labelsize=14
for i, s in enumerate(['winter', 'spring']):
    for j, v in enumerate(plot_dict.keys()):

        input_sims = copy.deepcopy(param[f'sim_dict_{s}'])
        for key in input_sims:
            input_sims[key]['dir'] = input_sims[key]['dir'].format(typ='GridStat', subtyp='lower_atm_below_sfc_mask')

        for fl, c in zip(plot_dict[v]['fcst_leads'], ['k', 'b', 'r', 'darkgreen']):
            print(f'\nCreating subplot for {s} {v} f{fl:02d}h')

            # Determine valid times
            valid_tmp = copy.deepcopy(valid_times[s])
            for itime in itime_skip[s]:
                try:
                    valid_tmp.remove(itime + dt.timedelta(hours=fl))
                except ValueError:
                    print(f"Cannot remove {itime}")

            # Read in data
            print('Reading in data...')
            verif_df = {}
            for key in input_sims.keys():
                fnames = ['%s/%s_%02d0000L_%sV_%s.txt' %
                          (input_sims[key]['dir'], 
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
                                                       line_type=plot_dict[v]['line_type'],
                                                       stats_kw={'agg':True})

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
                                  ci_opt='t_dist',
                                  ci_kw={'acct_lag_corr':True, 'mats_ste':False},
                                  plot_pct_diff_kw={'lw':1.5, 'c':c, 'label':f'{fl}-hr fcst'},
                                  plot_ci_kw={'lw':0.75, 'c':c})
            if i == 0:
                ax.set_xlabel('')
            if j > 0:
                ax.set_ylabel('')
            ax.set_title(f"{letters[3*i+j]}) {s} {plot_dict[v]['name']}", size=labelsize)
            ax.grid(True, color='gray', linewidth=0.5)

axes[0, 0].legend(ncols=4, loc=(0.25, -1.68))
if out_fname[-3:] == 'pdf':
    plt.savefig(out_fname)
else:
    plt.savefig(out_fname, dpi=700)


"""
End lower_troposphere_rmse_vs_uas_number.py
"""
