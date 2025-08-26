import os
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from Isentropic.geometry import diameter_from_area, radius_from_area


base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, "rao_curves")

theta_n_path = os.path.join(data_dir,"theta_n (80% length).csv") # initial angle points
theta_e_path = os.path.join(data_dir, "theta_e (80% length).csv") # exit angle points


def load_curve_data(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.lower()
    ratio = df["expansion"].values
    angle = df["angle"].values
    return (ratio, angle)

def initial_angle_fit(x, a, b, c):
    return a + b * np.log10(x) + c * np.log10(x)**2 # degrees

def exit_angle_fit(x, a, b, c):
    return a + b * np.exp(-c * x) # degrees

x1, y1 = load_curve_data(theta_n_path)
theta_n_80_bounds = ([20,3,0.8], [23, 6, 1.2])
popt_n, _ = curve_fit(initial_angle_fit, x1, y1, bounds=theta_n_80_bounds)


x2, y2 = load_curve_data(theta_e_path)
theta_e_80_bounds = ([6, 6, 0], [8, 8, 0.5])
popt_e, _ = curve_fit(exit_angle_fit, x2, y2, bounds=theta_e_80_bounds)

# dictionary for fit parameters and function
load_fit_params = {
    "theta_n": {
        "a": popt_n[0],
        "b": popt_n[1],
        "c": popt_n[2],
        "func": initial_angle_fit
    },
    "theta_e": {
        "a": popt_e[0],
        "b": popt_e[1],
        "c": popt_e[2],
        "func": exit_angle_fit  
    }
}

# rao bell nozzle geometry

# engine efficiency assumed to be 80% of a total bell nozzle; past 85% is diminishing returns, under 70% is bad performance

def divergent_length_bell(throat_area, exit_area):
    r_throat = radius_from_area(throat_area)
    r_exit = radius_from_area(exit_area)
    # assumes 80% size so 0.8 the length
    return ((r_exit - r_throat) / np.tan(np.radians(15))) * 0.8 # if needed, convert 0.8 to a variable and add another parameter to engine inputs class

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

'''
# === Test Section to Validate Code ===

# === 1. Define test inputs ===
At = 0.78539816339  # throat radius in meters (or unit)
epsilon = 3  # area expansion ratio
Ae = epsilon * At
theta_n = 33  # initial bell angle in degrees (from fit)
theta_e = 7   # exit bell angle in degrees (from fit)
bell_percent = 0.8



L = divergent_length_bell(At, Ae)

# === 3. Generate each section ===
x1, y1 = throat_entry_curve(At)
x2, y2 = throat_exit_curve(At, theta_n)
x3, y3 = create_bell_curves(theta_n, theta_e, L, Ae, x2[-1], y2[-1])

# === 4. Concatenate full profile ===
x_total = np.concatenate([x1, x2, x3])
y_total = np.concatenate([y1, y2, y3])

# === 5. Plot ===
plt.figure(figsize=(10, 4))
plt.plot(x_total, y_total, label="Bell Nozzle Profile")
plt.scatter([x1[-1], x2[-1], x3[0], x3[-1]], [y1[-1], y2[-1], y3[0], y3[-1]], color='red', s=15, label='Curve Joints')
plt.axis("equal")
plt.grid()
plt.title(f"Rao Bell Nozzle (ε = {epsilon}, θₙ = {theta_n}°, θₑ = {theta_e}°)")
plt.xlabel("Axial Distance")
plt.ylabel("Radius")
plt.legend()
plt.tight_layout()
plt.show()
'''
