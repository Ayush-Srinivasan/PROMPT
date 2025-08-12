import numpy as np

# exit Mach Number
def exit_mach(Atmospheric_Pressure, Chamber_Pressure, Gamma):
    return np.sqrt((2 / (Gamma - 1)) * ((Atmospheric_Pressure / Chamber_Pressure)**((1 - Gamma) / Gamma) - 1)) 

# exit temperature
def exit_temperature(Chamber_Temperature, Gamma, Mach):
    return Chamber_Temperature * (1 + ((Gamma - 1) / 2) * Mach **2) ** -1  

# exit pressure
def exit_pressure(Chamber_Pressure, Gamma, Mach):
    (Chamber_Pressure/100000) * (1 + ((Gamma - 1) / 2) * Mach**2) ** (-Gamma / (Gamma - 1))

# exit velocity
def exit_velocity(Mach, Gamma, Specific_Gas_Constant, Exit_Temperature):
    return Mach * np.sqrt(Gamma * Specific_Gas_Constant * Exit_Temperature)

# expansion ratio
def expansion_ratio(Gamma, Mach):
    return (((Gamma + 1) / 2) ** ((1 - Gamma) / (2 * (Gamma - 1)))) * (((1 + (((Gamma - 1) / 2) * Mach**2)) ** ((1 + Gamma) / (2 * (Gamma - 1))))/ Mach)