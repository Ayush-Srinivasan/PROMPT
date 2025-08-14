import sys
import os
import numpy as np
from dataclasses import dataclass
from .engine_inputs import EngineInputs


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Isentropic import (
    # isentropic_equations.py
    specific_gas_constant, exit_mach, exit_temperature, exit_pressure, exit_velocity, expansion_ratio, 
    # engine_performance.py
    mass_flow_rate, specific_impulse, throat_area, exit_area, characteristic_velocity,           
    # conical_nozzle_geometry.py                                           
    throat_length, chamber_diameter, chamber_length, exit_diameter, divergent_length, convergent_length, total_length, 
    # bell_nozzle_geometry.py                   
    initial_angle_fit, exit_angle_fit, divergent_length_bell, throat_entry_curve, throat_exit_curve, create_bell_curves, load_fit_params,
    # geometry.py 
    diameter_from_area, radius_from_area, radius_from_diameter, area_from_radius                                                            
)

from Data import load_materials, load_propellant


@dataclass
class EngineDesignResult:
    mach_exit: float    
    T_exit: float       # K
    v_exit: float       # m/s
    p_exit: float       # Pa
    mdot: float         # kg/s
    a_throat: float     # m^2
    a_exit: float       # m^2
    ER: float           
    Isp: float          # s
    c_star: float       # m/s

def engine_analysis(inputs: EngineInputs) -> dict:
    
    # isentropic equations
    SGC = specific_gas_constant(inputs.cp, inputs.gamma) # J/kg*K
    mach_exit = exit_mach(inputs.chamber_pressure, inputs.gamma)
    T_exit = exit_temperature(inputs.chamber_temperature, inputs.gamma, mach_exit)
    p_exit = exit_pressure(inputs.chamber_pressure, inputs.gamma, mach_exit)
    v_exit = exit_velocity(mach_exit, inputs.gamma, SGC, T_exit)
    ER = expansion_ratio(inputs.gamma, mach_exit)

    # characterizing equations
    mdot = mass_flow_rate(inputs.thrust, v_exit)
    Isp = specific_impulse(inputs.thrust, mdot)
    a_throat = throat_area(mdot, inputs.chamber_temperature, inputs.chamber_pressure, inputs.gamma, SGC)
    a_exit = exit_area(a_throat, ER)
    c_star = characteristic_velocity(inputs.chamber_pressure, a_throat, mdot)

    return EngineDesignResult(
        mach_exit=mach_exit,
        T_exit=T_exit,
        v_exit=v_exit,
        p_exit=p_exit,
        mdot=mdot,
        a_throat=a_throat,
        a_exit=a_exit,
        ER=ER,
        Isp=Isp,
        c_star=c_star
    )   

@dataclass
class ConicalNozzleGeometry:
    diameter_chamber: float     # m
    diameter_throat: float      # m
    diameter_exit: float        # m

    radius_chamber: float       # m
    radius_throat: float        # m
    radius_exit: float          # m

    length_chamber: float       # m
    length_convergent: float    # m
    length_throat: float        # m
    length_divergent: float     # m
    length_total: float         # m

    convergent_angle: float     # degrees
    divergent_angle: float      # degrees

def conical_nozzle_sizing(geometry: EngineDesignResult, inputs: EngineInputs) -> dict:
    # diameters
    diameter_chamber = chamber_diameter(geometry.a_throat, inputs.contraction_ratio)
    diameter_throat = diameter_from_area(geometry.a_throat)
    diameter_exit = exit_diameter(geometry.a_exit)

    # radius
    radius_chamber = radius_from_diameter(diameter_chamber)
    radius_throat = radius_from_diameter(diameter_throat)
    radius_exit = radius_from_diameter(diameter_exit) 
    
    # lengths
    length_chamber = chamber_length(diameter_chamber)
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
        divergent_angle=inputs.divergent_angle
    )

    
@dataclass
class BellNozzleGeometry:
    initial_angle: float    # degrees
    exit_angle: float       # degrees
    chamber_radius: float   # m
    throat_radius: float    # m
    exit_radius: float      # m
    nozzle_length: float    # m
    length_chamber: float   # m
    chamber_area: float     # m^2
    contraction_ratio: float               
    x_points: float         # m
    y_points: float         # m
    bell_percent: float     # percentage

def bell_nozzle_sizing(geometry: EngineDesignResult, inputs: EngineInputs) -> dict:
    nozzle_length = divergent_length_bell(geometry.a_throat, geometry.a_exit)
    # theta_n fit parameters
    a_n = load_fit_params["theta_n"]["a"]
    b_n = load_fit_params["theta_n"]["b"]
    c_n = load_fit_params["theta_n"]["c"]

    initial_angle = initial_angle_fit(geometry.ER, a_n, b_n, c_n) # gets initial angle

    # theta_e fit parameters
    a_e = load_fit_params["theta_e"]["a"]
    b_e = load_fit_params["theta_e"]["b"]
    c_e = load_fit_params["theta_e"]["c"]   

    exit_angle = exit_angle_fit(geometry.ER, a_e, b_e, c_e) # gets exit angle

    # gets radiuses and length
    throat_radius = radius_from_area(geometry.a_throat)
    exit_radius = radius_from_area(geometry.a_exit)

    nozzle_length = divergent_length_bell(geometry.a_throat, geometry.a_exit)

    # nozzle points
    x1, y1 = throat_entry_curve(geometry.a_throat)
    x2, y2 = throat_exit_curve(geometry.a_throat, initial_angle)
    x3, y3 = create_bell_curves(initial_angle, exit_angle, nozzle_length, geometry.a_exit, x2[-1], y2[-1])

    x_points = np.concatenate([x1, x2, x3]) # connects all points together # m
    y_points = np.concatenate([y1, y2, y3]) # connects all points together # m

    # If CAD includes filleting or blending at the throat, chamber radius is not correct, therefore CR is incorrect as well
    # This value may underestimate true chamber radius. If so, use true chamber geometry
    chamber_radius = y1[0] # initial point of chamber gives chamber radius 
    chamber_area = area_from_radius(chamber_radius)
    contraction_ratio = chamber_area / geometry.a_throat
    chamber_diameter = chamber_radius * 2
    l_chamber = chamber_length(chamber_diameter)

    return BellNozzleGeometry(
        initial_angle=initial_angle,        # degrees
        exit_angle=exit_angle,              # degrees
        chamber_radius=chamber_radius,      # m
        throat_radius=throat_radius,        # m
        exit_radius=exit_radius,            # m
        nozzle_length=nozzle_length,        # m
        length_chamber=l_chamber,            # m
        chamber_area=chamber_area,          # m^2
        contraction_ratio=contraction_ratio,               
        x_points=x_points,                  # m
        y_points=y_points,                  # m
        bell_percent=80.0                   # percentage
    )




