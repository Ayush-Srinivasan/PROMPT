from dataclasses import dataclass

@dataclass
class EngineInputs:
    chamber_pressure: float         # Pa
    chamber_temperature: float      # K
    ambient_pressure: float         # Pa
    gamma: float                    # Specific heat ratio
    cp: float                       # Specific heat [kJ/kg·K]
    thrust: float                   # N
    convergent_angle: float         # degreees
    divergent_angle: float          # degrees
    contraction_ratio: float        # should be from 2-5 for small engines and 5-8 for large engines
    throat_ratio: float             # should be between 0.5 and 1 for conical nozzles
    fuel_name: str = "RP-1"
    oxidizer_name: str = "LOX"
    source: str = "GUI"             # or "CEA"