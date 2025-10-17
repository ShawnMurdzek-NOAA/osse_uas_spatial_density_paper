"""
Plot Histograms of Added UAS Errors as a Function of Autocorrelation

shawn.s.murdzek@noaa.gov
"""

#---------------------------------------------------------------------------------------------------
# Import Modules
#---------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np


#---------------------------------------------------------------------------------------------------
# Input Parameters
#---------------------------------------------------------------------------------------------------

# Error standard deviation
stdev = 0.5

# Error bins for histogram
ybins = np.arange(-10, 10.1, 0.2)

# Number of observations per flight. Must be evenly divisible by tchunk
nobs = 600
tchunk = 30

# Number of iterations
niter = 10000

# Autocorrelation parameters
autocorr = [0, 0.5, 0.95, 0.985, 0.995]
colors = ['k', 'gray', '#1E88E5', '#D81B60', '#FFC107']

# Output file
out_fname = '../figs/UASerrVSautocorr.pdf'


#---------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------

# Check nobs and tchunk
if nobs % tchunk != 0:
    raise ValueError('nobs % tchunk must be 0!')

# Create arrays to hold error profiles
err_profiles = {}
for a in autocorr:
    err_profiles[a] = np.zeros([niter, nobs])

# Create error profiles
for i in range(niter):
    gaussian = np.random.normal(scale=stdev, size=nobs)
    for a in autocorr:
        err_profiles[a][i, 0] = gaussian[0]
        for j in range(1, nobs):
            err_profiles[a][i, j] = gaussian[j] + (a * err_profiles[a][i, j-1]) 

# Plot histograms of errors from last time step
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 4))
plt.subplots_adjust(left=0.15, bottom=0.12, right=0.97, top=0.98)

errs = 0.5*(ybins[1:] + ybins[:-1])
for a, c in zip(autocorr, colors):

    # Print decorrelation times
    print()
    print(f"Autocorrelation = {a}")
    for thres in [1/np.e, 0.01, 0.001]:
        print(f"Decorrelation time (thres = {thres:.3f}) = {np.log(thres) / np.log(a):.3f}")

    hist = np.histogram(err_profiles[a][:, -1], bins=ybins)[0]
    #ax.plot(errs, hist, c=c, ls='-', label=a)  # PDF
    ax.plot(errs, np.cumsum(hist) / np.sum(hist), c=c, ls='-', label=f"$A$ = {a}")  # CDF

# Annotations
ax.legend()
ax.grid(True)
ax.set_xlabel('UAS added T errors (K)', size=12)
ax.set_ylabel('normalized cumulative frequency', size=12)
ax.set_xlim([ybins.min(), ybins.max()])
ax.set_ylim([0, 1])

"""
Old code to plot 2D histograms

# Plot results as a histogram
fig, axes = plt.subplots(nrows=len(autocorr), figsize=(6, 8), sharex=True, sharey=True)
plt.subplots_adjust(left=0.12, bottom=0, right=0.9, top=0.94, hspace=0.3)
time = np.arange(0, nobs+0.001, tchunk)
ntime = len(time) - 1
for i, (a, letter) in enumerate(zip(autocorr, ['a', 'b', 'c', 'd', 'e'])):

    # Create histogram
    hist = np.zeros([len(ybins)-1, ntime])
    for j in range(ntime):
        hist[:, j] = np.histogram(err_profiles[a][:, (j*tchunk):((j+1)*tchunk)], bins=ybins)[0]

    # Make plot
    ax = axes[i]
    cax = ax.pcolormesh(time, ybins, hist, cmap='plasma', vmin=0, vmax=(niter*tchunk/10))
    ax.set_title(f"{letter}) Autocorrelation = {a}", size=16)
    ax.set_ylabel('error', size=12)

# Add annotations
axes[-1].set_xlabel('time (s)', size=12)
cbar = plt.colorbar(cax, ax=axes, orientation='horizontal', pad=0.06)
cbar.set_label('count', size=12)
"""

plt.savefig(out_fname)
plt.close()


"""
End uas_error_vs_autocorr.py 
"""
