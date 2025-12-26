import numpy as np
from numpy.typing import NDArray
from dataclasses import dataclass

from .engine_inputs import EngineInputs # engine input file
from CEA.CEA_Outputs import CEAOutputs
from Isentropic.rao_curves.rao_fit_curves import get_rao_coeffs


from Isentropic import (
    # isentropic_equations.py
    isentropic_eqns,
    # engine_performance.py
    performance_characterization,           
    # conical_nozzle_geometry.py                                           
    throat_length, chamber_diameter, chamber_length, exit_diameter, divergent_length, convergent_length, total_length, conical_nozzle_graph, 
    # bell_nozzle_geometry.py                   
    initial_angle_fit, exit_angle_fit, divergent_length_bell,
    # geometry.py 
    diameter_from_area, radius_from_area, radius_from_diameter, area_from_radius                                                            
)



@dataclass
class EngineDesignResult:
    mach_exit: NDArray[np.float64]    
    T_throat: NDArray[np.float64]     # K
    T_exit: NDArray[np.float64]      # K
    v_exit: NDArray[np.float64]       # m/s
    p_exit: NDArray[np.float64]       # Pa
    p_throat: NDArray[np.float64]     # Pa
    mdot: NDArray[np.float64]         # kg/s
    a_throat: NDArray[np.float64]    # m^2
    a_exit: NDArray[np.float64]       # m^2
    ER: NDArray[np.float64]           
    Isp: NDArray[np.float64]        # s
    c_star: NDArray[np.float64]       # m/s

def engine_analysis(inputs: EngineInputs, cea: CEAOutputs):
    
    # isentropic equations
    SGC, mach_exit, T_throat, T_exit, p_throat, p_exit, v_exit, ER = isentropic_eqns(cea.specific_heat, cea.gamma, inputs.chamber_pressure, cea.T_chamber, inputs.ambient_pressure)

    # characterizing equations
    mdot, Isp, c_star, a_throat, a_exit = performance_characterization(inputs.thrust, v_exit, cea.T_chamber, inputs.chamber_pressure, cea.gamma, SGC, ER)

    return EngineDesignResult(
        mach_exit=mach_exit,
        T_throat=T_throat,
        T_exit=T_exit,
        v_exit=v_exit,
        p_exit=p_exit,
        p_throat=p_throat,
        mdot=mdot,
        a_throat=a_throat,
        a_exit=a_exit,
        ER=ER,
        Isp=Isp,
        c_star=c_star
    )   

@dataclass
class ConicalNozzleGeometry:
    diameter_chamber: NDArray[np.float64]     # m
    diameter_throat: NDArray[np.float64]      # m
    diameter_exit: NDArray[np.float64]        # m

    radius_chamber: NDArray[np.float64]       # m
    radius_throat: NDArray[np.float64]        # m
    radius_exit: NDArray[np.float64]          # m

    length_chamber: NDArray[np.float64]       # m
    length_convergent: NDArray[np.float64]    # m
    length_throat: NDArray[np.float64]        # m
    length_divergent: NDArray[np.float64]     # m
    length_total: NDArray[np.float64]         # m

    convergent_angle: NDArray[np.float64]     # degrees
    divergent_angle: NDArray[np.float64]      # degrees
    

def conical_nozzle_sizing(geometry: EngineDesignResult, inputs: EngineInputs):
    # diameters
    diameter_chamber = chamber_diameter(geometry.a_throat, inputs.contraction_ratio)
    diameter_throat = diameter_from_area(geometry.a_throat)
    diameter_exit = exit_diameter(geometry.a_exit)

    # radius
    radius_chamber = radius_from_diameter(diameter_chamber)
    radius_throat = radius_from_diameter(diameter_throat)
    radius_exit = radius_from_diameter(diameter_exit) 
    
    # lengths
    length_chamber = chamber_length(inputs.l_star, geometry.a_throat, inputs.convergent_angle, inputs.contraction_ratio)
    length_convergent = convergent_length(geometry.a_throat, diameter_chamber, inputs.convergent_angle)
    length_throat = throat_length(inputs.throat_ratio, geometry.a_throat)
    length_divergent = divergent_length(geometry.a_throat, geometry.a_exit, inputs.divergent_angle)
    length_total = total_length(length_chamber, length_convergent, length_throat, length_divergent)



    return ConicalNozzleGeometry(
        # diameters (m)
        diameter_chamber=diameter_chamber,
        diameter_throat=diameter_throat,
        diameter_exit=diameter_exit,

        # radius (m)
        radius_chamber=radius_chamber,
        radius_throat=radius_throat,
        radius_exit=radius_exit,

        # length (m)
        length_chamber=length_chamber,
        length_convergent=length_convergent,
        length_throat=length_throat,
        length_divergent=length_divergent,
        length_total=length_total,

        # angles (degrees)
        convergent_angle=inputs.convergent_angle,
        divergent_angle=inputs.divergent_angle,
    )

    
@dataclass
class BellNozzleGeometry:
    initial_angle: NDArray[np.float64]    # degrees
    exit_angle: NDArray[np.float64]       # degrees
    chamber_radius: NDArray[np.float64]   # m
    throat_radius: NDArray[np.float64]    # m
    exit_radius: NDArray[np.float64]      # m
    nozzle_length: NDArray[np.float64]    # m
    length_chamber: NDArray[np.float64]   # m
    chamber_area: NDArray[np.float64]     # m^2

def bell_nozzle_sizing(geometry: EngineDesignResult, inputs: EngineInputs):
    nozzle_length = divergent_length_bell(geometry.a_throat, geometry.a_exit)

    (a_n, b_n, c_n), (a_e, b_e, c_e) = get_rao_coeffs(inputs.bell_percent) # gets coefficients based on engine inputs

    initial_angle = initial_angle_fit(geometry.ER, a_n, b_n, c_n) # gets initial angle

    exit_angle = exit_angle_fit(geometry.ER, a_e, b_e, c_e) # gets exit angle

    # gets radiuses and length
    throat_radius = radius_from_area(geometry.a_throat)
    exit_radius = radius_from_area(geometry.a_exit)

    # If CAD includes filleting or blending at the throat, chamber radius is not correct, therefore CR is incorrect as well
    # This value may underestimate true chamber radius. If so, use true chamber geometry
    l_chamber = chamber_length(inputs.l_star, geometry.a_throat, inputs.convergent_angle, inputs.contraction_ratio)

    diameter_chamber = chamber_diameter(geometry.a_throat, inputs.contraction_ratio)
    chamber_radius = radius_from_diameter(diameter_chamber)
    chamber_area = area_from_radius(chamber_radius)

    return BellNozzleGeometry(
        initial_angle=initial_angle,        # degrees
        exit_angle=exit_angle,              # degrees
        chamber_radius=chamber_radius,      # m
        throat_radius=throat_radius,        # m
        exit_radius=exit_radius,            # m
        nozzle_length=nozzle_length,        # m
        length_chamber=l_chamber,            # m
        chamber_area=chamber_area,          # m^2              
    )




