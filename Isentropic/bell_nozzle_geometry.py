from __future__ import annotations
import numpy as np
#import matplotlib.pyplot as plt
from Isentropic.geometry import radius_from_area


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Core.engine_analysis import FullDesignResult
    from Core.engine_inputs import EngineInputs



def initial_angle_fit(x, a, b, c):
    return a + b * np.log10(x) + c * np.log10(x)**2 # degrees

def exit_angle_fit(x, a, b, c):
    return a + b * np.exp(-c * x) # degrees


# rao bell nozzle geometry

# engine nozzle length assumed to be 80% of a total conical nozzle; past 85% is diminishing returns, under 70% is bad performance

def divergent_length_bell(throat_area, exit_area, bell_length):
    r_throat = radius_from_area(throat_area)
    r_exit = radius_from_area(exit_area)
    return ((r_exit - r_throat) / np.tan(np.radians(15))) * bell_length 

def throat_entry_curve(a_throat):
    throat_radius = radius_from_area(a_throat)
    theta_angles = np.linspace(np.radians(-135), np.radians(-90), 50) # radians
    x = 1.5 * throat_radius * np.cos(theta_angles) 
    y = 1.5 * throat_radius * np.sin(theta_angles) + 1.5 * throat_radius + throat_radius
    return (x , y)

def throat_exit_curve(a_throat, initial_angle):
    throat_radius = radius_from_area(a_throat)
    theta_angles = np.linspace(np.radians(-90), np.radians(initial_angle - 90), 50) # radians
    x = 0.382 * throat_radius * np.cos(theta_angles) 
    y = 0.382 * throat_radius * np.sin(theta_angles) + 0.382 * throat_radius + throat_radius    
    return (x , y)

def create_bell_curves(initial_angle, final_angle, nozzle_length, exit_area, N_x, N_y): # take conical nozzle geometry class
    # Bezier curve variables
    E_y = radius_from_area(exit_area)
    E_x = nozzle_length

    m_1 = np.tan(np.radians(initial_angle))
    m_2 = np.tan(np.radians(final_angle))

    N_x = N_x
    N_y = N_y

    c_1 = N_y - m_1 * N_x
    c_2 = E_y - m_2 * E_x

    Q_x = (c_2 - c_1)/(m_1 - m_2)
    Q_y = (m_1 * c_2 - m_2 * c_1)/(m_1 - m_2)

    t_intervals = np.linspace(0,1,100)
    
    x_t = N_x * (1 - t_intervals)**2  + 2 * (1 - t_intervals) * t_intervals * Q_x + E_x * t_intervals ** 2 
    y_t = N_y * (1 - t_intervals)**2  + 2 * (1 - t_intervals) * t_intervals * Q_y + E_y * t_intervals ** 2 

    return (x_t, y_t)

def chamber_converging_curve(chamber_length, converging_length, CR, a_throat, x1, y1):
    A_c = CR * a_throat
    r_c = radius_from_area(A_c)

    x0, y0 = -converging_length, r_c        # chamber end
    x2, y2 = x1[0], y1[0]          # entry start

    m0 = 0.0                           # chamber wall slope
    dx = x1[1] - x1[0]
    dy = y1[1] - y1[0]
    m2 = dy / dx                       # throat-entry slope

    # Solve for control point C
    xc = (y0 - y2 + m2 * x2) / m2
    yc = y0

    # Bézier evaluation
    t = np.linspace(0.0, 1.0, 100)

    x_converging = (1 - t)**2 * x0 + 2*(1 - t)*t * xc + t**2 * x2
    y_converging = (1 - t)**2 * y0 + 2*(1 - t)*t * yc + t**2 * y2

    x_ch = np.linspace(-(chamber_length + converging_length), -converging_length, 100)
    y_ch = np.full_like(x_ch, r_c)

    x_points = np.concatenate([x_ch, x_converging[1:]])
    y_points = np.concatenate([y_ch, y_converging[1:]])

    return x_points, y_points

