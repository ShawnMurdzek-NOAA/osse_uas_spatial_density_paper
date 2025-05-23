"""
Postage Stamp Plots of Ceiling and Specific Humidity Forecasts

shawn.s.murdzek@noaa.gov
"""

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.cm as mcm
import xarray as xr
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import pyart.graph.cm_colorblind as art_cm
import pandas as pd

import pyDA_utils.plot_model_data as pmd
import pyDA_utils.upp_postprocess as uppp


#---------------------------------------------------------------------------------------------------
# Input Parameters
#---------------------------------------------------------------------------------------------------

# Simulation directories
NR_dir = '/work2/noaa/wrfruc/murdzek/nature_run_winter/UPP'
ctrl_dir = '/work2/noaa/wrfruc/murdzek/RRFS_OSSE/syn_data_rrfs-workflow_orion/winter/NCO_dirs/ptmp/prod/rrfs.20220201/22'
uas150_dir = '/work2/noaa/wrfruc/murdzek/RRFS_OSSE/syn_data_rrfs-workflow_orion/winter_uas_150km/NCO_dirs/ptmp/prod/rrfs.20220201/22'
uas35_dir = '/work2/noaa/wrfruc/murdzek/RRFS_OSSE/syn_data_rrfs-workflow_orion/winter_uas_35km/NCO_dirs/ptmp/prod/rrfs.20220201/22'
sims = {'NR': [f"{NR_dir}/20220201/wrfprs_202202012200_er.grib2",
               f"{NR_dir}/20220202/wrfprs_202202020000_er.grib2",
               f"{NR_dir}/20220202/wrfprs_202202020200_er.grib2"],
        'no UAS': [f"{ctrl_dir}/rrfs.t22z.prslev.f000.conus_3km.grib2",
                   f"{ctrl_dir}/rrfs.t22z.prslev.f002.conus_3km.grib2",
                   f"{ctrl_dir}/rrfs.t22z.prslev.f004.conus_3km.grib2"],
        '150-km UAS': [f"{uas150_dir}/rrfs.t22z.prslev.f000.conus_3km.grib2",
                       f"{uas150_dir}/rrfs.t22z.prslev.f002.conus_3km.grib2",
                       f"{uas150_dir}/rrfs.t22z.prslev.f004.conus_3km.grib2"],
        '35-km UAS': [f"{uas35_dir}/rrfs.t22z.prslev.f000.conus_3km.grib2",
                      f"{uas35_dir}/rrfs.t22z.prslev.f002.conus_3km.grib2",
                      f"{uas35_dir}/rrfs.t22z.prslev.f004.conus_3km.grib2"]}

# Files containing UAS sites
uas_site_files = {'150-km UAS': ['/work2/noaa/wrfruc/murdzek/src/osse_ob_creator/fix_data/uas_site_locs_150km.txt'],
                  '35-km UAS': ['/work2/noaa/wrfruc/murdzek/src/osse_ob_creator/fix_data/uas_site_locs_35km.txt1',
                                '/work2/noaa/wrfruc/murdzek/src/osse_ob_creator/fix_data/uas_site_locs_35km.txt2',
                                '/work2/noaa/wrfruc/murdzek/src/osse_ob_creator/fix_data/uas_site_locs_35km.txt3']}

# General parameters
figsize = (8, 8.5)
lon = [-87, -80]
lat = [32, 37]
NR_col_titles = ['2200 UTC', '0000 UTC', '0200 UTC']
fcst_col_titles = ['f00h', 'f02h', 'f04h']
ceil_max = 4000
ceil_field = 'CEIL_EXP2'

# Figure-specific parameters
# Atlanta sits at ~320 m MSL. Ceilings are a few 100 to ~1200 m AGL. So focus on P levels below 850 hPa
fig_param = {'ceil22':{'fname':'../figs/Ceil22Fcst.png',
                       'field':ceil_field,
                       'prs': np.nan,
                       'diff': False,
                       'cbar_label': 'cloud ceiling ({units})',
                       'units': 'm AGL',
                       'cntf_kw':{'cmap':art_cm.HomeyerRainbow,
                                  'levels':np.arange(0, ceil_max+1, 200)}},
             'SPFH22P900':{'fname':'../figs/SPFH22P{P_mb}Fcst.png',
                           'field':'SPFH_P0_L100_GLC0',
                           'prs': 90000,
                           'diff': True,
                           'cbar_label': '{P_mb}-hPa SPFH ({units})',
                           'units': 'g kg$^{-1}$',
                           'cntf_kw':{'cmap':'plasma',
                                      'levels':np.arange(0, 7.5, 0.5)},
                           'cntf_diff_kw':{'cmap':'bwr_r',
                                           'levels':np.arange(-3, 3.1, 0.4),
                                           'extend':'both'}}}
