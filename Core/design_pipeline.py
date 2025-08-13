import sys
import os
from dataclasses import dataclass
from Core.engine_inputs import EngineInputs

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Isentropic import (
    specific_gas_constant, exit_mach, exit_temperature, exit_pressure, exit_velocity, expansion_ratio,
    mass_flow_rate, specific_impulse, throat_area, exit_area, characteristic_velocity
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

    



