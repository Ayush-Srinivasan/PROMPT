import numpy as np
from scipy.constants import g


def performance_characterization(thrust, exit_velocity, chamber_temperature, chamber_pressure, gamma, sgc, area_ratio):
    
    m_dot = thrust / exit_velocity
    
    Isp = thrust / (m_dot * g)
    
    throat_area = (m_dot * np.sqrt(chamber_temperature) / chamber_pressure) * ( np.sqrt(gamma / sgc) * ((gamma + 1)/2) ** ((gamma + 1)/(2 * (gamma - 1))) )** -1
    
    exit_area = throat_area * area_ratio
    
    c_star = chamber_pressure * throat_area / m_dot

    return m_dot, Isp, c_star, throat_area, exit_area

'''
def mass_flow_rate(thrust, exit_velocity):
    return thrust / exit_velocity

def specific_impulse(thrust, m_dot):
    return thrust / (m_dot * g)

def throat_area(m_dot, chamber_temperature, chamber_pressure, gamma, sgc):
    return (m_dot * np.sqrt(chamber_temperature) / chamber_pressure) * ( np.sqrt(gamma / sgc) * ((gamma + 1)/2) ** ((gamma + 1)/(2 * (gamma - 1))) )** -1

def exit_area(throat_area, area_ratio):
    return throat_area * area_ratio

def characteristic_velocity(chamber_pressure, throat_area, m_dot):
    return chamber_pressure * throat_area / m_dot
'''