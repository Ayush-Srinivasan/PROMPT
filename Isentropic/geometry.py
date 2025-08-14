import numpy as np

# compute diamter and radius from area 

# d = sqrt(4*A/pi)
def diameter_from_area(area):
    return np.sqrt(area * 4/np.pi)

# r = sqrt(A/pi)
def radius_from_area(area):
    return np.sqrt(area/np.pi)

def radius_from_diameter(diameter):
    return diameter/2

def area_from_radius(radius):
    return np.pi * radius ** 2