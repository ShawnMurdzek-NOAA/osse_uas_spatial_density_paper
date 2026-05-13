"""
Copy UAS CSV files and Remove Unnecessary Obs

Only include type 136 (UAS thermodynamic obs)

shawn.s.murdzek@noaa.gov
"""

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

from pyDA_utils import bufr


#---------------------------------------------------------------------------------------------------
# Inputs
#---------------------------------------------------------------------------------------------------

# UAS spatial densities
uas_density = [300, 300, 150, 100, 75, 35]

# Time stamps
times = ['202204301200'] + 5*['202204292100']

# Input data (include {n} placeholder for UAS spatial density and {t} placeholder for time stamp)
in_data = '/work/noaa/wrfruc/murdzek/nature_run_spring/obs/uas_obs_{n:d}km/superob_uas/{t}.rap.fake.prepbufr.csv'


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

for d, t in zip(uas_density, times):
    if d == 35:
        df = bufr.bufrCSV('/work/noaa/wrfruc/murdzek/nature_run_spring/obs/uas_obs_35km/combine_obs/superob_uas/202204292100.rap.fake.prepbufr.csv').df
    else:
        df = bufr.bufrCSV(in_data.format(n=d, t=t)).df

    # Only keep UAS thermodynamic obs
    df_new = df.loc[df['TYP'] == 136, :]

    # Save new DataFrame
    fname = f'./uas_obs_{d}km/superob_uas/{t}.rap.fake.prepbufr.csv'
    bufr.df_to_csv(df_new, fname)


"""
End prep_uas_ob_csvs.py
"""
