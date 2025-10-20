"""
Vertical Profiles for Verification of the Lower Atmosphere For Added UAS Error Tests

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
valid_times = [dt.datetime(2022, 4, 29, 21) + dt.timedelta(hours=i) for i in range(159)]

# X-axis labels
xlabel = {'TMP': 'T diff (K)',
          'SPFH': 'Q diff (g kg$^{-1}$)',
          'UGRD_VGRD': 'winds diff (m s$^{-1}$)'}

# X-axis limits
xlim = {0: {'RMSE': {'TMP': [-0.6, 0.02],
                     'SPFH': [-7e-4, 2e-5],
                     'UGRD_VGRD': [-2.23, 0.1]}},
        6: {'RMSE':{'TMP': [-0.38, 0.01],
                    'SPFH': [-3.8e-4, 2e-5],
                    'UGRD_VGRD': [-1.3, 0.05]}}}

# Output file (include {stat} and {fhr} placeholders)
out_fname = '../figs/VprofUASErrTest.pdf'


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

# Read in simulation and plotting information
with open(yml_fname, 'r') as fptr:
    param = yaml.safe_load(fptr)

sim_dict = {}
sim_dict['ctrl'] = param['sim_dict_err']['ctrl']
for key in param['sim_dict_err'].keys():
    if key[:3] == 'uas':
        sim_dict[f'{key} $-$ ctrl'] = param['sim_dict_err'][key]

plot_dict = param['lower_atm']

# Make plots
for istat, stat in enumerate(['RMSE']):
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(6.5, 5), sharey=True)
    plt.subplots_adjust(left=0.14, bottom=0.21, right=0.98, top=0.93, hspace=0.2, wspace=0.1)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    for i, fhr in enumerate([0, 6]):
        print(f'\nMaking plot for {stat} f{fhr:02d}h')
        for j, v in enumerate(list(plot_dict.keys())):
            print(f'{v}')
            input_sims = copy.deepcopy(sim_dict)
            ax = axes[i, j]
            for key in input_sims:
                input_sims[key]['dir'] = input_sims[key]['dir'].format(typ='GridStat', subtyp='lower_atm_below_sfc_mask')

            _ = mp.plot_ua_vprof(input_sims,
                                 valid_times,
                                 fcst_lead=fhr,
                                 plot_stat=plot_dict[v]['plot_stat'][istat],
                                 ax=ax,
                                 verbose=False,
                                 exclude_plvl=[100, 150, 200, 250, 300, 400, 500],
                                 diffs=True,
                                 include_zero=True,
                                 **plot_dict[v]['kwargs'])

            # Formatting
            ax.set_title('')
            ax.text(0.05, 0.88, f'{letters[3*i+j]})', size=12, weight='bold', transform=ax.transAxes,
                    backgroundcolor='white')

            # Legend
            if (i == 0) and (j == 0):
                ax.legend(ncols=2, fontsize=10, loc=(0.3, -1.8))
            else:
                ax.get_legend().remove()

            # X label
            if i == 1:
                ax.set_xlabel(xlabel[v], size=12)
            else:
                ax.set_xlabel('')

            # Y label
            if (j == 0):
                ax.set_ylabel(f"{fhr}-hr forecast\npressure (hPa)", size=12)
            else:
                ax.set_ylabel('')

            # Ticks
            ax.set_xlim(xlim[fhr][stat][v])
            ax.set_ylim([1000, 580])
            ax.set_yticks(ticks=[1000, 900, 800, 700, 600], 
                          labels=['1000', '900', '800', '700', '600'],
                          minor=False)
            ax.tick_params(which='both', labelsize=10)

            # Specific humidity ticks
            if j == 1:
                formatter = mticker.FuncFormatter(lambda x, pos: f"{x*1e3:.2f}")
                ax.xaxis.set_major_formatter(formatter)

    plt.suptitle(f"spring {stat}", size=16)
    plt.savefig(out_fname.format(stat=stat, fhr=fhr))
    plt.close()


"""
End lower_troposphere_verif_vprofs_test_autocorr.py
"""
