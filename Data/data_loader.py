import pandas as pd
from dataclasses import dataclass
import os

# propellant properties class
@dataclass
class Propellant:
    name: str
    density: float                  # kg/m^3

def load_propellant(path) -> dict:
    df = pd.read_csv(path)
    return {
        row["name"]: Propellant(name = row["name"], density = row["density"])
        for _, row in df.iterrows()
    }

# material properties class
@dataclass
class Material:
    name: str
    yield_strength: float           # MPa
    ultimate_strength: float        # MPa
    youngs_modulus: float           # GPa
    poisson_ratio: float            
    thermal_conductivity: float     # W/mK
    specific_heat: float            # J/(kg*K)
    thermal_expansion: float        # 1/K
    max_operating_temp: float       # K
    melting_point: float            # K

def load_materials(path) -> dict:
    df = pd.read_csv(path)
    return{
        row["Material"]: Material(
            name = row["Material"], 
            yield_strength = row["Yield Strength (MPa)"], 
            ultimate_strength = row["Ultimate Strength (MPa)"], 
            youngs_modulus = row["Young's Modulus (GPa)"],
            poisson_ratio = row["Poisson's Ratio"], 
            thermal_conductivity = row["Thermal Conductivity (W/mK)"], 
            specific_heat = row["Specific Heat Capacity (J/kgK)"], 
            thermal_expansion = row["Thermal Expansion Coefficient (1/K)"], 
            max_operating_temp = row["Max Operating Temp (K)"], 
            melting_point = row["Melting Point (K)"]
            )
        for _, row in df.iterrows()
    }



