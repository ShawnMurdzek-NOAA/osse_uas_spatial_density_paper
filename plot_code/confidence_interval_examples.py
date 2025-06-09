"""
Comparing Different Methods for Computing Confidence Intervals

shawn.s.murdzek@noaa.gov
"""

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

import yaml
import copy
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

import metplus_OSSE_scripts.plotting.metplus_plots as mp
import metplus_OSSE_scripts.plotting.metplus_tools as mt


#---------------------------------------------------------------------------------------------------
# Input Parameters
#---------------------------------------------------------------------------------------------------

# YAML file with simulation and plotting info
yml_fname = 'verif_sim_info.yml'

# Valid times
valid_times = [dt.datetime(2022, 4, 29, 21) + dt.timedelta(hours=i) for i in range(159)]

# Forecat lead time
fcst_lead = 6

# Output file
out_fname = f'../figs/example_CIs_wspd80_f{fcst_lead}.png'


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

# Adjust valid times based on fcst_lead
valid_times = valid_times[fcst_lead:]

# Read in simulation and plotting information
with open(yml_fname, 'r') as fptr:
    param = yaml.safe_load(fptr)

# Only read in two simulations for simplicity
sim_dict = {}
sim_dict['ctrl'] = param['sim_dict_spring']['ctrl']
sim_dict['uas_150km'] = param['sim_dict_spring']['uas_150km']
for key in sim_dict.keys():
    sim_dict[key]['dir'] = sim_dict[key]['dir'].format(subtyp='additional_2D', typ='GridStat')

plot_dict = param['other_2d_dieoff']['additional_2D']['UGRD_VGRD']['kwargs']

# Configure figure
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(12, 12))
plt.subplots_adjust(left=0.17, bottom=0.05, right=0.98, top=0.9, hspace=0.4, wspace=0.47)

# Time series of RMSEs at the analysis time
ax = axes[0, 0]
verif_df = mp.plot_sfc_timeseries(sim_dict,
                                  valid_times,
                                  fcst_lead=fcst_lead,
                                  diffs=False,
                                  plot_stat='VECT_RMSE',
                                  ax=ax,
                                  file_prefix=plot_dict['file_prefix'],
                                  line_type=plot_dict['line_type'],
                                  plot_param=plot_dict['plot_param'],
                                  diff_kw=plot_dict['diff_kw'],
                                  toggle_pts=False,
                                  verbose=True)
diff_sim_dict = copy.deepcopy(sim_dict)
diff_sim_dict['uas_150km']['color'] = 'b'
diff_df = mp.plot_sfc_timeseries(diff_sim_dict,
                                 valid_times,
                                 fcst_lead=fcst_lead,
                                 diffs=True,
                                 plot_stat='VECT_RMSE',
                                 ax=ax,
                                 file_prefix=plot_dict['file_prefix'],
                                 line_type=plot_dict['line_type'],
                                 plot_param=plot_dict['plot_param'],
                                 diff_kw=plot_dict['diff_kw'],
                                 toggle_pts=False,
                                 include_zero=True)
ax.grid()

# Subset diff_df and extract differences
diff = mt.subset_verif_df(diff_df[0]['uas_150km'], plot_dict['plot_param'])['VECT_RMSE'].values
ctrl_rmse = mt.subset_verif_df(verif_df[0]['ctrl'], plot_dict['plot_param'])['VECT_RMSE'].values
uas_rmse = mt.subset_verif_df(verif_df[0]['uas_150km'], plot_dict['plot_param'])['VECT_RMSE'].values

# Histogram of differences
ax = axes[0, 1]
ax.hist(diff, bins=15)
ax.axvline(0, ls='--', c='k')
ax.grid()
ax.set_xlabel('difference', size=14)
ax.set_ylabel('counts', size=14)

# Plot various confidence intervals
# Note that all tests are paired b/c we are using differences
ax = axes[1, 0]
level = 0.95
ci_param = {'t standard': {'option': 't_dist'},
            't autocorr': {'option': 't_dist',
                           'ci_kw': {'acct_lag_corr':True,
                                     'mats_ste':False}},
            't autocorr (MATS)': {'option': 't_dist',
                                  'ci_kw': {'acct_lag_corr':True,
                                            'mats_ste':True}},
            'bootstrap paired': {'option': 'bootstrap',
                                 'ci_kw': {'bootstrap_kw': {'n_resamples':10000}}}}
