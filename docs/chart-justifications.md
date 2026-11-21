# Chart choices and justifications

The report's "why this chart" text comes from this file. For each figure it records what we chose, the alternatives we considered, why we rejected them (with lecture references) and the design decisions we made.

---

## Figure 1: Area burned vs number of fires (two-panel line chart)

**Chosen:** two stacked line charts sharing one time axis. Yearly totals are drawn in grey, with a bold trailing 10-year moving average.

**Why a line chart:** time has a meaningful order. Lecture 3 (p.3) says a line plot shows the trend of y over an ordered x, and the trend is the question (Q1).

**Alternatives considered:**
- **Bar chart of yearly area.** Bars suit comparing discrete categories (L3 p.14). With 76 bars the eye reads individual years, not the long-term trend, and a second series cannot share the axis cleanly.
- **One chart with two y-axes (area and count).** This was rejected because a dual axis lets the designer slide either line up or down and invent a "crossing" point, so the comparison it suggests is arbitrary. Two aligned panels with their own zero baselines keep both honest.
- **Scatter of area vs year with a fitted trend line (L3 p.13).** It is good for relationships but hides the year-to-year sequence that makes 2023 visible as a spike.

**Design decisions (L9 angle, frame and focus; L3 pp.4–6):**
- **Focus:** the context (yearly values) is grey, the signal (the moving average) is in colour, and the 2023 record is annotated in red with its multiple of the next-worst year. This follows the FT example in L3 p.4.
- **Frame:** the years before 1980 are shaded as "incomplete reporting", because several agencies only report fully from the 1970s–80s. That keeps the early rise in fire counts from being misread as a real change.
- **Trailing rather than centred average:** a centred window needs future years, so its last five points would use a shrinking window. A trailing window is computed the same way for every year.
- **Labels and baselines:** labels sit directly on the lines instead of in a legend, both y-axes start at zero, and the wide aspect ratio avoids exaggerating the slope (L3 p.6).

---

## Figure 2: When the land burns (year x month heatmap)

**Chosen:** a heatmap with years as columns and months as rows. Colour shows the hectares burned in that month, on a sequential single-ramp scale (pale to dark).

**Why a heatmap:** we need to show two ordered dimensions at once (76 years x 8 months = 608 cells) on one page. A heatmap is the densest honest view of a grid of magnitudes. The instructor's own research figures in L1 use heatmaps with colour bars, and Plotly Express covers `density_heatmap`/`imshow` (L19).

**Alternatives considered:**
- **Small multiples of 76 monthly line charts:** each panel would be tiny, and the seasonal band would disappear.
- **Stacked bars per year, split by month:** every month after the first has a floating baseline, so its segments cannot be compared across years (L3 p.17 shows stacked bars working only for a few parts).
- **Radial (polar) season chart for every year:** these overlap into clutter, and rose charts make area grow with the square of the value (L11 p.9).

**Design decisions:**
- **Square-root colour scale, not linear or log.** A linear scale leaves all but a dozen cells pale. A log scale (first draft) turned almost every summer cell near-black and hid the extremes. Square root keeps zero at zero and stays monotonic, so the record months still stand out. The scale is stated on the colour bar.
- **One hue family from pale to dark** (sequential, never a rainbow). Cells under 100 ha are grey, so "almost nothing" reads differently from "small".
- **Frame:** only March–October are shown, since they hold 99.8% of the dated area. That is stated in the caption.
- **Focus:** the 2023 column is outlined, and its record May (6.5 Mha, ranked first of 76 Mays) is called out.

---

## Figure 3: 2023 by jurisdiction (treemap)

**Chosen:** a treemap of 2023's 17.6 Mha. Tile area is proportional to hectares. The four headline jurisdictions are filled in ember and the rest in neutral grey; the seven smallest are grouped and named in a footnote.

