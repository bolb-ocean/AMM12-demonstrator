import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Load dataset
ds = xr.open_dataset("bathy_GEBCO_AMM12.nc")

# Extract variables and squeeze time
bathy = ds['bathy_metry'].squeeze()
lon = ds['glamt'].squeeze()
lat = ds['gphit'].squeeze()

# Create figure and axes
fig, axes = plt.subplots(ncols=2, figsize=(14, 8),
                         subplot_kw={'projection': ccrs.Mercator()})

# Common plotting function
def plot_bathymetry(ax, data, title):
    pcm = ax.pcolormesh(lon, lat, data, cmap='Blues_r', shading='auto', transform=ccrs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cfeature.LAND, zorder=100, edgecolor='black')
    ax.gridlines(draw_labels=True)
    ax.set_title(title)
    return pcm

# Left: full bathymetry
pcm1 = plot_bathymetry(axes[0], bathy, "Full Bathymetry")

# Right: shallow bathymetry < 200m
bathy_shallow = bathy.where(bathy < 200)
pcm2 = plot_bathymetry(axes[1], bathy_shallow, "Shelf Bathymetry (<200m)")

# Colorbars
fig.colorbar(pcm1) #, ax=axes[0], orientation='horizontal', label='Depth (m)')
fig.colorbar(pcm2) #, ax=axes[1], orientation='horizontal', label='Depth (m)')

plt.tight_layout()
plt.savefig('Bathy_domcfg_GEBCO.png')

