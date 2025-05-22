"""
Dieoff Plots for Severe Weather Parameter Verification

Show plots of percent reductions in RMSEs

shawn.s.murdzek@noaa.gov
"""

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

import yaml
import copy
import datetime as dt
import matplotlib.pyplot as plt

import metplus_OSSE_scripts.plotting.metplus_plots as mp


#---------------------------------------------------------------------------------------------------
# Input Parameters
#---------------------------------------------------------------------------------------------------

# YAML file with simulation and plotting info
yml_fname = 'verif_sim_info.yml'

# Valid times
valid_times = [dt.datetime(2022, 4, 29, 21) + dt.timedelta(hours=i) for i in range(159)]

# Y-axis label
ylabel = {'MLCAPE': 'MLCAPE % diff',
          'MLCIN': 'MLCIN % diff',
          'SRH03': '0$-$3 km SRH % diff'}

# Output file
out_fname = '../figs/SevereWxDieoffPct.pdf'


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

# Read in simulation and plotting information
with open(yml_fname, 'r') as fptr:
    param = yaml.safe_load(fptr)
sim_dict = {}
sim_dict['ctrl'] = param['sim_dict_spring']['ctrl']
exp_name = []
for key in param['sim_dict_spring'].keys():
    if key[:3] == 'uas':
        sim_dict[f'{key} $-$ ctrl'] = param['sim_dict_spring'][key]
        exp_name.append(key)
plot_dict = param['severe_wx_spring']['severe_wx_env']

# Make plot
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(6, 6), sharex=True)
plt.subplots_adjust(left=0.12, bottom=0.29, right=0.99, top=0.93, hspace=0.08, wspace=0.35)
letters = ['a', 'b', 'c', 'd']
fcst_lead = [0, 1, 2, 3, 6, 12]
for i, (v, c, ls) in enumerate(zip(list(plot_dict.keys()),
                                   ['k', 'gray', 'saddlebrown'],
                                   ['-', '-.', ':'])):
    print(f'Making plot for {v}')
    input_sims = copy.deepcopy(sim_dict)
    for key in input_sims:
        input_sims[key]['dir'] = input_sims[key]['dir'].format(typ='GridStat', subtyp='severe_wx_env')

    # Control run
    ctrl_sim = {}
    if v == 'SRH03':
        name = "ctrl 0$-$3 km SRH"
    else:
        name = f"ctrl {v}"
    ctrl_sim[name] = input_sims['ctrl']
    ctrl_sim[name]['color'] = c
    ctrl_sim[name]['ls'] = ls
    _ = mp.plot_sfc_dieoff(ctrl_sim, 
                           valid_times,
                           fcst_lead=fcst_lead,
                           plot_stat=plot_dict[v]['plot_stat'][0],
                           ax=axes[0, 0],
                           verbose=False,
                           **plot_dict[v]['kwargs'])

    # Percent differences
    _ = mp.plot_sfc_dieoff(input_sims, 
                           valid_times,
                           fcst_lead=[0, 1, 2, 3, 6, 12],
                           plot_stat=plot_dict[v]['plot_stat'][0],
                           ax=axes[int((i+1) / 2), (i+1) % 2],
                           verbose=False,
                           diffs=False,
                           pct_diffs=True,
                           include_ctrl=False,
                           include_zero=True,
                           **plot_dict[v]['kwargs'])

# Formatting
for i in range(4):
    ax = axes[int(i/2), i%2]

    # Subplot labels
    ax.set_title('')
    ax.text(0.04, 0.885, f'{letters[i]})', size=12, weight='bold', transform=ax.transAxes,
            backgroundcolor='white')

    # Legend
    if i == 0:
        ax.legend(ncols=3, fontsize=12, loc=(-0.1, -1.5))
    elif i == 1:
        ax.legend(ncols=2, fontsize=12, loc=(-1.15, -2))
    else:
        ax.get_legend().remove()

    # X label
    if i > 1:
        ax.set_xlabel('lead time (hr)', size=12)
    else:
        ax.set_xlabel('')

    # Y label
    if i == 0:
        ax.set_ylabel('J kg$^{-1}$', size=12)
    else:
        ax.set_ylabel(ylabel[list(plot_dict.keys())[i-1]], size=12)

    # Axes limits
    if i > 0:
        ax.set_ylim([-48, 11])

plt.suptitle('RMSE % diffs for gridpoints with MUCAPE > 50 J kg$^{-1}$', size=16)
plt.savefig(out_fname)


"""
End severe_wx_parameter_dieoff.py
"""
