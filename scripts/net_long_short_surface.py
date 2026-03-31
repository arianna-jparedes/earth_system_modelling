import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker

# Paths
nc = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/data/surface-energy-vars-annual.nc"
png_sw = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/graphs/surface_net_short_annual.png"
png_lw = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/graphs/surface_net_long_annual.png"
png_net = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/graphs/surface_net_radiation_annual.png"

# Variables
var_lw = "avg_snlwrf"
var_sw = "avg_snswrf"
lat_name = "latitude"
lon_name = "longitude"
title_sw = "Surface net incoming solar radiation from ERA5 (1991-2020)"
title_lw = "Surface net outgoing longwave radiation from ERA5 (1991-2020)"
title_net = "Surface net radiation from ERA5 (1991-2020)"
title_cbar = "Radiation Flux (W m$^{-2}$)"

# SHORTWAVE
ds = xr.open_dataset(nc)
da_sw = ds[var_sw].isel(valid_time=0)

# Range
vmin_sw = float(da_sw.min())
vmax_sw = float(da_sw.max())
start_sw = int(np.floor(vmin_sw / 20.0)*20.0)
end_sw = int(np.ceil(vmax_sw / 20.0)*20.0)
levels_sw = np.arange(start_sw, end_sw+20.0, 20)
ticks_sw = np.arange(start_sw+20.0, end_sw, 40)
norm = mcolors.Normalize(vmin=vmin_sw, vmax=vmax_sw)

# Graph
fig = plt.figure(figsize=(12, 8), dpi=200)
ax = plt.axes(projection=ccrs.Mollweide(central_longitude=180))

im = ax.contourf(
    ds[lon_name], ds[lat_name], da_sw,
    levels=levels_sw,
    transform=ccrs.PlateCarree(),
    cmap="turbo",
    norm=norm
)

plt.title(title_sw, fontsize=18, fontweight="bold", pad=16)

# Map
ax.coastlines(linewidth=0.9)
gl = ax.gridlines(linewidth=0.5, color="k", alpha=0.3, linestyle="--")

# Colorbar
cb = plt.colorbar(im, ax=ax, orientation="horizontal", pad=0.05, shrink=0.9, aspect=30)
cb.set_label(title_cbar, fontsize=16, fontweight="bold")
cb.set_ticks(ticks_sw)
cb.ax.set_xticklabels([f"{t:.0f}" for t in ticks_sw])
cb.ax.tick_params(labelsize=15)

plt.savefig(png_sw, bbox_inches="tight")
plt.close()

# LONGWAVE
da_lw = ds[var_lw].isel(valid_time=0)*(-1)

# Range
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
    ds[lon_name], ds[lat_name], da_lw,
    levels=levels_lw,
    transform=ccrs.PlateCarree(),
    cmap="turbo",
    norm=norm
)

plt.title(title_lw, fontsize=18, fontweight="bold", pad=16)

# Map
ax.coastlines(linewidth=0.9)
gl = ax.gridlines(linewidth=0.5, color="k", alpha=0.3, linestyle="--")

# Colorbar
cb = plt.colorbar(im, ax=ax, orientation="horizontal", pad=0.05, shrink=0.9, aspect=30)
cb.set_label(title_cbar, fontsize=16, fontweight="bold")
cb.set_ticks(ticks_lw)
cb.ax.set_xlim(start_lw, end_lw)
cb.ax.set_xticklabels([f"{t:.0f}" for t in ticks_lw])
cb.ax.tick_params(labelsize=15)

plt.savefig(png_lw, bbox_inches="tight")
plt.close()

# NET
da_net = ds[var_sw].isel(valid_time=0) + ds[var_lw].isel(valid_time=0)

# Range
vmin_net = 0.0
vmax_net = 220.0
start_net = int(np.floor(vmin_net / 20.0) * 20.0)
end_net = int(np.ceil(vmax_net  / 20.0) * 20.0)
levels_net = np.arange(start_net, end_net + 20.0, 20)
ticks_net = np.arange(start_net + 20.0, end_net, 20)

# Graph
fig = plt.figure(figsize=(12, 8), dpi=200)
ax = plt.axes(projection=ccrs.Mollweide(central_longitude=180))
im = ax.contourf(
    ds[lon_name], ds[lat_name], da_net,
    levels=levels_net, transform=ccrs.PlateCarree(),
    cmap="turbo",
    extend="both",
)

plt.title(title_net, fontsize=18, fontweight="bold", pad=16)

# Map
ax.coastlines(linewidth=0.9)
ax.gridlines(linewidth=0.5, color="k", alpha=0.3, linestyle="--")

# Colorbar
cb = plt.colorbar(im, ax=ax, orientation="horizontal", pad=0.05, shrink=0.9, aspect=30)
cb.set_label(title_cbar, fontsize=16, fontweight="bold")
cb.set_ticks(ticks_net)
cb.ax.set_xticklabels([f"{t:.0f}" for t in ticks_net])
cb.ax.tick_params(labelsize=15)

plt.savefig(png_net, bbox_inches="tight")
plt.close()

