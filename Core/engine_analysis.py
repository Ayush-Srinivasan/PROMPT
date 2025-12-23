from __future__ import annotations
from dataclasses import dataclass
from typing import List, Union

from .engine_inputs import EngineInputs
from .nozzle_pipeline import engine_analysis, bell_nozzle_sizing, conical_nozzle_sizing, EngineDesignResult, ConicalNozzleGeometry, BellNozzleGeometry
from CEA.CEA_Outputs import CEAOutputs
from CEA.CEARunner import CEArun


@dataclass
class DesignPoint:
    cea: CEAOutputs
    perf: EngineDesignResult
    nozzle: Union[ConicalNozzleGeometry, BellNozzleGeometry]


@dataclass
class DesignSweepResult:
    points: List[DesignPoint] = []


def run_full_design(inputs: EngineInputs) -> DesignSweepResult:
    cea_rows = CEArun(inputs)  # uses default eps=40.0 inside CEArun

    if not cea_rows:
        raise ValueError("CEA returned no results.")

    points:List[DesignPoint] = []
    for cea in cea_rows:
        print("engine_analysis is:", engine_analysis)
        perf = engine_analysis(inputs, cea)

        if inputs.nozzle_type == "bell":
            nozzle = bell_nozzle_sizing(perf, inputs)
        else:
            nozzle = conical_nozzle_sizing(perf, inputs)

        points.append(DesignPoint(cea=cea, perf=perf, nozzle=nozzle))

    return DesignSweepResult(points=points)