**Why a treemap:** the question is part-to-whole ("how was 2023's total split?"). L8 recommends treemaps over sunbursts when there are many parts (p.14) and suggests highlighting particular tiles with colour (p.15). Area is proportional to value, with consistent scaling (p.17).

**Alternatives considered:**
- **Pie or donut:** 13 slices are unreadable, and angles are harder to judge than lengths or areas (L8 pp.4–5).
- **Ranked bar chart:** more precise for comparing values one against another. But the point here is the share of one year's total, and Figure 6 already uses ranked bars for the all-time comparison, so a different form avoids repeating it.
- **Choropleth of 2023:** larger provinces would look more important simply because of their size, not because of the hectares burned.

**Design decisions:** in an early draft the tiles were coloured by size, which repeated what area already showed (a value ramp on categories is an anti-pattern). Colour now carries only the focus (L9 p.24). Labels sit inside the tiles, and narrow tiles get wrapped labels.

---

## Figure 4: cause share of fires vs area (two waffle charts)

**Chosen:** two 10x10 waffle charts side by side. Each square is 1% of all fires (left) or of all hectares burned (right), coloured by cause, with large direct percentage labels.

**Why waffles:** the story is a contrast of two part-to-whole splits (54% of fires are human-caused but only 12% of the area). Waffles make percentages countable and always sum to 100 (L8 pp.18–19). We used largest-remainder rounding so that each grid holds exactly 100 squares (L8 p.3: parts must sum to 100%).

**Alternatives considered:**
- **Two pies:** comparing angles across two pies is weak (L8 p.4).
- **Grouped bars:** precise, but they lose the "share of a whole" reading.
- **Sankey from cause to size class:** considered and dropped at the design stage (L9 p.12, "learn to kill it"). It would need far more ink to say the same thing, and its many cause-to-size flows would cross (L10 p.6).

**Design decisions:** the squares are drawn directly in Matplotlib rather than through `pywaffle`, because pywaffle overrides the figure layout and the titles collided. Corners are slightly rounded and gaps are even. Unknown is grey on purpose, so it recedes.

---

## Figure 5: two fire seasons (radar chart)

**Chosen:** a radar (closed polar line) chart with one spoke per month. The radius is each cause's share of its own fires, with a reading guide and two headline numbers beside it.

**Why radar:** months are cyclic. December sits next to January, and a radar shows the shape of a season at a glance (L11 p.5). Normalising within each cause compares timing, not volume.

**Alternatives considered:**
- **Polar bar (rose) chart:** rejected because a rose chart's area grows with the square of the value, which exaggerates peaks (L11 pp.9, 12).
- **Grouped bar chart of 12 months:** accurate, but it breaks the cycle at December–January, and the two seasonal shapes are harder to see.
- **Line chart:** a valid alternative (L11 p.8 shows the same data as a line chart). We kept the radar because the cyclic shape is the message.

**Design decisions:** the loop is closed (L11 p.6). Lines carry the identity and the fills are very light. Direct peak annotations replace a legend, and the ring labels sit on the left of the spoke so they stay clear of the data.

---

## Figure 6: where each cause burns (ranked stacked horizontal bars)

**Chosen:** horizontal bars of total area by agency, split by cause, ranked by total, starting at zero, with a direct total and a lightning-share label on each bar.

**Why:** we are comparing magnitudes across 13 categories, which is the bar chart's job (L3 p.14). Horizontal bars keep the long names readable, the ranking makes the order meaningful (L3 p.19), and the zero baseline keeps lengths honest (L3 p.18).

**Alternatives considered:**
- **Choropleth by province:** shows geography but not magnitude precisely, and big territories dominate visually. Figure 10 covers geography instead.
- **Grouped bars by cause:** three bars x 13 agencies is cluttered.
- **100% stacked bars:** these would hide that the East barely burns at all.

---

## Figure 7: a few huge fires do almost all the burning (mirrored log histogram)

