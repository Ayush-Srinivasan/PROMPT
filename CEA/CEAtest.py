import numpy as np
from rocketcea.cea_obj_w_units import CEA_Obj

cea = CEA_Obj(
    oxName='LOX',
    fuelName='RP1',
    pressure_units='bar',
    temperature_units='K',
    density_units='kg/m^3',
    specific_heat_units='kJ/kg-K',
)

Pc_bar = 20.0          # chamber pressure
eps_dummy = 40.0       # arbitrary; we don't care about nozzle here

OF_values = np.arange(0.8, 4.0, 0.2)   # 0.8, 1.0, ..., 3.8

for MR in OF_values:   # MR = O/F for biprop in RocketCEA
    # Chamber temperature (does NOT need eps)
    Tc = cea.get_Tcomb(Pc=Pc_bar, MR=MR)

    # Chamber MW and gamma (needs eps arg but chamber result is independent of eps)
    mw_ch, gamma_ch = cea.get_Chamber_MolWt_gamma(Pc=Pc_bar, MR=MR, eps=eps_dummy)

    # Densities: chamber / throat / exit
    rho_ch, _, _ = cea.get_Densities(Pc=Pc_bar, MR=MR, eps=eps_dummy)

    # Heat capacities: chamber / throat / exit
    cp_ch, _, _ = cea.get_HeatCapacities(Pc=Pc_bar, MR=MR, eps=eps_dummy)

    print(f"MR={MR:4.1f} | rho={rho_ch:8.3f} | gamma={gamma_ch:6.4f} | "
          f"MW={mw_ch:7.3f} | Tc={Tc:8.2f} | cp={cp_ch:8.4f}")