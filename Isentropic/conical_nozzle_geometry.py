import numpy as np
from .geometry import diameter_from_area, radius_from_area, line_plot
from Core.engine_analysis import FullDesignResult

# conical nozzle geometry
def throat_length(throat_ratio, throat_area):
    throat_diameter = diameter_from_area(throat_area)
    return throat_ratio * throat_diameter # m

def chamber_diameter(throat_area, contraction_ratio):
    throat_diameter = diameter_from_area(throat_area)
    return throat_diameter * np.sqrt(contraction_ratio) # m

def chamber_length(L_star, Throat_Area, Converging_Angle, Contraction_Ratio):
    return  (L_star - (1/3) * np.sqrt(Throat_Area / np.pi) * (1 / np.tan(np.deg2rad(Converging_Angle)))* (Contraction_Ratio**(1/3) - 1)) / Contraction_Ratio

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

# to be used for graphs of conical nozzle or for plugging into 3D CAD softwares
def conical_nozzle_graph(result: FullDesignResult):
                         
    # diverging section
    y_1 = np.linspace(0, result.nozzle.length_divergent, 100)
    x_1 = line_plot(result.nozzle.radius_throat, result.nozzle.length_divergent, result.nozzle.radius_exit, 0, y_1)

    # throat section
    y_2 = np.linspace(result.nozzle.length_divergent, (result.nozzle.length_throat + result.nozzle.length_divergent), 100)
    x_2 = result.nozzle.radius_throat * np.ones(100)

    # converging section
    y_3 = np.linspace((result.nozzle.radius_throat + result.nozzle.length_divergent), (result.nozzle.radius_throat + result.nozzle.length_divergent + result.nozzle.length_convergent), 100)
    x_3 = line_plot(result.nozzle.radius_chamber, (result.nozzle.radius_throat + result.nozzle.length_divergent + result.nozzle.length_convergent), result.nozzle.radius_throat, (result.nozzle.radius_throat + result.nozzle.length_divergent), y_3)

    # chamber section
    y_4 = np.linspace((result.nozzle.radius_throat + result.nozzle.length_divergent + result.nozzle.length_convergent), (result.nozzle.radius_throat + result.nozzle.length_divergent + result.nozzle.length_convergent + l_chamber), 100)
    x_4 = result.nozzle.radius_chamber * np.ones(100)
    
    x_points = np.concatenate([x_1, x_2, x_3, x_4]) # radial
    y_points = np.concatenate([y_1, y_2, y_3, y_4]) # axial
    
    return(x_points, y_points)
