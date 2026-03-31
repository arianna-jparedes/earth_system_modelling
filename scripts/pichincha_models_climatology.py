import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Paths
data_dir = Path("/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/data")
out_dir = Path("/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/graphs")

# Load datasets
era5 = xr.open_dataset(data_dir / "era5_monthly_box.nc")
miroc6 = xr.open_dataset(data_dir / "miroc6_monthly_box.nc")
miroc6_ssp = xr.open_dataset(data_dir / "miroc6_ssp370_box.nc")
mri = xr.open_dataset(data_dir / "mri_monthly_box.nc")
mri_ssp = xr.open_dataset(data_dir / "mri_ssp370_box.nc") 
nor = xr.open_dataset(data_dir / "nor_monthly_box.nc")
nor_ssp = xr.open_dataset(data_dir / "nor_ssp370_box.nc")


# Metadata
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

models = [(miroc6, "MIROC6", "#E63946"),
          (mri, "MRI-ESM2-0", "#457B9D"),
          (nor, "NorESM2-MM", "#2A9D8F"),]

models_ssp = [(miroc6_ssp, "MIROC6", "#E63946"),
              (mri_ssp, "MRI-ESM2-0", "#457B9D"),
              (nor_ssp, "NorESM2-MM", "#2A9D8F"),]

variables = {
    "t2m": {
        "title": "Near-Surface Air Temperature – Pichincha \n Historical (1979–2014)",
        "title2": "Near-Surface Air Temperature – Pichincha \n SSP370 (2070–2100)",
        "ylabel": "Temperature (K)",
        "out": out_dir / "clim_t2m_pichincha.png",
        "out2": out_dir / "clim_t2m_pichincha_ssp370.png",
        "era5_factor": 1.0,
        "model_factor": 1.0,
    },
    "tp": {
        "title": "Precipitation – Pichincha \n Historical (1979–2014)",
        "title2": "Precipitation – Pichincha \n SSP370 (2070–2100)",
        "ylabel": "Precipitation (mm day⁻¹)",
        "out": out_dir / "clim_tp_pichincha.png",
        "out2": out_dir / "clim_tp_pichincha_ssp370.png",
        "era5_factor": 1.0,
        "model_factor": 1.0,
    },
    "e": {
        "title": "Evapotranspiration – Pichincha \n Historical (1979–2014)",
        "title2": "Evapotranspiration – Pichincha \n SSP370 (2070–2100)",
        "ylabel": "Evapotranspiration (mm day⁻¹)",
        "out": out_dir / "clim_e_pichincha.png",
        "out2": out_dir / "clim_e_pichincha_ssp370.png",
        "era5_factor": 1.0,
        "model_factor": 1.0,
    },
}

colors_models = ["#E63946", "#457B9D", "#2A9D8F"]
labels_models = ["MIROC6", "MRI-ESM2-0", "NorESM2-MM"]

# Shared y-limits
y_limits = {}
for var in variables:
    all_vals = []
    all_vals.append(era5[var].values.squeeze())
    for (ds, _, _) in models:
        all_vals.append(ds[var].values.squeeze())
    for (ds, _, _) in models_ssp:
        all_vals.append(ds[var].values.squeeze())
    combined = np.concatenate([v.ravel() for v in all_vals])
    margin = (combined.max() - combined.min()) * 0.05
    y_limits[var] = (combined.min() - margin, combined.max() + margin)

# Graphs Historicals
for var, meta in variables.items():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=200)

    # ERA5
    era5_vals = era5[var].values.squeeze()
    ax.plot(range(1, 13), era5_vals, color="black", linewidth=2.5,
            linestyle="-", marker="o", markersize=6, label="ERA5", zorder=5)

    # Models
    for (ds, label, color) in models:
        vals = ds[var].values.squeeze()
        ax.plot(range(1, 13), vals, linewidth=2, linestyle="--",
                marker="s", markersize=5, color=color, label=label)

    ax.set_title(meta["title"], fontsize=16, fontweight="bold", pad=12)
    ax.set_ylabel(meta["ylabel"], fontsize=14, fontweight="bold")
    ax.set_xlabel("Month", fontsize=14, fontweight="bold")
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(months, fontsize=14)
    ax.tick_params(labelsize=14)
    ax.legend(fontsize=14, framealpha=0.9)
    ax.grid(linewidth=0.5, alpha=0.4, linestyle="--")
    ax.set_ylim(y_limits[var])

    plt.tight_layout()
    plt.savefig(meta["out"], bbox_inches="tight")
    plt.close()

era5.close()
miroc6.close()
mri.close()
nor.close()

# Graphs Projections
for var, meta in variables.items():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=200)

    # Models
    for (ds, label, color) in models_ssp:
        vals = ds[var].values.squeeze()
        ax.plot(range(1, 13), vals, linewidth=2, linestyle="--",
                marker="s", markersize=5, color=color, label=label)

    ax.set_title(meta["title2"], fontsize=16, fontweight="bold", pad=12)
    ax.set_ylabel(meta["ylabel"], fontsize=14, fontweight="bold")
    ax.set_xlabel("Month", fontsize=14, fontweight="bold")
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(months, fontsize=14)
    ax.tick_params(labelsize=14)
    ax.legend(fontsize=14, framealpha=0.9)
    ax.grid(linewidth=0.5, alpha=0.4, linestyle="--")
    ax.set_ylim(y_limits[var])

    plt.tight_layout()
    plt.savefig(meta["out2"], bbox_inches="tight")
    plt.close()

miroc6_ssp.close()
mri_ssp.close()
nor_ssp.close()

