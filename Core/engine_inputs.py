from dataclasses import dataclass
from typing import Optional

@dataclass
class EngineInputs:
    # Required  
    chamber_pressure: float          # Pa
    thrust: float                   # N

    nozzle_type: str                # "conical" or "bell"
    convergent_angle: float         # deg
    divergent_angle: float          # deg
    contraction_ratio: float        # Ac/At
    throat_ratio: float
    l_star: float

    bell_percent: str
    fuel_name: str
    oxidizer_name: str

    # Defaults 
    
    # Ambient pressure
    external_pressure_flag: bool = False
    ambient_pressure: float = 101325.0   # Pa

    # frozen vs equilibrium
    frozen_flag: bool = False

    # O/F single
    OF: Optional[float] = None

    # O/F sweep
    OF_min: Optional[float] = None
    OF_max: Optional[float] = None
    OF_increment: Optional[float] = None

    source: str = "GUI"