import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import datetime as dt
import os, sys

sys.path.append('/modules/')
import ndbc_buoy_package as buoy

#station = '44095'; txt = 'Oregon Inlet, NC'
station = '44056'; txt = 'Duck, NC Inshore'
#station = '44100'; txt = 'Duck, NC Offshore'
#station = '44086'; txt = 'Nags Head, NC'

da = buoy.sst_dayofyear_tseries(station)

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

day = da.time
SSTdave = np.array(da)

### Create a climatology from the running mean
SSTdave_clim = np.nanmean(SSTdave, axis=0)
N = 60# Length of running mean
clim_run = running_mean(SSTdave_clim, N)
SST_dave_clim_run = np.nan*np.ones((366, ))
SST_dave_clim_run[int(N/2):len(clim_run)+int(N/2)] = clim_run

### Plot
year1 = int(np.array(da.year[0]))
year2 = int(np.array(da.year[-1]))
nyear = len(da.year)

plt.close()
for n in range(nyear):
    plt.plot(day, SSTdave[n, :], color='gray')
    if int(np.array(da.year[n])) == year2:
        plt.plot(day, SST_dave_clim_run, color='r')
        plt.plot(day, SSTdave[n, :], color='k')

plt.grid(True)
plt.ylim(0, 30)
plt.xlabel('Day of the Year')
plt.ylabel('SST [$^{\circ}$C]')
plt.title('NDBC ' + station + ' ' + txt)

### Save Figure as a pdf
fig_path = os.path.abspath('')
figname = '/figs/sst_dayofyear_' + str(year1) + '-' + str(year2) + \
        '_ndbc_' + station + '_clim.pdf'
figdir = fig_path + figname
plt.savefig(figdir, bbox_inches='tight')
plt.show()



