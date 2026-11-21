"""One-off preparation of the map layers (run once; output is reused).

1. NFDB burned-area polygons 1972-2024 (2.5 GB of shapefiles) -> simplified
   GeoPackage at print resolution (1 km tolerance; a 6.5 in map of Canada at
   300 dpi is ~2.5 km per pixel, so nothing visible is lost).
2. Natural Earth admin-1 (public domain) -> Canadian provinces/territories in
   the same Lambert Conformal Conic projection as the NFDB polygons.

Run:  python code/prepare_geo.py
"""
from pathlib import Path

import geopandas as gpd
import pandas as pd
import warnings

import pyogrio

warnings.filterwarnings("ignore", "GeoSeries.notna", UserWarning)

ROOT = Path(__file__).resolve().parents[1]
RAW = next((d for d in (ROOT / "data" / "raw" / "NFDB_poly", ROOT.parent / "ProjectData" / "NFDB_poly")
            if d.exists()), ROOT / "data" / "raw" / "NFDB_poly")
OUT = ROOT / "data_derived"
NE = ROOT / "assets" / "geo" / "ne_admin1" / "ne_10m_admin_1_states_provinces.shp"
COLS = ["SRC_AGENCY", "YEAR", "SIZE_HA", "CAUSE"]
TOLERANCE_M = 1000


def burn_scars():
    parts = []
    for shp in sorted(RAW.glob("NFDB_poly_*.shp")):
        g = pyogrio.read_dataframe(shp, columns=COLS)
        g = g[g.YEAR.between(1972, 2024)]
        g["geometry"] = g.geometry.simplify(TOLERANCE_M, preserve_topology=False)
        g = g[~g.geometry.is_empty & g.geometry.notna()]  # drops <~1 km2 scars; 99.06% of area kept
        parts.append(g)
        print(f"{shp.name}: {len(g):,} polygons")
    scars = pd.concat(parts, ignore_index=True)
    scars = gpd.GeoDataFrame(scars, geometry="geometry", crs=parts[0].crs)
    return scars


def provinces(crs):
    ne = gpd.read_file(NE, columns=["iso_a2", "name", "postal"])
    can = ne[ne.iso_a2 == "CA"].to_crs(crs)
    can["geometry"] = can.geometry.simplify(2000)
    return can


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    scars = burn_scars()
    scars.to_file(OUT / "burn_scars_1972_2024.gpkg", driver="GPKG")
    prov = provinces(scars.crs)
    prov.to_file(OUT / "canada_provinces.gpkg", driver="GPKG")
    print("saved", len(scars), "scars;", len(prov), "provinces; CRS:", scars.crs.name)
