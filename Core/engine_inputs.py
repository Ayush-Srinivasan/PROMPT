from dataclasses import dataclass
from typing import Optional

@dataclass
class EngineInputs:
    chamber_pressure: float         # Pa

    # OF Single Run
    OF: Optional[float] = None

    # OF Sweep
    OF_min: Optional[float] = None
    OF_max: Optional[float] = None
    OF_increment: Optional[float] = None

    # Ambient Pressure Flag
    external_pressure_flag: bool
    ambient_pressure: float         # Pa

    # frozen or equilibrium
    frozen_flag: bool
    
    thrust: float                   # N

    nozzle_type: str                # nozzle type
    convergent_angle: float         # degreees
    divergent_angle: float          # degrees
    contraction_ratio: float        # should be from 2-5 for small engines and 5-8 for large engines
    throat_ratio: float             # should be between 0.05 and 0.2 for conical nozzles
    l_star: float                   # check documentation
    bell_percent: str                # bell nozzle length percentage
    fuel_name: str 
    oxidizer_name: str 
    source: str = "GUI"             # or "CEA"