'''
             'RH22P950':{'fname':'../figs/RH22P{P_mb}Fcst.png',
                         'field':'RH_P0_L100_GLC0',
                         'prs': 95000,
                         'diff': True,
                         'cbar_label': '{P_mb}-hPa RH (%)',
                         'cntf_kw':{'cmap':'plasma',
                                    'levels':np.arange(0, 101, 4)},
                         'cntf_diff_kw':{'cmap':'bwr_r',
                                         'levels':np.arange(-30, 31, 4),
                                         'extend':'both'}},
             'RH22P925':{'fname':'../figs/RH22P{P_mb}Fcst.png',
                         'field':'RH_P0_L100_GLC0',
                         'prs': 92500,
                         'diff': True,
                         'cbar_label': '{P_mb}-hPa RH (%)',
                         'cntf_kw':{'cmap':'plasma',
                                    'levels':np.arange(0, 101, 4)},
                         'cntf_diff_kw':{'cmap':'bwr_r',
                                         'levels':np.arange(-30, 31, 4),
                                         'extend':'both'}},
             'RH22P900':{'fname':'../figs/RH22P{P_mb}Fcst.png',
                         'field':'RH_P0_L100_GLC0',
                         'prs': 90000,
                         'diff': True,
                         'cbar_label': '{P_mb}-hPa RH ({units})',
                         'units': '%',
                         'cntf_kw':{'cmap':'plasma',
                                    'levels':np.arange(0, 101, 4)},
                         'cntf_diff_kw':{'cmap':'bwr_r',
                                         'levels':np.arange(-30, 31, 4),
                                         'extend':'both'}},
             'RH22P875':{'fname':'../figs/RH22P{P_mb}Fcst.png',
                         'field':'RH_P0_L100_GLC0',
                         'prs': 87500,
                         'diff': True,
                         'cbar_label': '{P_mb}-hPa RH (%)',
                         'cntf_kw':{'cmap':'plasma',
                                    'levels':np.arange(0, 101, 4)},
                         'cntf_diff_kw':{'cmap':'bwr_r',
                                         'levels':np.arange(-30, 31, 4),
                                         'extend':'both'}},
             'RH22P850':{'fname':'../figs/RH22P{P_mb}Fcst.png',
                         'field':'RH_P0_L100_GLC0',
                         'prs': 85000,
                         'diff': True,
                         'cbar_label': '{P_mb}-hPa RH (%)',
                         'cntf_kw':{'cmap':'plasma',
                                    'levels':np.arange(0, 101, 4)},
                         'cntf_diff_kw':{'cmap':'bwr_r',
                                         'levels':np.arange(-30, 31, 4),
                                         'extend':'both'}},
             'RH22P975':{'fname':'../figs/RH22P{P_mb}Fcst.png',
                         'field':'RH_P0_L100_GLC0',
                         'prs': 97500,
                         'diff': True,
                         'cbar_label': '{P_mb}-hPa RH (%)',
                         'cntf_kw':{'cmap':'plasma',
                                    'levels':np.arange(0, 101, 4)},
                         'cntf_diff_kw':{'cmap':'bwr_r',
                                         'levels':np.arange(-30, 31, 4),
                                         'extend':'both'}}}
'''

#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

start = dt.datetime.now()
print(f"start = {start.strftime('%Y%m%d %H:%M:%S')}")

# Read in site locations and stitch sites together if needed
site_dfs = {}
for key in uas_site_files.keys():
    tmp = []
    for f in uas_site_files[key]:
        tmp.append(pd.read_csv(f))
    site_dfs[key] = pd.concat(tmp)

# Read in data and compute ceilings AGL
sims_ds = {}
for key in sims.keys():
    sims_ds[key] = []
    for fname in sims[key]:
        tmp_ds = xr.open_dataset(fname, engine='pynio')
        tmp_ds = uppp.compute_ceil_agl(tmp_ds, no_ceil=np.nan)
        tmp_ds[ceil_field].values[tmp_ds[ceil_field].values > ceil_max] = np.nan  # Needed to prevent red outline around areas w/ cloud ceilings
        tmp_ds['SPFH_P0_L100_GLC0'].values = tmp_ds['SPFH_P0_L100_GLC0'].values * 1000  # Convert from kg/kg to g/kg
        sims_ds[key].append(tmp_ds)

# Determine figure configuration
nrows = len(sims)
ncols = len(sims[list(sims.keys())[0]])

