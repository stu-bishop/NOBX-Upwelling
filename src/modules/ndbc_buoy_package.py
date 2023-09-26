import numpy as np
import xarray as xr
import datetime as dt

def sst_dayofyear_tseries(station):

    url = 'https://dods.ndbc.noaa.gov/thredds/dodsC/data/stdmet/' \
            + station + '/' + station + 'h9999.nc'
    ds = xr.open_dataset(url)

    year1 =  np.array(ds.time[0]).astype('datetime64[Y]').astype(int) + 1970
    year2 =  np.array(ds.time[-1]).astype('datetime64[Y]').astype(int) + 1970
    year = np.arange(year1, year2+1); nyear = len(year)
    day = np.arange(1, 367); nday = len(day)

    SSTdave = np.nan*np.ones((nyear, nday))
    for n in range(nyear):
        sst = ds.sea_surface_temperature.sel(
                time = slice(
                    '01-01-' + str(year[n]), '12-31-' + str(year[n])
                    )
                )
        sst_dave = sst.resample(time='1D').mean()
        time1 = np.array(sst_dave.time[0])
        years = time1.astype('datetime64[Y]').astype(int) + 1970
        months = time1.astype('datetime64[M]').astype(int) % 12 + 1
        days = (time1.astype('datetime64[D]') - 
                time1.astype('datetime64[M]')).astype(int) + 1
        dday = dt.datetime(years, months, days) - dt.datetime(years, 1, 1)
        iday = np.where(day == dday.days+1)[0]; iday = iday[0]
        ntime = len(sst_dave)
        SSTdave[n, iday:ntime+iday:] = sst_dave.squeeze()
        del iday

    da = xr.DataArray(
            data=SSTdave,
            dims=["year", "time"],
            coords=dict(
            time=day,
            year=year,
            ),
            attrs=dict(
            description="sea surface temperature",
            units="degC",
            ),
        )

    return da


