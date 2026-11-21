"""Generate canada_on_fire.ipynb (the narrative notebook) from the figure list.

Run:  python code/build_notebook.py
Then: jupyter nbconvert --to notebook --execute --inplace canada_on_fire.ipynb
"""
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
C = []

C.append(md("""# Canada on Fire: Seven Decades of Wildfire Patterns, Causes and Extremes
**COMP 6934: Introduction to Data Visualization · Fall 2026 · Group 15**

This notebook reproduces every figure in the report, in report order. All cleaning lives in `code/fire_data.py`, the visual system in `code/style.py`, and each figure is one function in `code/figures.py`. Running the notebook top to bottom regenerates `figures/*.pdf` (for LaTeX) and `figures/*.png` (previews).

**Data:** Canadian National Fire Database (CNFDB), Canadian Forest Service, Natural Resources Canada, https://cwfis.cfs.nrcan.gc.ca/en/fire-history, Open Government Licence – Canada. Point data `NFDB_point_20260811.txt`; burned-area polygons 1972–2024.

**Questions**
1. Is the area burned each year increasing, and how unusual was 2023?
2. How do lightning- and human-caused fires differ in where they happen, when they happen, and how big they get?
3. Do a small number of very large fires account for most of the burned area, and has the typical fire size changed by decade?
4. Where are Canada's main wildfire hotspots, and have they shifted over time?"""))
C.append(code("""import sys
from pathlib import Path
sys.path.insert(0, str(Path("code").resolve()))

import matplotlib.pyplot as plt
import pandas as pd
import fire_data as fd
import style as st
import figures as F

st.apply()
%matplotlib inline"""))
C.append(md("""## 1. Data and cleaning decisions
- Years kept: 1950–2025 (drops `YEAR = -999` and 171 sparse pre-1950 records).
- Cause: H = Human, N = Lightning, U = Unknown (kept, shown in grey).
- Seasonal figures drop records with unknown month (`MONTH = 0`).
- Several agencies only report fully from the 1970s–80s, so trend figures shade the years before 1980.
- The burned-area polygons are simplified to 1 km by `code/prepare_geo.py`, which keeps 99.06% of the mapped area. Run that script once before the maps."""))
C.append(code("""df = fd.load_fires()
print(f"{len(df):,} fires, {df.YEAR.min()}–{df.YEAR.max()}")
df.head()"""))
C.append(code("""summary = df.groupby("cause", observed=True).agg(
    fires=("SIZE_HA", "size"),
    area_Mha=("SIZE_HA", lambda s: s.sum() / 1e6),
    median_ha=("SIZE_HA", "median"))
summary.round(2)"""))

FIGS = [
    ("Q1: Is the area burned increasing, and how unusual was 2023?", [
        ("fig1_trend", "Figure 1: Fewer fires, more land burned",
         "The 10-year average area burned has risen while the number of fires has fallen since the "
         "early 1990s; 2023 (17.6 Mha) burned about twice the next-worst year."),
        ("fig2_season_heatmap", "Figure 2: When the land burns",
         "Burning is concentrated in May–August (97% of dated area). 2023 started early, with the "
         "largest May on record (6.5 Mha)."),
        ("fig3_treemap_2023", "Figure 3: 2023 by jurisdiction",
         "2023 was national, not regional: Quebec, NWT, BC and Alberta each burned 2–4 Mha, together "
         "77% of the year's total."),
    ]),
    ("Q2: How do lightning and human fires differ?", [
        ("fig4_waffle_cause", "Figure 4: Share of fires vs share of area",
         "People start 54% of fires but cause only 12% of the area burned; lightning starts 44% but "
         "burns 84%."),
        ("fig5_radar_season", "Figure 5: Two fire seasons",
         "Human fires peak in May (spring, before green-up); 90% of lightning fires start in June–August."),
        ("fig6_region_cause", "Figure 6: Where each cause burns",
         "The NWT (96% lightning) and the Prairie provinces dominate area burned; the Maritimes barely burn."),
    ]),
    ("Q3: Do a few huge fires dominate, and has typical size changed?", [
        ("fig7_size_histogram", "Figure 7: A few huge fires do almost all the burning",
         "Fires of 200 ha or more are 4.8% of fires but 98.9% of the area burned; 72% of fires stay "
         "under 1 ha."),
        ("fig8_boxen_decade", "Figure 8: Escaped lightning fires are getting bigger",
         "Among fires that grow past 1 ha, the median lightning fire rose from 6 ha (1990s) to 50 ha "
         "(2020s); human fires did not change."),
    ]),
    ("Q4: Where are the hotspots, and have they shifted?", [
        ("fig9_burn_scars", "Figure 9: Half a century of burn scars",
         "Burning follows one boreal belt from Yukon to Quebec; the newest scars concentrate in the NWT, "
         "northern Alberta/Saskatchewan and northern Quebec."),
        ("fig10_ignition_maps", "Figure 10: Where fires start, by cause",
         "Lightning ignitions spread across the remote interior; human ignitions trace roads, rivers "
         "and the populated south."),
    ]),
]
for i, (section, figs) in enumerate(FIGS, start=2):
    C.append(md(f"## {i}. {section}"))
    for fn, title, point in figs:
        C.append(md(f"### {title}\n**Point this figure supports:** {point}"))
        C.append(code(f'fig, facts = F.{fn}(df)\nst.save(fig, "{fn}")\nplt.show()\nfacts'))

C.append(md("""## 6. Conclusions (draft)
1. **Q1:** Area burned is rising even as fires become fewer, and 2023 was an outlier in both size and timing.
2. **Q2:** The two causes are different problems. Human fires are frequent, early-season and near people; lightning fires are fewer, mid-summer, remote, and responsible for most of the area.
3. **Q3:** Area burned is extremely concentrated in rare large fires, and the escaped lightning fires are getting larger.
4. **Q4:** The boreal belt is stable in location, but recent decades concentrate in the NWT and northern Quebec."""))

nb = nbf.v4.new_notebook()
nb["cells"] = C
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nbf.write(nb, ROOT / "canada_on_fire.ipynb")
print("notebook written:", len(C), "cells")
