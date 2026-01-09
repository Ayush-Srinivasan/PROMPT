from pathlib import Path
from CEA.CEA_Outputs import CEAOutputs
from Core.engine_analysis import FullDesignResult
import pandas as pd

def exportCEAResults(cea: CEAOutputs, out_dir: str, filename: str = "cea_results.csv") -> dict[str, str]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not filename.lower().endswith(".csv"):
        filename += ".csv"

    CEAResults = {
        'OF': cea.OF_Ratio,
        'P_chamber(Bar)': cea.p_chamber,
        'T_chamber(K)': cea.T_chamber,
        'gamma': cea.gamma,
        'density(kg/m^3)': cea.density_chamber,
        'mw(kg/mol)': cea.molecular_weight
    }

    n = len(cea.OF_Ratio)
    assert all(len(v) == n for v in CEAResults.values()), "CEA array length mismatch"

    df = pd.DataFrame(CEAResults)

    path = out_dir / filename

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="raise")
    
    df.to_csv(path, index = False, float_format="%.8g")

    return {"CEA": str(path)}

import numpy as np
import pandas as pd
from pathlib import Path

def exportEngineData(results, inputs, out_dir: str, filename="engine_data.csv"):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    OF = np.asarray(results.cea.OF_Ratio)
    n = OF.size
    nan = np.full(n, np.nan)

    perf = results.perf
    noz = results.nozzle

    # --- geometry-independent ---
    df = {
        "OF": OF,
        "At(m^2)": perf.a_throat,
        "Ae(m^2)": perf.a_exit,
        "ER": perf.ER,
        "Isp(s)": perf.Isp,
        "cstar(m/s)": perf.c_star,
        "v_exit(m/s)": perf.v_exit,
        "mdot(kg/s)": perf.mdot,
        "T_chamber(K)": results.cea.T_chamber,
        "T_throat(K)": perf.T_throat,
        "T_exit(K)": perf.T_exit,
        "nozzle_type": [inputs.nozzle_type] * n,
    }

    # --- conical nozzle ---
    if inputs.nozzle_type == "conical":
        df.update({
            "Rc(m)": noz.radius_chamber,
            "Rt(m)": noz.radius_throat,
            "Re(m)": noz.radius_exit,
            "L_chamber(m)": noz.length_chamber,
            "L_convergent(m)": noz.length_convergent,
            "L_throat(m)": noz.length_throat,
            "L_divergent(m)": noz.length_divergent,
            "L_total(m)": noz.length_total,
            "divergent_angle(deg)": noz.divergent_angle,
            "theta_n(deg)": nan,
            "theta_e(deg)": nan,
            "bell_percent": nan,
            "L_nozzle(m)": nan,
            "Ac(m^2)": nan,
        })

    # --- bell nozzle ---
    else:
        df.update({
            "Rc(m)": noz.chamber_radius,
            "Rt(m)": noz.throat_radius,
            "Re(m)": noz.exit_radius,
            "L_chamber(m)": noz.length_chamber,
            "L_convergent(m)": noz.length_convergent,
            "L_throat(m)": nan,
            "L_divergent(m)": nan,
            "L_total(m)": nan,
            "divergent_angle(deg)": nan,
            "theta_n(deg)": noz.initial_angle,
            "theta_e(deg)": noz.exit_angle,
            "bell_percent": np.full(n, inputs.bell_percent),
            "L_nozzle(m)": noz.nozzle_length,
            "Ac(m^2)": noz.chamber_area,
        })

    df = pd.DataFrame(df)
    path = out_dir / filename
    df.to_csv(path, index=False, float_format="%.8g")
    return {"engine": str(path)}

    
def exportNozzleDatapoints(x, y, out_dir: str, filename: str = "cea_results.csv") -> dict[str, str]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not filename.lower().endswith(".csv"):
        filename += ".csv"
    
    x = np.asarray(x, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()

    if x.size != y.size:
        raise ValueError(f"x and y length mismatch: {x.size} vs {y.size}")

    df = pd.DataFrame({
        "x_m": x,
        "y_m": y,
    })

    path = out_dir / filename
    df.to_csv(path, index=False, float_format="%.8g")

    return {"nozzle": str(path)}