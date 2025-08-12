import os
from Data import load_materials, load_propellant

# finds data files
data_find = "data"
fuel_path = os.path.join(data_find, "Propellant Densities.csv")
oxidizer_path = os.path.join(data_find,"Oxidizer Densities.csv")
materials_path = os.path.join(data_find, "Material Properties.csv")

# chamber material properties
materials = load_materials(materials_path)

# propellant and oxidizer properties
fuel = load_propellant(fuel_path)
oxidizer = load_propellant(oxidizer_path)

# confirmation message
print(f"Loaded {len(fuel)} fuels, {len(oxidizer)} oxidizers, and {len(materials)} materials.")