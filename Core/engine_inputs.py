from dataclasses import dataclass

@dataclass
class EngineInputs:
    chamber_pressure: float         # Pa
    chamber_temperature: float      # K
    ambient_pressure: float         # Pa
    gamma: float                    # Specific heat ratio
    cp: float                      # Specific heat [J/kg·K]
    thrust: float                   # N
    fuel_name: str = "RP-1"
    oxidizer_name: str = "LOX"
    source: str = "GUI"             # or "CEA"