import numpy as np

def fuel_flow_rate(mdot, gamma): 
    return mdot * (1/(1 + gamma))       # kg/s

def ox_flow_rate(mdot, gamma):
    return mdot * (gamma/(1 + gamma))   # kg/s

def volumetric_flow_rate(mdot, density):
    return mdot / density               # m^3/s                  