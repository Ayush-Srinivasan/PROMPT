from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional


@dataclass(frozen=True)
class PlotTheme:
    fig_bg: str
    ax_bg: str
    fg: str          # text/ticks/spines
    grid: str
    colors: List[str]  # line color cycle


THEMES: Dict[str, PlotTheme] = {
    "light": PlotTheme(
        fig_bg="#ffffff",
        ax_bg="#ffffff",
        fg="#111111",
        grid="#cccccc",
        colors=["#164f77", "#ff7f0e", "#2ca02c", "#d62728"],
    ),
    "dark": PlotTheme(
        fig_bg="#1e1e1e",
        ax_bg="#1e1e1e",
        fg="#ffffff",
        grid="#444444",
        colors=["#ff6b6b","#1E79D4", "#ffae57", "#7fdc7f"],
    ),
    # magenta; for funsies
    "barbie": PlotTheme(
        fig_bg="#1A0F14",   # Night
        ax_bg="#1A0F14",
        fg="#FFF0F6",       # Cream White
        grid="#6A2E4F",     # Rose border
        colors=[
            "#E0218A",      # Barbie Pink
            "#F6A1C3",      # Bubblegum
            "#4AA3DF",      # Contrast blue
            "#7FD6C2",      # Mint accent
        ],
    ),
    "brat": PlotTheme(
        
        fig_bg="#0F120A",    # Deep olive-black
        ax_bg="#0F120A",
        fg="#E6ECD8",        # Soft off-white
        grid="#2A301A",      # Olive grid / border
        colors=[
            "#B4DD13",      # Brat Green (primary curve)
            "#A6F200",      # Acid highlight
            "#6F7A60",      # Muted sage (secondary curve)
            "#E6A700",      # Warm warning / contrast

        ],
        
        #fig_bg="#8ACE00",    # same brat green as UI
        #ax_bg="#8ACE00",
        #fg="#000000",        # hard black text/axes
        #grid="#2A2A00",      # dirty dark grid
        #colors=[
           # "#000000",  # primary curve (black)
           # "#39FF14",  # laser highlight
           # "#004400",  # deep toxic green
           # "#1A531A",  # secondary deep green
        #],
    ),
    # "system" maps to a default; treat as light unless you want OS detection
    "system": PlotTheme(
        fig_bg="#ffffff",
        ax_bg="#ffffff",
        fg="#111111",
        grid="#cccccc",
        colors=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"],
    ),
}


def apply_mpl_theme(fig, ax, theme_name: str) -> PlotTheme:
    t = THEMES.get((theme_name or "system").strip().lower(), THEMES["system"])

    fig.patch.set_facecolor(t.fig_bg)
    ax.set_facecolor(t.ax_bg)

    # ticks / labels / title
    ax.tick_params(colors=t.fg)
    ax.xaxis.label.set_color(t.fg)
    ax.yaxis.label.set_color(t.fg)
    ax.title.set_color(t.fg)

    # spines
    for spine in ax.spines.values():
        spine.set_color(t.fg)

    # grid
    ax.grid(True, color=t.grid, alpha=0.6)

    if hasattr(ax, "zaxis"):
        ax.zaxis.label.set_color(t.fg)

        ax.xaxis._axinfo["grid"]["color"] = t.grid
        ax.yaxis._axinfo["grid"]["color"] = t.grid
        ax.zaxis._axinfo["grid"]["color"] = t.grid

        ax.xaxis._axinfo["tick"]["color"] = t.fg
        ax.yaxis._axinfo["tick"]["color"] = t.fg
        ax.zaxis._axinfo["tick"]["color"] = t.fg

    return t