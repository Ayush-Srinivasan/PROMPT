from dataclasses import dataclass

@dataclass
class EngineInputs:
    chamber_pressure: float         # Pa
    OF_min: float
    OF_max: float
    OF_increment: float
    ambient_pressure: float         # Pa
    thrust: float                   # N
    convergent_angle: float         # degreees
    divergent_angle: float          # degrees
    contraction_ratio: float        # should be from 2-5 for small engines and 5-8 for large engines
    throat_ratio: float             # should be between 0.05 and 0.2 for conical nozzles
    l_star: float                   # check documentation
    bell_percent: str                # bell nozzle length percentage
    fuel_name: str 
    oxidizer_name: str 
    source: str = "GUI"             # or "CEA"