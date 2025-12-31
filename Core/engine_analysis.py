from __future__ import annotations
from dataclasses import dataclass
from typing import Union

from .engine_inputs import EngineInputs
from .nozzle_pipeline import engine_analysis, bell_nozzle_sizing, conical_nozzle_sizing, EngineDesignResult, ConicalNozzleGeometry, BellNozzleGeometry
from CEA.CEA_Outputs import CEAOutputs
from CEA.CEARunner import CEArun


@dataclass
class FullDesignResult:
    cea: CEAOutputs
    perf: EngineDesignResult
    nozzle: Union[ConicalNozzleGeometry, BellNozzleGeometry]


def engine_design_run(inputs: EngineInputs) -> FullDesignResult:
    cea = CEArun(inputs)  
    if cea is None:
        raise ValueError("CEA returned no results.")

    perf = engine_analysis(inputs, cea)  # returns arrays in EngineDesignResult

    if inputs.nozzle_type == "bell":
        nozzle = bell_nozzle_sizing(perf, inputs)
    else:
        nozzle = conical_nozzle_sizing(perf, inputs)

    return FullDesignResult(cea=cea, perf=perf, nozzle=nozzle)