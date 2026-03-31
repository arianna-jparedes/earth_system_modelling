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
models = [(data_dir / "miroc6_mean.nc", "MIROC6"),
          (data_dir / "mri_mean.nc", "MRI-ESM2-0"),
          (data_dir / "nor_mean.nc", "NorESM2-MM")]

# Variables
variables = {
    "t2m": {
        "title_cbar": "Surface Air Temperature (K)",
        "cmap": "OrRd",
        "out": out_dir / "mean_t2m.png",
        "vmin": 220, "vmax": 300, "step": 10,
    },
    "tp": {
        "title_cbar": "Precipitation (mm day⁻¹)",
        "cmap": "PuBuGn",
        "out": out_dir / "mean_tp.png",
        "vmin": 0, "vmax": 20, "step": 2,
    },
    "e": {
        "title_cbar": "Evapotranspiration (mm day⁻¹)",
        "cmap": "YlGnBu",
        "out": out_dir / "mean_e.png",
        "vmin": 0, "vmax": 10, "step": 1,
    },
}

for var, meta in variables.items():
    # Load all datasets
    datasets = [(xr.open_dataset(f), label) for f, label in models]

    # Shared colorbar range: mean of maxima and mean of minima
    start = meta["vmin"]
    end = meta["vmax"]
    step = meta["step"]
    levels = np.arange(start, end + step, step)
    ticks = np.arange(start, end + step, step*2)
    
    # One figure per variable, 3 panels side by side
    fig, axes = plt.subplots(1, 3, figsize=(24, 8), dpi=200, subplot_kw={"projection": ccrs.Mollweide(central_longitude=180)})

    for ax, (ds, label) in zip(axes, datasets):
        da = ds[var].isel(time=0)
        
        im = ax.contourf(
            ds["lon"], ds["lat"], da,
            levels=levels, transform=ccrs.PlateCarree(),
            cmap=meta["cmap"], extend="both",
        )
        # Title: variable description + model label
        ax.set_title(f"{label} - Historical (1979-2014)", fontsize=20, fontweight="bold", pad=10)
        ax.coastlines(linewidth=1.0)
        ax.gridlines(linewidth=0.5, color="k", alpha=0.3, linestyle="--")

        # Individual colorbar under each panel
        cb = fig.colorbar(im, ax=ax, orientation="horizontal", pad=0.04, shrink=0.85, aspect=28)
        cb.set_label(meta["title_cbar"], fontsize=16, fontweight="bold")
        cb.set_ticks(ticks)
        cb.ax.tick_params(labelsize=16)

    plt.tight_layout()
    plt.savefig(meta["out"], bbox_inches="tight")
    plt.close()

    for ds, _ in datasets:
        ds.close()
