import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Load dataset
ds = xr.open_dataset("AMM_R12_sco_domcfg_with_bathy.nc")
ds_gebco = xr.open_dataset("bathy_GEBCO_AMM12.nc")

# Extract variables and squeeze time
bathy = ds['bathy_metry'].squeeze()
bathy_gebco = ds_gebco['bathy_metry'].squeeze()

var = bathy_gebco - bathy
lon = ds['glamt'].squeeze()
lat = ds['gphit'].squeeze()

# Create figure and axes
fig, axes = plt.subplots(ncols=2, figsize=(14, 8),
                         subplot_kw={'projection': ccrs.Mercator()})

# Common plotting function
def plot_bathymetry(ax, data, title,vmin=-300, vmax=300):
    pcm = ax.pcolormesh(lon, lat, data, cmap='seismic', shading='auto', transform=ccrs.PlateCarree(),vmin=vmin, vmax=vmax)
    ax.coastlines()
    ax.add_feature(cfeature.LAND, zorder=100, edgecolor='black')
    ax.gridlines(draw_labels=True)
    ax.set_title(title)
    return pcm

# Left: full bathymetry
pcm1 = plot_bathymetry(axes[0], var, "Full Bathymetry (GEBCO - AMM12)")

# Right: shallow bathymetry < 200m
var = var.where(bathy_gebco < 200)
pcm2 = plot_bathymetry(axes[1], var, "Shelf Bathymetry (<200m) (GEBCO - AMM12)",vmin=-100, vmax=100)

# Colorbars
fig.colorbar(pcm1) #, ax=axes[0], orientation='horizontal', label='Depth (m)')
fig.colorbar(pcm2) #, ax=axes[1], orientation='horizontal', label='Depth (m)')

plt.tight_layout()
plt.savefig('Bathy_domcfg_GEBCO_diff_AMM12.png')

