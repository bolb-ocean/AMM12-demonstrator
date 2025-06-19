import xarray as xr
import numpy as np

# Input file
filenm = 'AMM_R12_sco_domcfg.nc'

# Open the dataset
ds = xr.open_dataset(filenm)

# Extract variables
e3t_0 = ds.e3t_0
tmask = ds.e3t_0.squeeze() * 0.0
bottom_level = ds.bottom_level.squeeze()

# Compute tmask
for i in range(len(ds.e3t_0.squeeze()[0, :, 0])):
    for j in range(len(ds.e3t_0.squeeze()[0, 0, :])):
        tmask[:bottom_level[i, j].values, i, j] = 1
        tmask[:, 0, :] = 0.0
        tmask[:, :, 0] = 0.0
        tmask[:, -1, :] = 0.0
        tmask[:, :, -1] = 0.0

# Compute bathymetry
bathymetry = (e3t_0 * tmask).sum(dim='z').where(bottom_level > 0, 0.0)

# Assign to dataset
ds['bathy_metry'] = bathymetry

# Save the output
ds.to_netcdf('AMM_R12_sco_domcfg_with_bathy.nc')
