"""
Vertical Profiles for Verification of the Full Troposphere

shawn.s.murdzek@noaa.gov
"""

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

import yaml
import copy
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

import metplus_OSSE_scripts.plotting.metplus_plots as mp


#---------------------------------------------------------------------------------------------------
# Input Parameters
#---------------------------------------------------------------------------------------------------

# YAML file with simulation and plotting info
yml_fname = 'verif_sim_info.yml'

# Valid times
valid_times_spring = [dt.datetime(2022, 4, 29, 21) + dt.timedelta(hours=i) for i in range(159)]
valid_times_winter = [dt.datetime(2022, 2, 1, 9) + dt.timedelta(hours=i) for i in range(159)]

# X-axis labels
xlabel = {'TMP': 'T diff (K)',
          'SPFH': 'Q diff (g kg$^{-1}$)',
          'UGRD_VGRD': 'winds diff (m s$^{-1}$)'}

# X-axis limits
xlim = {'TMP': [-0.7, 0.02],
        'SPFH': [-7e-4, 2e-5],
        'UGRD_VGRD': [-2.2, 0.1]}

# Simulations to plot
sims = ['uas_150km', 'uas_35km']

# Forecast hour
fhr = 0

# Output file (include {stat} and {fhr} placeholders)
out_fname = '../figs/FullTropRMSE.pdf'


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

# Read in simulation and plotting information
with open(yml_fname, 'r') as fptr:
    param = yaml.safe_load(fptr)

sim_dict_spring = {}
sim_dict_spring['ctrl'] = param['sim_dict_spring']['ctrl']
for key in sims:
    sim_dict_spring[f'spring {key} $-$ ctrl'] = param['sim_dict_spring'][key]

sim_dict_winter = {}
sim_dict_winter['ctrl'] = param['sim_dict_winter']['ctrl']
for key in sims:
    sim_dict_winter[f'winter {key} $-$ ctrl'] = param['sim_dict_winter'][key]

# Set line style for each season
for key in sim_dict_spring:
    sim_dict_spring[key]['ls'] = '--'
for key in sim_dict_winter:
    sim_dict_winter[key]['ls'] = '-'

plot_dict = param['full_atm']

# Make plots
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(6.5, 4), sharey=True)
plt.subplots_adjust(left=0.11, bottom=0.28, right=0.98, top=0.92, wspace=0.1)
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
for i, (sim_dict, ttl, valid_times) in enumerate(zip([sim_dict_winter, sim_dict_spring],
                                                     ['winter', 'spring'],
                                                     [valid_times_winter, valid_times_spring])):
    for j, (v, stat) in enumerate(zip(list(plot_dict.keys()), ['RMSE', 'RMSE', 'VECT_RMSE'])):
        print(f'{ttl} {v}')
        input_sims = copy.deepcopy(sim_dict)
        for key in input_sims:
            input_sims[key]['dir'] = input_sims[key]['dir'].format(typ='GridStat', subtyp='upper_air_below_sfc_mask')

        # Difference plot
        _ = mp.plot_ua_vprof(input_sims,
                             valid_times,
                             fcst_lead=fhr,
                             plot_stat=stat,
                             ax=axes[j],
                             verbose=False,
                             diffs=True,
                             include_zero=True,
                             **plot_dict[v]['kwargs'])

# Formatting
for i, v in enumerate(list(plot_dict.keys())):
    ax = axes[i]
    ax.grid(True)

    # Subplot label
    ax.set_title('')
    ax.text(0.04, 0.92, f'{letters[i]})', size=12, weight='bold', transform=ax.transAxes,
            backgroundcolor='white')

    # Legend
    if (i == 0):
        ax.legend(ncol=2, fontsize=10, loc=(0.3, -0.4))
    else:
        ax.get_legend().remove()

    # X label
    ax.set_xlabel(xlabel[v], size=12)

    # Y label
    if (i == 0):
        ax.set_ylabel(f"pressure (hPa)", size=12)
    else:
        ax.set_ylabel('')

    # Ticks
    ax.set_xlim(xlim[v])
    ax.set_ylim([1000, 90])
    ax.set_yticks(ticks=[1000, 700, 500, 300, 200, 100], 
                  labels=['1000', '700', '500', '300', '200', '100'],
                  minor=False)
    ax.tick_params(which='both', labelsize=10)

    # Specific humidity ticks
    if i == 1:
        formatter = mticker.FuncFormatter(lambda x, pos: f"{x*1e3:.2f}")
        ax.xaxis.set_major_formatter(formatter)

plt.suptitle(f"{fhr}-hr RMSE", size=16)
plt.savefig(out_fname)
plt.close()


"""
End full_troposphere_verif_vprof.py
"""
