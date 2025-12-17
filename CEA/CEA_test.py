from Core.engine_inputs import EngineInputs
from CEA.CEARunner import CEArun   # import from the package

engine_in = EngineInputs(
    chamber_pressure = 20 * 1e5, # bar
    OF_min = 0.8, 
    OF_max = 3.8,
    OF_increment = 0.2,
    ambient_pressure = 101325, # Pa
    thrust = 5500, # N
    convergent_angle = 45, # degrees
    divergent_angle = 15, # degrees
    contraction_ratio = 5.5,
    throat_ratio = 0.05,
    fuel_name = "RP1",
    oxidizer_name = "LOX",
)

outputs = CEArun(engine_in)
print("Got", len(outputs), "CEA rows:")
for row in outputs:
    print(
        f"OF={row.OF_Ratio:3.1f} | "
        f"gamma={row.gamma:6.4f} | "
        f"Tc={row.T_chamber:8.2f} | "
        f"rho={row.density_chamber:7.3f} | "
        f"cp={row.specific_heat:7.4f}"
        )

