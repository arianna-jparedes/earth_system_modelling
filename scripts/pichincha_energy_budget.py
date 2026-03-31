import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# Paths
fn = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/data/pichincha_energy_means.nc"
ds = xr.open_dataset(fn)

# Extract variables
SH = (-ds["avg_ishf"]).squeeze()
LE = (-ds["avg_slhtf"]).squeeze()
sw = (ds["avg_snswrf"]).squeeze()   
lw = (ds["avg_snlwrf"]).squeeze()    

# Calculate variables
Rn = sw + lw
G = Rn - SH - LE

# Graph
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
x = np.arange(12)

plt.figure(figsize=(8,8), dpi=200)
plt.plot(x, Rn.values, color="black", linewidth=2.0)
plt.plot(x, SH.values, color="red", linewidth=2.0, linestyle="--")
plt.plot(x, LE.values, color="royalblue", linewidth=2.0, linestyle=":")
plt.plot(x, G.values, color="orange", linewidth=2.0, linestyle="-.")

plt.xticks(x, months, fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel(r"W m$^{-2}$", fontsize=14, fontweight="bold")
plt.xlabel("Months", fontsize=14, fontweight="bold")
plt.title("Energy Balance from ERA5 (Pichincha-Ecuador)",
          fontsize=16, fontweight="bold", pad=15)

# Inline labels
plt.text(6, Rn.values[6]+5, "R", color="black", fontsize=14)
plt.text(5, SH.values[5]+5, "SH", color="red", fontsize=14)
plt.text(4, LE.values[4]+5, "LE", color="royalblue", fontsize=14)
plt.text(6, G.values[6]+5, "G", color="orange", fontsize=14)

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/graphs/pichincha_energy_budget.png", dpi=200)
plt.close()