for i, key in enumerate(list(ci_param.keys())):
    ci = mt.confidence_interval_mean(diff, level=level, **ci_param[key])
    ax.plot(ci, [i, i], lw=5)
    #print(f"{key} = {ci[0]}, {ci[1]}")
ax.set_xlabel('difference', size=14)
ax.set_yticks(np.arange(len(ci_param)), list(ci_param.keys()), size=14)
autocorr = np.around(np.corrcoef(diff[1:], diff[:-1])[0, -1], decimals=5)
ax.set_title(f"Diff Confidence Intervals\nAutocorr = {autocorr}", size=16)
ax.grid()

# Create fake % diff confidence intervals by dividing the diff CIs by the ctrl mean RMSE
ax = axes[1, 1]
print('\nFake Pct Diff')
for i, key in enumerate(list(ci_param.keys())):
    ci = mt.confidence_interval_mean(diff, level=level, **ci_param[key])
    ci = [100 * ci[0] / np.mean(ctrl_rmse), 100 * ci[1] / np.mean(ctrl_rmse)]
    ax.plot(ci, [i, i], lw=5)
    print(f'CI range ({key}) = {np.abs(ci[1] - ci[0])}')
ax.set_xlabel('pct difference', size=14)
#ax.set_xlim([-13.5, -8])
ax.set_yticks(np.arange(len(ci_param)), list(ci_param.keys()), size=14)
ax.set_title(f"100 * Diff CI / Avg Ctrl RMSE", size=16)
ax.grid()

# Compute percent differences two different ways
def pct_diff_1(exp, ctrl):
    return 1e2 * (np.mean(exp) - np.mean(ctrl)) / np.mean(ctrl)

def pct_diff_2(exp, ctrl):
    return 1e2 * np.mean((exp - ctrl) / ctrl)

print(f"\npct_diff_1 = {pct_diff_1(uas_rmse, ctrl_rmse)}")
print(f"pct_diff_2 = {pct_diff_2(uas_rmse, ctrl_rmse)}\n")

# Plot % diff 1 confidence intervals
ax = axes[2, 0]
ci_bs_param = {'bootstrap': {'n_resamples': 10000},
               'bootstrap paired': {'n_resamples': 10000,
                                    'paired': True}}
print('\nPct Diff 1')
for i, key in enumerate(list(ci_bs_param.keys())):
    ci = mt.confidence_interval_bootstrap_pct_diff(uas_rmse, ctrl_rmse, level=level, fct=pct_diff_1, 
                                                   bootstrap_kw=ci_bs_param[key])
    ax.plot(ci, [i, i], lw=5)
    print(f'CI range ({key}) = {np.abs(ci[1] - ci[0])}')
ax.set_xlabel('pct difference', size=14)
#ax.set_xlim([-13.5, -8])
ax.set_yticks(np.arange(len(ci_bs_param)), list(ci_bs_param.keys()), size=14)
ax.set_title(f"Pct Diff 1 CIs", size=16)
ax.grid()

# Plot % diff 2 confidence intervals
ax = axes[2, 1]
pct_diff_raw = 1e2 * (uas_rmse - ctrl_rmse) / ctrl_rmse
print('\nPct Diff 2')
for i, key in enumerate(list(ci_param.keys())):
    ci = mt.confidence_interval_mean(pct_diff_raw, level=level, **ci_param[key])
    ax.plot(ci, [i, i], lw=5)
    print(f'CI range ({key}) = {np.abs(ci[1] - ci[0])}')
ax.set_xlabel('pct difference', size=14)
#ax.set_xlim([-13.5, -8])
ax.set_yticks(np.arange(len(ci_param)), list(ci_param.keys()), size=14)
ax.set_title(f"Pct Diff 2 CIs", size=16)
ax.grid()

plt.savefig(out_fname)
plt.close()


"""
confidence_interval_examples.py
"""
