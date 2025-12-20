import json
from pathlib import Path

rao_fit_parameters = {
    "theta_n_60": {
        "a": 25.38122,
        "b": 15.45578,
        "c": -2.41793
    },
    "theta_e_60": {
        "a": 11.84008,
        "b": 10.37225,
        "c": 0.102654
    },    
    "theta_n_70": {
        "a": 23.43466,
        "b": 13.09155,
        "c": -1.54022
    },
    "theta_e_70": {
        "a": 9.20012,
        "b": 9.6289,
        "c": 0.108466
    }, 
    "theta_n_80": {
        "a": 19.78431,
        "b": 10.12162,
        "c": -0.968714
    },
    "theta_e_80": {
        "a": 6.48333,
        "b": 7.82595,
        "c": 0.122249
    },    
    "theta_n_90": {
        "a": 21.10044,
        "b": 11.15402,
        "c": -0.991682
    },
    "theta_e_90": {
        "a": 5.84611,
        "b": 8.11254,
        "c": 0.143292
    },
    "theta_n_100": {
        "a": 20.37189,
        "b": 9.84689,
        "c": -0.37436
    },
    "theta_e_100": {
        "a": 4.38196,
        "b": 7.29628,
        "c": 0.148981
    },
}

# Output Path
DATA_DIR = Path(__file__).parent
OUTPUT_PATH = DATA_DIR / "rao_fit_params.json"

# ---- Write JSON ----
with OUTPUT_PATH.open("w") as f:
    json.dump(rao_fit_parameters, f, indent=4)

print(f"Saved Rao fit parameters to: {OUTPUT_PATH}")