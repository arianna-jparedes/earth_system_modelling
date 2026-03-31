import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator

# Paths
fn1 = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/data/pev_pichincha_mean.nc"
fn2 = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/data/tp_pichincha_mean.nc"
fn3 = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/data/e_pichincha_mean.nc"
fn4 = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/data/t2m_pichincha_mean.nc"

# Files
ds1 = xr.open_dataset(fn1)
ds2 = xr.open_dataset(fn2)
ds3 = xr.open_dataset(fn3)
ds4 = xr.open_dataset(fn4)

# Extract variables
pev = ds1["pev"].squeeze()*-1000
tp = ds2["tp"].squeeze()*1000
e = ds3["e"].squeeze()*-1000
t = ds4["t2m"].squeeze()-273.15

# Graph
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
x = np.arange(12)
fig, ax1 = plt.subplots(figsize=(11,8), dpi=200)
ax1.plot(x, pev.values, color="black", linewidth=2)
ax1.plot(x, tp.values, color="royalblue", linestyle="--", linewidth=2)
ax1.plot(x, e.values, color="orange", linestyle=":", linewidth=2)
ax1.set_xticks(x)
ax1.set_xticklabels(months, fontsize=16)
ax1.tick_params(axis="y", labelsize=16)
ax1.set_xlabel("Months", fontweight="bold", fontsize=16)
ax1.set_ylabel("mm day$^{-1}$", fontweight="bold", fontsize=16)

# Right y axis
ax2 = ax1.twinx()
ax2.plot(x, t.values, color="darkred", linewidth=2)
ax2.set_ylabel("Temperature (°C)", fontweight="bold", fontsize=16, color="darkred")
ax2.tick_params(axis="y", labelcolor="darkred", labelsize=16)
ax1.yaxis.set_major_locator(LinearLocator(6))
ax2.yaxis.set_major_locator(LinearLocator(6))
ax1.yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
ax2.yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))

# Inline labels
ax1.text(x[8] + 0.3, pev.values[8] + 0.3, "PET", color="black", va="center", fontsize=16)
ax1.text(x[1] + 0.3, tp.values[1] + 0.3, "P", color="royalblue", va="center", fontsize=16)
ax1.text(x[3] + 0.3, e.values[3] + 0.3, "E", color="orange", va="center", fontsize=16)
ax2.text(x[6] + 0.3, t.values[6] + 0.1, "T2M", color="darkred", va="center", fontsize=16)
plt.title("Water Balance from ERA5 (Pichincha-Ecuador)", fontsize=18, fontweight="bold", pad=15)
ax1.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/graphs/pichincha_hydro_cycle.png", dpi=200)
plt.close()
