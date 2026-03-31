import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# Paths
data_dir = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/data"
graphs_dir = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/graphs"

# Dates to process
pairs = [[("2010", "10"), ("2015", "12")],
        [("2013", "04"), ("2013", "08")],]
labels = {"2010_10": "Oct 2010", "2013_04": "Apr 2013",
          "2013_08": "Aug 2013", "2015_12": "Dec 2015"}

# Local time 
UTC_OFFSET = -5

# Function to manage data
def load_energy(yr, mm):
    tag = f"{yr}_{mm}"
    ds_tisr = xr.open_dataset(f"{data_dir}/tisr_ERA5_{tag}_box.nc")
    ds_sshf = xr.open_dataset(f"{data_dir}/sshf_ERA5_{tag}_box.nc")
    ds_slhf = xr.open_dataset(f"{data_dir}/slhf_ERA5_{tag}_box.nc")
 
    # Extract variables
    tisr = ds_tisr["tisr"].squeeze().mean(dim=["latitude", "longitude"])
    sshf = ds_sshf["sshf"].squeeze().mean(dim=["latitude", "longitude"])
    slhf = ds_slhf["slhf"].squeeze().mean(dim=["latitude", "longitude"])
 
    # Diurnal cycle
    Rn = tisr.rename({"valid_time": "time"}).groupby("time.hour").mean() / 3600
    SH = sshf.rename({"valid_time": "time"}).groupby("time.hour").mean() / -3600
    LE = slhf.rename({"valid_time": "time"}).groupby("time.hour").mean() / -3600
    G = Rn - SH - LE
 
    # Shift UTC
    local_hours = (np.arange(24) + UTC_OFFSET) % 24
    sort_idx = np.argsort(local_hours)
    x = local_hours[sort_idx]
    return x, Rn.values[sort_idx], SH.values[sort_idx], LE.values[sort_idx], G.values[sort_idx]

# Compare in pairs
for pair in pairs:
    data = {f"{yr}_{mm}": load_energy(yr, mm) for yr, mm in pair} 
    all_vals = np.concatenate([np.stack([Rn, SH, LE, G]) for _, Rn, SH, LE, G in data.values()])
    ymin = np.floor(all_vals.min() / 50) * 50 - 20
    ymax = np.ceil(all_vals.max() / 50) * 50 + 20
 
    # Plots
    for yr, mm in pair:
        tag = f"{yr}_{mm}"
        x, Rn, SH, LE, G = data[tag]
 
        plt.figure(figsize=(10, 8), dpi=200)
        plt.plot(x, Rn, color="black", linewidth=2.5)
        plt.plot(x, SH, color="red", linewidth=2.5, linestyle="--")
        plt.plot(x, LE, color="royalblue", linewidth=2.5, linestyle=":")
        plt.plot(x, G,  color="orange", linewidth=2.5, linestyle="-.")
 
        plt.xticks(x[::3], [f"{h:02d}" for h in x[::3]], fontsize=18)
        plt.yticks(fontsize=18)
        plt.ylim(ymin, ymax)
        plt.ylabel(r"W m$^{-2}$", fontsize=18, fontweight="bold")
        plt.xlabel("Hour (local time, UTC-5)", fontsize=18, fontweight="bold")
        plt.title(f"Diurnal Energy Budget from ERA5 ({labels[tag]})\n"
                  "Pichincha - Ecuador", fontsize=20, fontweight="bold", pad=15)
 
        # Inline labels
        plt.text(x[9], Rn[10], "Rn", color="black", fontsize=18)
        plt.text(x[13], SH[12], "SH", color="red", fontsize=18)
        plt.text(x[9], LE[10], "LE", color="royalblue", fontsize=18)
        plt.text(x[12], G[13], "G", color="orange", fontsize=18)
 
        plt.axhline(0, color="gray", linewidth=0.8, linestyle="--")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{graphs_dir}/diurnal_energy_budget_{tag}.png", dpi=200)
        plt.close()
