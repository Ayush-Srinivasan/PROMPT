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


# equation for conical nozzle geometry and line plots; takes y = mx + b and solves for x points with each y point

def line_plot(x_upper, y_upper, x_lower, y_lower, y_point):
    slope = (y_upper - y_lower) / (x_upper - x_lower)
    y_intercept = y_lower - (slope * x_lower)
    x_point = (y_point - y_intercept) / slope;
    return(x_point)