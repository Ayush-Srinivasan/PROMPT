import os
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from .geometry import diameter_from_area, radius_from_area


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
popt_e, _ = curve_fit(exit_angle_fit, x2, y2)

# dictionary for fit parameters and function
fit_params = {
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


