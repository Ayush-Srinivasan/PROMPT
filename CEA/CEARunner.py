import numpy as np
from rocketcea.cea_obj_w_units import CEA_Obj
from Core.engine_inputs import EngineInputs

cea = CEA_Obj(
    oxName = EngineInputs.oxidizer_name,
    fuelName = EngineInputs.fuel_name_name,
    pressure_units= 'bar',
    temperature_units= 'K',
    density_units= 'kg/m^3',
    specific_heat_units= 'kJ/kg-K',
)

def CEArun(Chamber_Pressure, OF_min, OF_max, OF_increment):

    Pc_bar = Chamber_Pressure         # chamber pressure
    eps= 40.0       # arbitrary; we don't care about nozzle here

    OF_values = np.arange(OF_min, OF_max, OF_increment)   # 0.8, 1.0, ..., 3.8


    for MR in OF_values:

        chamber_temperature = cea.get_Tcomb(Pc=Pc_bar, MR=MR)

        molecular_weight, gamma = cea.get_Chamber_MolWt_gamma(Pc=Pc_bar, MR=MR, eps=eps)

        density, _, _ = cea.get_Densities(Pc=Pc_bar, MR=MR, eps=eps, frozen=1, frozenAtThroat=0)

        specific_heat, _, _ = cea.get_HeatCapacities(Pc=Pc_bar, MR=MR, eps=eps, frozen=1, frozenAtThroat=0)
    
    return(OF_values, chamber_temperature, molecular_weight, gamma, density, specific_heat)

