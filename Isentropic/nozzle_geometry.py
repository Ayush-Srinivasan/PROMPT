import numpy as np
from .geometry import diameter_from_area, radius_from_area

# conical nozzle geometry
def throat_length(throat_ratio, throat_area):
    throat_diameter = diameter_from_area(throat_area)
    return throat_ratio * throat_diameter # m

def chamber_diameter(throat_area, contraction_ratio):
    throat_diameter = diameter_from_area(throat_area)
    return throat_diameter * np.sqrt(contraction_ratio) # m

def chamber_length(chamber_diameter):
    D_cm = chamber_diameter * 100 # cm
    return 10 * np.exp(0.029 * np.log(D_cm)**2 + 0.47 * np.log(D_cm) + 1.94) # m

def exit_diameter(exit_area):
    return diameter_from_area(exit_area) # m

def conical_nozzle_length(throat_area, exit_area, divergent_half_angle):
    r_throat = radius_from_area(throat_area)
    r_exit = radius_from_area(exit_area)
    return (r_exit - r_throat) / np.tan(np.rad2deg(divergent_half_angle))

# rao bell nozzle geometry
