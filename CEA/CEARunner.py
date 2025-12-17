import numpy as np
from rocketcea.cea_obj_w_units import CEA_Obj
from dataclasses import dataclass
from Core.engine_inputs import EngineInputs

@dataclass 
class CEA_Outputs:
    OF_Ratio: float
    p_chamber: float
    gamma: float
    T_chamber: float
    molecular_weight: float
    density_chamber: float
    specific_heat: float


# example dataclass; this will take in GUI data
'''
### change to gui values
engine_in = EngineInputs(
    chamber_pressure = 20 * 1e5,
    OF_min = 0.8,
    OF_max = 4.0,
    OF_increment = 0.2,
    ambient_pressure = 101325,
    thrust = 5500,
    convergent_angle = 45,
    divergent_angle = 15, 
    contraction_ratio = 5.5,
    throat_ratio = 0.05,
    fuel_name = "RP1",
    oxidizer_name = 'LOX',
)
'''

def CEArun(engine_in: EngineInputs):

    Pc_bar = engine_in.chamber_pressure / 1e5        # chamber pressure
    eps= 40.0       # arbitrary; we don't care about nozzle here

    cea = CEA_Obj(
        oxName = engine_in.oxidizer_name,
        fuelName = engine_in.fuel_name,
        pressure_units= 'bar',
        temperature_units= 'K',
        density_units= 'kg/m^3',
        specific_heat_units= 'kJ/kg-K',
    )

    OF_values = np.arange(engine_in.OF_min, engine_in.OF_max + engine_in.OF_increment, engine_in.OF_increment)   # increments OF Values

    CEA_results = []

    for MR in OF_values:

        chamber_temperature = cea.get_Tcomb(Pc=Pc_bar, MR=MR)

        molecular_weight, gamma = cea.get_Chamber_MolWt_gamma(Pc=Pc_bar, MR=MR, eps=eps)

        density, _, _ = cea.get_Densities(Pc=Pc_bar, MR=MR, eps=eps, frozen=1, frozenAtThroat=0)

        specific_heat, _, _ = cea.get_HeatCapacities(Pc=Pc_bar, MR=MR, eps=eps, frozen=1, frozenAtThroat=0)
    
        # dataclass instance for each OF
        row = CEA_Outputs(
            OF_Ratio = MR,
            p_chamber = Pc_bar,
            gamma = gamma,
            T_chamber = chamber_temperature,
            molecular_weight = molecular_weight,
            density_chamber = density,
            specific_heat = specific_heat, 
        )
        CEA_results.append(row)

    return(CEA_results)