"""
Plot Ob Locations for all Ob Types for a Single Variable

Used to create figure 1

shawn.s.murdzek@noaa.gov
"""

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import metpy.calc as mc
from metpy.units import units
import metpy.constants as const
import scipy.interpolate as si
import datetime as dt
import sys

import pyDA_utils.gsi_fcts as gsi


#---------------------------------------------------------------------------------------------------
# Input Parameters
#---------------------------------------------------------------------------------------------------

# O-Bs are found in the "ges" files and O-As are found in the "anl" files
# Can 1 or 2 datasets. Key is the name of the dataset
tmpl = '/mnt/lfs4/BMC/wrfruc/murdzek/tmp_diags/diag_conv_uv_ges.%s.nc4'
dates = [dt.datetime(2024, 3, 25, 0)]

fnames = {}
fnames['real'] = [tmpl % d.strftime('%Y%m%d%H') for d in dates]

# Variable to plot (only necessary for the uv diag files)
diag_var = 'u'

# Subset of each observation type to plot ('all' - all obs, 'assim' - only obs that are assimilated)
data_subset = 'all'

# Filter observations based on another field (e.g., pressure, height)
use_filter = False
filter_field = 'Height_AGL'
filter_min = 400
filter_max = 600

# Option to convert 'Height' from MSL to AGL. This requires a RRFS input file to extract the surface
# terrain height. Resulting field is 'Height_AGL'
convert_msl_to_agl = True
rrfs_fname = '/mnt/lfs4/BMC/wrfruc/murdzek/tmp_diags/rrfs.t12z.natlev.f000.conus_3km.grib2'

# Output directory and string to add to output file names
out_dir = './'
out_str = ''

# Use passed command-line arguments
if len(sys.argv) > 1:
    dates = [dt.datetime.strptime(sys.argv[1], '%Y%m%d%H')]
    fnames['real'] = [tmpl % d.strftime('%Y%m%d%H') for d in dates]
    out_str = sys.argv[2]
    if out_str == 'all':
        use_filter = False
    elif sys.argv[2] == 'upper_trop':
        use_filter = True
        filter_min = 5000
        filter_max = 10000
    elif sys.argv[2] == 'near_sfc':
        use_filter = True
        filter_min = -100
        filter_max = 50
    elif sys.argv[2] == 'pbl':
        use_filter = True
        filter_min = 500
        filter_max = 1000


#---------------------------------------------------------------------------------------------------
# Compute Statistics
#---------------------------------------------------------------------------------------------------

data_names = list(fnames.keys())
if fnames[data_names[0]][0].split('_')[-2] == 'uv':
    vname = '%s_Obs_Minus_Forecast_adjusted' % diag_var
else:
    vname = 'Obs_Minus_Forecast_adjusted'
    diag_var = fnames[data_names[0]][0].split('_')[-2]

# Extract data
diag_df = {}
for key in data_names:
    print('Dataset = %s' % key)
    diag_df[key] = gsi.read_diag(fnames[key])
    if data_subset == 'assim':
        diag_df[key] = diag_df[key].loc[diag_df[key]['Analysis_Use_Flag'] == 1, :]
diag_dates = np.unique(diag_df[data_names[0]]['date_time'])

# Convert height from MSL to AGL if desired
if convert_msl_to_agl:
    diag_df[key] = gsi.compute_height_agl_diag(diag_df[key], rrfs_fname)

# Filter observations
if use_filter:
    for key in data_names:
        diag_df[key] = diag_df[key].loc[(diag_df[key][filter_field] >= filter_min) &
                                        (diag_df[key][filter_field] <= filter_max), :]
        diag_df[key].reset_index(inplace=True, drop=True)

# Create list of ob types
ob_typ = np.unique(diag_df[data_names[0]]['Observation_Type'].values)
if len(data_names) > 1:
    for key in data_names[1:]:
        ob_typ = np.unique(np.concatenate([ob_typ, diag_df[key]['Observation_Type'].values]))

# Add all observation types
ob_typ = np.concatenate([ob_typ, [0]])

# Plot data
for typ in ob_typ:
    fig = plt.figure(figsize=(10, 8))

    for i, key in enumerate(data_names):
        ax = fig.add_subplot(i+1, 1, len(data_names), projection=ccrs.LambertConformal()) 
        if typ > 0:
            lat = diag_df[key].loc[diag_df[key]['Observation_Type'] == typ, 'Latitude'].values
            lon = diag_df[key].loc[diag_df[key]['Observation_Type'] == typ, 'Longitude'].values
        else:
            lat = diag_df[key].loc[:, 'Latitude'].values
            lon = diag_df[key].loc[:, 'Longitude'].values
        ax.plot(lon, lat, 'b.', transform=ccrs.PlateCarree())
        ax.coastlines('50m', edgecolor='gray', linewidth=0.75)
        borders = cfeature.NaturalEarthFeature(category='cultural',
                                               scale='50m',
                                               facecolor='none',
                                               name='admin_1_states_provinces')
        ax.add_feature(borders, edgecolor='gray', linewidth=0.5)
        lakes = cfeature.NaturalEarthFeature(category='physical',
                                             scale='50m',
                                             facecolor='none',
                                             name='lakes')
        ax.add_feature(lakes, edgecolor='gray', linewidth=0.5)
        ax.set_extent([237, 291, 21.5, 50])

    # Add additional metrics
    if typ > 0:
        ttl = ('ob type = %d\nstart = %d, end = %d, var = %s, subset = %s' % 
               (typ, np.amin(diag_dates), np.amax(diag_dates), diag_var, data_subset)) 
    else:
        ttl = ('ob type = all\nstart = %d, end = %d, var = %s, subset = %s' % 
               (np.amin(diag_dates), np.amax(diag_dates), diag_var, data_subset)) 
    if use_filter:
        ttl = ttl + f'\n{filter_min} $\leq$ {filter_field} $\leq$ {filter_max}'

    plt.suptitle(ttl, size=18) 

    plt.savefig('%s/loc_ob%s_%s_%s_%s_%d_%d.pdf' % 
                (out_dir, typ, out_str, diag_var, data_subset, np.amin(diag_dates), np.amax(diag_dates)))
    plt.close() 


"""
End diag_ob_locs.py
"""
