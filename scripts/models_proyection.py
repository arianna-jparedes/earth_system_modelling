import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import numpy as np
import matplotlib.colors as mcolors
from pathlib import Path

# Paths
data_dir = Path("/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/data")
out_dir = Path("/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/graphs")

# Models
models = [(data_dir / "proy_miroc6.nc", "MIROC6"),
          (data_dir / "proy_mri.nc", "MRI-ESM2-0"),
          (data_dir / "proy_nor.nc", "NorESM2-MM")]

# Variables
variables = {
    "t2m": {
        "title_cbar": "Projected Surface Air Temperature (K)",
        "cmap": "RdBu_r",
        "out": out_dir / "change_t2m.png",
        "vmin": -2, "vmax": 10, "step": 2,
    },
    "tp": {
        "title_cbar": "Projected Precipitation (mm day⁻¹)",
        "cmap": "BrBG",
        "out": out_dir / "change_tp.png",
        "vmin": -3, "vmax": 3, "step": 1,
    },
    "e": {
        "title_cbar": "Projected Evapotranspiration (mm day⁻¹)",
        "cmap": "PiYG",
        "out": out_dir / "change_e.png",
        "vmin": -3, "vmax": 3, "step": 1,
    },
}

for var, meta in variables.items():
    # Load all datasets
    datasets = [(xr.open_dataset(f), label) for f, label in models]

    # Shared colorbar range (Predefine)
    start = meta["vmin"]
    end = meta["vmax"]
    step = meta["step"]
    levels = np.arange(start, end + step, step)
    ticks = np.arange(start, end + step, step*2)
    norm = mcolors.TwoSlopeNorm(vmin=start, vcenter=0.0, vmax=end)
    
    # Graphs
    fig, axes = plt.subplots(1, 3, figsize=(24, 8), dpi=200, subplot_kw={"projection": ccrs.Mollweide(central_longitude=180)})

    for ax, (ds, label) in zip(axes, datasets):
        da = ds[var].isel(time=0)
        
        im = ax.contourf(
            ds["lon"], ds["lat"], da,
            levels=levels, transform=ccrs.PlateCarree(),
            cmap=meta["cmap"], norm=norm, extend="both",
        )
        
        ax.set_title(f"{label} - SSP370 (2070-2100)", fontsize=20, fontweight="bold", pad=10)
        ax.coastlines(linewidth=1.0)
        ax.gridlines(linewidth=0.5, color="k", alpha=0.3, linestyle="--")

        # Graphs
        cb = fig.colorbar(im, ax=ax, orientation="horizontal", pad=0.04, shrink=0.85, aspect=28)
        cb.set_label(meta["title_cbar"], fontsize=18, fontweight="bold")
        cb.set_ticks(ticks)
        cb.ax.set_xticklabels([f"{t:.2g}" for t in ticks], fontsize=18)
        cb.ax.tick_params(labelsize=18)

    plt.tight_layout()
    plt.savefig(meta["out"], bbox_inches="tight")
    plt.close()

    for ds, _ in datasets:
        ds.close()
