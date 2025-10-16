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
xlabel_ctrl = {'TMP': 'temperature (K)',
               'SPFH': 'specific humidity (g kg$^{-1}$)',
               'UGRD_VGRD': 'winds (m s$^{-1}$)'}
xlabel_diff = {'TMP': 'T diff (K)',
               'SPFH': 'Q diff (g kg$^{-1}$)',
               'UGRD_VGRD': 'winds diff (m s$^{-1}$)'}

# X-axis limits
xlim = {0: {'RMSE': {'TMP': [-0.7, 0.02],
                     'SPFH': [-7e-4, 2e-5],
                     'UGRD_VGRD': [-2.2, 0.1]},
            'Bias': {'TMP': [-0.2, 0.2],
                     'SPFH': [-1.5e-4, 1e-4],
                     'UGRD_VGRD': [-0.18, 0.3]}},
        6: {'RMSE':{'TMP': [-0.41, 0.01],
                    'SPFH': [-3.8e-4, 2e-5],
                    'UGRD_VGRD': [-1.1, 0.05]},
            'Bias': {'TMP': [-0.15, 0.2],
                     'SPFH': [-8e-5, 9e-5],
                     'UGRD_VGRD': [-0.07, 0.14]}}}

# Output file (include {stat} and {fhr} placeholders)
out_fname = '../figs/Vprof3row{stat}{fhr}.pdf'


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
#sim_dict_spring['ctrl $-$ no_aircft'] = param['sim_dict_no_aircft']['spring']

sim_dict_winter = {}
sim_dict_winter['ctrl'] = param['sim_dict_winter']['ctrl']
for key in param['sim_dict_winter'].keys():
    if key[:3] == 'uas':
        sim_dict_winter[f'{key} $-$ ctrl'] = param['sim_dict_winter'][key]

plot_dict = param['lower_atm']

# Make plots
for istat, stat in enumerate(['RMSE', 'Bias']):
#for istat, stat in enumerate(['RMSE']):
    for fhr in [0, 6]:
        print(f'\nMaking plot for {stat} f{fhr:02d}h')
        fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(6.5, 8), sharey=True)
        plt.subplots_adjust(left=0.14, bottom=0.14, right=0.98, top=0.95, hspace=0.46, wspace=0.1)
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        for i, (sim_dict, ttl, valid_times, c, ls) in enumerate(zip([sim_dict_winter, sim_dict_spring],
                                                                    ['winter', 'spring'],
                                                                    [valid_times_winter, valid_times_spring],
                                                                    ['k', 'gray'],
                                                                    ['-', '-.'])):
            for j, v in enumerate(list(plot_dict.keys())):
                print(f'{ttl} {v}')
                input_sims = copy.deepcopy(sim_dict)
                for key in input_sims:
                    input_sims[key]['dir'] = input_sims[key]['dir'].format(typ='GridStat', subtyp='lower_atm_below_sfc_mask')

                # Control run
                ctrl_sim = {}
                ctrl_sim[f"{ttl} ctrl"] = input_sims['ctrl']
                ctrl_sim[f"{ttl} ctrl"]['color'] = c
                ctrl_sim[f"{ttl} ctrl"]['ls'] = ls
                _ = mp.plot_ua_vprof(ctrl_sim,
                                     valid_times,
                                     fcst_lead=fhr,
                                     plot_stat=plot_dict[v]['plot_stat'][istat],
                                     ax=axes[0, j],
                                     verbose=False,
                                     exclude_plvl=[100, 150, 200, 250, 300, 400, 500],
                                     diffs=False,
                                     **plot_dict[v]['kwargs'])

                # Difference plot
                _ = mp.plot_ua_vprof(input_sims,
                                     valid_times,
                                     fcst_lead=fhr,
                                     plot_stat=plot_dict[v]['plot_stat'][istat],
                                     ax=axes[i+1, j],
                                     verbose=False,
                                     exclude_plvl=[100, 150, 200, 250, 300, 400, 500],
                                     diffs=True,
                                     include_zero=True,
                                     **plot_dict[v]['kwargs'])

        # Formatting
        for i in range(3):
            for j, v in enumerate(list(plot_dict.keys())):
                ax = axes[i, j]

                # Subplot label
                ax.set_title('')
                ax.text(0.05, 0.88, f'{letters[3*i+j]})', size=12, weight='bold', transform=ax.transAxes,
                        backgroundcolor='white')

                # Legend
                if (i == 0) and (j == 1):
                    ax.legend(ncols=2, fontsize=10, loc=(-0.25, -0.44))
                elif (i == 2) and (j == 0):
                    ax.legend(ncols=3, fontsize=10, loc=(0, -0.59))
                else:
                    ax.get_legend().remove()

                # X label
                if i == 0:
                    ax.set_xlabel(xlabel_ctrl[v], size=12)
                else:
                    ax.set_xlabel(xlabel_diff[v], size=12)

                # Y label
                if (i == 0) and (j == 0):
                    ax.set_ylabel(f"pressure (hPa)", size=12)
                elif (i == 1) and (j == 0):
                    ax.set_ylabel(f"winter\npressure (hPa)", size=12)
                elif (i == 2) and (j == 0):
                    ax.set_ylabel(f"spring\npressure (hPa)", size=12)
                else:
                    ax.set_ylabel('')

                # Ticks
                if i > 0:
                    ax.set_xlim(xlim[fhr][stat][v])
                ax.set_ylim([1000, 580])
                ax.set_yticks(ticks=[1000, 900, 800, 700, 600], 
                              labels=['1000', '900', '800', '700', '600'],
                              minor=False)
                ax.tick_params(which='both', labelsize=10)
                if i == 0:
                    ax.grid()

                # Specific humidity ticks
                if j == 1:
                    formatter = mticker.FuncFormatter(lambda x, pos: f"{x*1e3:.2f}")
                    ax.xaxis.set_major_formatter(formatter)

        plt.suptitle(f"{fhr}-hr {stat}", size=16)
        plt.savefig(out_fname.format(stat=stat, fhr=fhr))
        plt.close()


"""
End lower_troposphere_verif_vprofs.py.py
"""
