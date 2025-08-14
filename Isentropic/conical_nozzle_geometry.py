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

def divergent_length(throat_area, exit_area, divergent_half_angle):
    r_throat = radius_from_area(throat_area)
    r_exit = radius_from_area(exit_area)
    return (r_exit - r_throat) / np.tan(np.radians(divergent_half_angle)) # m

def convergent_length(throat_area, diameter_chamber, convergent_half_angle):
    r_chamber = diameter_chamber/2
    r_throat = radius_from_area(throat_area)
    return (r_chamber - r_throat) / np.tan(np.radians(convergent_half_angle)) # m

def total_length(l_chamber, l_convergent, l_throat, l_divergent):
    return l_chamber + l_convergent + l_throat + l_divergent # m