# Make plots
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
for plot_name in fig_param.keys():
    print(f'\nMaking plot for {plot_name}')
    fig = plt.figure(figsize=figsize)
    for i, s in enumerate(sims_ds.keys()):

        print(s)

        if np.isnan(fig_param[plot_name]['prs']):
            zind = np.nan
            out_fname = fig_param[plot_name]['fname']
            cbar_label = fig_param[plot_name]['cbar_label'].format(units=fig_param[plot_name]['units'])
        else:
            P_Pa = fig_param[plot_name]['prs']
            zind = np.where(sims_ds[s][0]['lv_ISBL0'] == P_Pa)[0][0]
            zind_NR = np.where(sims_ds['NR'][0]['lv_ISBL0'] == P_Pa)[0][0]
            P_mb = str(int(fig_param[plot_name]['prs'] / 100))
            out_fname = fig_param[plot_name]['fname'].format(P_mb=P_mb)
            cbar_label = fig_param[plot_name]['cbar_label'].format(P_mb=P_mb, units=fig_param[plot_name]['units'])
        print(f"zind = {zind}")

        for j, ds in enumerate(sims_ds[s]):
            print(f'subplot {j+1}')

            # Difference plot
            if fig_param[plot_name]['diff'] and i > 0:
                out = pmd.PlotOutput([ds, sims_ds['NR'][j]], 
                                     'upp', fig, nrows, ncols, i*ncols + j + 1, 
                                     proj=ccrs.PlateCarree())

                # Add location of Atlanta, GA
                out.plot(-84.3885, 33.7501, plt_kw={'markersize':10, 'marker':'*', 'color':'k'})

                # Add UAS sites
                if (s in site_dfs.keys()) and (j == 0):
                    out.plot(site_dfs[s]['lon (deg E)'], site_dfs[s]['lat (deg N)'], 
                            plt_kw={'color':'gray', 'marker':'.', 'markersize':3, 'linewidth':0})

                out.contourf(fig_param[plot_name]['field'], cbar=False, 
                             ingest_kw={'zind':[zind, zind_NR], 'diff':True,
                                        'indices':[None, [[2, 3180, 3], [3, 5400, 3]]]},
                             cntf_kw=fig_param[plot_name]['cntf_diff_kw'])

                cax_diff = out.cax

            # Not a difference plot
            else:
                out = pmd.PlotOutput([ds], 'upp', fig, nrows, ncols, i*ncols + j + 1, 
                                     proj=ccrs.PlateCarree())

                # Add location of Atlanta, GA
                out.plot(-84.3885, 33.7501, plt_kw={'markersize':10, 'marker':'*', 'color':'k'})

                out.contourf(fig_param[plot_name]['field'], cbar=False, 
                             ingest_kw={'zind':[zind]},
                             cntf_kw=fig_param[plot_name]['cntf_kw'])

                cax = out.cax

            out.set_lim(lat[0], lat[1], lon[0], lon[1])
            out.ax.coastlines('10m', edgecolor='k', linewidth=0.75)
            borders = cfeature.NaturalEarthFeature(category='cultural',
                                                   scale='10m',
                                                   facecolor='none',
                                                   name='admin_1_states_provinces')
            out.ax.add_feature(borders, linewidth=0.75, edgecolor='k')
            
            if j == 0:
                out.ax.set_ylabel(s, size=16)
            if i == 0:
                out.ax.set_title(f"{letters[ncols*i+j]}) {s}: {NR_col_titles[j]}", size=14)
            else:
                out.ax.set_title(f"{letters[ncols*i+j]}) {s}: {fcst_col_titles[j]}", size=14)

    # Add colorbar(s)
    if fig_param[plot_name]['diff']:

        cb_diff_ax = fig.add_axes([0.87, 0.02, 0.03, 0.68])
        cbar_diff = plt.colorbar(cax_diff, cax=cb_diff_ax, orientation='vertical', aspect=35, pad=0.1)
        cbar_diff.set_label(f"difference (RRFS $-$ NR) in {cbar_label}", size=14)
        cbar_diff.ax.tick_params(labelsize=11)

        cb_ax = fig.add_axes([0.87, 0.72, 0.03, 0.25])
        cbar = plt.colorbar(cax, cax=cb_ax, orientation='vertical', aspect=35, pad=0.1)
        cbar.set_label(cbar_label, size=14)
        cbar.ax.tick_params(labelsize=11)

    else:

        cb_ax = fig.add_axes([0.86, 0.02, 0.03, 0.93])
        cbar = plt.colorbar(out.cax, cax=cb_ax, orientation='vertical', aspect=35, pad=0.1)
        cbar.set_label(cbar_label, size=14)
        cbar.ax.tick_params(labelsize=11)

    plt.subplots_adjust(left=0.02, bottom=0.02, right=0.85, top=0.95, hspace=0.3, wspace=0.1)
    plt.savefig(out_fname, dpi=700)
    plt.close()

print(f'\nElapsed time = {(dt.datetime.now() - start).total_seconds()} s')


"""
End postage_stamp_ceil_RH.py
"""
