import xarray as xr
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

def drown_field(field, mask):
    mask_bool = mask == 1
    drowned = field.copy()
    nan_mask = ~mask_bool
    dist, inds = ndimage.distance_transform_edt(nan_mask, return_indices=True)
    drowned.values[nan_mask] = field.values[tuple(i[nan_mask] for i in inds)]
    return drowned

# Open datasets
ds = xr.open_dataset("amm12_restart_oce.nc")
ds_mask = xr.open_dataset("tmask.nc")

tmask = ds_mask.tmask  # Full tmask with dims (t?, z, y, x)

filled_vars = {}

for var_name, var in ds.data_vars.items():
    dims = var.dims
    print(dims)
    if 't' in dims:
        filled_data = []
        for t_idx in range(var.sizes['t']):
            if 'z' in dims:
                filled_levels = []
                for z_idx in range(var.sizes['z']):
                    field = var.isel(t=t_idx, z=z_idx)
                    # Use tmask at z_idx if possible, else fallback to z=0
                    if 'z' in tmask.dims and tmask.sizes['z'] > z_idx:
                        mask_slice = tmask.isel(z=z_idx)
                    else:
                        mask_slice = tmask.isel(z=0)
                    filled = drown_field(field, mask_slice)
                    filled_levels.append(filled)
                filled_t = xr.concat(filled_levels, dim='z')
            else:
                # No vertical dim, use first vertical level of tmask
                field = var.isel(t=t_idx)
                mask_slice = tmask.isel(z=0)
                filled_t = drown_field(field, mask_slice)
            filled_data.append(filled_t)
        if 'z' in dims:
            filled_var = xr.concat(filled_data, dim='t').transpose('t', 'z', 'y', 'x')
        else:
            filled_var = xr.concat(filled_data, dim='t').transpose('t', 'y', 'x')
        filled_vars[var_name] = filled_var
    else:
        # Variables without time dimension, leave unchanged or handle separately if needed
        filled_vars[var_name] = var

filled_ds = xr.Dataset(filled_vars, coords=ds.coords)

# Optionally save
filled_ds.to_netcdf("amm12_restart_oce_drowned.nc", unlimited_dims="t")

