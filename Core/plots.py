from __future__ import annotations

from matplotlib.figure import Figure
from Core.plot_style import apply_mpl_theme


def plot_isp_vs_of(of, isp, *, theme: str = "system"):
    fig = Figure(figsize=(6, 4), dpi=120)
    ax = fig.add_subplot(111)

    t = apply_mpl_theme(fig, ax, theme)
    ax.plot(of, isp, linewidth=2.0, color=t.colors[0])

    ax.set_xlabel("O/F Ratio")
    ax.set_ylabel("Isp (s)")
    ax.set_title("Isp vs O/F Ratio")

    fig.tight_layout()
    return fig


def plot_velocity_vs_of(of, v_exit, cstar=None, *, theme: str = "system"):
    fig = Figure(figsize=(6, 4), dpi=120)
    ax = fig.add_subplot(111)

    t = apply_mpl_theme(fig, ax, theme)
    ax.plot(of, v_exit, linewidth=2.0, color=t.colors[2], label="Exit velocity")

    if cstar is not None:
        ax.plot(of, cstar, linewidth=2.0, color=t.colors[1], label="c*")

    ax.set_xlabel("O/F Ratio")
    ax.set_ylabel("Velocity (m/s)")
    ax.set_title("Velocities vs O/F Ratio")
    ax.legend(facecolor=t.ax_bg, edgecolor=t.grid, labelcolor=t.fg)

    fig.tight_layout()
    return fig


def plot_temp_vs_of(of, t_chamber, t_throat=None, t_exit=None, *, theme: str = "system"):
    fig = Figure(figsize=(6, 4), dpi=120)
    ax = fig.add_subplot(111)

    t = apply_mpl_theme(fig, ax, theme)
    ax.plot(of, t_chamber, linewidth=2.0, color=t.colors[0], label="Chamber")

    if t_throat is not None:
        ax.plot(of, t_throat, linewidth=2.0, color=t.colors[1], label="Throat")

    if t_exit is not None:
        ax.plot(of, t_exit, linewidth=2.0, color=t.colors[3], label="Exit")

    ax.set_xlabel("O/F Ratio")
    ax.set_ylabel("Temperature (K)")
    ax.set_title("Temperatures vs O/F Ratio")
    ax.legend(facecolor=t.ax_bg, edgecolor=t.grid, labelcolor=t.fg)

    fig.tight_layout()
    return fig