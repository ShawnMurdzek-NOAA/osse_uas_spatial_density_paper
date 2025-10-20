"""
Dieoff Plots for Verification of Other 2D Fields

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
valid_times_spring = [dt.datetime(2022, 4, 29, 21) + dt.timedelta(hours=i) for i in range(159)]
valid_times_winter = [dt.datetime(2022, 2, 1, 9) + dt.timedelta(hours=i) for i in range(159)]

# Y-axis label
ylabel_ctrl = {'UGRD_VGRD': 'm s$^{-1}$'}
ylabel_diff = {'UGRD_VGRD': '% diff'}

# Output file
out_fname = '../figs/Wind80m2dDieoffPct.pdf'


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

# Read in simulation and plotting information
with open(yml_fname, 'r') as fptr:
    param = yaml.safe_load(fptr)

sim_dict_spring = {}
sim_dict_spring['ctrl'] = param['sim_dict_spring']['ctrl']
for key in param['sim_dict_spring'].keys():
    if key[:3] == 'uas':
        sim_dict_spring[f'{key} $-$ ctrl'] = param['sim_dict_spring'][key]

sim_dict_winter = {}
sim_dict_winter['ctrl'] = param['sim_dict_winter']['ctrl']
for key in param['sim_dict_winter'].keys():
    if key[:3] == 'uas':
        sim_dict_winter[f'{key} $-$ ctrl'] = param['sim_dict_winter'][key]

plot_dict = param['other_2d_dieoff']['additional_2D']

# Make plot
ncols = len(plot_dict.keys())
fig, axes = plt.subplots(nrows=3, ncols=ncols, figsize=(3, 7), sharex=True)
plt.subplots_adjust(left=0.29, bottom=0.32, right=0.98, top=0.95, hspace=0.1, wspace=0.1)
letters = ['a', 'b', 'c', 'd', 'e', 'f']
for i , v in enumerate(list(plot_dict.keys())):
    for j, (sim_dict, ttl, valid_times, c, ls) in enumerate(zip([sim_dict_winter, sim_dict_spring], 
                                                                ['winter', 'spring'],
                                                                [valid_times_winter, valid_times_spring],
                                                                ['k', 'gray'],
                                                                ['-', '-.'])):
        print(f'Making plot for {ttl} {v}')
        input_sims = copy.deepcopy(sim_dict)
        for key in input_sims:
            input_sims[key]['dir'] = input_sims[key]['dir'].format(typ='GridStat', subtyp='additional_2D')

        # Control run
        ctrl_sim = {}
        ctrl_sim[f"{ttl} ctrl"] = input_sims['ctrl']
        ctrl_sim[f"{ttl} ctrl"]['color'] = c
        ctrl_sim[f"{ttl} ctrl"]['ls'] = ls
        _ = mp.plot_sfc_dieoff(ctrl_sim, 
                               valid_times,
                               fcst_lead=[0, 1, 2, 3, 6, 12],
                               plot_stat=plot_dict[v]['plot_stat'][0],
                               ax=axes[0],
                               verbose=False,
                               diffs=False,
                               **plot_dict[v]['kwargs'])

        # Percent difference plot
        _ = mp.plot_sfc_dieoff(input_sims, 
                               valid_times,
                               fcst_lead=[0, 1, 2, 3, 6, 12],
                               plot_stat=plot_dict[v]['plot_stat'][0],
                               ax=axes[j+1],
                               verbose=False,
                               diffs=True,
                               include_ctrl=False,
                               include_zero=True,
                               **plot_dict[v]['kwargs'])

# Formatting
for i, v in enumerate(list(plot_dict.keys())):
    for j in range(3):
        ax = axes[j]

        # Subplot labels
        ax.set_title('')
        ax.text(0.865, 0.08, f'{letters[3*i+j]})', size=12, weight='bold', transform=ax.transAxes,
                backgroundcolor='white')

        # Legend
        if (i == 0) and (j == 0):
            ax.legend(ncols=1, fontsize=10, loc=(0.18, -2.89))
        elif (i == 0) and (j == 2):
            ax.legend(ncols=1, fontsize=10, loc=(0.06, -1.55))
        else:
            ax.get_legend().remove()

        # X label
        if j == 2:
            ax.set_xlabel('lead time (hr)', size=12)
        else:
            ax.set_xlabel('')

        # Y label
        if j == 0:
            ax.set_ylabel(ylabel_ctrl[v], size=12)
        elif j == 1:
            ax.set_ylabel(f"winter\n{ylabel_diff[v]}", size=12)
        elif j == 2:
            ax.set_ylabel(f"spring\n{ylabel_diff[v]}", size=12)

        # Ticks
        #if j == 2:
        #    ax.set_yticks(ticks=[0, -0.2, -0.4, -0.6, -0.8, -1])
        if j > 0:
            ax.set_ylim([-33, 3])
        ax.tick_params(axis='both', which='major', labelsize=10)
        if j == 0:
            ax.grid()

axes[0].set_title('80-m Winds RMSEs', size=14)
plt.savefig(out_fname)
plt.close()


"""
End other_dieoff.py
"""
