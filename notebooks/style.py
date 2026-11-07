"""Shared figure style for the Canada on Fire report.

Every figure notebook starts with:

    import style
    style.apply()

and colours figures only with the constants below, so the whole report reads as one set.
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

FIGURES = Path(__file__).resolve().parent.parent / "figures"

# Widths in inches for a 12pt LaTeX article with 1in margins (\textwidth = 6.5in)
FULL_WIDTH = 6.5
HALF_WIDTH = 3.15

# Ink and chrome
INK = "#0b0b0b"         # titles, primary text
SECONDARY = "#52514e"   # annotations, tick labels
MUTED = "#898781"       # axis labels, minor notes
GRID = "#e1e0d9"        # hairline gridlines
AXIS = "#c3c2b7"        # baselines and axis lines
LAND = "#f3f2ee"        # province fill on maps
BORDER = "#c3c2b7"      # province outlines on maps

# Cause colours: the same in every figure. Blue/orange pass the colour-blind checks on white;
# Unknown is a de-emphasised grey and is always labelled.
CAUSE_COLORS = {"Human": "#2a78d6", "Lightning": "#eb6834", "Unknown": "#94928b"}
CAUSE_ORDER = ["Lightning", "Human", "Unknown"]

# Single-series emphasis: neutral for context, ACCENT for the thing the reader should look at
NEUTRAL = "#94928b"
ACCENT = "#d24a24"

# Sequential "heat" ramp for magnitude (heat map, choropleth, burn maps). Lightness falls evenly,
# light (near zero) to dark (most area burned).
HEAT_STEPS = ["#fdf1e7", "#fbd3b5", "#f6a77c", "#ec7446", "#d24a24", "#a3300f", "#6b1d08"]
HEAT = LinearSegmentedColormap.from_list("heat", HEAT_STEPS)


def apply():
    """Set matplotlib defaults for every report figure."""
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 8.5,
        "axes.titlesize": 9,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 8,
        "axes.labelsize": 8.5,
        "axes.labelcolor": SECONDARY,
        "axes.edgecolor": AXIS,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "grid.linestyle": "-",
        "xtick.color": AXIS,
        "ytick.color": AXIS,
        "xtick.labelcolor": SECONDARY,
        "ytick.labelcolor": SECONDARY,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "xtick.major.size": 3,
        "ytick.major.size": 0,
        "lines.linewidth": 1.6,
        "lines.solid_capstyle": "round",
        "lines.solid_joinstyle": "round",
        "legend.fontsize": 8,
        "legend.frameon": False,
        "legend.handlelength": 1.2,
        "legend.handleheight": 0.9,
        "text.color": INK,
        "figure.dpi": 110,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
        "pdf.fonttype": 42,     # embed real fonts so text stays selectable in the PDF
    })


def ygrid(ax):
    """Hairline horizontal gridlines only."""
    ax.yaxis.grid(True)
    ax.xaxis.grid(False)


def map_axes(ax):
    """Strip axes from a map panel."""
    ax.set_axis_off()
    ax.set_aspect("equal")


def save(fig, name):
    """Save a figure as PDF (for LaTeX) and PNG (for quick previews) in figures/."""
    FIGURES.mkdir(exist_ok=True)
    fig.savefig(FIGURES / f"{name}.pdf")
    fig.savefig(FIGURES / f"{name}.png", dpi=200)
    plt.show()
