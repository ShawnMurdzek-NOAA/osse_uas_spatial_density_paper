"""
Plot Locations of UAS Sites

shawn.s.murdzek@noaa.gov
"""

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd


#---------------------------------------------------------------------------------------------------
# Input Parameters
#---------------------------------------------------------------------------------------------------

# Text files with UAS site locations
uas_site_files = {'a) 150-km spacing': 
                     {'fnames': 
                         ['/work2/noaa/wrfruc/murdzek/src/osse_ob_creator/fix_data/uas_site_locs_150km.txt'],
                      'ms':3},
                  'b) 35-km spacing': 
                      {'fnames':
                          ['/work2/noaa/wrfruc/murdzek/src/osse_ob_creator/fix_data/uas_site_locs_35km.txt1',
                           '/work2/noaa/wrfruc/murdzek/src/osse_ob_creator/fix_data/uas_site_locs_35km.txt2',
                           '/work2/noaa/wrfruc/murdzek/src/osse_ob_creator/fix_data/uas_site_locs_35km.txt3'],
                       'ms':1}}

# Output file name
out_fname = '../figs/SiteLocs.pdf'


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

# Read in site locations and stitch sites together if needed
site_dfs = {}
for key in uas_site_files.keys():
    tmp = []
    for f in uas_site_files[key]['fnames']:
        tmp.append(pd.read_csv(f))
    site_dfs[key] = pd.concat(tmp)

# Plot site locations
fig = plt.figure(figsize=(6, 1+3*len(site_dfs)))
for i, key in enumerate(site_dfs.keys()):
    ax = fig.add_subplot(len(site_dfs), 1, i+1, projection=ccrs.LambertConformal())

    ax.plot(site_dfs[key]['lon (deg E)'], site_dfs[key]['lat (deg N)'], 'r.', 
            transform=ccrs.PlateCarree(), ms=uas_site_files[key]['ms'])

    scale = '10m'
    ax.coastlines(scale, lw=0.6)
    borders = cfeature.NaturalEarthFeature(category='cultural',
                                           scale=scale,
                                           facecolor='none',
                                           name='admin_1_states_provinces')
    ax.add_feature(borders, lw=0.3)
    lakes = cfeature.NaturalEarthFeature(category='physical',
                                           scale=scale,
                                           facecolor='none',
                                           name='lakes')
    ax.add_feature(lakes, lw=0.3)
    ax.set_extent([-122, -69, 21, 50])

    ax.set_title(f"{key} (n = {len(site_dfs[key])})", size=18)

    plt.savefig(out_fname)

plt.subplots_adjust(left=0.02, bottom=0.02, right=0.98, top=0.96)


"""
End plot_uas_sites.py 
"""
