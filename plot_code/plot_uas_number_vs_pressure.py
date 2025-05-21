"""
Plot Number of UAS Superobs As a Function of Pressure

shawn.s.murdzek@noaa.gov
"""

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

import pyDA_utils.bufr as bufr


#---------------------------------------------------------------------------------------------------
# Input Parameters
#---------------------------------------------------------------------------------------------------

# UAS spatial densities
uas_density = [300, 150, 100, 75, 35]

# Input data (include {n} placeholder for UAS spatial density)
in_data = '/work/noaa/wrfruc/murdzek/nature_run_spring/obs/uas_obs_{n:d}km/superob_uas/202204292100.rap.fake.prepbufr.csv'

# Pressure bins
pbins = np.arange(480, 1050, 10)

# Output file
out_fname = '../figs/UASnumberVSprs.pdf'


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

colors = ['#66CCEE', '#AA3377', '#228833', '#CCBB44', '#4477AA']

# Bin UAS obs by pressure
n_uas = {}
for d in uas_density:
    print(f'Binning UAS obs for the {d} km network')
    if d == 35:
        df = bufr.bufrCSV('/work/noaa/wrfruc/murdzek/nature_run_spring/obs/uas_obs_35km/combine_obs/superob_uas/202204292100.rap.fake.prepbufr.csv').df
    else:
        df = bufr.bufrCSV(in_data.format(n=d)).df
    uas_p = df.loc[df['TYP'] == 136, 'POB'].values
    n_uas[d] = np.histogram(uas_p, bins=pbins)[0]

# Plot results
print('Making plot')
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3, 3))
plt.subplots_adjust(left=0.24, bottom=0.17, right=0.98, top=0.97)
p_plot = 0.5*(pbins[1:] + pbins[:-1])
for d, c in zip(uas_density, colors):
    ax.plot(n_uas[d], p_plot, c=c, lw=1.5, label=f'{d} km')

# Make plot look nice
s = 12
ax.set_ylabel('pressure (hPa)', size=s)
ax.set_xlabel('number of UAS superobs', size=s)
ax.grid()
ax.legend(fontsize=s)
ax.set_ylim([pbins[-1], pbins[0]])
ax.set_xlim(0, 3500)
ax.set_yscale('log')
ax.set_yticks(ticks=[1000, 900, 800, 700, 600, 500],
              labels=['1000', '900', '800', '700', '600', '500'],
              minor=False)

plt.savefig(out_fname)
plt.close()


"""
End plot_uas_number_vs_pressure.py
"""
