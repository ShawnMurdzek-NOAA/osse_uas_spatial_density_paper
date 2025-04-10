"""
Vertical Profiles for Verification of the Lower Atmosphere

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

# X-axis labels
xlabel = {'TMP': 'temperature (K)',
          'RH': 'relative humidity (%)',
          'UGRD_VGRD': 'winds (m s$^{-1}$)'}

# X-axis tick locations
xticks = {'RMSE': {0: {'TMP': [-0.5, 0, 0.5, 1],
                       'RH': [-5, 0, 5, 10, 15],
                       'UGRD_VGRD': [-2, -1, 0, 1, 2, 3]},
                   6: {'TMP': [-0.5, 0, 0.5, 1, 1.5, 2],
                       'RH': [-5, 0, 5, 10, 15, 20, 25],
                       'UGRD_VGRD': [-1, 0, 1, 2, 3, 4]}},
          'bias': {0: {'TMP': [-0.2, -0.1, 0, 0.1, 0.2],
                       'RH': [-2, -1, 0, 1, 2, 3],
                       'UGRD_VGRD': [-0.2, -0.1, 0, 0.1, 0.2]},
                   6: {'TMP': [-0.2, 0, 0.2, 0.4, 0.6],
                       'RH': [-2, 0, 2, 4, 6, 8],
                       'UGRD_VGRD': [-0.6, -0.4, -0.2, 0, 0.2]}}}

# Output file (include {stat} and {fhr} placeholders)
out_fname = '../figs/Vprof{stat}{fhr}.pdf'


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

plot_dict = param['lower_atm']

# Make plots
for istat, stat in enumerate(['RMSE', 'bias']):
    for fhr in [0, 6]:
        print(f'\nMaking plot for {stat} f{fhr:02d}h')
        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(6.5, 6), sharex='col', sharey=True)
        plt.subplots_adjust(left=0.15, bottom=0.18, right=0.97, top=0.92, hspace=0.1, wspace=0.1)
        letters = ['a', 'b', 'c', 'd', 'e', 'f']
        for i, (sim_dict, ttl, valid_times) in enumerate(zip([sim_dict_winter, sim_dict_spring],
                                                             ['winter', 'spring'],
                                                             [valid_times_winter, valid_times_spring])):
            for j, v in enumerate(list(plot_dict.keys())):
                ax = axes[i, j]
                print(f'{ttl} {v}')
                input_sims = copy.deepcopy(sim_dict)
                for key in input_sims:
                    if v == 'RH':
                        input_sims[key]['dir'] = input_sims[key]['dir'].format(typ='GridStat', subtyp='RHobT')
                    else:
                        input_sims[key]['dir'] = input_sims[key]['dir'].format(typ='GridStat', subtyp='lower_atm_below_sfc_mask')
                _ = mp.plot_ua_vprof(input_sims,
                                     valid_times,
                                     fcst_lead=fhr,
                                     plot_stat=plot_dict[v]['plot_stat'][istat],
                                     ax=ax,
                                     verbose=False,
                                     toggle_pts=False,
                                     mean_legend=False,
                                     exclude_plvl=[100, 150, 200, 250, 300, 400, 500],
                                     **plot_dict[v]['kwargs'])

                ax.set_ylim([1000, 580])
                if (i == 1) and (j == 0):
                    ax.legend(ncols=3, fontsize=10, loc=(-0.2, -0.5))
                else:
                    ax.get_legend().remove()
                ax.set_yticks(ticks=[1000, 900, 800, 700, 600], 
                              labels=['1000', '900', '800', '700', '600'],
                              minor=False)
                ax.set_xticks(ticks=xticks[stat][fhr][v], minor=False)
                ax.tick_params(which='both', labelsize=10)
                ax.set_title('')
                if i == 0:
                    ax.set_xlabel('')
                else:
                    ax.set_xlabel(xlabel[v], size=12)
                if j == 0:
                    ax.set_ylabel(f"{ttl}\npressure (hPa)", size=12)
                else:
                    ax.set_ylabel('')
                ax.text(0.05, 0.9, f'{letters[3*i+j]})', size=12, weight='bold', transform=ax.transAxes,
                        backgroundcolor='white')

        plt.suptitle(f"{fhr}-hr {stat}", size=16)
        plt.savefig(out_fname.format(stat=stat, fhr=fhr))
        plt.close()


"""
End lower_troposphere_verif_vprofs.py.py
"""
