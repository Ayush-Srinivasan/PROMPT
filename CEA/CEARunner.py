import numpy as np
from rocketcea.cea_obj_w_units import CEA_Obj
from Core.engine_inputs import EngineInputs
from typing import List
from CEA.CEA_Outputs import CEAOutputs



def of_grid(engine_in: EngineInputs) -> np.ndarray:
    """
    Returns an array of mixture ratios to evaluate.

    Modes:
    - Single: engine_in.OF is not None
    - Sweep: engine_in.OF_min / OF_max / OF_increment are all not None
    """
    # -------------------------
    # Single-point mode
    # -------------------------
    if engine_in.OF is not None:
        of = float(engine_in.OF)
        if of <= 0.0:
            raise ValueError("O/F must be positive.")
        return np.array([of], dtype=float)

    # -------------------------
    # Sweep mode (require fields)
    # -------------------------
    if engine_in.OF_min is None or engine_in.OF_max is None or engine_in.OF_increment is None:
        raise ValueError("Sweep mode requires OF_min, OF_max, and OF_increment (or provide OF for single mode).")

    of_min = float(engine_in.OF_min)
    of_max = float(engine_in.OF_max)
    step   = float(engine_in.OF_increment)

    if of_min <= 0.0 or of_max <= 0.0:
        raise ValueError("O/F values must be positive.")
    if of_min > of_max:
        raise ValueError("O/F min must be <= O/F max.")
    if step <= 0.0:
        raise ValueError("O/F step must be > 0.")

    # include endpoint robustly
    n = int(np.floor((of_max - of_min) / step + 1.0000001)) + 1
    grid = of_min + step * np.arange(n, dtype=float)
    grid = grid[grid <= of_max + 1e-12]
    return grid


def CEArun(engine_in: EngineInputs, eps: float = 40.0) -> CEAOutputs:
    """
    Compute chamber properties over a single O/F or an O/F sweep.
    Returns a list of CEAOutputs rows, one per O/F.
    """
    Pc_bar = engine_in.chamber_pressure / 1e5  # Pa -> bar

    cea = CEA_Obj(
        oxName=engine_in.oxidizer_name,
        fuelName=engine_in.fuel_name,
        pressure_units="bar",
        temperature_units="K",
        density_units="kg/m^3",
        specific_heat_units="kJ/kg-K",
    )

    OF_values = of_grid(engine_in).astype(float)

    # frozen or equilibrium CEA run
    frozen_eqm = 1 if engine_in.frozen_flag else 0
    n = OF_values.size

    T_chamber = np.empty(n, dtype=float)
    gamma = np.empty(n, dtype=float)
    mol_wt = np.empty(n, dtype=float)
    density = np.empty(n, dtype=float)
    cp = np.empty(n, dtype=float)
    
    for i, MR in enumerate(OF_values):
        T_chamber[i] = cea.get_Tcomb(Pc=Pc_bar, MR=MR)

        mw_i, gamma_i = cea.get_Chamber_MolWt_gamma(Pc=Pc_bar, MR=MR, eps=eps)
        mol_wt[i] = mw_i
        gamma[i] = gamma_i

        dens_i, _, _ = cea.get_Densities(
            Pc=Pc_bar, MR=MR, eps=eps, frozen=frozen_eqm, frozenAtThroat=0
        )
        density[i] = dens_i

        cp_i, _, _ = cea.get_HeatCapacities(
            Pc=Pc_bar, MR=MR, eps=eps, frozen=frozen_eqm, frozenAtThroat=0
        )
        cp[i] = cp_i

    return CEAOutputs(
        OF_Ratio=OF_values,
        p_chamber=np.full(n, Pc_bar, dtype=float),
        gamma=gamma,
        T_chamber=T_chamber,
        molecular_weight=mol_wt,
        density_chamber=density,
        specific_heat=cp,
    )