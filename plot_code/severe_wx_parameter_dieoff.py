"""
Dieoff Plots for Severe Weather Parameter Verification

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
ylabel = {'MLCAPE': 'MLCAPE (J kg$^{-1}$)',
          'MLCIN': 'MLCIN (J kg$^{-1}$)',
          'SRH03': '0$-$3 km SRH (m$^{2}$ s$^{-2}$)'}

# Output file
out_fname = '../figs/SevereWxDieoff.pdf'


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

# Read in simulation and plotting information
with open(yml_fname, 'r') as fptr:
    param = yaml.safe_load(fptr)
sim_dict = {}
sim_dict['ctrl'] = param['sim_dict_spring']['ctrl']
for key in param['sim_dict_spring'].keys():
    if key[:3] == 'uas':
        sim_dict[f'{key} $-$ ctrl'] = param['sim_dict_spring'][key]
plot_dict = param['severe_wx_spring']['severe_wx_env']

# Make plot
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(6, 10), sharex=True)
plt.subplots_adjust(left=0.14, bottom=0.07, right=0.98, top=0.95, hspace=0.08)
letters = ['a', 'b', 'c']
for i, ax in enumerate(axes):
    v = list(plot_dict.keys())[i]
    print(f'Making plot for {v}')
    input_sims = copy.deepcopy(sim_dict)
    for key in input_sims:
        input_sims[key]['dir'] = input_sims[key]['dir'].format(typ='GridStat', subtyp='severe_wx_env')
    _ = mp.plot_sfc_dieoff(input_sims, 
                           valid_times,
                           fcst_lead=[0, 1, 2, 3, 6, 12],
                           plot_stat=plot_dict[v]['plot_stat'][0],
                           ax=ax,
                           verbose=False,
                           **plot_dict[v]['kwargs'])

    if i == 0:
        ax.legend(ncols=2, fontsize=12)
    else:
        ax.get_legend().remove()
    ax.tick_params(axis='both', which='major', labelsize=11)
    ax.set_title('')
    ax.set_ylabel(ylabel[v], size=14)
    if i != 2:
        ax.set_xlabel('')
    ax.text(0.02, 0.92, f'{letters[i]})', size=14, weight='bold', transform=ax.transAxes, 
            backgroundcolor='white')

plt.suptitle('RMSEs for gridpoints with MUCAPE > 50 J kg$^{-1}$', size=17)
plt.savefig(out_fname)


"""
End severe_wx_parameter_dieoff.py
"""