def bell_nozzle_graph(result: FullDesignResult, inputs: EngineInputs, idx: int = 0):

    At = float(np.atleast_1d(result.perf.a_throat)[idx])
    Ae = float(np.atleast_1d(result.perf.a_exit)[idx])

    theta_n = float(np.atleast_1d(result.nozzle.initial_angle)[idx])
    theta_e = float(np.atleast_1d(result.nozzle.exit_angle)[idx])
    L_div   = float(np.atleast_1d(result.nozzle.nozzle_length)[idx])

    L_ch   = float(np.atleast_1d(result.nozzle.length_chamber)[idx])
    L_conv = float(np.atleast_1d(getattr(result.nozzle, "l_converging", 0.0))[idx])

    x1, y1 = throat_entry_curve(At)
    x2, y2 = throat_exit_curve(At, theta_n)
    x3, y3 = create_bell_curves(theta_n, theta_e, L_div, Ae, x2[-1], y2[-1])
    x_ch, y_ch = chamber_converging_curve(L_ch, L_conv, inputs.CR, At, x1, y1)

    axial = np.concatenate([x_ch, x1, x2, x3]) # connects axial points together
    radial = np.concatenate([y_ch, y1, y2, y3]) # connects radial points together
    return(axial, radial)



"""
# === Test Section to Validate Code ===

# === 1. Define test inputs ===
At = 1  # throat radius in meters (or unit)
epsilon = 3  # area expansion ratio
Ae = epsilon * At
theta_n = 33  # initial bell angle in degrees (from fit)
theta_e = 7   # exit bell angle in degrees (from fit)
bell_percent = 0.8

L = divergent_length_bell(At, Ae, 0.8)
CR = 3.5
L_chamber = 0.9
L_converging = 1

x_total, y_total = bell_nozzle_graph(At, Ae, theta_n, theta_e, L, L_chamber, L_converging, CR)

# === 5. Plot ===
plt.figure(figsize=(10, 4))
plt.plot(x_total, y_total, label="Bell Nozzle Profile")
plt.axis("equal")
plt.grid()
plt.title(f"Rao Bell Nozzle (ε = {epsilon}, θₙ = {theta_n}°, θₑ = {theta_e}°)")
plt.xlabel("Axial Distance")
plt.ylabel("Radius")
plt.legend()
plt.tight_layout()
plt.show()
"""

'''
# === 3. Generate each section ===
x1, y1 = throat_entry_curve(At)


### Test Section
# Inputs
CR = 4
L_chamber = 0.9
L_converging = 1

r_t = radius_from_area(At)
r_c = np.sqrt(CR) * r_t

# Number of points
N_ch = 120
# ---- Quadratic Bézier converger (slope-matched) ----

# Endpoints
x0, y0 = -L_converging, r_c        # chamber end
x2, y2 = x1[0], y1[0]              # throat-entry start

# Slopes
m0 = 0.0                           # chamber wall slope
dx = x1[1] - x1[0]
dy = y1[1] - y1[0]
m2 = dy / dx                       # throat-entry slope

# Solve for control point C
xc = (y0 - y2 + m2 * x2) / m2
yc = y0

# Bézier evaluation
N_cv = 180
t = np.linspace(0.0, 1.0, N_cv)

x_cv = (1 - t)**2 * x0 + 2*(1 - t)*t * xc + t**2 * x2
y_cv = (1 - t)**2 * y0 + 2*(1 - t)*t * yc + t**2 * y2


x_ch = np.linspace(
    -(L_chamber + L_converging),  # upstream end
    -L_converging,                # downstream end (chamber → converger junction)
    N_ch
)
y_ch = np.full_like(x_ch, r_c)


x2, y2 = throat_exit_curve(At, theta_n)
x3, y3 = create_bell_curves(theta_n, theta_e, L, Ae, x2[-1], y2[-1])

# === 4. Concatenate full profile ===
x_total = np.concatenate([x_ch, x_cv[1:], x1[1:], x2[1:], x3])
y_total = np.concatenate([y_ch, y_cv[1:], y1[1:], y2[1:], y3])

'''