import sys
import os
from dataclasses import dataclass
from .engine_inputs import EngineInputs

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Isentropic import (
    specific_gas_constant, exit_mach, exit_temperature, exit_pressure, exit_velocity, expansion_ratio,                  # isentropic_equations.py
    mass_flow_rate, specific_impulse, throat_area, exit_area, characteristic_velocity,                                  # engine_performance.py
    throat_length, chamber_diameter, chamber_length, exit_diameter, divergent_length, convergent_length, total_length,  # nozzle_geometry.py
    diameter_from_area, radius_from_area, radius_from_diameter                                                          # geometry.py 
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

    




