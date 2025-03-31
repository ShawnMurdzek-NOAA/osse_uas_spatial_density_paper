"""
Plot Raw and Superobbed UAS Vertical Profiles

Used for figure 3

shawn.s.murdzek@noaa.gov
"""

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

import xarray as xr
import matplotlib.pyplot as plt
import metpy.calc as mc
from metpy.units import units
import numpy as np
import sys
import yaml

import pyDA_utils.bufr as bufr
import pyDA_utils.plot_model_data as pmd
import pyDA_utils.map_proj as mp


#---------------------------------------------------------------------------------------------------
# Input Parameters
#---------------------------------------------------------------------------------------------------

# BUFR file with raw UAS profile
bufr_file_raw = '/work/noaa/wrfruc/murdzek/nature_run_spring/obs/uas_obs_300km/err_uas_csv/202204301200.rap.fake.prepbufr.csv'

# BUFR file with superobbed UAS profile
bufr_file_superob = '/work/noaa/wrfruc/murdzek/nature_run_spring/obs/uas_obs_300km/superob_uas/202204301200.rap.fake.prepbufr.csv'

# Ob type for thermodynamic measurements 
ob_typ_thermo = 136

# SID to plot
sid = "'UA000038'"

# Output file name (include %s placeholder for SID)
out_fname = '../figs/UASRawVsSuperob.pdf'


#---------------------------------------------------------------------------------------------------
# Make Plots
#---------------------------------------------------------------------------------------------------

# Read in BUFR CSV files
bufr_csv_raw = bufr.bufrCSV(bufr_file_raw)
bufr_csv_superob = bufr.bufrCSV(bufr_file_superob)

# Extract the desired SID
raw_thermo = bufr_csv_raw.df.loc[(bufr_csv_raw.df['SID'] == sid) & 
                                 (bufr_csv_raw.df['TYP'] == ob_typ_thermo)].copy()
superob_thermo = bufr_csv_superob.df.loc[(bufr_csv_superob.df['SID'] == sid) & 
                                         (bufr_csv_superob.df['TYP'] == ob_typ_thermo)].copy()

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 6))
plt.subplots_adjust(left=0.15, bottom=0.1, right=0.98, top=0.98)

v = 'TOB'
ax.plot(raw_thermo[v], raw_thermo['ZOB'], 'r-', label='raw')
ax.plot(superob_thermo[v], superob_thermo['ZOB'], 'ko', markersize=10, label='superob')

ax.set_ylim(bottom=0)
ax.set_xlabel("temperature ($^{\circ}$C)", size=16)
ax.set_ylabel('height (m MSL)', size=16)
ax.grid()
ax.legend(fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=12)

plt.savefig(out_fname)


"""
End plot_raw_superob_uas_vprofs.py 
"""
