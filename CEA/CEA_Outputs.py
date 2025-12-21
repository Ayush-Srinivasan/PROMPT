from dataclasses import dataclass

@dataclass 
class CEAOutputs:
    OF_Ratio: float
    p_chamber: float
    gamma: float
    T_chamber: float
    molecular_weight: float
    density_chamber: float
    specific_heat: float