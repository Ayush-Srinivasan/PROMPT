import numpy as np
from scipy.constants import R

def isentropic_eqns(Gamma, Chamber_Pressure, Chamber_Temperature, Ambient_Pressure, Molecular_Weight):

    # equation 1
    Specific_Gas_Constant = (R / Molecular_Weight)*1000

    # equation 2   
    Exit_Mach = np.sqrt((2/(Gamma-1))*((Chamber_Pressure/Ambient_Pressure)**((Gamma-1)/Gamma) - 1)) 

    # equation 14
    Throat_Temperature = Chamber_Temperature * (1 + ((Gamma - 1) / 2)) ** -1  # K

    # equation 3
    Exit_Temperature = Chamber_Temperature * (1 + ((Gamma - 1) / 2) * Exit_Mach **2) ** -1  # K

    # equation 15
    Throat_Pressure = (Chamber_Pressure) * (1 + ((Gamma - 1) / 2)) ** (-Gamma / (Gamma - 1)) # Pa

    # equation 4
    Exit_Pressure = (Chamber_Pressure) * (1 + ((Gamma - 1) / 2) * Exit_Mach**2) ** (-Gamma / (Gamma - 1)) # Pa

    # equation 5
    Exit_Velocity = Exit_Mach * np.sqrt(Gamma * Specific_Gas_Constant * Exit_Temperature) # m/s

    # equation 6
    Expansion_Ratio = (((Gamma + 1) / 2) ** (- (Gamma + 1) / (2 * (Gamma - 1)))) * (((1 + (((Gamma - 1) / 2) * Exit_Mach**2)) ** ((1 + Gamma) / (2 * (Gamma - 1))))/ Exit_Mach)

    return Specific_Gas_Constant, Exit_Mach, Throat_Temperature, Exit_Temperature, Throat_Pressure, Exit_Pressure, Exit_Velocity, Expansion_Ratio


