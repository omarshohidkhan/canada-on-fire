# Canada on Fire: design and build plan

COMP 6934 course project, Group 15. Written 2026-11-21. The final report is due Fri Dec 18, 11:59 p.m. NT.

## Intent

Tell one clear, evidence-based story about seven decades of Canadian wildfires using the Canadian National Fire Database (CNFDB). It answers the four questions from the approved proposal. The report is an 8-page LaTeX document (12pt), and runnable Python reproduces every figure exactly.

## Rules we hold ourselves to

These come from the course (L1 p.30, L3, L7, L8, L9, L11, L13).

- Every figure makes one point. Its title is the finding, and its caption states what it shows and what it supports.
- Angle, frame, focus. Highlight the focal element in colour, keep the context grey, and annotate the key numbers.
- Bars start at zero and are sorted by value. Part-to-whole charts sum to 100%.
- Choose bin widths and KDE bandwidths for appropriate detail, and avoid rose charts, which exaggerate area.
- Use one palette that colour-blind readers can tell apart, the same type sizes everywhere, and a source line on every figure.
- Use only course tools: Matplotlib, Seaborn, squarify, pywaffle and Plotly Express. There is no GeoPandas or Folium; maps are built from latitude/longitude scatter plots and KDE contours.
- Kill any figure that does not earn its place.

## Data decisions (assumption log)

- **Source:** `NFDB_point_20260811.txt` (CNFDB point data, NRCan, Open Government Licence – Canada).
- **Years:** keep 1950–2025. Drop `YEAR = -999` and the pre-1950 rows (171 records).
- **Cause:** H = Human, N = Lightning (natural), U = Unknown. Unknown is always shown in grey, never dropped silently.
- **Month:** seasonal figures drop `MONTH = 0`, the 3,725 records with an unknown month.
- **Size:** log-scale figures exclude `SIZE_HA = 0` (40,028 records). Area totals keep them, since they add 0 ha anyway.
- **Reporting coverage:** several agencies report fully only from the 1970s–80s (ON 1976, SK 1981, NB 1989). Trend figures shade the years before 1980, and comparisons by decade are read with that caveat. The report says this explicitly.
- **PC:** the Parks Canada agency is kept as its own category ("Parks Canada").

## Figure lineup

| # | Question | Plot type (lecture) | Point it supports |
|---|---|---|---|
| 1 | Q1 | Line + 10-yr moving average, 2 panels (L3) | Area burned rises while the number of fires falls; 2023 is double any other year |
| 2 | Q1 | Year x month heatmap (L19, instructor examples) | When each season burns; how 2023's season compares |
| 3 | Q1 | Treemap of 2023 area by province (L8) | The 2023 fires were spread across the country |
| 4 | Q2 | Two waffle charts (L8) | Humans start most fires, but lightning burns most of the area |
| 5 | Q2 | Radar line chart by month (L11) | Human fires peak in spring (May); lightning fires peak in summer (Jul) |
| 6 | Q2 | Sorted horizontal stacked bars (L3) | Where each cause burns: the North and the Prairies are lightning-dominated |
| 7 | Q3 | Log-histogram + cumulative-share line (L7) | 1% of fires make up about 85% of the area |
| 8 | Q3 | Boxen by decade (L12) | How typical and extreme fire sizes changed by decade |
| 9 | Q4 | Lat/lon scatter + KDE contours, two eras (L3, L13) | Where the hotspots are; whether large fires shifted north |

That is 9 figures of 9 distinct types, against a minimum of 5. Any figure that proves weak when rendered is cut (L9 p.12).

## Visual system

- **Page fit:** figures are sized to the LaTeX text width of 6.5 in (letter, 1 in margins). Full width is 6.5 in; half width is 3.15 in. They are saved as vector PDFs plus PNG previews and included at 100% scale.
- **Type:** Helvetica Neue (DejaVu Sans as fallback). Titles are 10.5pt bold, labels and ticks 8.5pt, notes and source lines 7pt grey.
- **Colours:** Lightning `#E08A00` (amber), Human `#1F5A99` (blue), Unknown `#9A9A9A` (grey), context `#C8C8C8`, ink `#222222`. The heatmap uses a sequential fire ramp (YlOrRd / "rocket_r"). The cause colours stay distinct under the common types of colour blindness.
- **Furniture:** no top or right spines, and light horizontal grid lines only where values are read. Labels sit directly on the data rather than in legends wherever possible.

## Build structure

```
Project/
  code/fire_data.py       load + clean + derived columns (single source of truth)
  code/style.py           rcParams, palette, helpers (titles, source line, save)
  canada_on_fire.ipynb    narrative notebook: one section per question, one cell per figure
  figures/                figN_name.pdf + .png (generated, never hand-edited)
  requirements.txt
  docs/design-and-plan.md
```

## Plan

1. Write `fire_data.py` and check it against the profile numbers (448,618 rows; 2023 = 17.6 Mha).
2. Write `style.py`, the shared look.
3. Build the figures one at a time. After each one, render it, inspect the PNG, and refine it until it is clean. Record the key numbers each caption needs.
4. Assemble the notebook: a markdown note before each figure stating its point and caption draft.
5. Verify reproducibility: run the notebook top to bottom with `jupyter nbconvert --execute` in a clean kernel and confirm that every figure regenerates.
6. Review the full set together for consistency, and cut or merge to fit 8 pages.
7. Build the companion website: the whole report as one modern scrolling page. The charts are interactive (Plotly Express, L19), built from `fire_data.py`. Large data is pre-aggregated so the page stays light. It uses the same palette and story order as the report and links to the PDF and code. Hosting is decided with the group at the end.
8. Write the LaTeX report.
9. Review the teammates' work.
