"""
Quick Script to Plot Height AGL for a Pressure Level

shawn.s.murdzek@noaa.gov
"""

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.feature as cfeature
import cartopy.crs as ccrs

import pyDA_utils.plot_model_data as pmd


#---------------------------------------------------------------------------------------------------
# Input Parameters
#---------------------------------------------------------------------------------------------------

# Input UPP file name
upp_file = '/work2/noaa/wrfruc/murdzek/nature_run_winter/UPP/20220201/wrfprs_202202012200_er.grib2'

# Pressure level in Pa
prs_lvl = 90000

# Plotting domain
lon = [-87, -80]
lat = [32, 37]

# Output file name
out_fname = f'../figs/hgt_agl_p{prs_lvl}.png'


#---------------------------------------------------------------------------------------------------
# Input Parameters
#---------------------------------------------------------------------------------------------------

# Compute height AGL field
ds = xr.open_dataset(upp_file, engine='pynio')
zind = np.where(ds['lv_ISBL0'] == prs_lvl)[0][0]
print(f'Vertical index = {zind}')
hgt = ds['HGT_P0_L100_GLC0'][zind, :, :].values - ds['HGT_P0_L1_GLC0'].values

# Make plot
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.LambertConformal())
cax = ax.pcolormesh(ds['gridlon_0'].values, ds['gridlat_0'].values, hgt, vmin=-100, vmax=1200, 
                    transform=ccrs.PlateCarree())
cbar = plt.colorbar(cax, ax=ax)
cbar.set_label('height AGL (m)', size=14)

ax.set_extent([lon[0], lon[1], lat[0], lat[1]])
ax.coastlines('10m', edgecolor='k', linewidth=0.75)
borders = cfeature.NaturalEarthFeature(category='cultural',
                                       scale='10m',
                                       facecolor='none',
                                       name='admin_1_states_provinces')
ax.add_feature(borders, linewidth=0.75, edgecolor='k')

plt.savefig(out_fname)


"""
End plot_hgt_agl_for_plvl.py
"""
