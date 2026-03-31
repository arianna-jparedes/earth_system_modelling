import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator

# Paths
data_dir = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/data"
graphs_dir = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/graphs"

# Pairs to compare with shared axes
pairs = [[("2010", "10"), ("2015", "12")],
        [("2013", "04"), ("2013", "08")],]
labels = {"2010_10": "Oct 2010", "2013_04": "Apr 2013",
          "2013_08": "Aug 2013", "2015_12": "Dec 2015"}

# Local time offset
UTC_OFFSET = -5

# Function to manage data
def load_water(yr, mm):
    tag = f"{yr}_{mm}"
    ds_pev = xr.open_dataset(f"{data_dir}/pev_ERA5_{tag}_box.nc")
    ds_tp = xr.open_dataset(f"{data_dir}/tp_ERA5_{tag}_box.nc")
    ds_e = xr.open_dataset(f"{data_dir}/e_ERA5_{tag}_box.nc")
    ds_t2m = xr.open_dataset(f"{data_dir}/t2m_ERA5_{tag}_box.nc")

    # Extract variables
    pev = ds_pev["pev"].squeeze().mean(dim=["latitude", "longitude"])
    tp = ds_tp["tp"].squeeze().mean(dim=["latitude", "longitude"])
    e = ds_e["e"].squeeze().mean(dim=["latitude", "longitude"])
    t2m = ds_t2m["t2m"].squeeze().mean(dim=["latitude", "longitude"])

    # Diurnal cycle
    pev = pev.rename({"valid_time": "time"}).groupby("time.hour").mean() * -1000 * 24
    tp = tp.rename({"valid_time": "time"}).groupby("time.hour").mean() *  1000 * 24
    e = e.rename({"valid_time": "time"}).groupby("time.hour").mean() * -1000 * 24
    t2m = t2m.rename({"valid_time": "time"}).groupby("time.hour").mean() - 273.15

    # Shift UTC
    local_hours = (np.arange(24) + UTC_OFFSET) % 24
    sort_idx = np.argsort(local_hours)
    x = local_hours[sort_idx]
    return x, pev.values[sort_idx], tp.values[sort_idx], e.values[sort_idx], t2m.values[sort_idx]

# To compare in pairs
for pair in pairs:
    data = {f"{yr}_{mm}": load_water(yr, mm) for yr, mm in pair}
    all_flux = np.concatenate([np.stack([pev, tp, e]) for _, pev, tp, e, _ in data.values()])
    all_t2m = np.concatenate([t2m for _, _, _, _, t2m in data.values()])

    ymin_flux = np.floor(all_flux.min() / 0.5) * 0.5 - 0.2
    ymax_flux = np.ceil(all_flux.max()  / 0.5) * 0.5 + 0.2
    ymin_t2m = np.floor(all_t2m.min()) - 0.5
    ymax_t2m = np.ceil(all_t2m.max())  + 0.5

    # Plots
    for yr, mm in pair:
        tag = f"{yr}_{mm}"
        x, pev, tp, e, t2m = data[tag]

        fig, ax1 = plt.subplots(figsize=(10, 8), dpi=200)
        ax1.plot(x, pev, color="black", linewidth=2)
        ax1.plot(x, tp, color="royalblue", linestyle="--", linewidth=2)
        ax1.plot(x, e, color="orange", linestyle=":", linewidth=2)

        ax1.set_xticks(x[::3])
        ax1.set_xticklabels([f"{h:02d}h" for h in x[::3]], fontsize=16)
        ax1.tick_params(axis="y", labelsize=14)
        ax1.set_xlabel("Hour (local time, UTC-5)", fontweight="bold", fontsize=16)
        ax1.set_ylabel("mm day$^{-1}$", fontweight="bold", fontsize=16)
        ax1.set_ylim(ymin_flux, ymax_flux)

        # Right y-axis for temperature
        ax2 = ax1.twinx()
        ax2.plot(x, t2m, color="darkred", linewidth=2)
        ax2.set_ylabel("Temperature (°C)", fontweight="bold", fontsize=16, color="darkred")
        ax2.tick_params(axis="y", labelcolor="darkred", labelsize=16)
        ax2.set_ylim(ymin_t2m, ymax_t2m)

        ax1.yaxis.set_major_locator(LinearLocator(6))
        ax2.yaxis.set_major_locator(LinearLocator(6))
        ax1.yaxis.set_major_formatter(plt.FormatStrFormatter("%.1f"))
        ax2.yaxis.set_major_formatter(plt.FormatStrFormatter("%.1f"))

        # Inline labels
        ax1.text(x[21], pev[18], "PET", color="black", va="center", fontsize=16)
        ax1.text(x[11], tp[12], "P", color="royalblue", va="center", fontsize=16)
        ax1.text(x[15], e[16], "E", color="orange", va="center", fontsize=16)
        ax2.text(x[21], t2m[20], "T2M", color="darkred", va="center", fontsize=16)

        plt.title(f"Diurnal Water Cycle from ERA5 ({labels[tag]})\n"
                  "Pichincha - Ecuador",
                  fontsize=18, fontweight="bold", pad=15)
        ax1.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{graphs_dir}/diurnal_water_cycle_{tag}.png", dpi=200)
        plt.close()
