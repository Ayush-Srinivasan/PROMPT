import numpy as np
from scipy.constants import atmosphere

# specific gas constant
def specific_gas_constant(specific_heat, Gamma):
    return specific_heat * (1 - (1/Gamma)) # J/(kg*K)

# exit Mach Number
def exit_mach(Chamber_Pressure, Gamma):
    return np.sqrt((2 / (Gamma - 1)) * ((atmosphere / Chamber_Pressure)**((1 - Gamma) / Gamma) - 1)) 

# exit temperature
def exit_temperature(Chamber_Temperature, Gamma, Mach):
    return Chamber_Temperature * (1 + ((Gamma - 1) / 2) * Mach **2) ** -1  # K

# exit pressure
def exit_pressure(Chamber_Pressure, Gamma, Mach):
    return (Chamber_Pressure/100000) * (1 + ((Gamma - 1) / 2) * Mach**2) ** (-Gamma / (Gamma - 1)) # Pa

# exit velocity
def exit_velocity(Mach, Gamma, Specific_Gas_Constant, Exit_Temperature):
    return Mach * np.sqrt(Gamma * Specific_Gas_Constant * Exit_Temperature) # m/s

# expansion ratio
def expansion_ratio(Gamma, Mach):
    return (((Gamma + 1) / 2) ** ((1 - Gamma) / (2 * (Gamma - 1)))) * (((1 + (((Gamma - 1) / 2) * Mach**2)) ** ((1 + Gamma) / (2 * (Gamma - 1))))/ Mach) 

