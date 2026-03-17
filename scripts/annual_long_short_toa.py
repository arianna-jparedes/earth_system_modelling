import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker

# Paths
nc_lw = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/data/top-net-long-annual.nc"
nc_sw = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/data/top-net-short-annual.nc"
png_sw = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/graphs/toa_net_short_annual.png"
png_lw = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/graphs/toa_net_long_annual.png"

# Variables
var_lw = "avg_tnlwrf"
var_sw = "avg_tnswrf"
lat_name = "latitude"
lon_name = "longitude"
title_sw = "Annual mean net incoming solar radiation at TOA (1991-2020)"
title_lw = "Net annual mean outgoing longwave radiation at TOA (1991-2020)"
title_cbar = "Radiation Flux (W m$^{-2}$)"

# SHORTWAVE
ds_sw = xr.open_dataset(nc_sw)
da_sw = ds_sw[var_sw].isel(valid_time=0)

# Colorbar
vmin_sw = float(da_sw.min())
vmax_sw = float(da_sw.max())
start_sw = int(np.floor(vmin_sw / 20.0)*20.0)
end_sw = int(np.ceil(vmax_sw / 20.0)*20.0)
levels_sw = np.arange(start_sw, end_sw+20.0, 20)
ticks_sw = np.arange(start_sw+20.0, end_sw, 20)
norm = mcolors.Normalize(vmin=vmin_sw, vmax=vmax_sw)

# Graph
fig = plt.figure(figsize=(12, 8), dpi=200)
ax = plt.axes(projection=ccrs.Mollweide(central_longitude=180))

im = ax.contourf(
    ds_sw[lon_name], ds_sw[lat_name], da_sw,
    levels=levels_sw,
    transform=ccrs.PlateCarree(),
    cmap="turbo",
    norm=norm
)

plt.title(title_sw, fontsize=15, fontweight="bold", pad=15)

# Map
ax.coastlines(linewidth=0.9)
gl = ax.gridlines(linewidth=0.5, color="k", alpha=0.3, linestyle="--")

# Colorbar
cb = plt.colorbar(im, ax=ax, orientation="horizontal", pad=0.05, shrink=0.8, aspect=30)
cb.set_label(title_cbar, fontsize=12, fontweight="bold")
cb.set_ticks(ticks_sw)
cb.ax.set_xticklabels([f"{t:.0f}" for t in ticks_sw])

plt.savefig(png_sw, bbox_inches="tight")
plt.close()

# LONGWAVE
ds_lw = xr.open_dataset(nc_lw)
da_lw = ds_lw[var_lw].isel(valid_time=0)*(-1)

# Colorbar
vmin_lw = float(da_lw.min())
vmax_lw = float(da_lw.max())
start_lw = int(np.floor(vmin_lw / 20.0)*20.0)
end_lw = int(np.ceil(vmax_lw / 20.0)*20.0)
levels_lw = np.arange(start_lw, end_lw+20.0, 20)
ticks_lw = np.arange(start_lw+20.0, end_lw, 20)

# Graph
fig = plt.figure(figsize=(12, 8), dpi=200)
ax = plt.axes(projection=ccrs.Mollweide(central_longitude=180))

im = ax.contourf(
    ds_lw[lon_name], ds_lw[lat_name], da_lw,
    levels=levels_lw,
    transform=ccrs.PlateCarree(),
    cmap="turbo",
    norm=norm
)

plt.title(title_lw, fontsize=15, fontweight="bold", pad=15)

# Map
ax.coastlines(linewidth=0.9)
gl = ax.gridlines(linewidth=0.5, color="k", alpha=0.3, linestyle="--")

# Colorbar
cb = plt.colorbar(im, ax=ax, orientation="horizontal", pad=0.05, shrink=0.8, aspect=30)
cb.set_label(title_cbar, fontsize=12, fontweight="bold")
cb.set_ticks(ticks_lw)
cb.ax.set_xlim(start_lw, end_lw)
cb.ax.set_xticklabels([f"{t:.0f}" for t in ticks_lw])

plt.savefig(png_lw, bbox_inches="tight")
plt.close()

