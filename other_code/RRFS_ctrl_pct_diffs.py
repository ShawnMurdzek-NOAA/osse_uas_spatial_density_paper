"""
Compute Percent Differences Between Two RRFS Control Runs

shawn.s.murdzek@noaa.gov
"""

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

import yaml
import copy
import glob
import numpy as np

import metplus_OSSE_scripts.plotting.metplus_tools as mt


#---------------------------------------------------------------------------------------------------
# Input Parameters
#---------------------------------------------------------------------------------------------------

# Input simulations
sim_dict = {'spring': 
             {'old': '/work2/noaa/wrfruc/murdzek/RRFS_OSSE/metplus_verif_grid_NR/app_orion/spring_2iter/upper_air/output/GridStat',
              'new': '/work2/noaa/wrfruc/murdzek/RRFS_OSSE/metplus_verif_grid_NR/rrfs-workflow_orion/spring/upper_air/output/GridStat'},
            'winter':
             {'old': '/work2/noaa/wrfruc/murdzek/RRFS_OSSE/metplus_verif_grid_NR/app_orion/winter_2iter/upper_air/output/GridStat',
              'new': '/work2/noaa/wrfruc/murdzek/RRFS_OSSE/metplus_verif_grid_NR/rrfs-workflow_orion/winter/upper_air/output/GridStat'}}

# Forecast lead times
fcst_leads = [0, 1, 2, 3, 6, 12]

# Variables
fcst_vars = {'TMP':'sl1l2', 'SPFH':'sl1l2', 'UGRD_VGRD':'vl1l2'}

# Valid times
valid_times = {}

# Subsetting parameters
subset = {'VX_MASK': 'FULL'}


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

# Open MET verification output
verif_df = {}
for s in sim_dict:
    print(f"Extracting files for {s}")
    verif_df[s] = {}
    for v in fcst_vars:
        print(v)
        verif_df[s][v] = {}
        for age in sim_dict[s]:
            verif_df[s][v][age] = {}
            for fl in fcst_leads:
                fnames = glob.glob(f"{sim_dict[s][age]}/grid_stat_FV3_TMP_vs_NR_TMP_{fl:02d}0000L_*V_{fcst_vars[v]}.txt")
                tmp = mt.read_ascii(fnames, verbose=False)
                subset_copy = copy.deepcopy(subset)
                subset_copy['FCST_VAR'] = v
                tmp2 = mt.subset_verif_df(tmp, subset_copy)
                verif_df[s][v][age][fl] = tmp2.sort_values(['FCST_VALID_BEG', 'FCST_LEV'], ignore_index=True)

# Compute percent differences
print()
for s in sim_dict:
    for v in fcst_vars:
        if v == 'UGRD_VGRD':
            stat = 'VECT_RMSE'
        else:
            stat = 'RMSE'
        for fl in fcst_leads:
            cond = True
            for f in ['FCST_VALID_BEG', 'FCST_LEV']:
                chk = np.all(verif_df[s][v]['old'][fl][f].values == verif_df[s][v]['new'][fl][f].values)
                cond = np.logical_and(cond, chk)
            if cond:
                all_stats = mt.compute_stats_entire_df(verif_df[s][v]['old'][fl], 
                                                       verif_df2=verif_df[s][v]['new'][fl],
                                                       line_type=fcst_vars[v],
                                                       agg=True,
                                                       diff_kw={'var':[stat], 'pct':True})
            print(f"{s} {v} {fl} pct diff = {all_stats[stat].values[0]:.3f}")


"""
End RRFS_ctrl_pct_diffs.py
"""
