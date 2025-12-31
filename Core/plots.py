from __future__ import annotations

from matplotlib.figure import Figure
from Core.plot_style import apply_mpl_theme
import numpy as np


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

def plot_nozzle_geometry(x, y, *, theme: str = "system"):
    fig = Figure(figsize=(4.5, 7.0), dpi=120)
    ax = fig.add_subplot(111)
    t = apply_mpl_theme(fig, ax, theme)

    ax.plot(x, y, linewidth=2.0, color=t.colors[0])
    ax.plot(-x, y, linewidth=2.0, color=t.colors[0])
    ax.set_xlabel("Radius (m)")
    ax.set_ylabel("Axial Distance (m)")
    ax.set_title("Engine Contour")
    ax.set_xlim(-3 * float(np.max(x)), 3 * float(np.max(x)))
    ax.set_ylim(float(np.min(y)), float(np.max(y)))
    ax.set_aspect("equal", adjustable="box")
    return fig

def plot_nozzle_revolution(x_radial, y_axial, *, theme="system", n_theta=80):
    fig = Figure(figsize=(7, 4.5), dpi=120)
    ax = fig.add_subplot(111, projection="3d")
    t = apply_mpl_theme(fig, ax, theme)

    theta = np.linspace(0.0, 2.0*np.pi, n_theta)

    Z = np.tile(y_axial[None, :], (n_theta, 1))
    R = np.tile(x_radial[None, :], (n_theta, 1))

    X = R * np.cos(theta[:, None])
    Y = R * np.sin(theta[:, None])
    
    H = float(np.max(Z) - np.min(Z))
    D = float(2.0 * np.max(X))
    ax.plot_surface(X, Y, Z, linewidth=0,  antialiased=True, alpha=0.95, color=t.colors[0], shade=True)
    ax.set_title("3D Surface of Revolution")
    # CAD-style top-down view
    ax.set_proj_type("ortho")
    # Optional: remove everything except geometry
    ax.set_aspect('equal')
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_zlabel("")
    ax.set_title("")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.grid(False)
    ax.xaxis.pane.set_visible(False)
    ax.yaxis.pane.set_visible(False)
    ax.zaxis.pane.set_visible(False)
    ax.xaxis.line.set_visible(False)
    ax.yaxis.line.set_visible(False)
    ax.zaxis.line.set_visible(False)

    return fig