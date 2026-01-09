from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray

@dataclass 
class CEAOutputs:
    OF_Ratio: NDArray[np.float64]
    p_chamber: NDArray[np.float64]
    gamma: NDArray[np.float64]
    T_chamber: NDArray[np.float64]
    molecular_weight: NDArray[np.float64]
    density_chamber: NDArray[np.float64]