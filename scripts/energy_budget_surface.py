import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker

# Paths
nc = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/data/surface-energy-vars-annual.nc"
png_sh = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/graphs/surface_sensible_heat_annual.png"
png_lh = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/graphs/surface_latent_heat_annual.png"
png_strg = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/graphs/surface_heat_storage_annual.png"

# Variables
var_lw = "avg_snlwrf"
var_sw = "avg_snswrf"
var_lh = "avg_slhtf"
var_sh = "avg_ishf"
lat_name = "latitude"
lon_name = "longitude"

title_lh = "Surface latent heat flux from ERA5 (1991-2020)"
title_sh = "Surface sensible heat flux from ERA5 (1991-2020)"
title_strg = "Surface heat storage from ERA5 (1991-2020)"
title_cbar = "Heat Flux (W m$^{-2}$)"

ds = xr.open_dataset(nc)

# SENSIBLE HEAT
da_sh = ds[var_sh].isel(valid_time=0) * (-1)

# Range
vmin_sh = float(da_sh.min())
vmax_sh = float(da_sh.max())
start_sh = int(np.floor(vmin_sh / 20.0) * 20)
end_sh = int(np.ceil(vmax_sh  / 20.0) * 20)
levels_sh = np.arange(start_sh, end_sh + 20, 20)
ticks_sh = np.arange(start_sh + 20, end_sh, 20)
norm_sh = mcolors.TwoSlopeNorm(vmin=start_sh, vcenter=0, vmax=end_sh)

# Graph
fig = plt.figure(figsize=(12, 8), dpi=200)
ax = plt.axes(projection=ccrs.Mollweide(central_longitude=180))

im = ax.contourf(
    ds[lon_name], ds[lat_name], da_sh,
    levels=levels_sh, transform=ccrs.PlateCarree(),
    cmap="RdBu_r", norm=norm_sh
)

plt.title(title_sh, fontsize=18, fontweight="bold", pad=16)

# Map
ax.coastlines(linewidth=0.9)
ax.gridlines(linewidth=0.5, color="k", alpha=0.3, linestyle="--")

# Colorbar
cb = plt.colorbar(im, ax=ax, orientation="horizontal", pad=0.05, shrink=0.9, aspect=30)
cb.set_label(title_cbar, fontsize=16, fontweight="bold")
cb.set_ticks(ticks_sh)
cb.ax.set_xticklabels([f"{t:.0f}" for t in ticks_sh])
cb.ax.tick_params(labelsize=15)

plt.savefig(png_sh, bbox_inches="tight")
plt.close()

# LATENT HEAT
da_lh = ds[var_lh].isel(valid_time=0) * (-1)

# Range
vmin_lh = 0.0
vmax_lh = 220.0
start_lh = int(np.floor(vmin_lh / 20.0) * 20)
end_lh = int(np.ceil(vmax_lh  / 20.0) * 20)
levels_lh = np.arange(start_lh, end_lh + 20, 20)
ticks_lh = np.arange(start_lh + 20, end_lh, 20)

# Graph
fig = plt.figure(figsize=(12, 8), dpi=200)
ax = plt.axes(projection=ccrs.Mollweide(central_longitude=180))

im = ax.contourf(
    ds[lon_name], ds[lat_name], da_lh,
    levels=levels_lh, transform=ccrs.PlateCarree(),
    cmap="turbo", extend='both'
)

plt.title(title_lh, fontsize=18, fontweight="bold", pad=16)

# Map
ax.coastlines(linewidth=0.9)
ax.gridlines(linewidth=0.5, color="k", alpha=0.3, linestyle="--")

# Colorbar
cb = plt.colorbar(im, ax=ax, orientation="horizontal", pad=0.05, shrink=0.9, aspect=30)
cb.set_label(title_cbar, fontsize=16, fontweight="bold")
cb.set_ticks(ticks_lh)
cb.ax.set_xticklabels([f"{t:.0f}" for t in ticks_lh])
cb.ax.tick_params(labelsize=15)

plt.savefig(png_lh, bbox_inches="tight")
plt.close()

# HEAT STORAGE (Rnet - SH - LH)
da_rnet = ds[var_sw].isel(valid_time=0) + ds[var_lw].isel(valid_time=0)
da_strg = da_rnet - da_sh - da_lh

# Range
vmin_strg = -200.0
vmax_strg = 200.0
start_strg = int(np.floor(vmin_strg / 40.0) * 40)
end_strg = int(np.ceil(vmax_strg  / 40.0) * 40)
levels_strg = np.arange(start_strg, end_strg + 40, 40)
ticks_strg = np.arange(start_strg + 40, end_strg, 40)
norm_strg = mcolors.TwoSlopeNorm(vmin=start_strg, vcenter=0, vmax=end_strg)

# Graph
fig = plt.figure(figsize=(12, 8), dpi=200)
ax = plt.axes(projection=ccrs.Mollweide(central_longitude=180))

im = ax.contourf(
    ds[lon_name], ds[lat_name], da_strg,
    levels=levels_strg, transform=ccrs.PlateCarree(),
    cmap="RdBu_r", norm=norm_strg,
    extend="both",
)

plt.title(title_strg, fontsize=18, fontweight="bold", pad=16)

# Map
ax.coastlines(linewidth=0.9)
ax.gridlines(linewidth=0.5, color="k", alpha=0.3, linestyle="--")

# Colorbar
cb = plt.colorbar(im, ax=ax, orientation="horizontal", pad=0.05, shrink=0.9, aspect=30)
cb.set_label(title_cbar, fontsize=16, fontweight="bold")
cb.set_ticks(ticks_strg)
cb.ax.set_xticklabels([f"{t:.0f}" for t in ticks_strg])
cb.ax.tick_params(labelsize=15)

plt.savefig(png_strg, bbox_inches="tight")
plt.close()
