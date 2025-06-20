import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

#Path to your data directory
data_dir = '$filepath/'

#Load regressor coefficients and domain
tides = xr.open_dataset(data_dir+'AMM12_1h_20120102_20120109_diamlr_coeffs_grid_T.nc')
dom = xr.open_dataset(data_dir'AMM_R12_sco_domcfg.nc')

#Pull complex components.
m2_sin = tides['diamlr_f001-diamlr_r001']
m2_cos = tides['diamlr_f001-diamlr_r002']
k1_sin = tides['diamlr_f001-diamlr_r003']
k1_cos = tides['diamlr_f001-diamlr_r004']
o1_sin = tides['diamlr_f001-diamlr_r005']
o1_cos = tides['diamlr_f001-diamlr_r006']
s2_sin = tides['diamlr_f001-diamlr_r007']
s2_cos = tides['diamlr_f001-diamlr_r008']

#Construct harmonic dataset with complex components.
tide_ha = xr.Dataset(data_vars=dict(
    m2_sin=(["y","x"],m2_sin.data.squeeze()),
    m2_cos=(["y","x"],m2_cos.data.squeeze()),
    s2_sin=(["y","x"],s2_sin.data.squeeze()),
    s2_cos=(["y","x"],s2_cos.data.squeeze()),
    k1_sin=(["y","x"],k1_sin.data.squeeze()),
    k1_cos=(["y","x"],k1_cos.data.squeeze()),
    o1_sin=(["y","x"],o1_sin.data.squeeze()),
    o1_cos=(["y","x"],o1_cos.data.squeeze())
),
  attrs=dict(description="Tidal harmonic constituents.")
                    )
#The constituents you have used.
constituents = ["m2","s2","k1","o1"]

#Calculate the amplitude and phase.
var_names=[]
for con in constituents:
    tide_ha[con+"_amp"] = (tide_ha[con+"_sin"]**2+tide_ha[con+"_cos"]**2)**.5
    tide_ha[con+"_pha"] = np.arctan(tide_ha[con+"_cos"]/tide_ha[con+"_sin"])

#Land mask for plotting.
for con in constituents:
    tide_ha[con+"_amp_mask"] = tide_ha[con+"_amp"].where(dom.top_level.squeeze()==1, np.nan)
    
#Plot for each constituent
for con in constituents:
    fig = plt.figure(dpi=600)
    plt.title('Cotidal chart for '+con)
    levels=np.linspace(-180.,180,6)
    im =plt.pcolormesh(tide_ha.x, tide_ha.y, tide_ha[con+"_amp_mask"].squeeze(),cmap='jet')
    conp = plt.contour(tide_ha.x, tide_ha.y, tide_ha[con+"_pha"].squeeze()*360*2/np.pi, colors='k',levels=np.arange(-180.,181,60),linestyles=np.where(levels >= 0, "--", "-"), linewidths=0.5)
    plt.clabel(conp,levels=[0], inline=True, fontsize=8)
    plt.colorbar(im,label='m')
    plt.savefig(con+'_cotide_demo.png')