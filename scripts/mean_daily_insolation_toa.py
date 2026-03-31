import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap, BoundaryNorm
import numpy as np

# Variables
nc_file = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/data/top-down-short-zonal.nc"
var_name = "avg_tdswrf"
lat_name = "lat"
lon_name = "lon"
time_name = "valid_time"

title = "Mean daily insolation at TOA from ERA5 (1991-2020)"
cbar_label = "Radiation Flux (W m$^{-2}$)"

# Open file
ds = xr.open_dataset(nc_file)
da = ds[var_name]                     
da2 = da.isel({lon_name: 0})     
months = np.arange(1, 13)
Z = da2.transpose(lat_name, time_name).values
lats = ds[lat_name].values

# Colormap
vmin = float(np.nanmin(Z))
vmax = float(np.nanmax(Z))
start = int(np.floor(vmin / 20.0) * 20.0)
end   = int(np.floor(vmax / 20.0) * 20.0)

levels = np.arange(start, end + 20.0, 20.0)
ticks  = np.arange(start, end + 20.0, 60.0)

# Assign 0 values as white
cmap = plt.get_cmap('turbo', len(levels) - 1)
newcolors = cmap(np.linspace(0, 1, len(levels) - 1))
zero_index = np.digitize([0], levels)[0] - 1

if 0 <= zero_index < len(newcolors):
    newcolors[zero_index] = [1, 1, 1, 1]

custom_cmap = ListedColormap(newcolors)
norm = BoundaryNorm(levels, custom_cmap.N)

# Graph
plt.figure(figsize=(8, 6), dpi=200)

month_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
yt_labels = ["90°S", "60°S", "30°S", "0°", "30°N", "60°N", "90°N"]

im = plt.contourf(
    months, lats, Z,
    levels=levels,
    cmap=custom_cmap, 
    norm=norm, 
    extend='neither'
)

plt.xticks(months, month_labels, fontsize=11)
plt.yticks(np.arange(-90, 91, 30), yt_labels, fontsize=11)
plt.xlabel("Months", fontsize=11, fontweight="bold")
plt.ylabel("Latitude", fontsize=11, fontweight="bold")
plt.title(title, fontsize=14, fontweight="bold", pad=15)

# Colorbar
cb = plt.colorbar(im, orientation="vertical", pad=0.05, fraction=0.046, aspect=20, shrink=1.0)
cb.set_label(cbar_label, fontsize=11, fontweight="bold")
cb.set_ticks(ticks)
cb.ax.set_yticklabels([f"{t:.0f}" for t in ticks], fontsize=11)

plt.tight_layout()
plt.savefig("/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/graphs/mean_daily_insolation.png", dpi=200)
plt.close()

