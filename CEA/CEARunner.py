import numpy as np
from rocketcea.cea_obj_w_units import CEA_Obj
from dataclasses import dataclass
from Core.engine_inputs import EngineInputs
from typing import List
from CEA.CEA_Outputs import CEAOutputs


# example dataclass; this will take in GUI data

def of_grid(engine_in: EngineInputs) -> np.ndarray:
    """
    Returns an array of mixture ratios to evaluate.
    Supports:
      - sweep mode: OF_min, OF_max, OF_increment > 0
      - single mode: (recommended) engine_in has OF_min == OF_max OR OF_increment <= 0
    """
    of_min = engine_in.OF_min
    of_max = engine_in.OF_max
    step = engine_in.OF_increment

    # Basic validation
    if of_min <= 0 or of_max <= 0:
        raise ValueError("O/F values must be positive.")
    if of_min > of_max:
        raise ValueError("O/F min must be <= O/F max.")

    # Single-point mode if step is None or <= 0 or min==max
    if (step is None) or (step <= 0) or (abs(of_max - of_min) < 1e-12):
        return np.array([of_min], dtype=float)

    # Sweep mode: include endpoint robustly
    n = int(np.floor((of_max - of_min) / step + 1.0000001)) + 1
    grid = of_min + step * np.arange(n)
    grid = grid[grid <= of_max + 1e-12]
    return grid


def CEArun(engine_in: EngineInputs, eps: float = 40.0) -> List[CEAOutputs]:
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

    OF_values = of_grid(engine_in)

    results: List[CEAOutputs] = []
    
    for MR in OF_values:
        T_chamber = cea.get_Tcomb(Pc=Pc_bar, MR=MR)

        mol_wt, gamma = cea.get_Chamber_MolWt_gamma(Pc=Pc_bar, MR=MR, eps=eps)

        density, _, _ = cea.get_Densities(Pc=Pc_bar, MR=MR, eps=eps, frozen=1, frozenAtThroat=0)

        cp, _, _ = cea.get_HeatCapacities(Pc=Pc_bar, MR=MR, eps=eps, frozen=1, frozenAtThroat=0)

        results.append(
            CEAOutputs(
                OF_Ratio=float(MR),
                p_chamber=float(Pc_bar),
                gamma=float(gamma),
                T_chamber=float(T_chamber),
                molecular_weight=float(mol_wt),
                density_chamber=float(density),
                specific_heat=float(cp),
            )
        )

    return results