import json
from pathlib import Path
import re
from functools import lru_cache
from typing import Tuple


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


def _parse_bell_percent(bell_percent: str) -> str:
    """
    Accepts:
      '70 Percent', '70%', '70'
    Returns:
      '70'
    """
    if bell_percent is None:
        raise ValueError("Bell nozzle selected but bell_percent is None.")

    m = re.search(r"(\d+)", bell_percent)
    if not m:
        raise ValueError(f"Could not parse bell_percent='{bell_percent}'.")
    return m.group(1)


@lru_cache(maxsize=1)
def load_rao_fit_params() -> dict:
    """
    Loads rao_fit_params.json once and caches it.
    """
    path = Path(__file__).parent / "rao_fit_params.json"
    with path.open("r") as f:
        return json.load(f)


def get_rao_coeffs(bell_percent: str) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    pct = _parse_bell_percent(bell_percent)
    params = load_rao_fit_params()

    key_n = f"theta_n_{pct}"
    key_e = f"theta_e_{pct}"

    if key_n not in params or key_e not in params:
        raise KeyError(
            f"Missing Rao fit keys '{key_n}' or '{key_e}' in rao_fit_params.json"
        )

    n = params[key_n]
    e = params[key_e]

    return (
        (float(n["a"]), float(n["b"]), float(n["c"])),
        (float(e["a"]), float(e["b"]), float(e["c"])),
    )
