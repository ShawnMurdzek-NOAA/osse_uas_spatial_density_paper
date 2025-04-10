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
ylabel = {'HPBL': 'PBL height (m)',
          'UGRD_VGRD': '80-m wind (m s$^{-1}$)'}

# Output file
out_fname = '../figs/Other2dDieoff.pdf'


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
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8, 7), sharex=True, sharey='row')
plt.subplots_adjust(left=0.12, bottom=0.2, right=0.97, top=0.9, hspace=0.1, wspace=0.1)
letters = ['a', 'c', 'b', 'd']
for i, (sim_dict, ttl, valid_times) in enumerate(zip([sim_dict_winter, sim_dict_spring], 
                                                     ['winter', 'spring'],
                                                     [valid_times_winter, valid_times_spring])):
    for j, v in enumerate(list(plot_dict.keys())):
        ax = axes[j, i]
        print(f'Making plot for {ttl} {v}')
        input_sims = copy.deepcopy(sim_dict)
        for key in input_sims:
            input_sims[key]['dir'] = input_sims[key]['dir'].format(typ='GridStat', subtyp='additional_2D')
        _ = mp.plot_sfc_dieoff(input_sims, 
                               valid_times,
                               fcst_lead=[0, 1, 2, 3, 6, 12],
                               plot_stat=plot_dict[v]['plot_stat'][0],
                               ax=ax,
                               verbose=False,
                               **plot_dict[v]['kwargs'])

        if (i == 1) and (j == 0):
            ax.legend(ncols=3, fontsize=14, loc=(-1.352, -1.65))
        else:
            ax.get_legend().remove()
        ax.tick_params(axis='both', which='major', labelsize=12)
        if j == 0:
            ax.set_title(ttl, size=16)
            ax.set_xlabel('')
        else:
            ax.set_title('')
        if i == 0:
            ax.set_ylabel(ylabel[v], size=16)
        else:
            ax.set_ylabel('')
        ax.text(0.03, 0.895, f'{letters[2*i+j]})', size=14, weight='bold', transform=ax.transAxes, 
                backgroundcolor='white')

plt.suptitle('RMSEs', size=20)
plt.savefig(out_fname)


"""
End other_dieoff.py
"""
