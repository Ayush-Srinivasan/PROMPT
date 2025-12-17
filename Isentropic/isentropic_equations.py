import numpy as np

def isentropic_eqns(Specific_Heat, Gamma, Chamber_Pressure, Chamber_Temperature, Ambient_Pressure):

    # equation 1
    Specific_Gas_Constant = Specific_Heat * 1000 * (1 - (1/Gamma))

    # equation 2   
    Exit_Mach = np.sqrt((2/(Gamma-1))*((Chamber_Pressure/Ambient_Pressure)**((Gamma-1)/Gamma) - 1)) 

    # equation 14
    Throat_Temperature = Chamber_Temperature * (1 + ((Gamma - 1) / 2)) ** -1  # K

    # equation 3
    Exit_Temperature = Chamber_Temperature * (1 + ((Gamma - 1) / 2) * Exit_Mach **2) ** -1  # K

    # equation 15
    Throat_Pressure = (Chamber_Pressure/100000) * (1 + ((Gamma - 1) / 2)) ** (-Gamma / (Gamma - 1)) # Pa

    # equation 4
    Exit_Pressure = (Chamber_Pressure/100000) * (1 + ((Gamma - 1) / 2) * Exit_Mach**2) ** (-Gamma / (Gamma - 1)) # Pa

    # equation 5
    Exit_Velocity = Exit_Mach * np.sqrt(Gamma * Specific_Gas_Constant * Exit_Temperature) # m/s

    # equation 6
    Expansion_Ratio = (((Gamma + 1) / 2) ** ((1 - Gamma) / (2 * (Gamma - 1)))) * (((1 + (((Gamma - 1) / 2) * Exit_Mach**2)) ** ((1 + Gamma) / (2 * (Gamma - 1))))/ Exit_Mach)

    return Specific_Gas_Constant, Exit_Mach, Throat_Temperature, Exit_Temperature, Throat_Pressure, Exit_Pressure, Exit_Velocity, Expansion_Ratio

'''
# specific gas constant
def specific_gas_constant(Specific_Heat, Gamma):
    return Specific_Heat * 1000 * (1 - (1/Gamma)) # J/(kg*K)

# exit Mach Number
def exit_mach(Chamber_Pressure, Gamma):
    return np.sqrt((2/(Gamma-1))*((Chamber_Pressure/atmosphere)**((Gamma-1)/Gamma) - 1)) 

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

def throat_pressure(Gamma, Chamber_Pressure):
    return (Chamber_Pressure/100000) * (1 + ((Gamma - 1) / 2)) ** (-Gamma / (Gamma - 1)) # Pa

def throat_temperature(Gamma, Chamber_Temperature):
    return Chamber_Temperature * (1 + ((Gamma - 1) / 2)) ** -1  # K
'''

