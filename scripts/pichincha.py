import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import rasterio
import cartopy.mpl.gridliner

# Paths
srtm_file = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/data/pichincha_srtm90.tif"
modis_file = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/data/pichincha_modis_lc.tif"
png_elev = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/graphs/pichincha_elevation.png"
png_veg = "/home/arya/Projects/Earth_System_Physics/earth_system_modelling/earth_system_modelling/graphs/pichincha_vegetation.png"

# Titles
title_elev = "Digital Elevation Model of Pichincha-Ecuador"
title_veg = "Land Cover of Pichincha-Ecuador"
title_cbar_elev = "Elevation (m a.s.l.)"

# Region bounds
LON_W, LON_E = -79.420, -77.801
LAT_S, LAT_N = -0.743, 0.444

# MODIS IGBP land cover classes
MODIS_CLASSES = {
    1:  "Evergreen needleleaf forest",
    2:  "Evergreen broadleaf forest",
    3:  "Deciduous needleleaf forest",
    4:  "Deciduous broadleaf forest",
    5:  "Mixed forest",
    6:  "Closed shrubland",
    7:  "Open shrubland",
    8:  "Woody savanna",
    9:  "Savanna",
    10: "Grassland",
    11: "Permanent wetland",
    12: "Cropland",
    13: "Urban and built-up",
    14: "Cropland / natural veg. mosaic",
    15: "Snow and ice",
    16: "Barren / sparsely vegetated",
    17: "Water",
}

MODIS_COLORS = {
    1:  "#1a6b1a",
    2:  "#006400",
    3:  "#4ca64c",
    4:  "#70b870",
    5:  "#228b22",
    6:  "#c8a86e",
    7:  "#d2b48c",
    8:  "#a0c060",
    9:  "#c8e860",
    10: "#ffff4c",
    11: "#6699cc",
    12: "#f096ff",
    13: "#fa0000",
    14: "#e8c8e8",
    15: "#f0f0f0",
    16: "#b4b4b4",
    17: "#0064c8",
}

proj = ccrs.PlateCarree()

# Province borders (Natural Earth 10m)
provinces = cfeature.NaturalEarthFeature(
    category="cultural",
    name="admin_1_states_provinces",
    scale="10m",
    facecolor="none",
    edgecolor="black",
    linewidth=0.7,
)

def add_map_features(ax):
    ax.set_extent([LON_W, LON_E, LAT_S, LAT_N], crs=proj)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
    ax.add_feature(provinces, zorder=4)
    gl = ax.gridlines(draw_labels=True, linewidth=0.4, color="grey",
                      alpha=0.6, linestyle="--", x_inline=False, y_inline=False)
    gl.top_labels = False
    gl.right_labels = False

# ELEVATION
with rasterio.open(srtm_file) as src:
    elev = src.read(1).astype(float)
    bounds = src.bounds

elev = np.where(elev < -1000, np.nan, elev)

vmin = 0
vmax = np.nanmax(elev)
ticks_elev = np.arange(int(np.floor(vmin / 500) * 500),
                        int(np.ceil(vmax / 500) * 500) + 500, 500)

fig = plt.figure(figsize=(10, 8), dpi=200)
ax = plt.axes(projection=proj)

im = ax.imshow(
    elev,
    cmap="terrain",
    vmin=vmin, vmax=vmax,
    extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
    transform=proj,
    origin="upper",
    interpolation="bilinear",
)

plt.title(title_elev, fontsize=14, fontweight="bold", pad=12)
add_map_features(ax)

cb = plt.colorbar(im, ax=ax, orientation="horizontal", pad=0.08, shrink=0.8, aspect=40)
cb.set_label(title_cbar_elev, fontsize=11, fontweight="bold")
cb.set_ticks(ticks_elev)
cb.ax.set_xticklabels([f"{t:.0f}" for t in ticks_elev])

plt.savefig(png_elev, bbox_inches="tight")
plt.close()

# MODIS LAND COVER
with rasterio.open(modis_file) as src:
    lc = src.read(1)
    bounds_lc = src.bounds

# Mask nodata
lc = np.where(lc == 255, 0, lc)

unique_classes = np.unique(lc[lc > 0])
colors_present = [MODIS_COLORS.get(c, "#cccccc") for c in unique_classes]
cmap_lc = mcolors.ListedColormap(colors_present)
bounds_norm = np.arange(len(unique_classes) + 1) - 0.5
norm_lc = mcolors.BoundaryNorm(bounds_norm, cmap_lc.N)

lc_indexed = np.full_like(lc, np.nan, dtype=float)
for idx, c in enumerate(unique_classes):
    lc_indexed[lc == c] = idx

patches = [
    mpatches.Patch(
        color=MODIS_COLORS.get(c, "#cccccc"),
        label=MODIS_CLASSES.get(c, f"Class {c}"),
    )
    for c in unique_classes
]

fig, ax = plt.subplots(figsize=(10, 6), dpi=200,
                       subplot_kw={"projection": proj})

ax.imshow(
    lc_indexed,
    cmap=cmap_lc, norm=norm_lc,
    extent=[bounds_lc.left, bounds_lc.right, bounds_lc.bottom, bounds_lc.top],
    transform=proj,
    origin="upper",
    interpolation="nearest",
)

plt.title(title_veg, fontsize=14, fontweight="bold", pad=12)
add_map_features(ax)

ax.legend(
    handles=patches,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.08),
    fontsize=8,
    framealpha=0.88,
    title_fontsize=9,
    borderaxespad=0,
    ncol=3,
)

plt.savefig(png_veg, bbox_inches="tight")
plt.close()
