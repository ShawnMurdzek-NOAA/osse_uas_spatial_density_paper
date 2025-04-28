"""
Plot Ob Locations for all Ob Types for a Single Variable

Used to create figure 1

shawn.s.murdzek@noaa.gov
"""

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import pyDA_utils.gsi_fcts as gsi


#---------------------------------------------------------------------------------------------------
# Input Parameters
#---------------------------------------------------------------------------------------------------

# GSI output diag file
# O-Bs are found in the "ges" files and O-As are found in the "anl" files
fname = '/work2/noaa/wrfruc/murdzek/RRFS_OSSE/real_data_app_orion/winter/rrfs.20220201/NCO_dirs/ptmp/prod/rrfs.20220201/12/diag_conv_t_ges.2022020112.nc4'

# Subset of each observation type to plot ('all' - all obs, 'assim' - only obs that are assimilated)
data_subset = 'all'

# RRFS field (needed to extract surface terrain height so MSL can be converted to AGL)
rrfs_fname = '/work2/noaa/wrfruc/murdzek/RRFS_OSSE/real_data_app_orion/winter/rrfs.20220201/NCO_dirs/ptmp/prod/rrfs.20220201/12/rrfs.t12z.natlev.f000.conus_3km.grib2'

# Output file name
out_fname = '../figs/TOBdist.pdf'


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

# Extract data
diag_df = gsi.read_diag([fname])
if data_subset == 'assim':
    diag_df = diag_df.loc[diag_df['Analysis_Use_Flag'] == 1, :]

# Convert height from MSL to AGL
diag_df = gsi.compute_height_agl_diag(diag_df, rrfs_fname)

# Create plot
use_filter = [False, False, True]
filter_min = [0, 0, 10]
filter_max = [0, 0, 2000]
title = ['a) all', 'b) near-surface', 'c) 10$-$2000 m AGL']
sid_ignore = [[],
              [120, 126, 130, 133, 134, 135],
              [180, 181, 183, 187, 188]]
fig = plt.figure(figsize=(5.5, 9))
for i in range(3):

    if use_filter[i]:
        red_df = diag_df.loc[(diag_df['Height_AGL'] >= filter_min[i]) &
                             (diag_df['Height_AGL'] <= filter_max[i]), :]
    else:
        red_df = diag_df

    for sid in sid_ignore[i]:
        red_df = red_df.loc[red_df['Observation_Type'] != sid]

    print('\nOb types when using the following considerations:')
    print(f'Filter = {use_filter[i]}, min = {filter_min[i]}, max = {filter_max[i]}')
    for typ in red_df['Observation_Type'].unique():
        print(f"{typ} (n = {len(red_df.loc[red_df['Observation_Type'] == typ])})")

    ax = fig.add_subplot(3, 1, i+1, projection=ccrs.LambertConformal())
    ax.plot(red_df['Longitude'] , red_df['Latitude'], 'b.', markersize=2, transform=ccrs.PlateCarree())

    ax.coastlines('50m', edgecolor='gray', linewidth=0.6)
    borders = cfeature.NaturalEarthFeature(category='cultural',
                                           scale='50m',
                                           facecolor='none',
                                           name='admin_1_states_provinces')
    ax.add_feature(borders, edgecolor='gray', linewidth=0.4)
    lakes = cfeature.NaturalEarthFeature(category='physical',
                                         scale='50m',
                                         facecolor='none',
                                         name='lakes')
    ax.add_feature(lakes, edgecolor='gray', linewidth=0.4)
    ax.set_extent([237, 291, 21.5, 50])

    ax.set_title(f"{title[i]} (n = {len(red_df)})", size=16)

date_dt = dt.datetime.strptime(str(diag_df['date_time'].values[0]), '%Y%m%d%H')
date_str = date_dt.strftime('%Y%m%d %H:%M UTC')
plt.suptitle(f"Temperature Observations\n({date_str})", size=20)
plt.subplots_adjust(left=0.02, bottom=0.02, right=0.98, top=0.87)

plt.savefig(out_fname)
plt.close()


"""
End diag_ob_locs.py
"""