**Chosen:** a two-panel histogram on one log-scaled size axis, with the share of fires above and the share of area burned mirrored below. Bars at 200 ha or more are highlighted in ember.

**Why:** Q3 asks about the shape of the size distribution and where the area comes from. A histogram shows shape (L7 pp.3–5). Fire size spans eight orders of magnitude, so a log x-axis is needed. Mirroring two percentages on the same bins shows the counts and the area pulling apart. Both panels are percentages, so this is not a dual-axis chart.

**Alternatives considered:**
- **Linear histogram:** every fire falls in the first bin.
- **Cumulative-share (Lorenz-style) curve:** strong for the "1% to 85%" claim, but abstract for a general audience. We quote that figure in the text instead.
- **Box plot:** hides the bimodal count-vs-area shape.

**Design decisions:** the bins are aligned so that 200 ha (the CNFDB large-fire threshold) is a bin edge, and there are four bins per decade, which gives appropriate detail (L7 p.5). The spike at 0.1 ha is a reporting-precision artefact, and the caption says so.

---

## Figure 8: escaped lightning fires are getting bigger (boxen by decade)

**Chosen:** boxen (letter-value) plots of fire size per decade, split by cause, on a log axis, with the median of each lightning decade labelled. Only fires that grew to at least 1 ha are included.

**Why boxen:** the question is about both the typical fire and the tail. L12 p.10 says boxen plots convey more about the shape, "particularly in the TAILS". Box and violin plots are also good for comparing many categories (L7 pp.10, 14).

**Alternatives considered:**
- **Box plot:** it collapses the tail into whiskers and outliers, and with 100k+ points per group the outliers become a solid smear.
- **Violin:** the KDE is smoothed over a log scale with a heavy reporting spike at 0.1 ha, so the bandwidth choice would dominate the shape (L13 p.8).
- **Line of median by decade:** this drops the distribution entirely.

**Framing decision:** fires under 1 ha were removed. They are mostly recorded at a fixed 0.1 ha precision, and that pile-up distorted every box. Fires of 1 ha or more (28% of fires) are the ones that "escape", so the result answers a cleaner question. The years before 1980 are shaded as incomplete reporting.

---

## Figure 9: burn-scar map, 1972–2024 (GIS map of polygons)

**Chosen:** mapped perimeters of 15,578 fires drawn on Canada's provinces in a Lambert conformal conic projection, coloured by decade on a single sequential ramp. The newest decades are drawn on top.

**Why a map:** Q4 is about geography. A projected map is the only form that shows where the burn belt lies and how recent scars cluster. It extends the lectures' scatter plot of locations (L3) to real perimeters, and the colour follows sequential-palette practice (one hue, pale to dark).

**Alternatives considered:**
- **Choropleth by province:** throws away the within-province pattern, which is the whole point.
- **Hexbin density:** loses the actual fire shapes, which are the most striking and honest evidence.
- **Web Mercator projection:** inflates the North, so Lambert conformal conic (the national atlas standard) is used instead.

**Data handling:** the perimeters were simplified at 1 km tolerance for print. Scars smaller than about 1 km² disappear, but 99.06% of the mapped area is kept, and the subtitle says so. The fire-free high Arctic is cropped.

---

## Figure 10: where fires start, by cause (small-multiple dot maps)

**Chosen:** two dot maps side by side, one dot per fire start (195k lightning and 242k human), with a shared projection and extent.

**Why:** small multiples let the eye compare the two geographies directly. With tiny, translucent dots, the density itself draws the pattern: lightning across the boreal interior, human fires along roads, rivers and the populated south. This is a geographic scatter plot (L3 p.8), with transparency to manage overplotting (L12).

**Alternatives considered:**
- **One map with two colours:** the colours overplot and mix.
- **2D KDE contours (L13):** they smooth away the road and river corridors that explain human ignitions.
- **Choropleth of counts:** loses all the within-province detail.
