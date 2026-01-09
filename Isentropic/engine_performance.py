import numpy as np
from scipy.constants import g


def performance_characterization(thrust, exit_velocity, chamber_temperature, chamber_pressure, gamma, sgc, area_ratio):
    
    m_dot = thrust / exit_velocity
    
    Isp = thrust / (m_dot * g)
    
    throat_area = (m_dot * np.sqrt(chamber_temperature) / chamber_pressure) * ( np.sqrt(sgc/ gamma) * ((gamma + 1)/2) ** ((gamma + 1)/(2 * (gamma - 1))) )
    
    exit_area = throat_area * area_ratio
    
    c_star = chamber_pressure * throat_area / m_dot

    return m_dot, Isp, c_star, throat_area, exit_area

