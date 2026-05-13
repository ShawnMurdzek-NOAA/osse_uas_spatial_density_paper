"""
Extract Aircraft and UAS OmB from GSI Diag Files

shawn.s.murdzek@noaa.gov
"""

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

import numpy as np
import datetime as dt
import xarray as xr

import pyDA_utils.gsi_fcts as gsi


#---------------------------------------------------------------------------------------------------
# Parameters
#---------------------------------------------------------------------------------------------------

# Input file names
parent1 = '/work/noaa/wrfruc/murdzek/RRFS_OSSE/syn_data_rrfs-workflow_orion/spring_uas_35km_autocorr0.95/NCO_dirs/ptmp/prod'
parent2 = '/work/noaa/wrfruc/murdzek/RRFS_OSSE/syn_data_rrfs-workflow_orion/spring_uas_35km_autocorr0.985/NCO_dirs/ptmp/prod'
times = [dt.datetime(2022, 4, 29, 21) + dt.timedelta(hours=t) for t in range(159)]
#times = [dt.datetime(2022, 5, 1, 0)]
in_fnames = {"0.95" : [f"{parent1}/rrfs.{t.strftime('%Y%m%d/%H/diag_conv_t_ges.%Y%m%d%H.nc4')}" for t in times],
             "0.985" : [f"{parent2}/rrfs.{t.strftime('%Y%m%d/%H/diag_conv_t_ges.%Y%m%d%H.nc4')}" for t in times]}

# Pressure bounds (hPa)
pmin = 700
pmax = 1050


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

for key in in_fnames:

    # Read in GSI diag files
    diag_full = gsi.read_diag(in_fnames[key], ftype='netcdf')
    diag = diag_full.loc[np.logical_and(diag_full['Pressure'] >= pmin, diag_full['Pressure'] <= pmax), :]
    omb_uas = {'omb': ((f"dum"), diag.loc[diag['Observation_Type'] == 136, 'Obs_Minus_Forecast_adjusted'].values)}
    omb_aircft = {'omb': ((f"dum"), diag.loc[(diag['Observation_Type'] == 130) |
                                             (diag['Observation_Type'] == 131) |
                                             (diag['Observation_Type'] == 133) |
                                             (diag['Observation_Type'] == 134) |
                                             (diag['Observation_Type'] == 135), 'Obs_Minus_Forecast_adjusted'].values)}

    # Save to netCDF
    for omb, typ, tag in zip([omb_uas, omb_aircft], ['UAS', 'commercial aircraft'], ['uas', 'aircft']):
        ds = xr.Dataset(omb)
        ds['omb'].attrs['units'] = 'K'
        ds['omb'].attrs['layer'] = f"{pmax} - {pmin} hPa"
        ds['omb'].attrs['desc'] = f"{typ} temperature obs - bgd for the spring_uas_35km_autocorr{key} experiment"
        ds.to_netcdf(f"omb_t_{tag}_A{key}.nc")


"""
End extract_uas_aircraft_omb.py
"""

